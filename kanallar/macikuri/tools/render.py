#!/usr/bin/env python3
"""Macikuri TV renderer: one JSON story spec -> finished mp4.

python3 render.py <spec.json> <out.mp4>

Spec:
{
  "format": "short" | "long",          # short = 1080x1920, long = 1920x1080
  "voice": "bm_george", "speed": 0.92,
  "scenes": [
    {"svg": "<svg viewBox='0 0 1080 1920' ...>...</svg>",   # or "svg_file": "scene1.svg" (relative to spec)
     "vo": "Narration for this scene.",
     "move": "in" | "out" | "left" | "right" | "up" | "down",  # slow camera move (default in)
     "fx": ["flicker", "shake", "red", "static"]}            # optional
  ]
}
Env: MK_ASSETS (kokoro model + fonts dir, default ../assets)
"""
import json, os, re, subprocess, sys, tempfile, math
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.environ.get('MK_ASSETS', os.path.join(HERE, '..', 'assets'))
SR = 24000
FPS = 30


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit('FAILED: ' + ' '.join(args)[:300] + '\n' + r.stderr[-1500:])


# ---------------- audio ----------------
def tts_scenes(scenes, voice, speed):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(ASSETS, 'kokoro-v1.0.int8.onnx'), os.path.join(ASSETS, 'voices-v1.0.bin'))
    out = []
    for sc in scenes:
        parts, words, t = [], [], 0.0
        for s in [x for x in re.split(r'(?<=[.?!…])\s+', sc['vo'].strip()) if x]:
            a, _ = k.create(s.replace('…', '...'), voice=voice, speed=speed, lang='en-us' if not voice.startswith('b') else 'en-gb')
            idx = np.where(np.abs(a) > 0.012)[0]
            if len(idx):
                a = a[max(idx[0] - 480, 0): min(idx[-1] + 1440, len(a))]
            d = len(a) / SR
            ws = s.split(); wt = [len(re.sub(r'\W', '', w)) + 2.5 + (4 if w[-1] in '.?!,' else 0) for w in ws]
            acc = 0
            for w, x in zip(ws, wt):
                words.append((t + d * acc / sum(wt), w)); acc += x
            parts += [a, np.zeros(int(0.28 * SR), np.float32)]
            t += d + 0.28
        tail = 0.35
        parts.append(np.zeros(int(tail * SR), np.float32))
        out.append({'audio': np.concatenate(parts).astype(np.float32), 'dur': t + tail, 'words': words})
    return out


def drone(dur, seed=7):
    """Low ambient horror bed: detuned sines + slow breathing noise."""
    rng = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9.0)
    a = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 55.7 * t) + 0.35 * np.sin(2 * np.pi * 82.4 * t)) * lfo
    noise = rng.standard_normal(n).astype(np.float32)
    k = int(SR * 0.004); noise = np.convolve(noise, np.ones(k) / k, mode='same')  # dark noise
    a = a * 0.06 + noise * 0.05 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 6.3))
    return a.astype(np.float32)


def hit(n_sec=1.2):
    """Low boom for scene changes."""
    t = np.arange(int(n_sec * SR)) / SR
    f = 70 * np.exp(-t * 2.5) + 30
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) * 0.5).astype(np.float32)


def static_burst(n_sec):
    rng = np.random.default_rng(3)
    a = rng.standard_normal(int(n_sec * SR)).astype(np.float32) * 0.18
    env = np.linspace(1, 0.2, len(a)); return a * env


# ---------------- captions ----------------
def ass_file(path, chunks, W, H):
    size = 112 if H > W else 76
    y = int(H * (0.70 if H > W else 0.86))
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Bebas Neue,{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,2,0,1,7,3,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def ts(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    lines = []
    for a, b, txt, hot in chunks:
        col = '{\\c&H9AFFF4&}' if hot else ''
        lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},C,,0,0,0,,{{\\pos({W // 2},{y})}}{col}{txt.upper()}")
    open(path, 'w').write(head + '\n'.join(lines) + '\n')


def chunk_words(words, end, per=3):
    out = []
    for i in range(0, len(words), per):
        g = words[i:i + per]
        a = g[0][0]; b = words[i + per][0] if i + per < len(words) else end
        txt = ' '.join(w for _, w in g)
        hot = any(re.sub(r'\W', '', w).isupper() and len(re.sub(r'\W', '', w)) > 1 for _, w in g)
        out.append((a, b, txt.replace('*', ''), hot))
    return out


# ---------------- video ----------------
def scene_clip(png, dur, move, fx, W, H, out):
    # png is 1.25x the frame; scale between 0.8..1.0 of it and crop
    D = max(dur, 0.5)
    BW, BH = int(W * 1.25), int(H * 1.25)
    if move == 'out':
        sw = f"{BW}-{BW - W * 1.02:.0f}*t/{D}"
    elif move in ('left', 'right', 'up', 'down'):
        sw = f"{W * 1.12:.0f}"
    else:
        sw = f"{W * 1.02:.0f}+{BW - W * 1.02:.0f}*0.55*t/{D}"
    cx = {'left': f"(iw-{W})*(1-t/{D})", 'right': f"(iw-{W})*t/{D}"}.get(move, f"(iw-{W})/2")
    cy = {'up': f"(ih-{H})*(1-t/{D})", 'down': f"(ih-{H})*t/{D}"}.get(move, f"(ih-{H})/2")
    if 'shake' in fx:
        cx += f"+6*sin(t*37)"; cy += f"+6*sin(t*29)"
    vf = [f"scale=w='{sw}':h=-2:eval=frame:flags=bicubic", f"crop={W}:{H}:'{cx}':'{cy}'", 'setsar=1']
    if 'red' in fx:
        vf.append("colorchannelmixer=rr=1.15:gg=0.75:bb=0.75")
    if 'flicker' in fx:
        vf.append("eq=brightness='-0.05*gt(sin(t*13)+sin(t*7.3),1.4)':eval=frame")
    vf += ['vignette=PI/4.2', 'noise=alls=4:allf=t', f'fps={FPS}', 'format=yuv420p']
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', str(FPS), '-i', png, '-t', f'{D:.3f}',
        '-vf', ','.join(vf), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-an', out])


def intro_clip(W, H, tmp, out, label=''):
    """Entry: TV static, then Macikuri pops on screen (1.7 s)."""
    frag = open(os.path.join(HERE, 'creature.svgfrag')).read()
    scale = (W / 800) * (0.95 if H > W else 0.6)
    defs = open(os.path.join(HERE, 'avatar.svg')).read()
    defs = defs[defs.index('<defs>'): defs.index('</defs>') + 7]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}'
           f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
           f'<g transform="translate({W / 2 + 10} {H * 0.45}) scale({scale})">{frag}</g>'
           f'<text x="{W / 2}" y="{H * 0.45 + 380 * scale}" text-anchor="middle" font-family="Creepster" '
           f'font-size="{int(140 * W / 1080)}" fill="#f4ff9a" stroke="#07050b" stroke-width="7" paint-order="stroke">MACIKURI TV</text>'
           + (f'<text x="{W / 2}" y="{H * 0.45 + 520 * scale}" text-anchor="middle" font-family="Bebas Neue" font-size="{int(84 * W / 1080)}" '
              f'fill="#ffffff" letter-spacing="6">{label.upper()}</text>' if label else '') + '</svg>')
    p = os.path.join(tmp, 'intro.svg'); open(p, 'w').write(svg)
    png = os.path.join(tmp, 'intro.png'); sh(['rsvg-convert', p, '-o', png])
    sh(['ffmpeg', '-y', '-loglevel', 'error',
        '-f', 'lavfi', '-i', f'nullsrc=s={W}x{H}:r={FPS}:d=0.5,geq=random(1)*255:128:128,format=yuv420p',
        '-loop', '1', '-framerate', str(FPS), '-t', '1.2', '-i', png,
        '-filter_complex',
        f"[1:v]scale={W}:{H},eq=brightness='-0.25*gt(random(0),0.8)':eval=frame,noise=alls=25:allf=t,format=yuv420p[m];"
        f"[0:v][m]concat=n=2:v=1:a=0,fps={FPS},format=yuv420p[v]",
        '-map', '[v]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', out])
    a = np.concatenate([static_burst(0.5), hit(1.2) * 1.4])
    return a


def main(spec_path, out_mp4):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    W, H = (1920, 1080) if spec.get('format') == 'long' else (1080, 1920)
    tmp = tempfile.mkdtemp(prefix='mk_')
    scenes = spec['scenes']
    aud = tts_scenes(scenes, spec.get('voice', 'bm_george'), float(spec.get('speed', 0.92)))

    clips = [os.path.join(tmp, 'c0.mp4')]
    label = f"{spec['series']} · PART {spec['episode']}" if spec.get('series') and spec.get('episode') else ''
    intro_a = intro_clip(W, H, tmp, clips[0], label)
    t0 = len(intro_a) / SR
    voice = [np.zeros(len(intro_a), np.float32)]
    fxa = [intro_a]
    chunks, t = [], t0
    for i, (sc, a) in enumerate(zip(scenes, aud)):
        svg = sc.get('svg') or open(os.path.join(base, sc['svg_file'])).read()
        sp = os.path.join(tmp, f's{i}.svg'); open(sp, 'w').write(svg)
        png = os.path.join(tmp, f's{i}.png')
        sh(['rsvg-convert', '-w', str(int(W * 1.25)), '-h', str(int(H * 1.25)), sp, '-o', png])
        c = os.path.join(tmp, f'c{i + 1}.mp4')
        scene_clip(png, a['dur'], sc.get('move', 'in'), sc.get('fx', []), W, H, c)
        clips.append(c)
        voice.append(a['audio'])
        b = hit() if i and 'static' not in sc.get('fx', []) else np.zeros(1, np.float32)
        if 'static' in sc.get('fx', []): b = static_burst(0.35)
        pad = np.zeros(len(a['audio']), np.float32); pad[:min(len(b), len(pad))] += b[:len(pad)] * 0.8
        fxa.append(pad)
        chunks += chunk_words([(t + w0, w) for w0, w in a['words']], t + a['dur'])
        t += a['dur']

    # bölüm sonu kartı
    if spec.get('episode'):
        last = spec.get('total') and int(spec['episode']) >= int(spec['total'])
        txt = 'THE END' if last else f"PART {int(spec['episode']) + 1} {spec.get('next', 'TOMORROW')}"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#050407"/>'
               f'<text x="{W / 2}" y="{H / 2}" text-anchor="middle" font-family="Creepster" font-size="{int(118 * W / 1080)}" fill="#ff3b3b">{txt}</text>'
               + ('' if last else f'<text x="{W / 2}" y="{H / 2 + 130 * W / 1080}" text-anchor="middle" font-family="Bebas Neue" font-size="{int(70 * W / 1080)}" fill="#f4ff9a" letter-spacing="4">FOLLOW SO YOU DON\'T MISS IT</text>')
               + '</svg>')
        sp = os.path.join(tmp, 'end.svg'); open(sp, 'w').write(svg)
        png = os.path.join(tmp, 'end.png'); sh(['rsvg-convert', '-w', str(int(W * 1.25)), '-h', str(int(H * 1.25)), sp, '-o', png])
        c = os.path.join(tmp, 'cend.mp4'); scene_clip(png, 1.8, 'in', ['flicker'], W, H, c); clips.append(c)
        voice.append(np.zeros(int(1.8 * SR), np.float32)); fxa.append(np.concatenate([hit(1.2), np.zeros(int(0.6 * SR), np.float32)]))

    # audio mix
    v = np.concatenate(voice); f = np.concatenate(fxa)
    d = drone(len(v) / SR + 0.1)[:len(v)]
    mix = v * 0.95 + f + d
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
    wav = os.path.join(tmp, 'mix.wav'); sf.write(wav, mix, SR)

    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write('\n'.join(f"file '{c}'" for c in clips))
    joined = os.path.join(tmp, 'joined.mp4')
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', joined])
    ass = os.path.join(tmp, 'cap.ass'); ass_file(ass, chunks, W, H)
    fontsdir = ASSETS
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', joined, '-i', wav,
        '-vf', f"ass={ass}:fontsdir={fontsdir}", '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-maxrate', '6M', '-bufsize', '12M',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out_mp4])
    print(out_mp4, round(len(mix) / SR, 1), 's')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

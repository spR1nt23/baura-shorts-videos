#!/usr/bin/env python3
"""Pazar uzun videosu: haftanın dikey bölümlerini tek yatay (1920x1080) videoda birleştirir.

python3 compile.py <out.mp4> ep01.mp4 ep02.mp4 ...
- İlk bölüm dışındakilerin Macikuri girişi (ilk 1.7 sn) kesilir, son bölüm dışındakilerin "PART N" kartı (son 1.8 sn) kesilir.
- Dikey video ortada, arkada bulanık büyütülmüş kopyası; sol üstte "PART N".
"""
import os, subprocess, sys, tempfile

INTRO, END = 1.7, 1.8


def sh(a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])


def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).strip())


def main(out, eps):
    tmp = tempfile.mkdtemp(prefix='mkc_')
    parts = []
    for i, e in enumerate(eps):
        ss = 0 if i == 0 else INTRO
        to = dur(e) - (0 if i == len(eps) - 1 else END)
        p = os.path.join(tmp, f'p{i}.mp4')
        vf = ("[0:v]split[a][b];[a]scale=1920:-2,crop=1920:1080,gblur=sigma=30,eq=brightness=-0.25[bg];"
              "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,"
              f"drawtext=fontfile={os.environ.get('MK_FONT', os.path.expanduser('~/.fonts/BebasNeue.ttf'))}:text='PART {i + 1}':x=60:y=50:fontsize=64:fontcolor=0xf4ff9a,"
              "fps=30,format=yuv420p[v]")
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{ss}', '-to', f'{to:.3f}', '-i', e, '-filter_complex', vf, '-map', '[v]', '-map', '0:a',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-maxrate', '6M', '-bufsize', '12M', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', p])
        parts.append(p)
    lst = os.path.join(tmp, 'l.txt'); open(lst, 'w').write('\n'.join(f"file '{p}'" for p in parts))
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', out])
    print(out, round(dur(out), 1), 's')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])

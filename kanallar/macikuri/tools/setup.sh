#!/usr/bin/env bash
# Macikuri TV kurulum: Kokoro TTS + fontlar + rsvg. Kullanım: bash tools/setup.sh  (assets -> kanallar/macikuri/assets)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ASSETS="${MK_ASSETS:-$HERE/../assets}"; mkdir -p "$ASSETS" ~/.fonts
command -v rsvg-convert >/dev/null || { SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO=sudo; $SUDO apt-get update -y >/dev/null && $SUDO apt-get install -y librsvg2-bin >/dev/null; }
if [ ! -s "$ASSETS/kokoro-v1.0.int8.onnx" ]; then
  rm -rf /tmp/ss && git clone -q --depth 1 https://github.com/spR1nt23/secret-spawn-videos.git /tmp/ss
  SS_ASSETS="$ASSETS" bash /tmp/ss/tools/setup.sh >/dev/null
fi
if [ ! -s "$ASSETS/creepster.ttf" ]; then
  T="$(mktemp -d)"; ( cd "$T" && npm pack -q @fontsource/creepster @fontsource/special-elite >/dev/null 2>&1 && for t in *.tgz; do mkdir -p "${t%.tgz}"; tar xzf "$t" -C "${t%.tgz}"; done )
  python3 -m pip install -q fonttools brotli 2>/dev/null || python3 -m pip install -q --break-system-packages fonttools brotli
  python3 - "$T" "$ASSETS" <<'PY'
import sys,glob,os
from fontTools.ttLib import TTFont
for f in glob.glob(sys.argv[1]+'/*/package/files/*latin-400-normal.woff'):
    n='creepster.ttf' if 'creepster' in f else 'special-elite.ttf'
    t=TTFont(f); t.flavor=None; t.save(os.path.join(sys.argv[2],n))
PY
fi
cp "$ASSETS"/*.ttf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
echo "Macikuri hazır: $ASSETS"

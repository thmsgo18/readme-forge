#!/usr/bin/env bash
# Turns a screen recording (webm, mp4, mov) into a README-friendly GIF.
#
# Usage: make_gif.sh INPUT OUTPUT.gif [--width 960] [--fps 12] [--start 0] [--duration N] [--speed 1] [--hold 2]
#   --start / --duration trim the clip (seconds), --speed 1.5 plays it 1.5x faster,
#   --hold 2 freezes the last frame 2 s (simulator recordings end on the last change).
# Target: under 5 MB. If bigger, lower --fps (10), --width (800), or trim.
set -euo pipefail

[ $# -ge 2 ] || { sed -n '2,9p' "$0"; exit 2; }
IN="$1"; OUT="$2"; shift 2
WIDTH=960; FPS=12; START=0; DURATION=""; SPEED=1; HOLD=0
while [ $# -gt 0 ]; do
  case "$1" in
    --width) WIDTH="$2"; shift 2 ;;
    --fps) FPS="$2"; shift 2 ;;
    --start) START="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --speed) SPEED="$2"; shift 2 ;;
    --hold) HOLD="$2"; shift 2 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (brew install ffmpeg)" >&2; exit 1; }

# Screen recordings have a variable frame rate: a static screen is one frame held for
# seconds. Convert to a constant rate first, then trim in the filter graph (an input -ss
# or a trim on the raw stream skips held screens entirely).
TRIM="trim=start=${START}"
[ -n "$DURATION" ] && TRIM="${TRIM}:duration=${DURATION}"
mkdir -p "$(dirname "$OUT")"
FILTER="fps=30,${TRIM},setpts=(PTS-STARTPTS)/${SPEED},fps=${FPS},tpad=stop_mode=clone:stop_duration=${HOLD},scale=${WIDTH}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle"
ffmpeg -loglevel error -y -i "$IN" -vf "$FILTER" -loop 0 "$OUT"

BYTES=$(wc -c < "$OUT" | tr -d ' ')
MB=$(awk "BEGIN {printf \"%.1f\", $BYTES/1048576}")
echo "saved $OUT ($MB MB)"
awk "BEGIN {exit !($BYTES > 5242880)}" && echo "warning: over 5 MB, lower --fps or --width, or trim with --start/--duration" >&2
exit 0

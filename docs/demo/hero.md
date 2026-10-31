# Hero image

`docs/assets/hero-github-forge.png` shows the top of the github-forge README as GitHub renders it, light and dark side by side.

To regenerate it from a clone of github-forge:

1. `python3 scripts/preview_readme.py README.md --screenshot --out /tmp/hero` (run from the github-forge folder, with this repository's scripts).
2. In both HTML files, point the terminal GIF to a still of its last frame (`ffmpeg -sseof -0.2 -i docs/assets/demo-audit.gif -frames:v 1 last.png`), so the score is visible. If a badge still shows an old value, replace its `camo.githubusercontent.com` URL with the direct shields.io URL: GitHub's image proxy caches badges for a while.
3. `node scripts/capture_web.cjs shot --url file:///tmp/hero/readme-light.html --out top-light.png --width 1012 --height 1060 --scale 2`, and the same for `readme-dark.html`.
4. Paste both captures side by side with rounded corners on a light grey background, then resize to 1800 pixels wide.

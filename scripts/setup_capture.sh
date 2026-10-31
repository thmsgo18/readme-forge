#!/usr/bin/env bash
# Installs playwright-core (driver only, no browser download) into a cache
# folder used by capture_web.cjs. It drives the Google Chrome already installed.
# Safe to run repeatedly.
set -euo pipefail

CACHE="${READMEFORGE_CACHE:-$HOME/.cache/readme-forge}"
VERSION="1.63.0"

if [ -f "$CACHE/node_modules/playwright-core/package.json" ]; then
  echo "playwright-core already installed in $CACHE"
  exit 0
fi

command -v node >/dev/null || { echo "node is required (brew install node)" >&2; exit 1; }
mkdir -p "$CACHE"
cd "$CACHE"
[ -f package.json ] || echo '{"name":"readme-forge-cache","private":true}' > package.json
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install --no-audit --no-fund --silent "playwright-core@$VERSION"
echo "playwright-core $VERSION installed in $CACHE"

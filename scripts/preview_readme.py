#!/usr/bin/env python3
"""Render a README the way GitHub does, and optionally screenshot it.

Usage: python3 preview_readme.py README.md [--out DIR] [--screenshot] [--repo OWNER/REPO]

Uses GitHub's own Markdown API (through the authenticated `gh` CLI), wraps the
result in GitHub's stylesheet, and writes preview-light.html and
preview-dark.html to DIR (default: a temp folder). Relative images resolve
against the README's folder. With --screenshot, also writes full-page PNGs
(via capture_web.cjs) so you can look at the result with your image viewer.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CSS = "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown-{theme}.min.css"
PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><base href="{base}">
<link rel="stylesheet" href="{css}">
<style>
  body {{ background: {bg}; margin: 0; }}
  .markdown-body {{ box-sizing: border-box; max-width: 980px; margin: 0 auto; padding: 32px 45px; }}
</style></head>
<body><article class="markdown-body">{html}</article></body></html>
"""


BLOCK_START = re.compile(r"^\s*([-*+]\s|\d+[.)]\s|#|\||>|<|```|~~~|$)")


def unwrap_soft_breaks(text):
    """GitHub's API in gfm mode renders every newline as <br> (comment style), while
    README files ignore single newlines. Join wrapped paragraph lines so the preview
    matches the README view, keeping code blocks, lists, tables, quotes and HTML intact."""
    out, fence = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if fence:
            out.append(line)
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith(("```", "~~~")):
            fence = stripped[:3]
            out.append(line)
            continue
        prev = out[-1] if out else ""
        can_join = (prev.strip() and not prev.rstrip().endswith(("  ", "\\")) and not prev.endswith("  ")
                    and not re.match(r"^\s*(#|\||<|```|~~~)", prev) and not BLOCK_START.match(line))
        if can_join:
            out[-1] = prev.rstrip() + " " + stripped
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def main():
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("--"):
        print(__doc__)
        sys.exit(2)
    readme = Path(argv[0]).resolve()
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else Path(tempfile.mkdtemp(prefix="readme-preview-"))
    out.mkdir(parents=True, exist_ok=True)
    repo = argv[argv.index("--repo") + 1] if "--repo" in argv else None
    if not repo:  # GitHub needs the repo as context to embed user-attachments videos
        remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=readme.parent,
                                capture_output=True, text=True).stdout
        m = re.search(r"github\.com[:/]([^/]+/[^/.\s]+?)(?:\.git)?\s*$", remote)
        repo = m.group(1) if m else None

    body = {"text": unwrap_soft_breaks(readme.read_text(encoding="utf-8")), "mode": "gfm"}
    if repo:
        body["context"] = repo
    res = subprocess.run(["gh", "api", "/markdown", "--input", "-"], input=json.dumps(body),
                         capture_output=True, text=True)
    if res.returncode != 0:
        print("gh api /markdown failed (is gh installed and authenticated?):\n" + res.stderr, file=sys.stderr)
        sys.exit(1)

    base = readme.parent.as_uri() + "/"
    stem = readme.stem.replace(".", "-").lower()
    pages = []
    for theme, bg in (("light", "#ffffff"), ("dark", "#0d1117")):
        page = out / f"{stem}-{theme}.html"
        page.write_text(PAGE.format(base=base, css=CSS.format(theme=theme), bg=bg, html=res.stdout), encoding="utf-8")
        pages.append((theme, page))
        print(f"wrote {page}")

    if "--screenshot" in argv:
        script = Path(__file__).with_name("capture_web.cjs")
        for theme, page in pages:
            png = page.with_suffix(".png")
            cmd = ["node", str(script), "shot", "--url", page.as_uri(), "--out", str(png),
                   "--width", "1012", "--height", "900", "--scale", "1", "--full-page", "--wait", "1500"]
            if theme == "dark":
                cmd.append("--dark")
            subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()

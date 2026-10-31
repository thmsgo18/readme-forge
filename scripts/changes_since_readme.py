#!/usr/bin/env python3
"""List what changed in a project since its README was last committed.

Usage: python3 changes_since_readme.py [PROJECT_DIR] [--since REF]

Prints JSON: the last commit that touched README.md / README.fr.md, the
commits since then, changed files grouped by kind, manifest version
changes, and the README images that may be stale because user-facing
code changed after they were last updated. Standard library only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

UI_EXT = {".dart", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss", ".swift", ".kt", ".xib",
          ".storyboard", ".arb", ".tape"}
MANIFESTS = ["package.json", "pyproject.toml", "pubspec.yaml", "Cargo.toml", "setup.cfg", "setup.py", "go.mod",
             "composer.json", "action.yml"]
IMAGE_RE = re.compile(r"(?:src=\"|\]\()(?!https?:)([^\")\s]+\.(?:png|jpe?g|gif|webp|svg))", re.I)


def git(args, cwd):
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def kind(path):
    p = Path(path)
    low = path.lower()
    if p.name in MANIFESTS or p.name.endswith((".lock", "-lock.json")):
        return "manifests"
    if low.startswith(".github/") or "workflow" in low:
        return "ci"
    if re.search(r"(^|/)(tests?|spec|__tests__)/|_test\.|\.test\.|\.spec\.", low):
        return "tests"
    if p.suffix.lower() in {".md", ".rst", ".txt"} or low.startswith("docs/"):
        return "docs"
    if p.suffix.lower() in UI_EXT and not low.startswith("docs/"):
        return "ui_or_source"
    return "source" if p.suffix else "other"


def version_of(text, name):
    patterns = {
        "package.json": r'"version"\s*:\s*"([^"]+)"',
        "pyproject.toml": r'^version\s*=\s*"([^"]+)"',
        "pubspec.yaml": r"^version:\s*([^\s#]+)",
        "Cargo.toml": r'^version\s*=\s*"([^"]+)"',
        "setup.cfg": r"^version\s*=\s*(\S+)",
    }
    m = re.search(patterns.get(name, r"$^"), text or "", re.M)
    return m.group(1) if m else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0] if args else ".").resolve()
    since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else None
    if git(["rev-parse", "--is-inside-work-tree"], root) != "true":
        print(json.dumps({"error": "not a git repository"}))
        sys.exit(1)

    base = since or git(["log", "-1", "--format=%H", "--", "README.md", "README.fr.md"], root)
    if not base:
        print(json.dumps({"error": "README.md was never committed: use the create or improve workflow"}))
        sys.exit(1)
    info = {
        "readme_commit": git(["log", "-1", "--format=%h %ad %s", "--date=short", base], root),
        "readme_uncommitted_changes": bool(git(["status", "--porcelain", "--", "README.md", "README.fr.md"], root)),
    }
    log = git(["log", f"{base}..HEAD", "--no-merges", "--format=%h%x09%ad%x09%s", "--date=short"], root)
    info["commits_since"] = [dict(zip(("hash", "date", "subject"), l.split("\t", 2))) for l in log.splitlines() if l]

    changed = git(["diff", "--name-status", f"{base}..HEAD"], root)
    uncommitted = git(["status", "--porcelain"], root)
    groups = {}
    for line in changed.splitlines():
        status, *paths = line.split("\t")
        path = paths[-1]
        if path in ("README.md", "README.fr.md"):
            continue
        groups.setdefault(kind(path), []).append(f"{status[0]} {path}")
    info["changed_files"] = {k: v[:80] for k, v in sorted(groups.items())}
    info["changed_counts"] = {k: len(v) for k, v in sorted(groups.items())}
    info["uncommitted_files"] = [l[3:] for l in uncommitted.splitlines()][:40]

    versions = {}
    for name in MANIFESTS:
        if (root / name).exists():
            old = version_of(git(["show", f"{base}:{name}"], root), name)
            new = version_of((root / name).read_text(encoding="utf-8", errors="replace"), name)
            if old != new:
                versions[name] = {"before": old, "now": new}
    tag_before = git(["describe", "--tags", "--abbrev=0", base], root)
    tag_now = git(["describe", "--tags", "--abbrev=0"], root)
    if tag_before != tag_now:
        versions["git_tag"] = {"before": tag_before or None, "now": tag_now or None}
    info["version_changes"] = versions

    # Images referenced by the README that predate later user-facing changes
    readme = root / "README.md"
    stale = []
    if readme.exists():
        for img in dict.fromkeys(IMAGE_RE.findall(readme.read_text(encoding="utf-8"))):
            if re.search(r"logo|icon|badge|banner", Path(img).name, re.I):
                continue  # identity assets do not follow UI changes
            img_date = git(["log", "-1", "--format=%ct", "--", img], root)
            if not img_date:
                stale.append({"image": img, "reason": "never committed"})
                continue
            later_ui = git(["log", f"--since={int(img_date) + 1}", "--format=%h", "--", "*.dart", "*.tsx", "*.jsx",
                            "*.vue", "*.svelte", "*.html", "*.css", "*.scss", "*.swift", "*.kt", "*.arb"], root)
            n = len(later_ui.splitlines()) if later_ui else 0
            if n:
                stale.append({"image": img, "reason": f"{n} commit(s) changed UI code after this image was last updated"})
    info["possibly_stale_images"] = stale
    demo = [str(p.relative_to(root)) for p in sorted((root / "docs" / "demo").glob("*"))] if (root / "docs" / "demo").is_dir() else []
    info["capture_scripts"] = demo
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

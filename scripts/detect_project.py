#!/usr/bin/env python3
"""Scan a project folder and print a JSON summary for writing its README.

Usage: python3 detect_project.py [PROJECT_DIR] [--no-github]

Standard library only. Reports manifests, version, languages, detected
technologies, project type hints, git facts, CI workflows, existing
community files and visual assets, and (unless --no-github) the GitHub
repository metadata read through the `gh` CLI.
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python < 3.11
    tomllib = None

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist", "build",
    ".dart_tool", "Pods", ".gradle", ".idea", ".vscode", "target", ".next", ".nuxt",
    "coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache", "DerivedData",
    ".tox", "site-packages", ".cache", "out", ".turbo", ".svelte-kit", "vendor",
}

LANG_BY_EXT = {
    ".py": "Python", ".ipynb": "Jupyter Notebook", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".dart": "Dart", ".swift": "Swift", ".kt": "Kotlin", ".java": "Java", ".go": "Go",
    ".rs": "Rust", ".c": "C", ".h": "C", ".cpp": "C++", ".cc": "C++", ".hpp": "C++",
    ".cs": "C#", ".php": "PHP", ".rb": "Ruby", ".r": "R", ".R": "R", ".tex": "TeX",
    ".vue": "Vue", ".svelte": "Svelte", ".html": "HTML", ".css": "CSS", ".scss": "SCSS",
    ".sh": "Shell", ".lua": "Lua", ".scala": "Scala", ".m": "Objective-C", ".sql": "SQL",
}

# dependency or file marker (lowercase) -> technology label used for badges
TECH_MARKERS = {
    "react": "React", "next": "Next.js", "vue": "Vue.js", "svelte": "Svelte", "@angular/core": "Angular",
    "vite": "Vite", "tailwindcss": "Tailwind CSS", "express": "Express", "fastify": "Fastify",
    "@nestjs/core": "NestJS", "electron": "Electron", "@tauri-apps/api": "Tauri", "typescript": "TypeScript",
    "vitest": "Vitest", "jest": "Jest", "prisma": "Prisma", "@prisma/client": "Prisma",
    "three": "Three.js", "d3": "D3.js", "socket.io": "Socket.IO", "@actions/core": "GitHub Actions",
    "@anthropic-ai/sdk": "Anthropic API", "openai": "OpenAI API", "anthropic": "Anthropic API",
    "django": "Django", "djangorestframework": "Django REST Framework", "fastapi": "FastAPI",
    "flask": "Flask", "streamlit": "Streamlit", "gradio": "Gradio", "pywebview": "pywebview",
    "torch": "PyTorch", "tensorflow": "TensorFlow", "keras": "Keras", "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn", "pandas": "pandas", "numpy": "NumPy", "matplotlib": "Matplotlib",
    "transformers": "Hugging Face Transformers", "sentence-transformers": "Sentence Transformers",
    "faiss-cpu": "FAISS", "faiss": "FAISS", "langchain": "LangChain", "chromadb": "ChromaDB",
    "librosa": "librosa", "opencv-python": "OpenCV", "sqlalchemy": "SQLAlchemy", "pydantic": "Pydantic",
    "typer": "Typer", "click": "Click", "rich": "Rich", "pytest": "pytest", "reportlab": "ReportLab",
    "psycopg2": "PostgreSQL", "psycopg2-binary": "PostgreSQL", "psycopg": "PostgreSQL", "pg": "PostgreSQL",
    "mysql2": "MySQL", "mongoose": "MongoDB", "pymongo": "MongoDB", "redis": "Redis",
    "sqlite3": "SQLite", "better-sqlite3": "SQLite", "drift": "SQLite", "sqflite": "SQLite",
    "flutter": "Flutter", "firebase_core": "Firebase", "firebase": "Firebase", "riverpod": "Riverpod",
    "flutter_riverpod": "Riverpod", "provider": "Provider", "go_router": "go_router",
}

COMMUNITY_FILES = ["README", "LICENSE", "CONTRIBUTING", "SECURITY", "CODE_OF_CONDUCT", "CHANGELOG"]
VISUAL_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp4", ".webm", ".mov"}
VISUAL_DIRS = {"docs", "doc", "assets", "screenshots", "images", "img", "media", ".github", "demo", "static"}


def run(cmd, cwd, timeout=15):
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith(".egg-info")]
        for f in filenames:
            yield Path(dirpath) / f


def read_toml(path):
    if tomllib is None:
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def yaml_block_keys(text, block):
    """Top-level keys of a 2-space indented YAML block (enough for pubspec.yaml)."""
    keys, inside = [], False
    for line in text.splitlines():
        if re.match(rf"^{block}:\s*$", line):
            inside = True
            continue
        if inside:
            if line and not line.startswith(" ") and not line.startswith("#"):
                break
            m = re.match(r"^  ([A-Za-z0-9_\-]+):", line)
            if m:
                keys.append(m.group(1))
    return keys


def parse_requirements(path):
    deps = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if line and not line.startswith("-"):
                deps.append(re.split(r"[<>=!~\[; ]", line)[0].lower())
    except OSError:
        pass
    return deps


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_github = "--no-github" not in sys.argv
    root = Path(args[0] if args else ".").resolve()
    info = {"root": str(root), "name": root.name, "manifests": [], "version": None,
            "license_field": None, "dependencies": [], "technologies": [], "type_hints": [],
            "scripts": {}}
    deps = []

    # --- manifests -------------------------------------------------------
    pkg = root / "package.json"
    if pkg.exists():
        data = read_json(pkg)
        info["manifests"].append("package.json")
        info["name"] = data.get("name") or info["name"]
        info["version"] = data.get("version")
        info["license_field"] = data.get("license")
        info["package_description"] = data.get("description")
        info["scripts"] = data.get("scripts", {})
        deps += list(data.get("dependencies", {})) + list(data.get("devDependencies", {}))
        if data.get("bin"):
            info["type_hints"].append("cli")
        if "vscode" in data.get("engines", {}):
            info["type_hints"].append("vscode-extension")
        if data.get("private") is False or (not data.get("private") and data.get("main")):
            info["type_hints"].append("library")

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        data = read_toml(pyproject)
        info["manifests"].append("pyproject.toml")
        project = data.get("project", {})
        poetry = data.get("tool", {}).get("poetry", {})
        info["name"] = project.get("name") or poetry.get("name") or info["name"]
        info["version"] = info["version"] or project.get("version") or poetry.get("version")
        if "version" in project.get("dynamic", []):
            info["version_source"] = "dynamic (likely git tags)"
        lic = project.get("license")
        info["license_field"] = info["license_field"] or (lic.get("text") if isinstance(lic, dict) else lic)
        info["package_description"] = project.get("description") or poetry.get("description")
        info["python_requires"] = project.get("requires-python")
        deps += [re.split(r"[<>=!~\[; ]", d)[0].lower() for d in project.get("dependencies", [])]
        deps += [d.lower() for d in poetry.get("dependencies", {}) if d.lower() != "python"]
        if project.get("scripts") or poetry.get("scripts"):
            info["type_hints"].append("cli")
            info["scripts"].update(project.get("scripts", {}) or poetry.get("scripts", {}))

    for req in ["requirements.txt", "requirements-dev.txt", "requirements/base.txt"]:
        if (root / req).exists():
            info["manifests"].append(req)
            deps += parse_requirements(root / req)
    for other in ["setup.py", "setup.cfg", "environment.yml", "Pipfile", "go.mod", "pom.xml",
                  "build.gradle", "build.gradle.kts", "composer.json", "Gemfile", "CMakeLists.txt",
                  "Makefile", "DESCRIPTION", "Dockerfile", "docker-compose.yml", "compose.yaml",
                  "mkdocs.yml", "action.yml", "SKILL.md", "manage.py", "vite.config.ts",
                  "vite.config.js", "next.config.js", "next.config.mjs", "tauri.conf.json"]:
        if (root / other).exists():
            info["manifests"].append(other)

    cargo = root / "Cargo.toml"
    if cargo.exists():
        data = read_toml(cargo).get("package", {})
        info["manifests"].append("Cargo.toml")
        info["version"] = info["version"] or data.get("version")
        info["license_field"] = info["license_field"] or data.get("license")
        deps += list(read_toml(cargo).get("dependencies", {}))

    pubspec = root / "pubspec.yaml"
    if pubspec.exists():
        text = pubspec.read_text(encoding="utf-8")
        info["manifests"].append("pubspec.yaml")
        m = re.search(r"^name:\s*([A-Za-z0-9_]+)", text, re.M)
        if m:
            info["name"] = m.group(1)
        m = re.search(r"^version:\s*([^\s#]+)", text, re.M)
        if m:
            info["version"] = info["version"] or m.group(1).split("+")[0]
        m = re.search(r"^description:\s*(.+)$", text, re.M)
        if m:
            info["package_description"] = m.group(1).strip().strip("\"'")
        deps += yaml_block_keys(text, "dependencies") + yaml_block_keys(text, "dev_dependencies")
        platforms = [p for p in ["android", "ios", "macos", "windows", "linux", "web"] if (root / p).is_dir()]
        info["flutter_platforms"] = platforms
        if "flutter" in deps:
            info["type_hints"].append("mobile" if {"android", "ios"} & set(platforms) else "flutter")

    if (root / "Makefile").exists():
        try:
            targets = re.findall(r"^([A-Za-z0-9_\-]+):", (root / "Makefile").read_text(encoding="utf-8"), re.M)
            info["make_targets"] = sorted(set(targets))[:30]
        except OSError:
            pass

    # --- files: languages, notebooks, assets --------------------------------
    lang_bytes, visuals, notebooks, tex = Counter(), [], 0, 0
    xcode = False
    for f in walk(root):
        ext = f.suffix if f.suffix in (".R",) else f.suffix.lower()
        rel = f.relative_to(root)
        if ext in LANG_BY_EXT:
            try:
                lang_bytes[LANG_BY_EXT[ext]] += f.stat().st_size
            except OSError:
                pass
        if ext == ".ipynb":
            notebooks += 1
        if ext == ".tex":
            tex += 1
        if ext in VISUAL_EXT and (rel.parts[0] in VISUAL_DIRS or len(rel.parts) == 1):
            try:
                visuals.append({"path": str(rel), "kb": round(f.stat().st_size / 1024)})
            except OSError:
                pass
        if f.name == "project.pbxproj":
            xcode = True
    total = sum(lang_bytes.values()) or 1
    info["languages"] = [{"name": k, "percent": round(100 * v / total, 1)}
                         for k, v in lang_bytes.most_common(8) if 100 * v / total >= 1]
    info["notebooks"] = notebooks
    info["existing_visuals"] = sorted(visuals, key=lambda v: v["path"])[:60]
    if xcode:
        info["type_hints"].append("apple-native")
    if notebooks >= 2 or (notebooks and not info["manifests"]):
        info["type_hints"].append("notebook/research")
    if tex >= 3:
        info["type_hints"].append("latex")
    if (root / "SKILL.md").exists() or list(root.glob("skills/*/SKILL.md")):
        info["type_hints"].append("claude-skill")
    if (root / ".claude-plugin" / "plugin.json").exists():
        info["type_hints"].append("claude-plugin")
    if (root / "action.yml").exists() or (root / "action.yaml").exists():
        info["type_hints"].append("github-action")
    if (root / "manage.py").exists():
        info["type_hints"].append("web-backend")
    if any((root / n).exists() for n in ["index.html", "public/index.html", "src/App.tsx", "src/App.jsx",
                                          "src/App.vue", "vite.config.ts", "vite.config.js"]):
        info["type_hints"].append("web-frontend")
    if "electron" in deps or "pywebview" in deps or "@tauri-apps/api" in deps:
        info["type_hints"].append("desktop")
    # Sub-projects (monorepo / fullstack): manifests one level down
    subs = []
    for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith(".")):
        found = [m for m in ["package.json", "pyproject.toml", "requirements.txt", "pubspec.yaml", "manage.py",
                             "Cargo.toml", "go.mod"] if (d / m).exists()]
        if found:
            subs.append({"dir": d.name, "manifests": found})
            if (d / "package.json").exists():
                sub = read_json(d / "package.json")
                deps += list(sub.get("dependencies", {})) + list(sub.get("devDependencies", {}))
            if (d / "requirements.txt").exists():
                deps += parse_requirements(d / "requirements.txt")
    if subs:
        info["subprojects"] = subs

    deps = sorted(set(d.lower() for d in deps if d))
    info["dependencies"] = deps[:120]
    techs = []
    for d in deps:
        label = TECH_MARKERS.get(d)
        if label and label not in techs:
            techs.append(label)
    info["technologies"] = techs
    info["type_hints"] = sorted(set(info["type_hints"]))

    # --- community / agent files -------------------------------------------
    present = {}
    for f in sorted(os.listdir(root)):
        for base in COMMUNITY_FILES:
            if f.upper().startswith(base):
                present.setdefault(base, []).append(f)
    gh_dir = root / ".github"
    for base in ["CONTRIBUTING", "SECURITY", "CODE_OF_CONDUCT"]:
        for f in gh_dir.glob(f"{base}*") if gh_dir.is_dir() else []:
            present.setdefault(base, []).append(f".github/{f.name}")
    info["community_files"] = present
    info["agent_docs"] = [n for n in ["CLAUDE.md", "AGENTS.md", "AGENT.md", ".cursorrules"] if (root / n).exists()]
    wf = gh_dir / "workflows"
    info["ci_workflows"] = sorted(p.name for p in wf.glob("*.y*ml")) if wf.is_dir() else []
    if (root / "README.md").exists():
        info["readme_lines"] = len((root / "README.md").read_text(encoding="utf-8", errors="replace").splitlines())

    # --- git -----------------------------------------------------------------
    git = {"is_repo": run(["git", "rev-parse", "--is-inside-work-tree"], root) == "true"}
    if git["is_repo"]:
        remote = run(["git", "remote", "get-url", "origin"], root)
        git["remote"] = remote
        m = re.search(r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?$", remote or "")
        if m:
            git["owner"], git["repo"] = m.group(1), m.group(2)
        git["branch"] = run(["git", "branch", "--show-current"], root)
        first = run(["git", "log", "--reverse", "--format=%ad", "--date=format:%Y"], root)
        git["first_commit_year"] = first.splitlines()[0] if first else None
        git["latest_tag"] = run(["git", "describe", "--tags", "--abbrev=0"], root)
        authors = run(["git", "shortlog", "-sn", "--all", "--no-merges", "HEAD"], root)
        git["authors"] = [re.sub(r"^\s*\d+\s+", "", a) for a in (authors or "").splitlines()][:8]
        subjects = run(["git", "log", "-12", "--format=%s"], root)
        git["recent_commit_subjects"] = (subjects or "").splitlines()
        status = run(["git", "status", "--porcelain"], root)
        git["uncommitted_changes"] = len(status.splitlines()) if status else 0
    info["git"] = git

    # --- GitHub --------------------------------------------------------------
    if use_github and git.get("owner"):
        raw = run(["gh", "repo", "view", f"{git['owner']}/{git['repo']}", "--json",
                   "description,repositoryTopics,visibility,homepageUrl,latestRelease,defaultBranchRef,"
                   "stargazerCount,isFork"], root, timeout=20)
        if raw:
            data = json.loads(raw)
            info["github"] = {
                "description": data.get("description"),
                "topics": [t["name"] for t in (data.get("repositoryTopics") or [])],
                "visibility": data.get("visibility"),
                "homepage": data.get("homepageUrl"),
                "latest_release": (data.get("latestRelease") or {}).get("tagName"),
                "default_branch": (data.get("defaultBranchRef") or {}).get("name"),
                "stars": data.get("stargazerCount"),
                "is_fork": data.get("isFork"),
            }
        else:
            info["github"] = {"error": "gh repo view failed (not authenticated, no access, or repo missing)"}

    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

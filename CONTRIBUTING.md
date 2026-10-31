# Contributing to readme-forge

Thanks for taking the time to contribute. Bug reports, fixes and new ideas are all welcome.

## Reporting a bug

Open an [issue](https://github.com/thmsgo18/readme-forge/issues) with:

- what you asked Claude, or the exact script command you ran,
- what you expected and what happened instead (full output, or the part of the README that came out wrong),
- your environment: OS, `python3 --version`, `node --version`, and the kind of project you were documenting.

For a security issue, do not open a public issue: see [SECURITY.md](SECURITY.md).

## Suggesting a feature

Open an issue describing the situation the skill handles badly before writing anything, so we can agree on the approach. A link to a public repository where it happens helps a lot.

## Development setup

Clone the repository anywhere and link it as a personal skill, so your edits apply immediately:

```bash
git clone https://github.com/thmsgo18/readme-forge.git
ln -s "$PWD/readme-forge" ~/.claude/skills/readme-forge
cd readme-forge
pre-commit install
bash scripts/setup_capture.sh   # only to work on screenshots and videos
```

## Running the checks

These are the commands CI runs on every pull request:

```bash
python3 -m py_compile scripts/*.py
node --check scripts/capture_web.cjs
for f in scripts/*.sh; do bash -n "$f"; done
python3 scripts/detect_project.py . --no-github
python3 scripts/lint_readme.py .
```

The last one lints this repository's own README with the skill's rules. Test a change on a real project too, ideally one with a UI and one without.

## Project conventions

- `SKILL.md` stays short and routes to `references/`, where the detailed rules live. Keep each reference focused on one topic.
- Scripts use the Python standard library only. `capture_web.cjs` needs `playwright-core` (installed by `setup_capture.sh`) and the user's Google Chrome; it never downloads a browser.
- Every rule the linter enforces is written in a reference file, and the other way round.
- Commits and pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/). The title becomes the commit on `main` (squash merge).

## Submitting a pull request

1. Fork the repository and create a branch from `main`.
2. Make your change, and try it on a real project when it changes what the skill produces.
3. Run the checks above.
4. Open a pull request that explains what changed and why.

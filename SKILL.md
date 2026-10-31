---
name: readme-forge
description: Write a professional bilingual README for the project in the current folder (README.md in English plus README.fr.md in French, linked to each other) with badges, real screenshots and GIFs captured from the running project, an MIT LICENSE, CONTRIBUTING.md, SECURITY.md, and the GitHub description and topics. Also scores an existing README out of 100 and updates a README after the code changed. Use it whenever the user wants to create, rewrite, improve, audit, update or polish a README or the GitHub presentation of a repository, for example "fais le readme", "refais le README", "README pro", "README bilingue", "prépare ce repo pour GitHub", "ajoute la licence, le contributing et le security", "description et topics GitHub", "audite mon README", "mets à jour le README", "write a README for this repo", "make this repo look professional", even when they mention only one of these pieces.
---

# readme-forge

Produce the full public face of a repository: a README that makes a visitor want to try the project within ten seconds, its French twin, the community files, the visuals, and the GitHub metadata. The quality bar: a centered header with a one-line promise, a row of badges, a hero visual right away, then short sections that get the reader running.

## Owner

Read the owner once per run, from the machine and the repository. Never guess, and never publish something the user did not choose to publish.

| | Where it comes from |
|---|---|
| Name (LICENSE, footer): `{{AUTHOR}}` | `git config user.name`, else `gh api user --jq .name`. Ask if both are empty or only give a login |
| GitHub login: `OWNER` in links and badges | The owner of the `origin` remote, else `gh api user --jq .login` |
| Security contact | GitHub private vulnerability reporting on a public repository. An email only if the user gives one for this purpose: ask, never take it from git config or commits |

Talk to the user in their language. Write the deliverables in the language each file requires.

## Pick the mode

| Situation | Mode | Go to |
|---|---|---|
| No README, or a minimal one | **Create** | the workflow below |
| A README exists but is not in readme-forge format, or the user wants it redone | **Improve** | audit it first (score before), then the workflow below |
| README.md and README.fr.md already in readme-forge format, and the project changed or the user asks to refresh | **Update** | `references/update-mode.md` |
| The user asks to rate, review or check a README | **Audit only** | `references/audit-rubric.md`, change nothing |

When the request is ambiguous between update and improve, run `scripts/changes_since_readme.py` and the lint: a README that passes the lint and needs a handful of edits is an update; one that needs restructuring is an improve.

## Deliverables

1. `README.md`: English, the main README.
2. `README.fr.md`: French, same content adapted (not a word-for-word translation).
3. `LICENSE`: MIT.
4. `CONTRIBUTING.md` and `SECURITY.md`: English only.
5. Visuals in `docs/assets/` (or the folder the repo already uses), plus the tapes or scenarios that produced them in `docs/demo/` so they can be regenerated.
6. GitHub description and topics (applied only after the user agrees).

## Hard rules

These come straight from the owner. Each exists because breaking it makes a repo look careless or machine-written.

- **No emoji anywhere**: READMEs, community files, GitHub description, topics, commit messages. This includes the check and cross marks in comparison tables (write "Yes" / "No", "Oui" / "Non") and decorative stars or rockets. Emojis are the first thing that makes a README read as generated.
- **No long dashes, and no hyphen pretending to be one.** No em dash, no en dash (ranges become "20 to 30 min"), no " - " or " -- " in the middle of a sentence. Rewrite with a comma, a colon, parentheses, or two sentences. Hyphenated words, CLI flags, list markers and table rules are fine.
- **Nothing that hints at AI authorship.** Commit messages never mention AI or Claude and never carry a `Co-Authored-By` or "Generated with" trailer, whatever your usual habit is. READMEs never say they were generated. (A README may of course talk about Claude when the project itself is a Claude skill: Claude is then the subject, not the author.)
- **Language switch at the very top of both READMEs**, exactly as in the header template.
- **Badges at the top**: technologies, license, version.
- **Length: 100 to 200 lines per README.** Long reference material (every command, every OS install path, full config) goes into `<details>` blocks or a `docs/` page linked from the README. A visitor skims; a wall of text loses them.
- **Nothing invented.** Every command, flag, number, feature, link and requirement must come from the code, the manifests, or from running the project. If something cannot be verified, leave it out or ask.
- **Ask before anything leaves the machine**: commit, push, `gh repo edit`, enabling a GitHub setting.

## Workflow

### 1. Understand the project

```bash
python3 ~/.claude/skills/readme-forge/scripts/detect_project.py .
```

The JSON gives manifests, version, languages, detected technologies, project type hints, git facts (remote, first commit year, authors, recent commit subjects), CI workflows, existing community files and images, and the GitHub state (visibility, description, topics, homepage, latest release).

Then read what a newcomer would need to understand the project: the existing README and docs, `CLAUDE.md` / `AGENTS.md`, the manifest, the entry points, the main modules, the tests and CI. Run the help output of a CLI. Work out, in your own words:

- what it is, in one sentence, and who it is for;
- the problem it solves and what makes it different from the obvious alternative;
- how someone installs and runs it, verified;
- the three to seven features that matter most to a user (not to the developer);
- the project type (see `references/readme-structure.md`), which drives sections and visuals.

**If a README already exists, you are improving it.** Score it first with `references/audit-rubric.md` and keep the report: it tells you what to fix and gives the "before" score. Then harvest everything accurate and valuable: commands, video embeds (`https://github.com/user-attachments/assets/...`), YouTube links, existing screenshots, logos, related-project links. Keep a note of what you drop and why, so you can tell the user.

**Visibility matters.** Dynamic shields.io badges and GitHub private vulnerability reporting only work on public repositories; for private ones use static badges and an email-only security contact. A private repository's README is a showcase (portfolio, store page companion): no Contributing section and no links to issues, which nobody else can open; a single footer line points to CONTRIBUTING.md and SECURITY.md. Store badges (App Store, registries) still work and matter more there.

### 2. Plan, then check in once

Before capturing anything (captures are the slow part, and a wrong angle wastes them), show the user a compact plan in French:

- the tagline (EN and FR) and the angle of the opening paragraph;
- the section list;
- the visuals: for each one, what it shows, how you will capture it, and its file name;
- the badges;
- the GitHub description and topics;
- only the questions you cannot answer from the code: a demo URL, whether it is published on a registry or store, the team members of a school project, data that must not appear on screen.

Use AskUserQuestion when available. If the user said to go ahead without questions, skip this step and state your assumptions in the final summary.

### 3. Capture the visuals

Read `references/visuals.md`. It covers terminal GIFs with vhs, web screenshots and videos with `scripts/capture_web.cjs`, iOS and Android simulators, desktop apps, and projects with no UI (Mermaid diagrams, code plus output).

Non-negotiable: use demo data, never the owner's real data, credentials or personal information, and look at every image you produce (open it with Read) before using it. A screenshot with an error toast, a debug banner, a half-loaded page or someone's email in it is worse than no screenshot. Stop every server or simulator you started.

### 4. Write README.md

Follow `references/readme-structure.md` for the header block, section order and per-type variations, `references/style-guide.md` for the writing, and `references/badges.md` for the badge rows.

### 5. Write README.fr.md

Same structure, same visuals, same badges, adapted to natural French. The French-specific rules are at the end of `references/style-guide.md`. Recompute every anchor link from the French headings.

### 6. LICENSE, CONTRIBUTING.md, SECURITY.md

Follow `references/community-files.md`. The MIT text is in `assets/LICENSE-MIT.txt`. Do not replace an existing non-MIT license without asking.

### 7. Verify

```bash
python3 ~/.claude/skills/readme-forge/scripts/lint_readme.py . --online
python3 ~/.claude/skills/readme-forge/scripts/preview_readme.py README.md --screenshot
python3 ~/.claude/skills/readme-forge/scripts/preview_readme.py README.fr.md --screenshot
```

Fix every lint error, and judge each warning. The preview renders the files through GitHub's own Markdown API in light and dark themes; open the PNGs and look at them as a visitor would: does the top screen sell the project, do the badges render with their icons, are images sharp and sized well, is anything invisible in dark mode (a black logo on a transparent background, for example)?

Then reread both READMEs once with fresh eyes, asking: would the owner have written this sentence? Is every claim true? Is there a shorter way to say it?

Finally, score README.md with `references/audit-rubric.md`. The target is 85 or more with zero lint errors; below that, fix the lowest criteria and score again. Keep the before and after scores for the summary.

### 8. GitHub metadata

Draft the description and topics following `references/github-metadata.md`. Do not apply them yet.

### 9. Wrap up and ask

Give the user a short summary in French: the audit score (before and after when a README existed), files created or changed, visuals captured, what was dropped from the old README and why, line counts, the proposed description and topics, and anything they should do by hand (for example uploading a social preview image). Then ask, in one AskUserQuestion with multiSelect, which of these to do:

- apply the description and topics on GitHub (and enable private vulnerability reporting on a public repo);
- commit;
- push.

Commit message: follow the repository's own convention, visible in the recent commit subjects (language, prefix style, tense). For example `docs: add bilingual README, MIT license and community files`, or `Ajoute un README bilingue, la licence MIT et les fichiers communautaires` in a repo that commits in French. No AI mention, no trailer. Stage only the files this skill created or changed, never unrelated work in progress.

## Reference files

- `references/readme-structure.md`: header template, section order, per-type variants, length budget. Read before writing.
- `references/style-guide.md`: voice, words to avoid, dash rewrites, French adaptation. Read before writing.
- `references/badges.md`: badge rows, URL patterns, technology colors and logos.
- `references/visuals.md`: how to capture each kind of project, embedding snippets, size limits.
- `references/community-files.md`: LICENSE, CONTRIBUTING.md, SECURITY.md templates and rules.
- `references/github-metadata.md`: description, topics, homepage, `gh` commands.
- `references/audit-rubric.md`: the 100-point rubric, the source check, the audit report format.
- `references/update-mode.md`: refreshing an existing readme-forge README after the project changed.

## Scripts

All in `~/.claude/skills/readme-forge/scripts/`:

| Script | Purpose |
|---|---|
| `detect_project.py [DIR]` | Project facts as JSON (add `--no-github` offline) |
| `lint_readme.py [DIR] [--online]` | Checks every hard rule, links, anchors, badges, EN/FR parity |
| `changes_since_readme.py [DIR] [--since REF]` | Commits, changed files, version bumps and possibly stale images since the README was last committed |
| `preview_readme.py FILE [--screenshot]` | GitHub-accurate render, light and dark, as HTML and PNG |
| `setup_capture.sh` | One-time install of the Playwright driver (uses the installed Chrome) |
| `capture_web.cjs shot ...` / `scenario FILE` | Web screenshots and scripted demo videos with a visible cursor |
| `make_gif.sh IN OUT.gif [...]` | Screen recording to an optimized GIF (`--hold` freezes the last frame) |
| `list_windows.swift [app]` | macOS window ids for `screencapture -l` |

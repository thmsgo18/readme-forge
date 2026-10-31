# README structure

## Contents
1. Header block (EN and FR templates)
2. Section order and line budget
3. Variants by project type
4. Visual placement
5. Footer
6. Worked skeleton

## 1. Header block

The first screen decides whether a visitor keeps reading. It must show, in this order: the language switch, the identity (logo or title), a one-line promise, the badges, a few navigation links. Then a horizontal rule and immediately the hero visual.

English (`README.md`):

```html
<p align="right"><b>English</b> | <a href="./README.fr.md">Français</a></p>

<p align="center">
  <img src="docs/assets/logo.png" alt="Project Name" width="360">
</p>

<p align="center">
  <b>One sentence that says what the reader gets, in their terms.</b>
</p>

<p align="center">
  <a href="https://github.com/OWNER/REPO/releases"><img src="https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&color=blue" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License MIT"></a>
  <a href="https://github.com/OWNER/REPO/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI"></a>
  <br>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> •
  <a href="#features">Features</a> •
  <a href="#how-it-works">How it works</a> •
  <a href="#contributing">Contributing</a>
</p>

---
```

French (`README.fr.md`), identical except for the text:

```html
<p align="right"><a href="./README.md">English</a> | <b>Français</b></p>
...
  <b>La même promesse, écrite comme un francophone l'écrirait.</b>
...
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-green?style=for-the-badge" alt="Licence MIT"></a>
...
  <a href="#démarrage-rapide">Démarrage rapide</a> •
  <a href="#fonctionnalités">Fonctionnalités</a> •
```

Notes:
- No logo in the repo: use `<h1 align="center">Project Name</h1>` instead of the image. Do not invent a logo.
- A logo with dark text on a transparent background disappears in GitHub dark mode. If the preview shows it, wrap it in `<picture>` with a `prefers-color-scheme: dark` source, or ask the user for a light variant.
- The separator in the nav row is the bullet `•` surrounded by spaces.
- Anchors follow GitHub's rule: lowercase, punctuation removed (accents kept), spaces become hyphens. "Besoin d'aide ?" becomes `#besoin-daide-`. The linter checks every anchor.

## 2. Section order and line budget

Target 100 to 200 lines in total. Rough budget:

| Section | Lines | Required |
|---|---|---|
| Header block + rule | 20 to 30 | yes |
| Hero visual | 3 to 5 | yes, unless truly nothing can be shown |
| Opening ("What is X?" or no heading) | 4 to 8 | yes |
| See it in action (video or GIF + YouTube badge) | 3 to 6 | when a video or long GIF exists |
| Quick start / Install | 10 to 30 | yes |
| Features | 8 to 15 | yes |
| Screenshots gallery | 6 to 15 | when there are 3+ good screenshots |
| Usage / Example | 10 to 25 | yes for CLIs, libraries, skills |
| How it works / Architecture | 5 to 15 | when it helps trust or contribution |
| Project-type extras (see below) | 5 to 20 | depends |
| Contributing | 1 to 3 | public: one sentence + link; private: one footer line |
| License | 2 | yes |
| Author / Related projects | 2 to 6 | yes for Author; Related when sibling repos exist |

Section rules:
- **Opening**: problem, then what the project does about it, then what makes it different. Concrete, short paragraphs. One line on an important constraint if relevant ("No account, no cloud. Everything lives in one file on your machine.").
- **Quick start**: the shortest verified path from zero to the first result, as copy-paste commands. Put alternatives (other OS, manual install) in `<details>`.
- **Features**: 5 to 8 bullets, each a bold lead of two to five words followed by one sentence of user benefit. Order by what a user cares about first.
- **Usage**: a real example with real output when possible. For an interactive tool, a transcript in a `text` code block.
- **Contributing**: "Bug reports and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md)." Add "Security issues: see [SECURITY.md](SECURITY.md)." on the same line or the next.
  Private repository: no Contributing section (nobody else can open issues or pull requests). End the README with one line instead, for example "Development notes: [CONTRIBUTING.md](CONTRIBUTING.md) · Security: [SECURITY.md](SECURITY.md)", and give the contact email for questions.
- **License**: `[MIT](LICENSE) © {{AUTHOR}}` (FR: `[MIT](LICENSE) © {{AUTHOR}}`, with the heading "Licence").
- **Author**: `Made by [OWNER](https://github.com/OWNER)` (FR: `Réalisé par [OWNER](https://github.com/OWNER)`). For a team project, list every member with their GitHub link.

## 3. Variants by project type

**CLI tool.** Hero: terminal GIF of the main command producing its result. Add a compact command reference table (or put the full one in `<details>`). Show shell completion or config only if they exist.

**Library / package.** Hero: a short code example with its output, or a diagram if the output is visual. Sections: Install (registry command), Usage (one minimal and one realistic example), API overview (table of the main entry points, link to full docs).

**Web app (frontend or full stack).** Hero: screenshot of the main screen at 1280 wide, or a GIF of the key flow. Add a screenshots gallery, the tech stack (badges are enough, or a short table split by front/back), and a "Run locally" section with the env vars required (names only, never values) and how to seed demo data. Link the live demo first if one exists.

**Mobile app.** Hero: a row of three or four phone screenshots side by side, or one GIF of the main flow in a phone-sized frame. Sections: Features, Screenshots, Build and run (per platform, with `<details>`), Privacy note if data stays on device.

**Desktop app.** Hero: the main window. Install per OS in `<details>` blocks, with what to do on the first launch (Gatekeeper, SmartScreen). State where user data lives.

**Claude skill or plugin.** Hero: a GIF or screenshots of the output the skill produces. Sections: Install (personal and project, plus the zip for the Claude apps if one exists), What it does, Example (a conversation transcript in a code block), How it works, Requirements.

**VS Code extension.** Hero: GIF inside VS Code. Sections: Getting started, Features (per command group), Commands table, Settings, Requirements. Marketplace badge for the version.

**GitHub Action.** Hero: a diagram of the pipeline (Mermaid) or a screenshot of the run summary or the PR it opens. Sections: Usage (workflow YAML), Inputs and outputs tables, Permissions required, Examples.

**ML, data or research project (often a school project).** Hero: the most telling result (plot, demo screenshot, results table) or the pipeline diagram. Sections: Context (course, school, year, team), Approach (pipeline diagram + short explanation), Results (table with metrics and the evaluation setup), Dataset (source, license, how to get it), Reproduce (environment and commands), Report or slides link if any. Be precise about numbers and never round them up.

**Template or asset collection.** Hero: a grid of previews (4 to 8 thumbnails). Sections: Browse, Install or use, Contribute a new item.

**Monorepo or full stack with sub-projects.** One README at the root presenting the whole product, with a "Project structure" section mapping folders to roles. Do not duplicate per-package READMEs.

## 4. Visual placement

- The hero sits right after the header rule, before any heading.
- One visual per idea. A screenshot that repeats the previous one adds length, not value.
- Prefer a 2-column table for pairs of screenshots (snippet in `references/visuals.md`).
- Every image has a meaningful `alt` text in the README's language.
- Put a `<sub>` caption under a gallery only if it adds information ("Screenshots of the real app, filled with demo data.").

## 5. Footer

End with Contributing, License, then Author or Related projects. No "Thanks for reading", no "Star this repo" banner with an emoji. A single sober line asking for a star is acceptable if the owner already uses one in that repo.

## 6. Worked skeleton

```markdown
<header block>

---

<p align="center">
  <img src="docs/assets/demo.gif" alt="Creating a project from the terminal" width="900">
</p>

Short opening paragraph: the problem in one or two sentences, then what the project does.

One sentence on what makes it different, or the constraint that matters.

## Quick start

```bash
install command
first command that produces a result
```

<details>
<summary>Other ways to install</summary>
...
</details>

## Features

- **Bold lead**: one sentence of user benefit.
- ...

## Screenshots

<table>...</table>

## How it works

Short explanation, optional Mermaid diagram.

## Contributing

Bug reports and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). Security issues: see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © {{AUTHOR}}

## Author

Made by [OWNER](https://github.com/OWNER)
```

# Audit rubric (score out of 100)

Adapted from the 22-criterion rubric of [adewale/good-readme](https://github.com/adewale/good-readme) (MIT), reworked for the owner's rules and for bilingual READMEs.

## Contents
1. When to audit
2. Inputs
3. The rubric (7 categories)
4. Source check (claims against code)
5. Report format

## 1. When to audit

- **Audit only**: the user asks to rate, review, check or audit a README. Produce the report, change nothing.
- **Before improving** an existing README: score it first, so the user sees where it stands and what will change.
- **After writing or updating** (step 7 of the workflow): score the result. The target is **85 or more** with zero lint errors. Below 85, fix the lowest criteria and score again before handing over.

Score `README.md`. The French twin is covered by the lint parity checks and by criterion 7.2; mention any French-only problem in the report.

## 2. Inputs

Gather these before scoring, so every point is backed by evidence:

```bash
python3 ~/.claude/skills/readme-forge/scripts/lint_readme.py . --online
python3 ~/.claude/skills/readme-forge/scripts/detect_project.py .
python3 ~/.claude/skills/readme-forge/scripts/preview_readme.py README.md --screenshot
```

Then read the README fully, look at the preview PNG (first screen as a visitor sees it), and run the source check (section 4).

## 3. The rubric

Score each criterion with the full range; half points are not used. "Good" describes the top score, "Bad" the bottom.

### 1. First screen (20)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 1.1 | Ten-second clarity | 5 | Tagline plus first paragraph say what it is and who it is for, in plain words | Logo and badges, then nothing explains the project before the first heading |
| 1.2 | Value | 5 | States the concrete benefit or what makes it different from the obvious alternative | No reason to pick it over doing nothing |
| 1.3 | Proof above the fold | 5 | A real screenshot, GIF or output is visible without scrolling far | No visual, a placeholder, or decoration that proves nothing |
| 1.4 | Header block | 5 | Language switch, name, one-line promise, useful badges that render, working nav links | Badge soup, broken badges, no switch, vague title |

### 2. Getting started (20)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 2.1 | Path to first result | 5 | Shortest verified path (store link, install command, `run` command) from zero to the first result | No quick start, or it needs heavy setup first |
| 2.2 | Complete install | 5 | Every step present, per platform where it differs, alternatives folded in `<details>` | Implicit steps, one bare command, "see docs" |
| 2.3 | Prerequisites | 5 | Runtime, toolchain and services listed before the steps | Discovered only when a command fails |
| 2.4 | Versions and platforms, truthfully | 5 | Minimum OS / runtime versions stated; what is available where (store, registry, from source) is explicit | A platform badge that suggests more than what exists, or no version information |

### 3. Show, don't tell (15)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 3.1 | Visuals | 5 | Real, current, sharp, consistent set with meaningful alt text, each showing something different | Stale, blurry, redundant, or missing alt text |
| 3.2 | Usage shown | 5 | A real example (command and output, transcript, GIF of the key flow) | Only prose, or pseudocode |
| 3.3 | Features as benefits | 5 | Concrete user outcomes, grouped or ordered by importance | Internal implementation details, or a vague list of adjectives |

### 4. Structure and length (15)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 4.1 | Order and headings | 4 | Value, proof, use, details; predictable section names in sentence case | Contributing before install, vague headings |
| 4.2 | Findable | 4 | Install command, main usage and license found in seconds | Key facts buried in paragraphs |
| 4.3 | Length | 4 | 100 to 200 lines, long material in `<details>` or docs/ | Wall of text, or too thin for the project |
| 4.4 | Formatting | 3 | Fenced code with languages, tables for comparisons, short paragraphs | Unformatted code, long dense paragraphs |

### 5. Accuracy (15)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 5.1 | Claims match the code | 5 | Every command, flag, path, setting and feature checked in section 4 | Any claim that the code contradicts (one wrong command is 2 points at most) |
| 5.2 | Versions and badges current | 4 | Version matches the manifest, tag or store; dynamic badges render | Old version numbers, badges showing errors |
| 5.3 | Links and anchors | 3 | Lint reports no broken file, image or anchor; external links point to stable pages | Broken links or anchors |
| 5.4 | Consistent with other files | 3 | Same commands and requirements as CONTRIBUTING.md, SECURITY.md, CI and manifests | Contradictions between files |

### 6. Honesty and completeness (10)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 6.1 | Limits and status | 4 | Says what it does not do, known limits, maturity when it matters (prototype, school project, maintained) | Reads as if it does everything |
| 6.2 | Help and contact | 2 | Where to report a bug or ask (issues on a public repo, email on a private one) | Nowhere |
| 6.3 | License and credits | 2 | License stated and matches LICENSE; third-party assets and team members credited | Missing or contradictory |
| 6.4 | Contribution pointer | 2 | Public repo: Contributing section linking CONTRIBUTING.md. Private repo: one footer line is enough | Public repo with no guidance |

### 7. House rules (5)

| # | Criterion | Max | Good | Bad |
|---|---|---|---|---|
| 7.1 | Owner's style rules | 3 | Lint clean: no emoji, no long dash or hyphen used as one, no AI mention, no hype words | Any lint error is 0 |
| 7.2 | Bilingual twin | 2 | README.fr.md exists, links back, same sections, visuals and facts, natural French | Missing, partial, or a literal translation |

### Rating

| Score | Rating |
|---|---|
| 90 to 100 | Exemplary |
| 75 to 89 | Strong |
| 60 to 74 | Adequate |
| 40 to 59 | Weak |
| 0 to 39 | Poor |

A README with lint errors cannot be rated above Adequate, whatever its total.

## 4. Source check (claims against code)

The most damaging README fault is a confident claim that is no longer true. For criteria 2.x, 5.1 and 5.4:

1. **Extract every checkable claim**: commands, flags, file paths, settings and environment variable names, versions, platform support, feature names, numbers ("80+ templates", "14-day planner").
2. **Find the authority** for each: manifest (`scripts`, `bin`, entry points, version), CLI parser, config schema, source files, CI workflow, store or registry listing.
3. **Classify**: confirmed, outdated (renamed, removed, changed), unverifiable.
4. **Correct from the source, never from memory.** If the source gives no answer, say so instead of guessing.

Report the non-confirmed claims in a short table: claim, status, evidence (file and line, or command output), correction.

## 5. Report format

Write the report to the user in French:

```markdown
## Audit du README : <projet>

**Note : 82 / 100 (Strong)** · lint : 0 erreur, 2 avertissements

| Catégorie | Note | Max |
|---|---|---|
| Premier écran | 18 | 20 |
| Démarrage | 14 | 20 |
| Montrer plutôt que dire | 13 | 15 |
| Structure et longueur | 14 | 15 |
| Exactitude | 12 | 15 |
| Honnêteté et complétude | 6 | 10 |
| Règles maison | 5 | 5 |

**Points forts** : the 3 best criteria, one line each.

**À corriger en priorité** (by impact): criterion, what is wrong, the exact fix.

**Vérification dans le code**: table of claims that are outdated or unverifiable.
```

Keep the detailed per-criterion scores available (a collapsed list) but lead with the summary. When this report precedes an improvement, end with the planned changes; when it follows one, show the score before and after.

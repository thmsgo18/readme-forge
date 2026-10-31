# Community files: LICENSE, CONTRIBUTING.md, SECURITY.md

All three in English. Same writing rules as the READMEs: no emoji, no long dash or hyphen used as one, nothing invented. When a file already exists, keep its accurate project-specific content (rules, commands, scope notes) and bring the rest up to these templates.

## LICENSE

Copy `assets/LICENSE-MIT.txt`, replace `{{YEAR}}` and `{{AUTHOR}}`:

- `{{AUTHOR}}`: the owner's name (SKILL.md, « Owner »). For a team project, ask whether to list all members or keep the owner only.
- `{{YEAR}}`: year of the first commit (`first_commit_year` from `detect_project.py`), or the current year if there is no history. Leave an existing correct year alone.

Cases to handle, not to steamroll:
- **Existing non-MIT license** (Apache, GPL, proprietary): ask before replacing. MIT is the default, but a license change on published code is the owner's call.
- **Third-party content** (vendored code, fonts, templates, datasets with their own license): MIT covers the owner's work only. Keep their license files, and add one line to the README License section: "Third-party templates keep their own licenses, see `templates/*/LICENSE`."
- **Manifest license field**: if `package.json`, `pyproject.toml`, `Cargo.toml` or similar has a license field that is missing or different, set it to `MIT` and mention it in the summary. A pubspec has no license field; leave it.
- File name exactly `LICENSE` (no extension), so GitHub detects it and shows "MIT license" in the sidebar.

## CONTRIBUTING.md

Target 40 to 90 lines. Tailored to the project: every command must exist and work. Skeleton:

```markdown
# Contributing to <Project>

Thanks for taking the time to contribute. Bug reports, fixes and new ideas are all welcome.

## Reporting a bug

Open an [issue](https://github.com/OWNER/REPO/issues) with:

- what you did (the exact command or steps),
- what you expected and what happened instead (full error message),
- your environment: OS, <runtime> version, <project> version.

For a security issue, do not open a public issue: see [SECURITY.md](SECURITY.md).

## Suggesting a feature

Open an issue describing the problem it solves before writing code, so we can agree on the approach.

## Development setup

```bash
git clone https://github.com/OWNER/REPO.git
cd REPO
<install dependencies>
<run the project locally>
```

## Running the tests

```bash
<test command>
<lint / type-check command, if any>
```

<One sentence on what CI runs, if CI exists.>

## Project conventions

<Only the rules that are real in this repo: from CLAUDE.md, AGENTS.md, linters, CI. Examples: supported versions, no raw SQL, both languages updated, migrations with a test. Skip this section if there are none.>

## Submitting a pull request

1. Fork the repository and create a branch from `main`.
2. Make your change, with tests when it changes behavior.
3. Run the tests and the linters.
4. Open a pull request that explains what changed and why.
```

Private repository: the issue tracker is invisible to anyone else, so replace the issue links with the contact email the user gave, if any and present the file as development notes for collaborators.

Adapt freely: drop "Running the tests" if there are none (and do not pretend there are), add "Adding a template" or "Adding a translation" when the project has that kind of extension point. Commit message conventions only if the repo visibly follows one.

## SECURITY.md

Target 20 to 50 lines.

```markdown
# Security Policy

## Supported versions

<Pick the true statement:>
Only the latest release is supported with security fixes. Please upgrade before reporting an issue.
<or> This project has a single rolling version on the `main` branch. Only the latest commit is supported.

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report it privately through [GitHub's private vulnerability reporting](https://github.com/OWNER/REPO/security/advisories/new).
<Only if the user gave a security email:> You can also write to <email>.

Include the affected version or commit, the steps to reproduce, and the impact you see. You can expect a first answer within a few days. Confirmed issues are fixed as fast as possible and credited in the release notes, unless you prefer to stay anonymous.

## Scope

<Two to five bullets that are specific to this project: what data it stores and where, which network calls it makes, which secrets it handles and how, what is out of scope by design. Skip the section rather than write generic filler.>
```

- **Private repository**: private vulnerability reporting does not exist there. Keep the email only and drop the advisory link.
- **Public repository**: the advisory link only works once private vulnerability reporting is enabled. Offer to enable it in the final step (see `github-metadata.md`).
- It is a solo, part-time project: promise "a few days", never a hard SLA.

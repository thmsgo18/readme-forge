# Update mode

Bring a README that is already in readme-forge format (README.md with a language switch, README.fr.md, community files) back in line with the project, without rewriting it. Idea taken from the `update-readme` skill of [gupsammy/Claudest](https://github.com/gupsammy/Claudest).

Use it when the user says the README is outdated, asks to refresh or sync it, or after a release. If the README is not in readme-forge format, or more than about half of it would change, use the improve workflow instead and say why.

## 1. Find what changed

```bash
python3 ~/.claude/skills/readme-forge/scripts/changes_since_readme.py .
```

It reports the last commit that touched the READMEs, every commit since, changed files grouped by kind, version changes in manifests and tags, README images that predate later UI changes, and the capture scripts kept in `docs/demo/`. Use `--since <tag or commit>` to compare with a release instead.

If `readme_uncommitted_changes` is true, the working copy of the README is newer than its last commit: read it as it is now, and mention it.

Read the commit subjects, then the diffs that matter (`git show <hash> --stat`, then the files themselves). Commit subjects are hints, not facts: confirm each change in the code before writing about it.

## 2. Classify

| Kind | Examples | README impact |
|---|---|---|
| New user-facing feature | new screen, command, flag, setting | add to Features or Usage if it matters to a user; skip small internals |
| Changed behavior | renamed command, new default, moved setting | correct every mention, in both languages |
| Removed | dropped command, platform, option | delete the mention |
| Requirements | new minimum version, new dependency to install | update prerequisites and install steps |
| Release | version bump, new tag, store release | badges, version mentions |
| UI change | screens redesigned | recapture the affected visuals |
| Internal | refactor, tests, CI, typo | nothing |

Then run the source check from `references/audit-rubric.md` (section 4) on the whole README: drift also happens without a commit that says so.

## 3. Plan, then confirm

Show the user, in French, a short list: each planned edit with the commit or file that justifies it, and the visuals to recapture. Recaptures are the slow part: list them separately so the user can skip them.

## 4. Edit minimally

- Use Edit, not Write: keep the existing structure, wording, order and badges. Change only what is wrong or missing.
- Apply every change to README.md and README.fr.md in the same pass, so the twins never diverge.
- New features join the existing list in the existing style; do not reorganize the section to fit one addition.
- Keep the 100 to 200 line target: if an addition pushes past it, fold something into `<details>`.
- Update CONTRIBUTING.md and SECURITY.md when commands, requirements or the data handled changed.

## 5. Refresh visuals

For each image flagged as possibly stale, look at the current app before deciding: a backend-only change does not need a new screenshot. Regenerate with the scripts in `docs/demo/` (vhs tapes, scenario JSON, seed scripts) so the new captures match the old ones in size, data and framing. Keep file names unchanged so the README needs no edit.

## 6. Verify and report

Run the lint and the audit (score after, target 85 or more). Report: the commits covered, each edit and its reason, visuals recaptured, line counts before and after, the score. Then ask before commit and push, as in the main workflow.

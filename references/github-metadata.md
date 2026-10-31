# GitHub metadata: description, topics, homepage

These show in the repo sidebar, in search results and on the owner's profile. They are often the first thing a visitor reads, before the README.

## Description

- English, one sentence, 80 to 200 characters (GitHub's hard limit is 350).
- Starts with what the project is or does, with the most searchable words early: "Flutter app to ...", "CLI to ...", "Claude skill that ...", "Full-stack event platform for ...".
- States the key differentiator when there is room: "fully offline", "single HTML file", "no server".
- Same rules as the READMEs: no emoji, no long dash, no hyphen used as a dash, no hype words.
- No trailing period for a single clause; a period is fine for a full sentence. Look at the owner's other repos and stay consistent.

Examples from the owner's repos:
- `CLI to create standalone LaTeX projects from templates`
- `Track your internship search (applications, companies, cover letters, interview prep, notes, CVs) in a local SQLite database behind a native desktop app for macOS, Windows, and Linux.`

## Topics

- 6 to 12 topics (GitHub allows 20). Lowercase, digits and hyphens only, 50 characters max each.
- Cover these angles, in this order of importance:
  1. what it is: `cli`, `desktop-app`, `flutter-app`, `vscode-extension`, `claude-skill`, `github-action`, `rest-api`;
  2. the domain and the problem, in the words people search: `job-search`, `latex-templates`, `music-recognition`, `dependency-management`;
  3. main language and frameworks: `python`, `typescript`, `flutter`, `react`, `django`;
  4. notable techniques or platforms: `sqlite`, `rag`, `faiss`, `github-actions`, `offline-first`, `cross-platform`.
- Prefer GitHub's established topics (the ones with a page at github.com/topics/NAME) over invented compounds.
- No vanity or noise: `awesome`, `best`, `cool`, `project`, `code`, the repo's own name unless it is a known brand, near-duplicates (`template` and `templates`).
- Keep existing topics that are still accurate; propose removing the ones that are wrong.

## Homepage

Set it when there is a real destination: a live demo, GitHub Pages site, store page, PyPI/npm/marketplace page. Leave it empty otherwise.

## Applying (only after the user agrees)

```bash
gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl,visibility
gh repo edit OWNER/REPO --description "..."
gh repo edit OWNER/REPO --add-topic cli,python,latex --remove-topic old-topic
gh repo edit OWNER/REPO --homepage "https://..."
```

Private vulnerability reporting (public repos only, so the SECURITY.md link works):

```bash
gh api repos/OWNER/REPO/private-vulnerability-reporting            # {"enabled": false}
gh api -X PUT repos/OWNER/REPO/private-vulnerability-reporting      # enable
```

Read the values back after applying and report them.

## Manual step to mention

GitHub's social preview image (the card shown when the repo link is shared) cannot be set through the API. If the project has a strong hero image or logo, suggest the owner upload a 1280x640 version in Settings, General, Social preview. Offer to produce that image from the hero screenshot (`sips` or ffmpeg crop and pad) and save it as `docs/assets/social-preview.png`.

## No GitHub repo yet

If the folder has no GitHub remote, still write the description and topics in the summary. Offer `gh repo create` only if the user asks; creating a repo and choosing its visibility is their decision.

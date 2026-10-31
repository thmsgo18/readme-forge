# Security Policy

## Supported versions

Only the latest release is supported with security fixes. Please upgrade before reporting an issue.

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report it privately through [GitHub's private vulnerability reporting](https://github.com/thmsgo18/readme-forge/security/advisories/new).

Include the affected version or commit, the steps to reproduce, and the impact you see. You can expect a first answer within a few days. Confirmed issues are fixed as fast as possible and credited in the release notes, unless you prefer to stay anonymous.

## Scope

- The skill reads the project it documents and writes README, community files and images inside it. It asks before committing, pushing or changing anything on GitHub.
- Screenshots and videos are taken with demo data. The skill must never capture real credentials or personal data; report any case where it does.
- `preview_readme.py` sends the README text to GitHub's Markdown API through your own `gh` login. `lint_readme.py --online` fetches badge URLs. Nothing else leaves your machine.
- `setup_capture.sh` installs `playwright-core` from npm into `~/.cache/readme-forge` and drives the Google Chrome already installed.

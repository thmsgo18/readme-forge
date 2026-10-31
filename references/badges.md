# Badges

## Layout

All badges use `style=for-the-badge`, the house style of this skill. Two rows inside one centered `<p>`, separated by `<br>`:

1. **Project row**: version, license, CI (only if a workflow exists), registry or store (only if published), platform (for apps).
2. **Stack row**: the 3 to 6 technologies a visitor would recognize and care about. The main language and the main framework first. Skip build tooling and minor libraries.

Eight badges in total is plenty. Every badge must say something true and useful; a "made with love" badge says nothing.

Wrap a badge in a link when there is an obvious target: license to `LICENSE`, version to the releases page or registry, CI to the workflow page. Stack badges need no link.

## Public vs private repository

shields.io reads GitHub anonymously, so dynamic badges (`github/v/release`, `github/actions/workflow/status`, `github/v/tag`) only work on **public** repos. On a private repo, or a repo with no remote yet, use static badges and take the version from the manifest:

```
https://img.shields.io/badge/version-1.2.0-blue?style=for-the-badge
```

A static version badge must be updated at each release; say so in the final summary.

## Version source, in order of preference

1. Published package: PyPI `https://img.shields.io/pypi/v/NAME?style=for-the-badge&color=blue`, npm `https://img.shields.io/npm/v/NAME?style=for-the-badge&color=blue`, pub.dev `https://img.shields.io/pub/v/NAME?style=for-the-badge&color=blue`, crates.io `https://img.shields.io/crates/v/NAME?style=for-the-badge&color=blue`, VS Marketplace `https://vsmarketplacebadges.dev/version/PUBLISHER.EXTENSION.svg?style=for-the-badge&label=marketplace&color=blue`. Check the package is really published under that name before using it.
2. GitHub release (public repo): `https://img.shields.io/github/v/release/OWNER/REPO?style=for-the-badge&color=blue`.
3. Git tag without release (public repo): `https://img.shields.io/github/v/tag/OWNER/REPO?sort=semver&style=for-the-badge&color=blue&label=version`.
4. Manifest version (any repo): static badge as above.

For a **mobile app on a store**, the store version is the one users see, and it works even when the repo is private:
- App Store: `https://img.shields.io/itunes/v/APP_ID?style=for-the-badge&label=App%20Store&color=0D96F6`. The numeric id comes from `curl -s "https://itunes.apple.com/lookup?bundleId=BUNDLE_ID"` (`trackId`, and `trackViewUrl` for the link). Look it up yourself before asking the user.
- Google Play: `https://img.shields.io/badge/Google_Play-PACKAGE_VERSION-414141?style=for-the-badge&logo=googleplay&logoColor=white` (no reliable dynamic badge; static, from the manifest).

Store buttons, linked to the store page, go in the project row or right under the hero:
- House style: `https://img.shields.io/badge/App_Store-Download-0D96F6?style=for-the-badge&logo=appstore&logoColor=white` (FR: `App_Store-T%C3%A9l%C3%A9charger-0D96F6`), and `https://img.shields.io/badge/Google_Play-Get_it-414141?style=for-the-badge&logo=googleplay&logoColor=white` (FR: `Google_Play-Disponible-414141`).
- Official Apple artwork, English only: `https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg` at `height="48"`.
- Use a neutral store link without the country and tracking parameters: `https://apps.apple.com/app/APP-SLUG/idAPP_ID`.

No version anywhere (no tag, no manifest version)? Ask the user whether to start at `0.1.0` or `1.0.0`; do not invent one silently.

## Other project-row badges

```
License   https://img.shields.io/badge/license-MIT-green?style=for-the-badge          (FR label: licence-MIT)
CI        https://img.shields.io/github/actions/workflow/status/OWNER/REPO/WORKFLOW.yml?branch=main&style=for-the-badge&label=CI
Python    https://img.shields.io/pypi/pyversions/NAME?style=for-the-badge             (published Python packages)
Platform  https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-3d8ff0?style=for-the-badge
Claude    https://img.shields.io/badge/claude-skill-d97757?style=for-the-badge        (Claude skills, the owner's existing style)
YouTube   https://img.shields.io/badge/YouTube-Watch_the_video-FF0000?style=for-the-badge&logo=youtube&logoColor=white
```

In static badge paths: a space is `%20` or `_`, a literal `-` is `--`, a literal `_` is `__`, `|` is `%7C`.

## Stack badges

Pattern: `https://img.shields.io/badge/LABEL-COLOR?style=for-the-badge&logo=SLUG&logoColor=white`

Verified slugs (October 2026):

| Technology | Color | Logo slug | Note |
|---|---|---|---|
| Python | 3776AB | python | |
| TypeScript | 3178C6 | typescript | |
| JavaScript | F7DF1E | javascript | `logoColor=black` |
| Node.js | 339933 | nodedotjs | label `Node.js` |
| React | 20232A | react | `logoColor=61DAFB` |
| Next.js | 000000 | nextdotjs | |
| Vue.js | 4FC08D | vuedotjs | |
| Svelte | FF3E00 | svelte | |
| Angular | 0F0F11 | angular | |
| Vite | 646CFF | vite | |
| Tailwind CSS | 06B6D4 | tailwindcss | |
| HTML5 | E34F26 | html5 | |
| CSS | 663399 | css | `css3` no longer exists |
| Express | 000000 | express | |
| NestJS | E0234E | nestjs | |
| Electron | 47848F | electron | |
| Tauri | 24C8D8 | tauri | |
| Django | 092E20 | django | |
| FastAPI | 009688 | fastapi | |
| Flask | 000000 | flask | |
| Streamlit | FF4B4B | streamlit | |
| PyTorch | EE4C2C | pytorch | |
| TensorFlow | FF6F00 | tensorflow | |
| scikit-learn | F7931E | scikitlearn | |
| pandas | 150458 | pandas | |
| NumPy | 013243 | numpy | |
| Jupyter | F37626 | jupyter | |
| Hugging Face | FFD21E | huggingface | `logoColor=black` |
| LangChain | 1C3C3C | langchain | |
| Anthropic | 191919 | anthropic | |
| Claude | D97757 | claude | |
| OpenAI | 412991 | (none) | no logo available, plain badge |
| Flutter | 02569B | flutter | |
| Dart | 0175C2 | dart | |
| Swift | F05138 | swift | |
| Kotlin | 7F52FF | kotlin | |
| Android | 3DDC84 | android | |
| iOS / macOS | 000000 | apple | |
| Windows | 0078D4 | (none) | no logo available |
| Linux | FCC624 | linux | `logoColor=black` |
| Java | ED8B00 | openjdk | |
| PHP | 777BB4 | php | |
| Go | 00ADD8 | go | |
| Rust | 000000 | rust | |
| C | A8B9CC | c | |
| C++ | 00599C | cplusplus | label `C%2B%2B` |
| C# / .NET | 512BD4 | dotnet | label `C%23` |
| R | 276DC3 | r | |
| LaTeX | 008080 | latex | |
| SQLite | 003B57 | sqlite | |
| PostgreSQL | 4169E1 | postgresql | |
| MySQL | 4479A1 | mysql | |
| MongoDB | 47A248 | mongodb | |
| Redis | FF4438 | redis | |
| Firebase | DD2C00 | firebase | |
| Supabase | 3FCF8E | supabase | |
| Prisma | 2D3748 | prisma | |
| Docker | 2496ED | docker | |
| GitHub Actions | 2088FF | githubactions | |
| Vitest | 6E9F18 | vitest | |
| Jest | C21325 | jest | |
| pytest | 0A9EDC | pytest | |
| Vercel | 000000 | vercel | |
| Render | 000000 | render | |
| VS Code | 007ACC | (none) | no logo available, `vscodium` exists but is another product |
| Bash / Shell | 4EAA25 | gnubash | |
| Three.js | 000000 | threedotjs | |
| D3.js | F9A03C | d3 | |
| Socket.IO | 010101 | socketdotio | |
| Zod | 3E67B1 | zod | |
| Godot | 478CBF | godotengine | |
| Unity | 000000 | unity | |
| Figma | F24E1E | figma | |

For anything not listed, look up the slug on simple-icons.org and confirm with `lint_readme.py --online`, which warns when a logo does not resolve.

## French README

Same badges, same order. Translate only word labels: `license` becomes `licence`, `platform` becomes `plateforme`, `Watch the video` becomes `Voir la vidéo` (`Voir_la_vid%C3%A9o`). Translate `alt` texts. Technology names never change.

<p align="right"><a href="./README.md">English</a> | <b>Français</b></p>

<h1 align="center">readme-forge</h1>

<p align="center">
  <b>Demandez un README. Recevez-le en deux langues, avec de vraies captures, des badges et les fichiers de la communauté, vérifié avec le rendu de GitHub lui-même.</b>
</p>

<p align="center">
  <a href="https://github.com/thmsgo18/readme-forge/releases"><img src="https://img.shields.io/github/v/release/thmsgo18/readme-forge?style=for-the-badge&color=blue&label=version" alt="Dernière version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-green?style=for-the-badge" alt="Licence MIT"></a>
  <a href="https://github.com/thmsgo18/readme-forge/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/thmsgo18/readme-forge/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI"></a>
  <br>
  <img src="https://img.shields.io/badge/claude-skill-d97757?style=for-the-badge" alt="Skill Claude">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown">
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#ce-que-vous-obtenez">Ce que vous obtenez</a> •
  <a href="#exemple">Exemple</a> •
  <a href="#fonctionnement">Fonctionnement</a> •
  <a href="#contribuer">Contribuer</a>
</p>

---

<p align="center">
  <img src="docs/assets/hero-github-forge.png" alt="Le README de github-forge écrit avec readme-forge, rendu par GitHub en thème clair et sombre" width="900">
</p>
<p align="center"><sub>Le README de <a href="https://github.com/thmsgo18/github-forge">github-forge</a>, écrit avec ce skill, tel que GitHub l'affiche en clair et en sombre.</sub></p>

Un README décide en dix secondes si quelqu'un essaie votre projet. La plupart tiennent en une ligne ou forment un mur de texte, avec une capture vieille de trois versions. readme-forge est un skill Claude Code qui lit votre projet, le lance, le capture avec des données de démonstration, et écrit le README qu'un visiteur lit vraiment : une promesse en une ligne, des badges, un visuel tout de suite, puis des sections courtes qui le mettent en route.

Il n'écrit rien qu'il ne puisse vérifier. Chaque commande, chiffre et fonctionnalité vient du code ou du projet lancé, et chaque image est contrôlée avant d'entrer dans le README.

## Installation

En skill personnel, disponible dans tous vos projets :

```bash
git clone https://github.com/thmsgo18/readme-forge.git ~/.claude/skills/readme-forge
```

Ou pour un seul dépôt :

```bash
git clone https://github.com/thmsgo18/readme-forge.git .claude/skills/readme-forge
```

Puis demandez à Claude Code, en français ou en anglais : « fais le README », « write the README », « audite mon README », « mets à jour le README ».

<details>
<summary>Prérequis</summary>

- `python3` pour les scripts (bibliothèque standard uniquement) et `git`.
- La [GitHub CLI](https://cli.github.com/), connectée, pour l'aperçu GitHub et les métadonnées du dépôt.
- Pour les captures et les vidéos : Node.js et Google Chrome. `scripts/setup_capture.sh` installe une fois le pilote Playwright, sans télécharger de navigateur.
- En option : [vhs](https://github.com/charmbracelet/vhs) pour les GIF de terminal, `ffmpeg` pour les enregistrements d'écran, Xcode ou le SDK Android pour les applications mobiles.

</details>

## Ce que vous obtenez

| Fichier | Contenu |
|---|---|
| `README.md` | En anglais, de 100 à 200 lignes : en-tête, badges, visuel principal, démarrage rapide, fonctionnalités, fonctionnement |
| `README.fr.md` | Son jumeau français, réécrit en français naturel plutôt que traduit, avec ses propres ancres |
| `docs/assets/` | Captures, GIF ou schémas tirés du projet en marche, avec des données de démonstration |
| `docs/demo/` | Les scripts qui les ont produits, pour pouvoir les refaire |
| `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` | Licence MIT et fichiers de la communauté adaptés au projet |
| Métadonnées GitHub | Une description et des topics, appliqués seulement avec votre accord |

Le skill s'adapte au type de projet : un GIF de terminal pour une CLI, une rangée de captures de téléphone pour une application mobile, la fenêtre principale pour une application de bureau, un schéma du pipeline et un tableau de résultats pour un projet de recherche.

## Exemple

Avant d'écrire, le skill audite l'existant. Le même linter vérifie son propre travail à la fin. Le voici, mot pour mot, sur un README de cinq lignes :

```text
$ python3 scripts/lint_readme.py .
ERROR   README.md:1: emoji 🚀: replace with words (Yes/No in tables)
ERROR   README.md:3: long dash (— or –): rewrite with a comma, colon, parentheses or two sentences; for ranges write 'to' ('20 to 30 min')
ERROR   README.md:5: missing local file: docs/guide.md
ERROR   README.md:1: no language switch to README.fr.md in the first lines
ERROR   README.md:1: fewer than 2 badges at the top
ERROR   README.fr.md:0: file is missing
ERROR   LICENSE:0: file is missing
warning README.md:3: AI-sounding wording: 'seamless'
warning README.md:3: AI-sounding wording: 'blazing fast'
warning README.md:5: 5 lines, target is 100 to 200
warning README.md:1: no version badge
warning README.md:1: no image at all: add a screenshot, GIF or diagram
README.md: 5 lines

7 error(s), 5 warning(s)
```

Demandez seulement un audit et vous obtenez une note sur 100, sur une grille de 30 critères, avec ce qu'il faut corriger en premier, sans que rien ne soit modifié.

## Fonctionnement

1. **Comprendre** : `detect_project.py` lit les manifestes, les langages, l'historique Git, la CI et l'état sur GitHub. Claude lit le code et lance le projet.
2. **Planifier** : vous validez la promesse, les sections, les visuels, les badges et les topics avant toute étape longue.
3. **Capturer** : de vraies captures et vidéos avec des données de démonstration, par Chrome, vhs, le simulateur iOS ou l'émulateur Android.
4. **Écrire** : les deux README et les fichiers de la communauté, avec un guide de style qui proscrit les emojis, les tirets longs et les tournures typiques des textes générés.
5. **Vérifier** : `lint_readme.py` contrôle chaque règle, lien, ancre et badge ; `preview_readme.py` affiche les deux fichiers avec l'API Markdown de GitHub, en clair et en sombre.
6. **Demander** : le commit, le push et la description GitHub n'ont lieu qu'avec votre accord.

| Script | Rôle |
|---|---|
| `detect_project.py` | Les faits sur le projet, en JSON |
| `lint_readme.py` | Chaque règle, les liens, les ancres, les badges, la parité entre l'anglais et le français |
| `preview_readme.py` | Le rendu exact de GitHub, en clair et en sombre, en HTML et en PNG |
| `capture_web.cjs` | Captures web et vidéos de démonstration scénarisées, avec un curseur visible |
| `make_gif.sh` | D'un enregistrement d'écran à un GIF optimisé |
| `changes_since_readme.py` | Ce qui a changé depuis la dernière mise à jour du README, et les images peut-être périmées |

## Projets liés

- [github-forge](https://github.com/thmsgo18/github-forge) : le skill qui installe et fait vivre les dépôts où vivent ces README.

## Contribuer

Les signalements de bugs et les pull requests sont bienvenus, voir [CONTRIBUTING.md](CONTRIBUTING.md). Problèmes de sécurité : voir [SECURITY.md](SECURITY.md).

## Licence

[MIT](LICENSE) © Thomas Gourmelen

## Auteur

Réalisé par [thmsgo18](https://github.com/thmsgo18)

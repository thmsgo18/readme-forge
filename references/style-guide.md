# Style guide

## Contents
1. Voice
2. The tagline
3. Words and constructions to avoid
4. Rewriting dashes
5. Formatting
6. French adaptation (README.fr.md)

## 1. Voice

Write like a developer who is proud of the tool and respects the reader's time.

- Second person, active voice, present tense: "Save the file and the PDF rebuilds."
- Lead with what the reader gets, then how it works.
- Concrete beats abstract: numbers, real commands, real names. "80+ templates", "1 to 3 minutes on first launch", "one `index.html` that opens offline" all do more than "powerful" or "flexible".
- Short sentences. One idea per sentence. One idea per bullet.
- Say what is true and stop. If a feature has a limit, a short honest note builds more trust than silence ("Editing works in Chromium browsers only.").
- Aim for this register, taken from READMEs written with this skill:
  - "Write your document. Save. Your PDF appears. That's it."
  - "No account, no cloud, no subscription. Everything lives in one file on your machine."
  - "You lose nothing PowerPoint gives a presenter, and you gain portability, longevity and a file you actually own."

## 2. The tagline

One sentence, ideally under 18 words, in bold under the logo. It states the outcome for the user, not the technology. Good shapes:

- Imperative sequence: "Write your document. Save. Your PDF appears."
- Outcome plus mechanism: "Describe your talk to Claude. It writes the slides and bundles them into one portable `index.html`."
- Contrast without a dash: "Track your internship search in a real local database, not another spreadsheet."

Avoid taglines that only name the category ("A modern CLI tool for LaTeX").

## 3. Words and constructions to avoid

They are the fingerprints of generated text. The linter warns on most of them; rewrite rather than swap for a synonym.

English words: seamless, leverage, robust, cutting-edge, game-changer, unlock, unleash, empower, elevate, delve, dive into, harness the power, streamline, effortless, next-level, revolutionize, supercharge, blazing fast, state-of-the-art, world-class, boasts, a breeze, journey, embark, comprehensive solution, all-in-one solution, tailored to your needs.

Constructions:
- "Whether you're a beginner or an expert, ..."
- "It's not just X, it's Y." / "More than just a ..."
- Three stacked adjectives: "fast, simple and powerful".
- Rhetorical openers: "Ever wondered how...?", "Tired of...?"
- Closing cheers: "Happy coding!", "Enjoy!".
- Every bullet starting with the same verb form, or every sentence the same length.
- Bold scattered through paragraphs. Bold the lead of a bullet or a key term, nothing else.
- Announcing instead of saying: "This section explains how to install..." Just give the steps.

Also avoid: marketing superlatives without proof, "simply" and "just" before a step that is not simple, exclamation marks, and headings phrased as questions unless it is the single "What is X?" opener.

## 4. Rewriting dashes

The hard rule bans em dashes, en dashes and " - " used as a dash. Pick the rewrite that matches what the dash was doing:

| Dash was doing | Rewrite with | Example |
|---|---|---|
| Adding an explanation | colon | "One file: engine, theme and fonts inlined." |
| Inserting an aside | parentheses or commas | "The light install (about 500 MB) needs no admin rights." |
| Contrasting | comma, or two sentences | "A real database, not another spreadsheet." |
| Listing a range | "to" | "Python 3.10 to 3.14", "20 to 30 min" |
| Separating label and text in a list | colon | "**Install**: one click runs the installer." |

French: same idea. "Une vraie base de données, pas un tableur de plus." / "de 1 à 3 minutes".

## 5. Formatting

- Headings in sentence case: "Quick start", not "Quick Start". Short, no final punctuation, no emoji.
- Code blocks always carry a language: `bash`, `powershell`, `python`, `json`, `text` for transcripts.
- Tables for comparisons, commands, options, statuses. Keep cells short.
- `<details>` with a `<summary>` for anything long that only some readers need (other OS, troubleshooting, full reference).
- GitHub alerts (`> [!TIP]`, `> [!NOTE]`, `> [!WARNING]`) at most twice per README.
- `<kbd>` for keys: <kbd>Cmd</kbd> + <kbd>K</kbd>.
- Arrows for UI paths are fine: "Settings → Features → Skills".
- Digits for numbers, a non-breaking unit style: "500 MB", "3 OS".

## 6. French adaptation (README.fr.md)

Rewrite, do not translate. Read each English paragraph, then write what a French developer would naturally say.

- Use "vous", unless the existing French files of the project use "tu".
- Keep the English terms French developers actually use: template, build, commit, pull request, issue, CLI, workflow, framework, release, open source. Do not force "gabarit" or "demande de tirage".
- Avoid calques: "supporter" (use "prendre en charge"), "délivrer" (use "fournir"), "adresser un problème" (use "traiter"), "être en charge de" (use "s'occuper de"), "basé sur" is fine.
- French typography as in the owner's files: a space before `:` `;` `?` `!`, guillemets « » for quotations in prose (code and UI labels keep their own quotes), decimal comma in prose numbers ("2,5 Go"), units in French (Mo, Go).
- Section names: Démarrage rapide, Installation, Fonctionnalités, Captures d'écran, Utilisation, Exemple, Fonctionnement, Prérequis, Contribuer, Sécurité, Licence, Auteur, Projets liés.
- Translate image `alt` texts, `<summary>` texts, captions and the word labels inside badges (license becomes licence, "single file" becomes "fichier unique"). Technology names stay as they are.
- Recompute anchors from the French headings, accents included: `#démarrage-rapide`, `#fonctionnalités`.
- French AI fingerprints to avoid: révolutionnaire, sans effort, en toute simplicité, n'attendez plus, plongez dans, boostez, de pointe, incontournable, un jeu d'enfant, que vous soyez X ou Y, libérez, sublimez, à portée de main, véritable allié, en un clin d'œil, fluide et intuitif, propulsé par.
- Same visuals as the English README. If the app has a French interface and switching language is cheap, French screenshots for the French README are a nice touch, with the same file names suffixed `.fr` (`home.fr.png`).

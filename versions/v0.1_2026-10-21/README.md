# v0.1, 21 Oct. 2026: first draft of the note

| File | Content | Built from |
|---|---|---|
| `Vote_Condorcet_SOTA_note_v0.1.pdf` | The note (36 pages) | `cd journals/working-paper && latexmk main.tex` |
| `Vote_Condorcet_executive-summary_en_v0.1.pdf` | Executive summary, English (2 pages) | `cd summaries/en/executive && latexmk main.tex` |
| `Vote_Condorcet_synthese_fr_v0.1.pdf` | Synthèse, French (2 pages) | `cd summaries/fr/executive && latexmk main.tex` |

Each PDF was built from the commit that added it to this folder. The drafting markers are on
(`\FinalVersion` is not defined). The summaries quote the note's numbers through macros
(`simulations/python/key_numbers.py`), so all three files agree.

This version is frozen. Later changes go to `manuscript/` and `summaries/`, and new PDFs of record go to
new folders under `versions/`. What changed in the results since this version: `manuscript/changes.md`.

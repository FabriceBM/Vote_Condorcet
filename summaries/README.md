# Summaries

This folder holds short documents derived from the note, for readers who will not read the note itself.
The note stays in `../manuscript/` and remains the single source: a summary adds no result of its own.

## Hierarchy: language, then kind of document

```
summaries/
├── README.md                 this file
├── shared/
│   └── layout.tex            layout common to every language and every kind: page, fonts, colours,
│                             boxes, title block
├── en/                       everything in English
│   └── executive/            executive summary, 2 pages
│       ├── executive-summary_en.tex   the source
│       ├── executive-summary_en.pdf   the current PDF
│       └── latexmkrc
└── fr/                       tout en français
    └── executive/            synthèse, 2 pages
        ├── synthese_fr.tex            la source
        ├── synthese_fr.pdf            le PDF à jour
        └── latexmkrc
```

Why this order:
- **Language first.** The project may have several documents in each language (executive summary,
  FAQ, a note for a committee). Talks are kept apart, by date, in `../presentations/`. A reader, or a translator, finds everything in their language
  under one folder, and each language can grow at its own pace.
- **The same kinds under each language.** `en/executive/` and `fr/executive/` hold the same document,
  section by section, so the two can be checked side by side. To add a kind of document, create it under
  every language that needs it, with the same name (`en/faq/`, `fr/faq/`). To add a language, add a
  folder next to `en/` and `fr/`.
- **Layout once.** `shared/layout.tex` holds everything that does not depend on the language. Every
  document sits two levels below `summaries/` (`<lang>/<kind>/<document>.tex`), so it loads the layout
  through the same relative paths, and the same paths to `../outputs/` work for all of them.
- **Each source named after its document,** as its PDF: `executive-summary_en.tex` gives
  `executive-summary_en.pdf`. Never `main.tex`, which on Overleaf would compile the note instead (below).

## Numbers and figures come from the note's outputs

A summary never types a number that the note computes.
- **Numbers.** `../simulations/python/key_numbers.py` reads `../outputs/tables/*.csv` and writes
  `key_numbers_en.tex` and `key_numbers_fr.tex` to `../outputs/tables/`. Both files define the same macro
  names (`\KNcontestedQVC`, …), with each language's decimal mark. `key_numbers.csv` gives the table, row
  and column behind each macro.
- **Figures.** They come from `../outputs/figures/`, which `../simulations/python/figures.py` writes. A
  figure with words in it gets a version per language (`fig_theta.pdf`, `fig_theta_fr.pdf`).

When the simulation changes, rerun `experiments.py`, `key_numbers.py` and `figures.py`, then rebuild the
summaries. The numbers follow automatically; the words may still need editing, in every language.

## Build

```bash
cd summaries/en/executive && latexmk      # writes executive-summary_en.pdf
cd summaries/fr/executive && latexmk      # writes synthese_fr.pdf
```

On Overleaf, set the document as the main document (Menu > Settings > Main document), for example
`summaries/fr/executive/synthese_fr.tex`. Overleaf moves to the document's folder and writes its output
to the project root. Every document sets `\input@path` so that its paths work from either place. A
document must not be called `main.tex`: pdfLaTeX looks first in the output folder, the project root, and
would compile the root `main.tex`, the note, instead. The French documents need the TeX Live French
language support (`texlive-lang-french` on Debian or Ubuntu; it is included on Overleaf).

Each document's folder holds its current PDF, named after the document (`executive-summary_en.pdf`,
`synthese_fr.pdf`), so readers find it next to its source. The build writes it there: commit it when the
summary changes. The PDFs of record of each version also go to `../versions/<version>/`, next to the PDF
of the note they summarise.

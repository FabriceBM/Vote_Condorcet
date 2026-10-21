# Summaries

This folder holds short documents derived from the note, for readers who will not read the note itself.
The note stays in `../manuscript/` and remains the single source: a summary adds no result of its own.

## Hierarchy

```
summaries/
├── README.md                 this file
└── executive/                one folder per kind of summary (executive, one-pager, slides, …)
    ├── shared/
    │   └── layout.tex        layout common to every language: page, fonts, colours, boxes, title block
    ├── en/                   one folder per language, the same content in each
    │   ├── main.tex          executive summary in English, 2 pages
    │   └── latexmkrc
    └── fr/
        ├── main.tex          synthèse en français, 2 pages
        └── latexmkrc
```

The levels follow two rules:
- **Kind, then language.** To add a kind of summary (`one-pager/`, `slides/`), create a sibling of
  `executive/` with the same `shared/` + `<lang>/` layout. To add a language, add a folder next to `en/`
  and `fr/`.
- **Layout once, content per language.** `shared/layout.tex` holds everything that does not depend on the
  language; `<lang>/main.tex` holds the text and the babel language. The language versions keep the same
  structure, section by section, so they can be checked side by side.

## Numbers and figures come from the note's outputs

A summary never types a number that the note computes.
- **Numbers.** `../simulations/python/key_numbers.py` reads `../outputs/tables/*.csv` and writes
  `../outputs/tables/key_numbers_en.tex` and `key_numbers_fr.tex`. Both files use the same macro names
  (`\KNcontestedQVC`, …) with each language's decimal mark. `key_numbers.csv` gives the table, row and
  column behind each macro.
- **Figures.** They come from `../outputs/figures/`, which `../simulations/python/figures.py` writes; it
  also writes a French version (`fig_theta_fr.pdf`).

When the simulation changes, rerun `experiments.py`, `key_numbers.py` and `figures.py`, then rebuild the
summaries. Their text may still need editing: the numbers update by themselves, the words do not.

## Build

```bash
cd summaries/executive/en && latexmk main.tex
cd summaries/executive/fr && latexmk main.tex
```

The French version needs the TeX Live French language support (`texlive-lang-french` on Debian or Ubuntu).
Built PDFs are not committed here. The PDFs of record go to `../versions/<version>/`, next to the PDF of
the note they summarise.

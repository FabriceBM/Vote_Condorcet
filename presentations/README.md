# Presentations

Every talk given on the project, one folder per talk, as in Immo_S2 (`presentations/2020-05_ibfi/`). The note
in `../manuscript/` stays the single source: a talk adds no result of its own.

## Talks

| Talk | Date | Event and audience | Length | Language | Note version | Slides | Status |
|---|---|---|---|---|---|---|---|
| [`Research-seminar/`](Research-seminar/) | to be set | Research seminar | about 40 min, 25 slides and 5 backup | English | v0.1.1 | [PDF](Research-seminar/Research-seminar_VotingWithVetoes.pdf) | in preparation |

Add a row for each new talk; keep the rows of past talks.

## Layout

```
presentations/
├── README.md                          this file: the index of talks
├── shared/
│   └── beamer-style.tex               the look shared by every talk (Metropolis, in the colours of the
│                                      figures and the summaries) and the note's notation
└── <Event>/                          one folder per talk, e.g. Research-seminar/
    ├── <Event>_<Title>.tex            the slides (Beamer); never main.tex
    ├── <Event>_<Title>.pdf            the PDF as presented
    ├── latexmkrc                      names the .tex, so that `latexmk` alone builds it
    └── notes.md                       after the talk: questions asked, feedback, what to change (optional)
```

- **Names.** The folder is named after the event (`Research-seminar/`), the slides after the event and the
  title (`Research-seminar_VotingWithVetoes.tex`), with `_fr` before the extension for a talk in French.
  The date goes in the table above. Two talks at events of the same name are told apart by the month, as
  in Immo_S2 (`2027-03_Research-seminar/`).
- **A new talk** starts as a copy of the latest talk's folder, renamed. The slides of different talks
  diverge freely; what they share (look, notation) is in `shared/`.
- **Numbers and figures** come from the note's outputs, never typed: the macros of
  `../outputs/tables/key_numbers_<lang>.tex` (written by `../simulations/python/key_numbers.py`, which
  also holds the results table of the talks) and the figures of `../outputs/figures/`.
- **After the talk**, set its date and status (`given`) in the table above, commit the PDF as presented,
  and leave the folder unchanged. If the simulation or the shared style changes later, rebuilding an old
  talk would change it: its committed PDF is the record of what was shown.

## Build

```bash
cd presentations/Research-seminar && latexmk     # writes the PDF next to the source
```

On Overleaf, set the slides' `.tex` file as the main document (Menu > Settings > Main document). Overleaf
moves to the talk's folder and writes its output to the project root; every talk sets `\input@path` so that
its paths work from either place. A talk must not be called `main.tex`: pdfLaTeX would compile the root
`main.tex`, the note, instead. `python3 tools/overleaf_zip.py --test` compiles every talk as Overleaf does.

The Metropolis theme reports one harmless `Overfull \vbox` on the title page, with any content.

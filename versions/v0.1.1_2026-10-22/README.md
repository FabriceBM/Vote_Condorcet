# v0.1.1, 22 Oct. 2026: the note with its bibliography checked against the official records

| File | Content | Built from |
|---|---|---|
| `Vote_Condorcet_SOTA_note_v0.1.1.pdf` | The note (36 pages) | `cd journals/working-paper && latexmk main.tex` |

**What changed since v0.1: the bibliography only.** Every entry was checked against its official record:
Crossref, doi.org, arXiv and the publishers' pages (`literature/reference-checks/README.md`). As a result:
- 16 DOIs were added;
- Balinski & Laraki is dated 2011;
- Kemeny (1959) has pages 571–591;
- four issue numbers were aligned on the records.

The text, the tables and the figures are unchanged. The executive summaries cite no reference, so their PDFs
of record stay in `../v0.1_2026-10-21/` (current copies in `summaries/<lang>/executive/`).

This version is frozen; later changes go to `manuscript/`.

# Concept map: concepts ↔ bibliography

`concept-map.xlsx` links every concept of the note to the bibliography, and every bibliography entry to
the concepts it supports, with the key ideas it conveys.

| Sheet | One row per | Columns |
|---|---|---|
| About | | Purpose, how to update, counts, and a reciprocity check: the links counted by concept, by entry and in the matrix must agree |
| Concepts to bibliography | concept (35) | concept · bibliography entries (oldest first) · definition and role in the note · note sections · concept id · number of entries |
| Bibliography to concepts | entry (98) | bibliography entry · concepts used · key ideas conveyed · citation key · cited in (sections) · full reference · DOI or URL · still to verify · number of concepts |
| Matrix | entry | one column per concept, `x` where linked, totals |

## How it is built

Each link is entered **once**:

| File | Content |
|---|---|
| `concepts.csv` | id, concept, definition and role in the note, note sections |
| `references.csv` | citation key, concept ids separated by `;`, key ideas conveyed |

`../../tools/concept_map.py` builds the rest:
- It reads both files and `../../manuscript/references.bib` (full references, DOIs, `verify` fields).
- It reads `../../manuscript/sections/*.tex` to find the sections that cite each entry.
- It derives the concept-to-bibliography sheet by inverting `references.csv`, so the two directions cannot
  disagree.
- Before writing anything, it checks four things:
  - every bibliography entry has a row;
  - every row is in the bibliography;
  - every concept id exists;
  - every concept has at least one entry.

The counts in the workbook are formulas on the Matrix sheet.

```bash
python3 tools/concept_map.py --check     # consistency checks only
python3 tools/concept_map.py             # checks, then writes concept-map.xlsx
```

The script writes formulas without their values. Excel computes them on opening. Other readers need a
recalculation first, for example with LibreOffice:
`soffice --headless --convert-to xlsx --outdir /tmp literature/concept-map/concept-map.xlsx`.

**To edit the map**, change the CSV files, never the workbook, and rerun the script. **When a reference
is added to the note**, add it to `references.bib` and to `references.csv`; the check fails until both
are done.

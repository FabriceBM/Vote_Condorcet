# What changed, version by version

Each entry gives:
- what moved in the note's results when the method changed, and why;
- the headline numbers before and after;
- the generated tables, cell by cell (`python3 tools/results_diff.py OLD NEW`).

The newest entry comes first.

## v0.1.1, 22 Oct. 2026: the bibliography checked against the official records

**No result changed.** Every table is unchanged (`python3 tools/results_diff.py` reports none), and so is
the text.

`tools/check_references.py` compared the 98 entries of `references.bib` with their official records:
Crossref and doi.org, the Library of Congress catalogue for books without a DOI, the EU Publications Office
for the Treaty, the authors' institutional repositories for two articles without a DOI, arXiv, and the
publishers' pages. The details are in `../literature/reference-checks/README.md`.
- **97 entries are confirmed by their official record.** One is not yet (below). No entry is fabricated.
- **Corrections:**
  - 16 DOIs added, all resolving;
  - Library of Congress control numbers added to the 5 books without a DOI (Condorcet, Arrow,
    Buchanan & Tullock, Regenwetter et al., Tideman);
  - the EU Treaty cited at its page, OJ C 202, 7.6.2016, p. 24, with its ELI identifier;
  - Felsenthal & Machover (2008) linked to its LSE record, where the manuscript is free to read;
  - Balinski & Laraki dated 2011, as in the MIT Press record (2010 before);
  - issue numbers of Holliday & Pacuit, Glynia et al., Kondratev & Nesterov and Krick aligned on the
    records;
  - the second author of Kondratev & Nesterov given in full.
- **Not yet confirmed: 1 entry,** down from 28 flagged. Kemeny (1959): its only record is on JSTOR, which
  refuses automated access, and the citing papers give 577 or 571 as its first page. It stays marked
  `verify` until checked by hand (`author-tasks.md` §2).

The note's PDF of record is in `../versions/v0.1.1_2026-10-22/`.

## v0.1, 21 Oct. 2026: first version

There is no earlier version to compare against. During development, before the first commit, three
choices changed the numbers. The reasons are in `research-agenda.md` §3.

1. **The veto tolerance.** It moved from U(1.25, 2.25) to U(1.5, 2.5): about 50% of the options vetoed
   before, 35–40% after. With half the menu vetoed:
   - every QVC with θ ≤ 25% fell back in 60–100% of elections;
   - the measure "consensus found" was never defined, because no option was acceptable to all 101 voters.
     It was replaced by worst-off efficiency.
2. **The tie-break.** It moved from (fewest vetoes, Borda) to (fewest vetoes, Schulze on the tied set). The
   Borda step made clone-independent rules (Split Cycle, approval) show clone effects of 1–2% in the clone
   table. They are now 0.0–0.2%.
3. **Manipulability.** The small-coalition column (at most 10% of the voters) was added. With full
   coalitions, every QVC with θ < 1/2 was manipulable in about 100% of elections, which did not tell the
   rules apart.

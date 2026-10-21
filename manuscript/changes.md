# What changed, version by version

Each entry gives:
- what moved in the note's results when the method changed, and why;
- the headline numbers before and after;
- the generated tables, cell by cell (`python3 tools/results_diff.py OLD NEW`).

The newest entry comes first.

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

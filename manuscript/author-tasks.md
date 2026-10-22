# Next steps for the author

This file lists what Fabrice Borel-Mathurin needs to decide, check or extend to take the note from
draft v0.1 to a version that can be circulated. Tick tasks off in the pull request that closes them.

## 1. Decisions

| | Task | Where |
|---|---|---|
| [ ] | Title, author line, affiliation, acknowledgements. `metadata.tex` currently says "Draft for discussion" | `metadata.tex` |
| [ ] | Confirm θ = 1/3 as the default, or choose 1/4 for a more consensual setting | §6.5, `research-agenda.md` §3 |
| [ ] | Decide whether the status quo is protected (a Debian-style ratio) for the intended use case | §6.5 |
| [ ] | Decide on the revision round (on or off; its length) | §6.6 |
| [ ] | Decide the target: an internal note, a working paper, or a journal | below, §4 |

## 2. Checks

| | Task | How |
|---|---|---|
| [ ] | Confirm the 3 entries still marked `verify` in `references.bib`. No official record of them is reachable from the checking environment: JSTOR refuses automated access. The other 95 entries are confirmed by their official records (`../literature/reference-checks/README.md`) | In a browser: JSTOR [1815369](https://www.jstor.org/stable/1815369), Plott (1967), issue 4 and pages 787–806; JSTOR [20026529](https://www.jstor.org/stable/20026529), Kemeny (1959), first page 577 or 571; LSE Research Online [24213](https://eprints.lse.ac.uk/24213/), Felsenthal & Machover (2008), last page 334 or 333 |
| [ ] | Read the key papers in full; the reference checks used publisher pages and abstracts | Bouton et al. (2018), Moulin (1981, 1982), Ianovski & Kondratev (2021), Kondratev & Ianovski (2024), Kondratev & Nesterov (2020), Greenberg (1979), Holliday & Pacuit (2023) |
| [ ] | Check the characterisation of Majority Judgment as monotonic, and the Monotonic column of Table 3 for fallback bargaining and the majoritarian compromise | Balinski & Laraki (2011), Felsenthal (2012) |
| [x] | Check that Debian's 3:1 ratio for constitutional amendments is unchanged in constitution v1.9 | Confirmed on debian.org, 22 Oct. 2026: "Amend this constitution, provided they agree with a 3:1 majority"; default option "None of the above"; quorum 3Q |
| [ ] | Proofread the propositions and proofs (Appendix A), in particular Proposition 2(ii) and Lemma 9 | |

## 3. Extensions, by value

1. **Real ballots.** Run the rules on Debian's published ranked ballots: options above and below
   "None of the above" give the acceptability line. Extend to PrefLib data sets. This would replace the
   stylised cultures with observed preferences.
2. **Robustness of the simulation:**
   - 1, 3 and 5 dimensions;
   - other numbers of options (5, 12, 20);
   - another veto tolerance;
   - heterogeneous proposal activity (flooding by one bloc).

   All are one-parameter changes in `cultures.py`.
3. **Strategic vetoing in more depth:**
   - optimal coalition strategies rather than three heuristics;
   - the minimum coalition size needed to manipulate, per rule.
4. **The revision round:** simulate a second round in which a compromise proposal is added when the
   fallback triggers.
5. **Open question §8.3:** is there a clone-independent rule with proportional veto power and a non-empty
   core, or a proof that the three are incompatible?

## 4. Outlets (to check against each one's scope)

| Option | Fit |
|---|---|
| Internal or technical note | As is, after §1–2 |
| *Social Choice and Welfare*, *Public Choice*, *Group Decision and Negotiation* | Needs extension 1 or 3, and a sharper statement of the new results: Propositions 2, 3 and 8, and the design argument |
| *Mathematical Social Sciences* | If the open question of §8.3 gets an answer |
| A practitioner outlet (governance, cooperatives, standards bodies) | §6 and §8.4, shortened |

# The Consensus review (Oct. 2026): what it says and how the note uses it

**What the review is.**
- **Report:** "State of Optimal Voting With Veto Rights", produced with the Consensus search engine
  (consensus.app). Its PDF is `261021_Consensus_LitReview_VotingRights.pdf`, 10 pages, generated on 21 Oct.
  2026.
- **Why the PDF is not in this repository:** its licence allows personal, non-commercial use only and
  forbids redistribution, and this repository is public. Keep the PDF in `literature/private/`, which git
  ignores.
- **What this file is:** a summary in our own words, written so that the note can be read without the
  report.

**Search behind it.** 8 searches and one citation-graph step. 537.6K records were retrieved, 281 were
eligible and 100 were included. It draws on economics, political science, social choice and
experimental work.

## Its conclusions

1. **No single rule is optimal.** The best-supported pattern is conditional: full unanimity is usually too
   restrictive for open-choice bargaining. Majority rule with a separate veto channel often does better,
   but only when vetoes are limited to blocking truly unacceptable changes.
2. **The answer depends on the problem:**
   - epistemic choice between a reform and the status quo: majority with veto is strongly supported
     (Bouton et al.);
   - selecting a compromise from an open set: veto, shortlisting, fallback and proportional-veto
     procedures can produce acceptable compromises, but none is manipulation-proof and several fail as
     ex-post compromises;
   - fast implementation: recent proposal procedures reach the Condorcet winner in one or two rounds, but
     only under single-peaked preferences and without hard vetoes (Gersbach; Gersbach & Valkanova).
3. **Rounds.** There is no general "more rounds are better" result. One or two rounds suffice in
   structured proposal models; more rounds create inertia and capture by vetoers in dynamic veto
   bargaining.
4. **Evidence strength (its Figure 6):**

   | Claim | Strength |
   |---|---|
   | Majority with veto beats unanimity for information aggregation | Strong |
   | Full unanimity is inefficient in open-choice bargaining | Strong |
   | One or two rounds suffice in structured settings | Moderate |
   | Fallback and shortlist rules are useful second-best devices | Moderate |
   | Tacit consensus gives everyone an effective veto | Weak |

5. **Gaps:**
   - one- or two-round proposal procedures with hard vetoes;
   - a comparative strategic evaluation of compromise rules under common assumptions;
   - when communication offsets the inefficiency of unanimity;
   - the weak link between empirical consensus research and formal veto-player theory.

## How the note uses it

- **§1 and §4:**
  - its framing (separate "block the unacceptable" from "approve");
  - its sources on committees, bargaining and rounds;
  - its evidence table (Table 2 of the note adapts and extends its Figure 6).
- **§8.3:** two of its open questions, "fast procedures with hard vetoes" and "strategic comparison of
  compromise rules".

## What the note adds

1. **The social-choice literature the review does not cover:**
   - Condorcet methods (Schulze, Ranked Pairs, Split Cycle);
   - independence of clones (Tideman), which is essential under an open agenda;
   - the proportional veto core (Moulin; Ianovski & Kondratev; Kondratev & Nesterov);
   - stability and quotas (Nakamura; Greenberg; Caplin & Nalebuff);
   - manipulation and efficiency studies (Green-Armytage et al.).
2. **Institutional practice:**
   - the IETF's rough consensus;
   - Debian's Schulze vote with "None of the above" as default;
   - the EU blocking minority;
   - the liberum veto.
3. **Formal results:**
   - deadlock under unanimity (Prop. 2);
   - flooding against proportional veto (Prop. 3);
   - the properties of the recommended procedure (Prop. 4–8).
4. **A concrete procedure, QVC(θ), with a Monte Carlo comparison of 21 rules.** This answers the review's
   second gap only in part: it is a simulation, not a strategic equilibrium analysis.

## Problems found in its reference list

These were checked on 21 Oct. 2026 (`reference-checks/2026-10-21_web-search.md`).

| Problem | Correction |
|---|---|
| "C., & Manove, M. (1993). Bargaining with Deadlines and Imperfect Player Control" | The first author is truncated. It is very probably Ma, C. A. & Manove, M., *Econometrica* 61(6). Not used in the note |
| Barberà & Gerber "(2015)", *Theoretical Economics* 12 | The volume is 2017; cited as 2017 |
| Kartik, Kleiner & Van Weelden "(2020)", AER | Published in 2021, 111(12):4046–4087 |
| Cailloux, Napolitano & Sanver "(2022)", RED 27 | Online 2022; the print issue is 27(3), 2023 |
| Breitmoser & Valasek "(2017)", "A rationale for unanimity in committees" | A working paper with no venue. Not used |
| Chen & Yang (2026), QJPS | Not checked. Not used |

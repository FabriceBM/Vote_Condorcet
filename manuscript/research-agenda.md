# Voting for a consensus with veto rights: research agenda (Oct. 2026)

## 0. The question

> A state-of-the-art note on the research consensus about optimal voting with veto rights.
> - **Audience:** engineers, actuaries, people with a strong scientific background.
> - **Goal:** define a voting procedure that lets a group vote for a consensus choice.
> - **Hypotheses:** any voter can propose as many choices as they wish, vote on *all* the choices proposed,
>   and has veto rights.
> - **Requirements:** the "best compromise" is reached, and the group does not get stuck, so veto rights
>   must not be too stringent.

| | Hypothesis or requirement | Where the note answers it |
|---|---|---|
| H1 | Open agenda: anyone proposes any number of options | §5.2 (clones), Prop. 3 and 7, table `clones` |
| H2 | Full ballots: everyone judges every option | §2.1 (ballot = ranking + acceptability line), §5 |
| H3 | Veto rights | §2.4 (three veto structures), §4 (literature), §6 |
| R1 | Best compromise | §2.5 (notions of compromise), Def. 5 (θ-compromise), Prop. 5–6, §7 |
| R2 | No deadlock | Prop. 2 (unanimity deadlocks), Prop. 4 (QVC always decides), table `deadlock_n` |

## 1. The answer in brief

The answer is the procedure **QVC(θ), Condorcet with a blocking quota**, with θ = 1/3 by default. It works
on one ballot:

1. Each voter ranks every option and marks the unacceptable ones.
2. Options vetoed by at least θn voters are excluded.
3. If that excludes every option, the least-vetoed options are kept.
4. The Schulze winner among the options left is elected.

Why this design: it follows from the principles P1–P6 of §6.1.
- P1: one ballot, no agenda.
- P2: ranking and blocking are separate acts.
- P3: vetoes are held by coalitions, not individuals.
- P4: the status quo is an option like the others.
- P5: the aggregation is clone-independent.
- P6: a decision is guaranteed.

## 2. The route

The note had to be a state of the art, which means a literature review. The goal was a procedure, which
means a design argued from that literature. The audience is quantitative, which means formal statements
and numbers. So the note has three layers:

1. **Literature** (§3–5). The starting point is the review of the uploaded Consensus report
   (`../literature/consensus-2026-10_review-notes.md`). It covers committee bargaining and unanimity against
   majority with veto. We extended it with social choice:
   - Condorcet methods and clones (Tideman, Schulze, Holliday–Pacuit);
   - proportional veto (Moulin, Ianovski–Kondratev);
   - stability and quotas (Nakamura, Greenberg, Caplin–Nalebuff);
   - institutional practice (IETF, Debian, the EU Council, the liberum veto).

   The references were checked by web search on 21 Oct. 2026, then against the official records on 22 Oct. 2026:
   `../literature/reference-checks/README.md`.
2. **Formal results** (§3, §5, §6, Appendix A). Eight propositions. Five are new or restated with proofs for
   this setting:
   - deadlock under unanimity;
   - flooding against proportional veto;
   - the properties of QVC;
   - strategic blocking.

   The others are standard and cited.
3. **Simulation** (§7, Appendix C). There are 21 rules and three electorates, with 2,000 elections each.
   Proposals come from voters, so clones arise naturally. Vetoes come from a tolerance fixed before the
   menu is known. The measures are:
   - Condorcet efficiency;
   - utility and worst-off efficiency;
   - acceptance;
   - contested outcomes;
   - deadlock;
   - clones;
   - manipulability by full and by small (10%) coalitions.

## 3. Design choices made along the way, and why

| Choice | Alternatives considered | Why |
|---|---|---|
| Veto = an acceptability line in the ranking | A separate veto budget per voter | A budget within one decision breaks independence of clones: each clone costs a veto (§6.6) |
| Blocking quota with fallback (absolute) | A relative quota: exclude options with θn more vetoes than the least-vetoed | Tested on 600 elections per culture. The relative quota almost never excludes anything and collapses to Schulze, so it does not protect minorities |
| Schulze for the majority step | Ranked Pairs, Split Cycle | All are clone-independent and Smith-consistent. Schulze is resolute, monotonic and used in practice (Debian). Split Cycle is often not resolute. Ranked Pairs would do equally well |
| Tie-break: fewest vetoes, then Schulze on the tied set, then a random order drawn before the vote | Borda as a second criterion | Borda is not clone-independent; with it as a tie-break, clone-independent rules showed spurious 1–2% clone effects in the first runs |
| θ = 1/3 by default | 1/4, 1/2 | Figure `fig_theta`. Below 20%, the fallback decides most elections and small-coalition manipulability is above 75%. From 40% up, the veto almost never binds. At 1/3: Condorcet efficiency ≥ 94%, fallback ≤ 6%, most of the worst-off gain kept |
| Status quo as an ordinary option | Status quo as the default (Debian-style) | A default turns every veto into a vote for inertia (§4.2). Protection stays available as an option for irreversible decisions (§6.5) |
| Measure "contested" at one third | At the quota | QVC(1/3) meets it by construction (Prop. 5). The note says so, and relies on utility and worst-off efficiency, which are not defined by vetoes, for the independent evidence |
| Small-coalition manipulability (10%) in addition to full coalitions | Full coalitions only | With full coalitions, every rule with θ < 1/2 is manipulable in ~100% of elections, so the measure does not discriminate (Prop. 8). Small coalitions are the realistic threat |
| Veto calibration: tolerance U(1.5, 2.5) in the spatial cultures, 35–40% of options vetoed | U(1.25, 2.25), about 50% vetoed | Vetoing half the menu made every option contested and the fallback universal. A veto should mark the unacceptable, not the below-average |

## 4. Evidence that would change the conclusions

- **Real ballots with acceptability lines.** Debian's general resolutions are an example (PrefLib holds
  others). These could show that vetoes are much rarer, so the fallback never binds and QVC equals Schulze,
  or much more frequent.
- **A laboratory test of strategic vetoing,** with and without named and reasoned vetoes.
- **A clone-proof proportional veto.** If such a rule exists, it would dominate QVC: it would be
  coalition-proof and robust to flooding (open question, §8.3).

## 5. Possible extensions

- **Repeated decisions:** endogenous status quo, veto budgets across decisions (storable votes).
- **Weighted voters,** for example shareholders or federations.
- **The two-round variant** (revision round), modelled with proposal dynamics à la Gersbach–Valkanova.
- **Multi-winner versions:** committees, budgets.

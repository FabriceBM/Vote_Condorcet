# Manuscript: "Voting for a consensus with veto rights: a state-of-the-art note" (draft v0.1, Oct. 2026)

This folder holds the note's content, independent of any journal. Edit the note here, and only here.
- The journal wrapper [`../journals/working-paper/main.tex`](../journals/working-paper/main.tex) pulls
  this content in with `\input`.
- The root [`../main.tex`](../main.tex) builds that wrapper; it is Overleaf's main document.
- The layout is the one of Immo_S2.

Other files:
- The question, the hypotheses and the route are in [`research-agenda.md`](research-agenda.md).
- What remains for the author is in [`author-tasks.md`](author-tasks.md).
- The sources, with notes, are in [`../literature/`](../literature/README.md). That includes the Consensus
  review the note starts from and the log of reference checks.

## Files

| File | Content |
|---|---|
| `metadata.tex` | Title, author, date |
| `abstract.tex` | Abstract and keywords |
| `body.tex` | Section order |
| `appendix.tex` | Appendix order |
| `preamble/packages.tex` | Packages the content needs (including `algorithm`, `algpseudocode`, `tabularx`, `enumitem`) |
| `preamble/macros.tex` | Notation (`\QVC`, `\PVC`, `\Adm`, `\veto`, `\Maj`, …) and the drafting markers |
| `preamble/theorems.tex` | Environments: proposition, lemma, corollary, definition, assumption, example, remark |
| `references.bib` | Only the entries the note cites. An entry with a `verify` field (which does not print) is incomplete or unconfirmed |
| `research-agenda.md` | Question, hypotheses, requirements, route, the design choices and why |
| `author-tasks.md` | Next steps: decisions, checks, extensions |
| `changes.md` | What moved in the results at each change of method, table by table (`../tools/results_diff.py`) |

## Sections, notes and tables

The hypotheses and requirements are set out in the research agenda, §0:
- **H1**, open agenda;
- **H2**, full ballots;
- **H3**, veto rights;
- **R1**, best compromise;
- **R2**, no deadlock.

| Section | File | Addresses | Tables and figures (script) |
|---|---|---|---|
| 1 Introduction | `sections/01_introduction.tex` | all | |
| 2 Setting and definitions | `sections/02_setting.tex` | H1–H3 | |
| 3 What no procedure can achieve | `sections/03_limits.tex` | R1, R2 | `cw_probability` (a); `fig_deadlock` (c), from `deadlock_n` (a) |
| 4 What research says about veto rights | `sections/04_veto_literature.tex` | H3, R2 | `tab:evidence` (in the text) |
| 5 Aggregating full ballots on an open agenda | `sections/05_aggregation.tex` | H1, H2 | `tab:properties` (in the text) |
| 6 The procedure | `sections/06_procedure.tex` | R1, R2 | `examples` (b); Algorithm 1 |
| 7 Simulation evidence | `sections/07_simulation.tex` | all | `perf_polarised`, `perf_spatial`, `clones`, `manipulability` (a); `fig_theta` (c) |
| 8 Discussion | `sections/08_discussion.tex` | | |
| 9 Conclusion | `sections/09_conclusion.tex` | | |
| A Proofs | `sections/A_proofs.tex` | | |
| B Algorithms | `sections/B_algorithms.tex` | | |
| C The simulation in detail | `sections/C_simulation.tex` | | `perf_impartial`, `theta_sweep`, `deadlock_n` (a) |

### Scripts

The scripts are in `../simulations/python/`. Run them from the repository root.

- **`voting.py`** (the rules):
  - Holds the election representation and the 21 rules. These include QVC(θ), the proportional veto core
    (max-flow test) and Schulze, Ranked Pairs and Split Cycle.
  - Holds `write_table`, which writes the tables in the note's caption style.
  - `--check` tests:
    - the PVC test against the definition;
    - Condorcet, Smith and Pareto consistency;
    - Schulze path strengths;
    - textbook examples;
    - Propositions 4–7.
- **`cultures.py`** (the random electorates): spatial, polarised, impartial and 1D. It covers open proposals,
  veto tolerances, grades and clones.
- **(a) `experiments.py`** (the Monte Carlo study):
  - Writes the tables `perf_*`, `manipulability`, `clones`, `theta_sweep`, `cw_probability` and `deadlock_n`.
  - `--check` tests:
    - the impartial-culture probabilities against their limits;
    - Black's median voter;
    - Proposition 2(i);
    - the consistency of the measures.
- **(b) `examples.py`** (the worked examples E1–E4): writes the table `examples`. `--check` tests the winners
  stated in Section 6.4.
- **(c) `figures.py`**: builds `fig_theta` and `fig_deadlock` from the CSV tables (PDF, plus a PNG preview).

Each script writes:
- its tables to `../outputs/tables/`, as `.csv` and `.tex`, label `tab:<name>`;
- its figures to `../outputs/figures/`, as `<name>.pdf`, label `fig:<name without fig_>`.

## Rules (as in Immo_S2)

- **Journal settings.** No `\documentclass`, page geometry, `\bibliographystyle` or other journal setting goes
  here. Those belong in `journals/<journal>/main.tex`.
- **Paths.** Paths in `\input` are relative to the wrapper: `../../manuscript/sections/...`,
  `../../outputs/tables/...`.
- **Generated tables.** Never edit the `.tex` in `outputs/tables/`: edit the script and rerun it. Tables
  written by hand stay in the text (`tab:evidence`, `tab:properties`).
- **Captions**, the same for tables and figures:
  - **Title**, in `\caption{}`: one short line saying what is shown, with no method and no final period.
    It goes above tables and below figures.
  - **Notes**, under it and smaller: what the rows, columns, lines or dots are, then the sample and the
    method.
  - **Source**, last line: the data or simulation, then the script.

  Generated tables use `\tabnotes{notes}{source}`; figures and tables written by hand use
  `\figurenotes{notes}{source}`. Both macros are in `preamble/macros.tex`.
- **Figures.** Use `\includegraphics{name}` with no path. Figures generated by code go in
  `../outputs/figures/`; static figures go in `figures/`.
- **Drafting markers.** There are two:
  - `\placeholder{...}`, in red: work still missing;
  - `\prelim{...}`, in orange: a number to update.

  `\FinalVersion`, commented out in the root `main.tex`, hides the first marker and prints the second in
  black. Before circulation, `grep -n 'placeholder\|prelim' manuscript/*.tex manuscript/sections/*.tex` must
  return nothing.
- **Citations.** Cite only entries of `references.bib`. Check each against the publisher's page:
  `grep -n verify manuscript/references.bib` lists the fields still to confirm.
- **Licensed material.** This repository is public, so no licensed PDF is committed: no publisher PDFs, and
  not the Consensus report, whose licence forbids redistribution. Keep them in `../literature/private/`,
  which git ignores.

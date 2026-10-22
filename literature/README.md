# Literature

The sources of the note, grouped by theme, with how each is used.

- **No PDFs.** The repository is public, so no publisher PDF is committed, and neither is the Consensus
  report the note started from: its licence allows personal, non-commercial use only. Keep such files in
  `literature/private/`, which git ignores.
- **Full references.** Every citation key below is in
  [`../manuscript/references.bib`](../manuscript/references.bib).
- **How they were checked.** First by web search (21 Oct. 2026), then against the official records: Crossref, doi.org,
  the Library of Congress catalogue, the EU Publications Office, arXiv and the publishers' pages (22 Oct. 2026).
  95 of the 98 are confirmed; 3 wait for a check by hand on JSTOR and the LSE repository. See
  [`reference-checks/README.md`](reference-checks/README.md).

## Starting point

| File | Content |
|---|---|
| `consensus-2026-10_review-notes.md` | The uploaded Consensus review "State of Optimal Voting With Veto Rights" (Oct. 2026): its conclusions, how the note uses them, what we added, and the errors in its references |
| `concept-map/concept-map.xlsx` | Spreadsheet linking every concept of the note to the bibliography and back, with the key ideas of each entry. Built by `../tools/concept_map.py` from `concept-map/concepts.csv` and `concept-map/references.csv`; see [`concept-map/README.md`](concept-map/README.md) |
| `reference-checks/` | Two checks of all 98 entries: by web search (21 Oct. 2026; it also answers content questions on the proportional veto core, Debian's counting rules, RFC 7282, TEU art. 16(4), Split Cycle and others), then against the official records (22 Oct. 2026, `../tools/check_references.py`). [`README.md`](reference-checks/README.md) gives the result: no entry is fabricated; 3 entries keep a flagged field |

## By theme (key: use in the note)

**Impossibility, majority and stability**
- `Arrow1951`, `Gibbard1973`, `Satterthwaite1975`: §3.1, manipulation is unavoidable.
- `Moulin1988noshow`, `BrandtGeistPeters2017`: §3.1, the no-show paradox of Condorcet methods.
- `Condorcet1785`, `Guilbaud1952`, `GehrleinFishburn1976`, `Gehrlein2006`: §3.2, cycles under the impartial
  culture (table `cw_probability`).
- `Black1948`, `RegenwetterEtAl2006`, `Tideman2006`, `TidemanPlassmann2012`: §3.2, cycles are rare in
  structured and real electorates.
- `Nakamura1979`, `Greenberg1979`, `CaplinNalebuff1988`, `McKelvey1976`, `Plott1967`: §3.4, stability against
  deadlock; Prop. 8, Greenberg's threshold.
- `BuchananTullock1962`, `Rae1969`: §3.4, the choice of a quota as a cost trade-off.
- `KondratevNesterov2020`: §3.3, majority power against veto power.

**Veto rights in committees and politics** (most come from the Consensus review)
- `BoutonLlorenteSaguerMalherbe2018` and `...2017`: §4.1, majority with veto beats unanimity.
- `MiettinenVanberg2025`, `PiazoloVanberg2025`, `LaingSlotznick1991`, `KagelSungWinter2010`,
  `AgranovTergiman2019`, `BreitmoserValasek2024`, `GlyniaThumXefteris2026`: §4.1.
- `Tsebelis1995`, `Tsebelis2002`, `RomerRosenthal1978`, `BaronFerejohn1989`, `Harrington1990`,
  `DziudaLoeper2016`, `AnesiSeidmann2015`, `AnesiDuggan2017`, `Nunnari2021`, `AnesiBowen2021`,
  `KartikKleinerVanWeelden2021`, `BarberaGerber2017`: §4.2, veto players, agenda power and the status quo.
- `Gersbach2025propose`, `GersbachValkanova2024`, `Gersbach2024forms`, `Bognar2015`: §4.3, rounds.

**Compromise rules and proportional veto**
- `Mueller1978`, `Moulin1981`, `Moulin1982`, `Moulin1983`, `IanovskiKondratev2021`, `KondratevIanovski2024`:
  §2.4, §4.4, §5.2, App. B (Lemma 9).
- `BramsKilgour2001`, `SertelYilmaz1999`, `HurwiczSertel1999`, `Anbarci1993`, `BarberaCoelho2017`,
  `BarberaCoelho2022`, `LaslierNunezSanver2021`, `CaillouxNapolitanoSanver2022`: §4.4.

**Aggregation rules, clones, manipulation**
- `Tideman1987`, `ZavistTideman1989`, `Schulze2011`, `HollidayPacuit2023splitcycle`,
  `HollidayPacuit2023stable`: §5, clones and Condorcet methods.
- `Smith1973`, `Fishburn1977`, `Simpson1969`, `Kemeny1959`, `YoungLevenglick1978`, `Young1988`, `Young1974`:
  §2, §5.
- `BramsFishburn1978`, `LaslierSanver2010`, `BalinskiLaraki2007`, `BalinskiLaraki2011`,
  `FelsenthalMachover2008`: evaluative rules.
- `Fishburn1984`, `LaffondLaslierLeBreton1993`, `BrandlBrandtSeedig2016`: maximal lotteries.
- `GreenArmytageTidemanCosman2016`, `Merrill1984`, `BartholdiToveyTrick1989manip`,
  `BartholdiToveyTrick1989hard`, `FaliszewskiProcaccia2010`, `Laslier2012loser`, `Felsenthal2012review`,
  `ElkindFaliszewskiSlinko2015`: manipulation, efficiency, computation.
- `BrandtEtAl2016handbook`, `MatteiWalsh2013`, `Mallows1957`: background, data.

**Consensus in practice**
- `Resnick2014rfc7282`: the IETF's rough consensus.
- `Krick2017`: tacit consent.
- `Rohac2008`: the liberum veto.
- `TEU2016art16`: the EU blocking minority.
- `Debian2024constitution`: Schulze with a default option.
- `Casella2005`: storable votes, for veto budgets across decisions.

`Mallows1957` (a ranking model for a future robustness culture) is in the bibliography file but not yet
cited; bibtex prints only cited entries.

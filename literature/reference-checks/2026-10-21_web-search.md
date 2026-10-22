# Reference checks, 21 Oct. 2026

Two background agents checked the references of the note on 21 Oct. 2026:
- **Part A:** social choice;
- **Part B:** veto rights, bargaining and institutions.

Their logs follow unchanged.

**How the checks were made.** The working environment could not reach doi.org, Crossref, JSTOR or arXiv
directly. Every check therefore relies on web-search views of publisher pages, RePEc/IDEAS, repository
records and abstracts, not on the full texts.

**What follows from that.**
- Fields that could not be confirmed carry a `verify` field in `../manuscript/references.bib`. That field
  does not print.
- Claims marked [to verify] below were either not used in the note, or used only in a form the abstract
  supports.

**Corrections made in the note after these checks.**
- Elkind, Faliszewski & Slinko (2015): *SCW* 45(2):345–377.
- Balinski & Laraki: the MIT Press book is dated 2010.
- Cailloux et al.: print issue 27(3), 2023.
- Hurwicz & Sertel: published by Palgrave Macmillan, chapter pp. 69–88.
- Debian: the counting rules are in §A.5 of constitution v1.9.

**Not used, because unverified.**
- The name "veto by consumption" for the selection rule of Ianovski & Kondratev (2021).
- The exact property table of Kondratev & Ianovski (2024).
- The list of Schulze adopters beyond Debian.

---

# Part A


Checked on 2026-10-21. This environment's network policy blocked doi.org, api.crossref.org, jstor.org, wikipedia.org and api.openalex.org, so WebFetch could not open any page. Every check below therefore relies on web-search results, which return snippets and summaries of publisher pages, RePEc/IDEAS, JSTOR listings, repositories and Wikipedia. The full texts of the papers were not read. The session's web-search budget ran out before the last few checks (the Guilbaud page range).

---

## 1. Probability that a Condorcet winner exists under impartial culture (IC) as n → ∞

| m (alternatives) | P(Condorcet winner), n → ∞ |
|---|---|
| 3 | 0.9123 |
| 4 | 0.8245 |
| 5 | 0.7487 |
| 6 | 0.6848 |
| 7 | 0.6308 |

(The same table continues with m = 8: 0.5849, m = 9: 0.5455, m = 10: 0.5113.)

- These are the values in the n = ∞ row of the IC table in M. Harrison-Trainor, "An Analysis of Random Elections with Large Numbers of Voters": https://homepages.math.uic.edu/~mht/papers/elections.pdf
- They agree with the classic results: Garman & Kamien (1968) give a paradox probability of about 0.087 for m = 3, so P(CW) ≈ 0.913. Fishburn (1973), as quoted in Brandl–Brandt–Seedig, gives "at least 63%" for seven alternatives (https://arxiv.org/pdf/1503.00694). For m = 3 the closed form is Guilbaud's formula, 3/4 + (3/(2π))·arcsin(1/3) ≈ 0.9123. Sources say Guilbaud (1952) gave the limit for three options (https://halshs.archives-ouvertes.fr/halshs-00198573v1/file/halshs-00198573.pdf), but the formula itself comes from standard knowledge and was not quoted by any page I saw.
- An exact integral formula and the convergence rate are in arXiv:2505.06028: https://arxiv.org/html/2505.06028v1
- **Not checked directly:** the table in Gehrlein (2006). The Springer pages were paywalled. If you want to cite Gehrlein (2006) or Gehrlein–Fishburn (1976) for these numbers, check the table in the book.

## 2. Caplin & Nalebuff (1988): the 64% result

From the abstract (https://www.econometricsociety.org/publications/econometrica/1988/07/01/64-majority-rule and https://ideas.repec.org/a/ecm/emetrp/v56y1988i4p787-814.html):
- **Setting:** each voter votes for the proposal closest, in Euclidean distance, to his or her ideal point. The ideal points have a density that is **concave over its support in R^n** (a convex support). The condition is plain concavity of the density, not log-concavity.
- **Result:** under these conditions 64%-majority rule has an **unbeatable proposal**, and **no electoral cycles** can occur.
- **Threshold in n dimensions:** 1 − (n/(n+1))^n. It increases with n towards 1 − 1/e ≈ 0.632, which is why "64%" always works. The method builds on the Simpson–Kramer min-max rule.
- The search snippets garbled the formula, so check its typography against the paper.
- A follow-up generalizes the density condition and states the **mean voter's** ideal point is unbeatable under 64% rule: Caplin & Nalebuff (1991), "Aggregation and Social Choice: A Mean Voter Theorem," *Econometrica* 59(1) (https://intouch.econometricsociety.org/publications/econometrica/1991/01/01/aggregation-and-social-choice-mean-voter-theorem). I did not confirm its pages.

## 3. Greenberg (1979): supermajority threshold for a nonempty core

From the abstract (https://www.econometricsociety.org/publications/econometrica/1979/05/01/consistent-majority-rules-over-compact-sets-alternatives):
- Let X be compact and convex of **dimension m**, and preferences convex and continuous. A d-majority equilibrium (a point to which fewer than d voters prefer any alternative) exists **for every profile if and only if d > (m/(m+1))·n**. In your notation, with dimension d, the threshold share is d/(d+1), with **strict** inequality.
- For a finite set of T alternatives, the condition is d > ((T−1)/T)·n.

## 4. Nakamura (1979): the Nakamura number

- **Definition:** for a simple game W (the family of winning coalitions), the Nakamura number ν(W) is the smallest number of winning coalitions whose intersection is empty. If the game has a veto player (it is collegial), no such family exists and ν(W) = +∞. Some authors instead set it to "number of alternatives + 1". Sources: https://en.wikipedia.org/wiki/Nakamura_number and Freixas & Kurz, arXiv:1711.06611 (https://arxiv.org/pdf/1711.06611).
- **Theorem (Nakamura 1979):** the core of the simple game with preferences is nonempty **for every profile of acyclic preferences** if and only if the set of alternatives is finite and **#alternatives < ν(W)**. Sources: Wikipedia, and Kumabe & Mihara, arXiv:0705.3227.
- **q-quota rule with n voters**, where a coalition wins if it has at least q members and n/2 < q < n: **ν = ⌈n/(n−q)⌉**. Freixas & Kurz attribute this to Ferejohn & Grether (1974) and Peleg (1978); their example is n = 5, q = 3, ν = 3. For q = n (unanimity) every voter has a veto and ν = ∞.
  - Consequence: the core is guaranteed nonempty for k alternatives iff k < ⌈n/(n−q)⌉. Equivalently, q > n(k−1)/k, which is the finite case of Greenberg's ((T−1)/T)·n.
- Simple majority has ν = 3 for every n except n = 4, where ν = 4 (Wikipedia).

## 5. Holliday & Pacuit, Split Cycle (Public Choice 197, 2023)

Sources: the abstract (https://link.springer.com/10.1007/s11127-023-01042-3) and the arXiv version (https://arxiv.org/pdf/2004.02350, https://ar5iv.arxiv.org/html/2004.02350).
- **Satisfies:** the Condorcet winner and Condorcet loser criteria, **monotonicity**, **independence of clones**, the narrowing criterion, the **Smith criterion**, independence of Smith-dominated alternatives (ISDA), **reversal symmetry** (Prop. 6.14 in the arXiv version), **positive involvement** and **negative involvement**. It also satisfies the new **immunity to spoilers**, and among known clone-independent methods only Split Cycle has all three of immunity to spoilers, positive involvement and negative involvement. The authors say it mitigates spoiler effects and strong no-show paradoxes.
- **Fails:** the **Schwartz criterion**, and **resolvability** in both its single-voter and asymptotic forms. So it is not resolute and often returns several tied winners. The authors argue that neither property is normatively compelling.
- Ranked Pairs, Beat Path (Schulze) and Stable Voting refine Split Cycle and usually pick a single winner (AAAI paper: https://ojs.aaai.org/index.php/AAAI/article/view/38729/42691).
- Axiomatic characterization (via "Coherent IIA", a weakened form of Arrow's IIA): Ding, Holliday & Pacuit, arXiv:2210.12503.
- **Mechanism:** within every majority cycle, discard the majority preference with the smallest margin. The undefeated candidates win (arXiv:2210.12503).

## 6. Green-Armytage, Tideman & Cosman (2016)

Sources: the abstract (https://ideas.repec.org/a/spr/sochwe/v46y2016i1p183-212.html) and the author's accepted version (https://www.jamesgreenarmytage.com/strategy-utility.pdf).
- The authors generate synthetic elections from two survey data sets, two spatial models, and the IC and IAC models. For each election they test whether each of **54 voting rules** is non-manipulable and whether it is efficient in the sense of maximizing summed utilities.
- **Hare (IRV) and Condorcet–Hare are the most strategy-resistant non-dictatorial rules.** Most rules have **very similar utilitarian-efficiency scores**. The exceptions are a few poor performers: **random dictator, plurality and anti-plurality**. The results are highly robust across the data-generating processes.
- Analytically, adding a **Condorcet provision** to a base rule **cannot introduce manipulability where none existed** for all but a few base rules. The authors conclude that the analysis supports **Condorcet–Hare**.

## 7. Schulze (2011): properties and adopters

- **Properties.** The title claims monotonicity, independence of clones, reversal symmetry and Condorcet consistency. The abstract of the extended version (arXiv:1804.02973, https://arxiv.org/pdf/1804.02973; also the 2017 draft at https://aso.icann.org/wp-content/uploads/2019/02/schulze1.pdf) lists **resolvability, Condorcet, Schwartz, Smith-IIA, Pareto, reversal symmetry, monotonicity, prudence, independence of clones**. It also gives an **O(C³) algorithm** for the winner, where C is the number of alternatives. The Schwartz criterion implies the Smith criterion, because the Schwartz set is contained in the Smith set.
- **Adopters named in Schulze's abstracts:** the **Pirate Party of Sweden**, the **Wikimedia Foundation** and the **Debian** project. Longer lists in Schulze's own materials (arXiv 2018; his brief to the Canadian House of Commons ERRE committee, https://ourcommons.ca/Content/Committee/421/ERRE/Brief/BR8397842/br-external/SchulzeMarkus-e.pdf) add, among others, Gentoo, Ubuntu, the Free Software Foundation, GnuPG, OpenStack, Sugar Labs, TopCoder, MTV, the Knight Foundation and several Pirate Parties.
- **Caveat:** I read the abstracts of the arXiv and 2017 versions, not the published SCW 2011 abstract. Check the exact list of adopters in the 2011 paper before quoting it as "listed in Schulze (2011)". I. D. Hill criticized the claims made for the 2003 *Voting Matters* preliminary version (https://votingmatters.org.uk/ISSUE18/I18P1.PDF).

## 8. Moulin (1988): the no-show paradox

- **Abstract:** "every Condorcet consistent method (viz., electing the Condorcet winner when there is one) must generate the paradox among **four or more candidates**". Scoring methods do not generate it. Source: University of Glasgow record, https://eprints.gla.ac.uk/92159
- The precise statement concerns **resolute (single-valued) Condorcet-consistent rules** with **at least 4 alternatives and at least 25 voters**. The 4-alternative bound is tight, because maximin satisfies participation with 3 alternatives.
- Brandt, Geist & Peters (SAT solving) lowered the voter bound to **12** and showed it is optimal: with 11 or fewer voters there are Condorcet-consistent rules that satisfy participation. Sources: arXiv:1602.08063 (https://arxiv.org/pdf/1602.08063v1) and https://ideas.repec.org/a/eee/matsoc/v90y2017icp18-27.html

---

## Verification log (one line per entry)

Legend:
- **[ok]** confirmed by a publisher, index or repository page.
- **[ok*]** confirmed only through a secondary or indirect source; the source is named.
- **[TV]** a field is still to verify (a `note` was added in the .bib).

| Key | Status | Source(s) |
|---|---|---|
| Condorcet1785 | ok | French Ministry of Defence digital library record (Paris, Imprimerie royale, 1785, [2]+CXCI+304 p., 4°): https://bibliotheques-numeriques.defense.gouv.fr/impression/document/437dc2fe-6978-42d8-bcba-2a9134007b1d |
| Arrow1951 | ok | Library catalogues and MR entry: Wiley, New York, 1951, Cowles Commission Monograph 12, xi+99 pp. |
| Gibbard1973 | ok | econometricsociety.org page; Wikipedia/Electowiki give doi:10.2307/1914083 (= JSTOR 1914083) |
| Satterthwaite1975 | TV (DOI) | Kellogg record and RePEc: JET 10(2):187–217, April 1975, with the full subtitle. DOI not shown anywhere |
| Black1948 | ok | DOI 10.1086/256633 confirmed (secondary listings) |
| May1952 | ok | econometricsociety.org; JSTOR stable 1907651 matches the DOI |
| Nakamura1979 | TV (DOI) | Reference lists: IJGT 8(1):55–61. No DOI found |
| Greenberg1979 | TV (DOI) | econometricsociety.org: 47(3), May 1979, 627–636; JSTOR stable 1910410 |
| CaplinNalebuff1988 | ok | econometricsociety.org, RePEc; JSTOR stable 1912699 matches the DOI |
| McKelvey1976 | ok* | DOI taken from Wikipedia ("McKelvey–Schofield chaos theorem"); volume, issue and pages also from RePEc reference lists |
| Plott1967 | TV (DOI) | Caltech Authors record (https://authors.library.caltech.edu/records/rzmbm-kft47), JSTOR stable 1815369. No DOI found |
| Moulin1988noshow | ok | Glasgow eprints record with the DOI |
| GehrleinFishburn1976 | TV (DOI) | RePEc: JET 13(1):14–25, August 1976. DOI not found |
| Gehrlein2006 | ok | Springer: Theory and Decision Library C, vol. 40, DOI 10.1007/3-540-33799-7 |
| Guilbaud1952 | TV (pages) | 5(4), Oct–Dec 1952. Most French citations give pp. 501–584 (e.g. "tome 5, n° 4, 1952 (pp. 501 à 584) P.U.F."). The JEHPS 2008 English translation says pp. 501–551, and Monjardet calls it a "roughly 50-page" paper, which fits 501–551. Not resolved |
| BrandtEtAl2016handbook | ok | Cambridge UP and Duke Scholars: DOI 10.1017/CBO9781107446984 |
| Schulze2011 | ok | RePEc and Schulze's brief: SCW 36(2):267–303, DOI confirmed |
| Tideman1987 | ok / TV (issue) | Springer DOI page: SCW 4:185–206, DOI 10.1007/BF00433944. The issue number (3) was not displayed |
| ZavistTideman1989 | ok / TV (issue) | Springer DOI page: SCW 6:167–173, DOI 10.1007/BF00303170. The issue number was not displayed |
| Kemeny1959 | TV (first page) | Daedalus 88(4), Fall 1959. 577–591 in most lists; LAMSADE gives 575–591 and a CUP reference list gives 571–91. JSTOR item 20026529 is titled "Mathematics without Numbers" |
| YoungLevenglick1978 | ok / TV (issue, pages) | SIAM DOI page (10.1137/0135023, where 0135 = volume 35). Issue and pages not displayed |
| Young1988 | ok | doi.org/10.2307/1961757 (Crossref) and RePEc: APSR 82(4):1231–1244 |
| Young1974 | ok* | RePEc: JET 9(1):43–52, Sept 1974. The DOI is built from the ScienceDirect PII 0022-0531(74)90073-8 shown on IDEAS |
| BartholdiToveyTrick1989hard | ok / TV (issue) | Springer DOI page: SCW 6:157–165, DOI 10.1007/BF00303169 |
| BartholdiToveyTrick1989manip | TV (DOI) | Full-text PDF header "Soc Choice Welfare (1989) 6:227–241"; course slides give 6(3) |
| HollidayPacuit2023splitcycle | ok | RePEc: Public Choice 197(1):1–62, Oct 2023, DOI 10.1007/s11127-023-01042-3 (online 29 Aug 2023). Springer may label the issue "1–2" |
| HollidayPacuit2023stable | ok | RePEc: CPE 34(3):421–433, Sept 2023, DOI 10.1007/s10602-022-09383-9 |
| Fishburn1977 | ok / TV (pages) | SIAM DOI page (10.1137/0133030); the cover shows vol. 33, issue 3. Pages not displayed |
| Smith1973 | ok | econometricsociety.org: 41(6), Nov 1973, 1027–1041; JSTOR 1914033 |
| Simpson1969 | TV (DOI) | RePEc: QJE 83(3):478–490 |
| BrandlBrandtSeedig2016 | ok | econometricsociety.org, RePEc, TUM |
| Fishburn1984 | TV (DOI) | RePEc: RES 51(4):683–692 |
| BramsFishburn1978 | ok | RePEc and Cambridge reference list with DOI 10.2307/1955105 |
| BalinskiLaraki2007 | ok | PNAS 104(21):8720–8725, DOI confirmed |
| BalinskiLaraki2011 | ok, **year differs** | Library catalogues and MAA: MIT Press hardcover, ISBN 978-0-262-01513-4, **(c) 2010**. The e-book (978-0-262-29560-4) is dated 28 Jan 2011; a paperback appeared in 2022. No DOI found |
| FelsenthalMachover2008 | ok | LSE Research Online eprint 24213: Homo Oeconomicus 25(3/4):319–334. No DOI |
| LaslierSanver2010 | ok | Springer: Studies in Choice and Welfare, DOI 10.1007/978-3-642-02839-7 |
| Laslier2012loser | ok | RePEc: pp. 327–351, DOI 10.1007/978-3-642-20441-8_13 |
| Felsenthal2012review | ok | RePEc (h/spr/stcchp/978-3-642-20441-8_3): pp. 19–91 |
| GreenArmytageTidemanCosman2016 | ok | RePEc and the author's page: SCW 46(1):183–212, DOI confirmed. Cosman's first name (Rafael) was not displayed in the sources |
| FaliszewskiProcaccia2010 | TV (DOI) | AGH BaDAP record: AI Magazine 31(4):53–64, 2010 |
| Mallows1957 | ok | Oxford Academic record: Biometrika 44(1–2):114–130, DOI 10.1093/biomet/44.1-2.114 |
| TidemanPlassmann2012 | ok | RePEc: chapter 9, pp. 217–251, DOI 10.1007/978-3-642-20441-8_9 |
| RegenwetterEtAl2006 | TV (DOI) | CUP copyright page: first published 2006, ISBN 978-0-521-82968-7 |
| MatteiWalsh2013 | ok | Springer and the authors' PDF: ADT 2013, LNAI 8176 (an LNCS sub-series), pp. 259–270, DOI confirmed |
| Merrill1984 | ok* | Wikipedia ("Condorcet efficiency") gives the DOI 10.2307/2110786 = JSTOR 2110786 |
| Tideman2006 | ok | Routledge (formerly Ashgate) and catalogues: Aldershot, 2006, ISBN 978-0-7546-4717-1 |
| ElkindFaliszewskiSlinko2015 | ok, **differs** | AGH BaDAP and Oxford ORA: **SCW 45(2):345–377** (online 17 Apr 2015), DOI 10.1007/s00355-015-0892-5 |
| BuchananTullock1962 | ok | Catalogues: Ann Arbor, University of Michigan Press, [1962], x+361 p. |
| Rae1969 | TV (DOI) | Cambridge Core and RePEc: APSR 63(1):40–56 |
| RomerRosenthal1978 | ok* | RePEc gives DOI **10.1007/BF03187594**; JSTOR stable 30023066; Public Choice 33(4):27–43 |
| LaffondLaslierLeBreton1993 | TV (DOI) | RePEc: GEB 5(1):182–201, January 1993 |


---

# Part B


How these were checked: this session could not open publisher pages, arXiv, Crossref or doi.org directly, because the environment's network policy blocked them. The answers below come from web-search extracts of the pages cited (abstracts, repository records and quoted passages) and from the Consensus paper index (abstracts). I mark each claim as one of:
- **[verified]**: seen in the cited source extract.
- **[to verify]**: from my own knowledge of the literature and not confirmed against the source in this session. Check it in the PDF before you quote it.

---

## 1. Moulin (1981, 1982): the proportional veto core

**Setting and veto function.** There are n voters (set N) and m alternatives (set A). The coalition sizes run t = 1..n.
- The proportional veto function is v(T) = ⌈m·t/n⌉ − 1. **[to verify: the exact rounding convention, in Moulin 1982 Sect. 2 / Ianovski–Kondratev Def. 1]**
- The intuition is "x % of the agents can veto x % of the candidates". **[verified, Moulin 1982 abstract]** https://www.econometricsociety.org/publications/econometrica/1982/01/01/voting-proportional-veto-power

**When an alternative is blocked.** A coalition T blocks (vetoes) x if there is a set B ⊆ A with |B| ≥ m − v(T) such that every member of T strictly prefers every b ∈ B to x.
- The proportional veto core is the set of alternatives that no coalition blocks.
- **[verified as restated in Ianovski & Kondratev]**: "a candidate is vetoed if some group of voters ranks at least m − v(T) candidates all better than that candidate". https://arxiv.org/abs/2003.09153

**Nonemptiness.** Moulin showed that the proportional veto core is non-empty for every profile.
- Secondary sources add that proportional veto power is the strongest anonymous veto distribution that keeps the core non-empty. In other words, the core it gives is minimal. **[verified as reported by arXiv:2003.09153 and the IJCAI 2025 approval-ballot paper https://arxiv.org/abs/2505.01395; the precise maximality statement is to verify in Moulin 1982]**

**Implementation (Moulin 1982, Econometrica 50(1)) [verified, abstract]:**
- The paper gives necessary conditions for a *neutral* social choice function to be *partially implementable in strong equilibrium* (that is, implementable by cooperative agents): the veto power of the coalitions must be maximally distributed.
- If the function is also veto-anonymous, a coalition's veto power must be (roughly) proportional to its size.
- "Voting by successive veto" is an example of a neutral, (nearly) veto-anonymous social choice function that is implementable.
- Moulin also proposed a "voting by veto tokens" procedure for selecting an outcome from the core. **[verified as reported by arXiv:2003.09153]**
- The exact form of the 1981 RES theorem (strong-equilibrium outcomes of the veto game and the core) is **[to verify]**. OUP page: https://academic.oup.com/restud/article-abstract/48/3/407/1544724

## 2. Ianovski & Kondratev (AAAI 2021): Computing the proportional veto core

**Abstract [verified]** (https://ojs.aaai.org/index.php/AAAI/article/view/16691, arXiv:2003.09153):
- The naive algorithm for the veto core is exponential.
- The only rules previously known for selecting from the veto core with an arbitrary number of voters violate either anonymity or neutrality.
- The authors give (i) a **polynomial-time algorithm for computing the veto core**, (ii) a **neutral and anonymous algorithm for selecting a candidate from it**, and (iii) a proof that **a pessimist can manipulate the veto core in polynomial time**.

**Algorithm.** Core membership reduces to a bipartite / flow condition of Hall type: a candidate is in the core iff a voter–candidate matching or flow exists that "absorbs" every coalition's veto. The exact flow network and the complexity bound are **[to verify in Sect. 4 of arXiv:2003.09153]**.
- Kizilkaya & Kempe (EC 2023) state independently that the Hall/matching condition "closely mirrors the classical definition of the (proportional) veto core". **[verified, abstract]** https://arxiv.org/abs/2305.19632

**"Veto by consumption" [to verify: the name and the parameters]:**
- This is the neutral and anonymous selection rule of the paper, modelled on probabilistic-serial "eating".
- Each candidate is a unit of equal size (n/m). Every voter "eats" (vetoes) the candidate they currently rank lowest among those not yet eliminated, all voters at the same speed. A candidate is eliminated when it is fully consumed, and its eaters move up to their next-worst remaining candidate.
- The last candidate to be fully consumed is selected.
- Properties: anonymous, neutral, polynomial, always in the proportional veto core.
- The abstract confirms only that the rule is anonymous, neutral and polynomial. The core-membership guarantee and the eating details should be checked in the selection section of the paper.
- Analogue: Kizilkaya–Kempe's continuous rule is the same process with candidate "support" initialised to plurality scores instead of equal sizes. **[verified, their abstract]**

## 3. Kondratev & Ianovski (AAMAS 2024): Veto core consistent preference aggregation

**[verified, abstract]** https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p1020.pdf
- Proportional veto principle: "a coalition of x% of the voters should be able to block roughly x% of the outcomes". This is contrasted with the majority and utilitarian principles.
- The paper analyses **two broad families of veto-core-consistent rules and six concrete examples** against **monotonicity, participation, and independence of unanimous losers**.
- Which rule satisfies which property is **[to verify in the paper's summary table]**. The search extracts did not include the results table.

**Incompatibility with Condorcet consistency.** This is my own check, valid for any n large enough.
- Take m = 3 with 51 % of voters x≻y≻z and 49 % y≻z≻x.
- x is the Condorcet winner.
- The 49 % coalition has v = ⌈3·0.49⌉ − 1 = 1 and unanimously ranks m − v = 2 alternatives above x, so x is vetoed.
- Hence no rule can be both Condorcet-consistent and veto-core-consistent.

**Journal version:** none found as of October 2026. Later papers (e.g. IJCAI 2025) still cite the AAMAS version.

## 4. Kondratev & Nesterov (2020): Measuring majority power and veto power

**[verified, abstract]** https://link.springer.com/doi/10.1007/s11127-019-00697-1, arXiv:1811.06739
- **Majority power** is the minimal share of voters that guarantees a victory to one of the majority's most-preferred candidates.
- **Veto power** is the minimal share of voters that allows a minority to veto each of their least-preferred candidates.
- The authors give tight bounds on these shares for common rules and order the rules.
  - **Instant-runoff voting has both the highest majority power and the highest veto power; plurality has the lowest.**
  - "In general, the greater is the majority power of a voting rule, the greater its veto power."
  - The three exceptions are **voting with proportional veto power, Black's rule and Borda's rule**: weak majority power and strong veto power, so they protect minorities.

**Formal criteria [to verify, Defs. in arXiv:1811.06739]:**
- *q-majority*: if more than a share q of voters rank the same k candidates (in any order) at the top, one of them wins.
- *q-veto*: if more than a share q rank the same k candidates at the bottom, none of them wins.
- These are stated for every k, so the thresholds may depend on k and m.

The exact numeric thresholds per rule (Condorcet-consistent rules, Borda, plurality, etc.) are in the paper's tables and were **not** retrieved.

## 5. Mueller (1978): Voting by veto

**[verified, abstract]** https://www.sciencedirect.com/science/article/abs/pii/0047272778900051
1. Each of the n committee members makes one proposal. The status quo is added, giving an issue set of n+1 alternatives.
2. After a **random draw of the voting order**, each member in turn eliminates (vetoes) one alternative from the issue set.
3. The remaining alternative wins.

Properties:
- For any set of proposals and any order, the procedure yields a unique winner.
- Its incentives push the winning proposal towards an equal sharing of the gains from collective action.
- No voter gets their worst outcome. **[verified, via arXiv:2003.09153]**
- The procedure is **not anonymous** (the order matters) and requires #alternatives = #voters + 1. **[verified, via arXiv:2003.09153]**
- It is decisive and neutral. **[verified, Sauermann (2017) chapter abstract]**
- Extensions: Moulin (1983), with an arbitrary number of vetoes per voter; Felsenthal & Machover (1992). **[verified]**

## 6. Brams & Kilgour (2001): Fallback bargaining

**[verified, abstract]** https://link.springer.com/article/10.1023/A:1011252808608
- **Fallback bargaining (FB).** Bargainers report preference rankings. They then "fall back, in lockstep, to less and less preferred alternatives (first choices, then adding second choices, and so on) until an alternative is found on which all bargainers agree". That alternative is the outcome. A rule other than unanimity (a q-quota) may give a different outcome.
- **Properties.**
  - The outcome is **always Pareto-optimal** but need not be unique.
  - Under unanimity it is "at least middling in everybody's ranking".
  - It may fail to select a Condorcet alternative, or even a majority's first choice.
  - It **maximises the bargainers' minimum "satisfaction"**, i.e. it is the maximin-rank outcome.
- **FB with impasse.** Bargainers may place "impasse" in their ranking, below which they will not descend because they prefer no agreement to any lower alternative. The impasse itself can become the outcome, foreclosing any agreement.
- **Manipulation.** The authors analyse it through best responses and Nash equilibria. A Chicken-type risk of a mutually worst outcome may deter misreporting.

## 7. Sertel's Majoritarian Compromise (MC)

**Definition [to verify, Sertel & Yılmaz 1999 Sect. 2 / Hurwicz & Sertel 1999].** MC was introduced in Sertel (1986), Boğaziçi lecture notes. **[verified]**
- For k = 1, 2, …, look at each voter's top-k set. Stop at the smallest k at which some alternative is in the top-k of a (strict) majority of voters.
- Select the alternative(s) with the largest such support at that k. This is the same as Bucklin's rule; residual ties are broken by the rule's tie-breaking convention.

**Properties [verified, abstract]** https://link.springer.com/doi/10.1007/s003550050164
- MC is Pareto-optimal and satisfies SNIP: it never chooses a strict majority's worst candidate.
- It is "majoritarian approving": it always picks an alternative that some majority places in the better "effective" half. Hence it is "majoritarian-optimal".
- It is **not Maskin-monotonic**, so not Nash-implementable, but it is **subgame-perfect implementable** on strict profiles.
- It is compared with consistency and Condorcet-consistency. That it fails Condorcet-consistency, as Bucklin does, is **[to verify in Sect. 4]**.

## 8. Debian Constitution: how a vote is counted

**Version.** The current text is **v1.9, ratified 26 March 2022** (v1.8 was ratified 28 January 2022). No later version was found as of October 2026. **[verified]** https://www.debian.org/devel/constitution
- The 2021 GR "Change the resolution process" (vote 2021-003, voted Jan. 2022, passed with 3:1) renamed old §A.6 to **§A.5 Vote Counting** and made **"None of the above"** the default option of a GR. **[verified]** https://www.debian.org/vote/2021/vote_003

**Counting steps (§A.5) [verified wording, as quoted from the current page]:**
1. Ballots rank the options; ties are allowed.
2. *Quorum.* If the ballot has a quorum R, any non-default option that does not receive at least R votes ranking it above the default option is dropped.
3. *Majority ratio vs. default.* "Any (non-default) option which does not defeat the default option by its required majority ratio is dropped". A defeats the default D by ratio N iff V(A,D) ≥ N·V(D,A) **and** V(A,D) > V(D,A). This wording dates from the 2015 GR, https://www.debian.org/vote/2015/vote_003. "If a supermajority of S:1 is required for A, its majority ratio is S; otherwise, its majority ratio is 1."
4. *Pairwise defeats* among the remaining options: A defeats B iff V(A,B) > V(B,A).
5. Take the transitive defeats and form the **Schwartz set**: "An option A is in the Schwartz set if for all options B, either A transitively defeats B, or B does not transitively defeat A".
6. *Drop the weakest defeats.* "If there are defeats between options in the Schwartz set, we drop the weakest such defeats from the list of pairwise defeats" and return to step 5. Weakness is measured by V(A,X), with a tie-break on V(X,A). This is the Schulze / "Cloneproof Schwartz Sequential Dropping" method, adopted in 2003: https://www.debian.org/vote/2003/vote_0002
7. *Final tie.* The winner comes from the Schwartz set with no defeats. If several options remain, the current text has the winner "randomly chosen from those options, via a mechanism chosen by the Project Secretary". Older versions used the casting vote. **[verified snippet; exact placement of this sentence (§A.5.9 vs. a body section) to verify]**
- Note in §A.5: options ranked above the default are those a voter finds *acceptable*; options below it are *unacceptable*. **[verified]**

**Quorum and supermajorities:**
- Q = half the square root of the number of current Developers. A GR quorum is **3Q**. **[verified in v1.1–v1.7 texts; same in v1.9 to verify]**
- Constitutional amendments (and foundation documents) need **3:1**. Overriding a Technical Committee decision needs **2:1**. **[verified for v1.7; v1.9 to verify]**
- Supermajorities apply only in step 3, as the ratio an option must reach against the default ("None of the above"). An option that fails it is dropped before the Schwartz/Schulze stage, so it is "defeated by the default".

## 9. RFC 7282 (Resnick 2014): rough consensus

**[verified headings]** https://www.rfc-editor.org/rfc/rfc7282
- §2 is titled **"Lack of disagreement is more important than agreement"**.
- §3 is titled **"Rough consensus is achieved when all issues are addressed, but not necessarily accommodated"**.

**Key idea.** Consensus is not unanimity or majority. The test is whether every objection has been *addressed*: answered and either accommodated or judged unpersuasive by the chair. It is not whether everyone agrees.

**Quotes:**
- End of §2 [verified fragments]: "...comes to the conclusion that either the objections are valid, and therefore make a change to address the objection, or that the objection was not really a matter of importance, but merely a matter of taste. ... That's why in the IETF, we talk about 'rough consensus'."
- Widely quoted from the RFC [verified as quoted on RIPE lists; **section number to verify, probably §2**]: "consensus is when everyone is sufficiently satisfied with the chosen solution, such that they no longer have specific objections to it."
- §3 example [verified paraphrase]: the chair judges "that the consensus is rough, in that there is still an objector, but the issue has been addressed."

## 10. TEU Art. 16(4): qualified majority and blocking minority

**[verified text, as reproduced at]** https://www.legislation.gov.uk/eut/teu/article/16 and consistent with https://www.consilium.europa.eu/en/council-eu/voting-system/qualified-majority/:
- Wording: "As from 1 November 2014, a qualified majority shall be defined as at least 55 % of the members of the Council, comprising at least fifteen of them and representing Member States comprising at least 65 % of the population of the Union."
- Blocking minority: "A blocking minority must include at least four Council members, failing which the qualified majority shall be deemed attained."
- Effect: with fewer than four members against, the population criterion is irrelevant. An abstention counts as a vote against. **[verified, Council site]**
- When the Council does not act on a Commission (or High Representative) proposal, the reinforced QMV of Art. 238(2) TFEU applies: 72 % of members representing 65 % of the population. **[verified, EUR-Lex glossary]**
- The OJ C 202, 7.6.2016 edition itself was not opened. Page numbers and the CELEX URL are **[to verify]**.

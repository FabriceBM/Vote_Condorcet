"""Voting rules for one decision with open proposals, full ballots and veto rights.

An election has n voters and m options (the status quo, when there is one, is an option like the others).
Each voter gives:
    U[i, x]    a utility, of which only the order matters (ties allowed): the ranking of all options;
    acc[i, x]  True if option x is acceptable to voter i, False if i vetoes it. The veto is a line drawn in
               the ranking: in the cultures and examples of this project, an option is never vetoed by a voter
               who accepts an option ranked below it;
    G[i, x]    a grade 0-5 (0 = reject, the veto), used by Majority Judgment only.

Every rule returns the set of tied winners (sorted indices). `resolve` breaks ties the same way for every
rule: fewest vetoes, then the Schulze winner among the tied options, then the lowest index (options are in
random order in the simulations). Both criteria are independent of clones, so the tie-break does not undo
that property of the rules that have it. Rules that can end without a decision (unanimity with the status quo as default, fallback
bargaining with impasse) return the status quo and set `Outcome.deadlock`.

The rule proposed in the note is QVC(theta), "Condorcet with a blocking quota": exclude every option vetoed
by at least a share theta of the voters; if that excludes every option, keep the least-vetoed ones; choose
the Schulze winner among the options left.

Run from the repository root:
    python3 simulations/python/voting.py --check     # brute-force and textbook checks of the rules
"""
import itertools
import os
import sys
from dataclasses import dataclass, field

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

OUT = os.environ.get("TAB_DIR", "outputs/tables")
CHAR_WIDTH = 0.0105                      # width of a character of a \small table, share of \linewidth


# ---------------------------------------------------------------------------------------------------------
#  Elections
# ---------------------------------------------------------------------------------------------------------
@dataclass
class Election:
    U: np.ndarray                        # (n, m) utilities; only the order within a row matters
    acc: np.ndarray                      # (n, m) True = acceptable, False = vetoed
    sq: int | None = None                # index of the status quo, if any
    G: np.ndarray | None = None          # (n, m) grades 0-5 for Majority Judgment; derived if None
    names: list | None = None            # option labels (examples only)
    cache: dict = field(default_factory=dict, repr=False)

    @property
    def n(self):
        return self.U.shape[0]

    @property
    def m(self):
        return self.U.shape[1]

    def N(self):
        """N[x, y] = number of voters who strictly prefer x to y."""
        if "N" not in self.cache:
            self.cache["N"] = (self.U[:, :, None] > self.U[:, None, :]).sum(0)
        return self.cache["N"]

    def vetoes(self):
        """Number of voters who veto each option."""
        if "v" not in self.cache:
            self.cache["v"] = (~self.acc).sum(0)
        return self.cache["v"]

    def ranks(self):
        """r[i, x] = 1 + number of options voter i strictly prefers to x (ties share the best rank)."""
        if "r" not in self.cache:
            self.cache["r"] = 1 + (self.U[:, None, :] > self.U[:, :, None]).sum(2)
        return self.cache["r"]

    def grades(self):
        """Grades 0-5: 0 for a vetoed option; acceptable options graded 1-5 by their rank among the voter's
        acceptable options (used when a culture gives no grades)."""
        if self.G is not None:
            return self.G
        if "G" not in self.cache:
            G = np.zeros(self.U.shape, dtype=int)
            for i in range(self.n):
                ok = np.flatnonzero(self.acc[i])
                if len(ok) == 0:
                    continue
                below = (self.U[i, ok][None, :] < self.U[i, ok][:, None]).sum(1)  # acceptable options below
                G[i, ok] = 1 + np.floor(4.999 * below / max(len(ok) - 1, 1)).astype(int)
            self.cache["G"] = G
        return self.cache["G"]

    def with_ballots(self, rows, U_rows, acc_rows, G_rows=None):
        """A copy in which the voters `rows` cast other ballots (strategic voting)."""
        U, acc = self.U.copy(), self.acc.copy()
        U[rows], acc[rows] = U_rows, acc_rows
        G = None
        if self.G is not None:
            G = self.G.copy()
            G[rows] = G_rows
        return Election(U, acc, self.sq, G, self.names)


@dataclass
class Outcome:
    winner: int
    tied: list
    deadlock: bool = False               # the status quo stays because nothing could pass
    fallback: bool = False               # QVC: every option was vetoed by the quota, least-vetoed kept


def borda(e):
    """Borda score, ties counted half: sum over y of (n + N[x,y] - N[y,x]) / 2."""
    N = e.N()
    return (e.n + N - N.T).sum(1) / 2 - e.n / 2


def resolve(e, tied, **flags):
    """One winner from a set of tied winners: fewest vetoes, then the Schulze winner among the tied options
    still in, then the lowest index."""
    tied = sorted(int(x) for x in tied)
    v = e.vetoes()
    left = [x for x in tied if v[x] == min(v[tied])]
    if len(left) > 1:
        left = schulze(e, left)
    return Outcome(min(left), tied, **flags)


def argmax_set(score, among=None):
    idx = np.arange(len(score)) if among is None else np.asarray(among)
    s = np.asarray(score)[idx]
    return list(idx[np.isclose(s, s.max())])


# ---------------------------------------------------------------------------------------------------------
#  Majority graphs on a subset of options
# ---------------------------------------------------------------------------------------------------------
def _widest(P):
    """Widest-path (max-min) strengths by Floyd-Warshall; P[x, y] = 0 when there is no edge."""
    P = P.astype(float).copy()
    for k in range(P.shape[0]):
        P = np.maximum(P, np.minimum(P[:, k:k + 1], P[k:k + 1, :]))
    return P


def schulze(e, among=None):
    """Schulze (2011) winners on the options `among`, link strength = winning votes."""
    idx = np.arange(e.m) if among is None else np.asarray(sorted(among))
    D = e.N()[np.ix_(idx, idx)]
    P = _widest(np.where(D > D.T, D, 0))
    np.fill_diagonal(P, 0)
    return [int(idx[a]) for a in range(len(idx)) if (P[a] >= P[:, a]).all()]


def split_cycle(e, among=None):
    """Split Cycle (Holliday and Pacuit, 2023): x defeats y if its margin over y exceeds the strength of the
    strongest path from y back to x (margins); the winners are the undefeated options."""
    idx = np.arange(e.m) if among is None else np.asarray(sorted(among))
    D = e.N()[np.ix_(idx, idx)]
    M = D - D.T
    W = _widest(np.where(M > 0, M, 0))
    defeated = (M > 0) & (M > W.T)                      # defeated[x, y]: x defeats y
    return [int(idx[b]) for b in range(len(idx)) if not defeated[:, b].any()]


def ranked_pairs(e, among=None):
    """Ranked Pairs (Tideman, 1987): lock majorities from the strongest (winning votes, then margin) unless
    they close a cycle; equal majorities taken in index order."""
    idx = np.arange(e.m) if among is None else np.asarray(sorted(among))
    D = e.N()[np.ix_(idx, idx)]
    k = len(idx)
    pairs = [(a, b) for a in range(k) for b in range(k) if D[a, b] > D[b, a]]
    pairs.sort(key=lambda p: (-D[p], -(D[p] - D[p[::-1]]), p))
    locked = np.zeros((k, k), dtype=bool)
    for a, b in pairs:
        reach, todo = {b}, [b]                          # can b already reach a?
        while todo:
            c = todo.pop()
            for d in np.flatnonzero(locked[c]):
                if d not in reach:
                    reach.add(d)
                    todo.append(d)
        if a not in reach:
            locked[a, b] = True
    return [int(idx[a]) for a in range(k) if not locked[:, a].any()]


def condorcet_winner(e, among=None):
    idx = np.arange(e.m) if among is None else np.asarray(sorted(among))
    D = e.N()[np.ix_(idx, idx)]
    for a in range(len(idx)):
        if all(D[a, b] > D[b, a] for b in range(len(idx)) if b != a):
            return int(idx[a])
    return None


def smith_set(e, among=None):
    """Smallest non-empty set of options that each beat or tie every option outside it."""
    idx = np.arange(e.m) if among is None else np.asarray(sorted(among))
    D = e.N()[np.ix_(idx, idx)]
    reach = D >= D.T                                    # x beats or ties y
    for k in range(len(idx)):
        reach |= reach[:, k:k + 1] & reach[k:k + 1, :]  # transitive closure
    # the Smith set is the set of options that reach every option through "beats or ties"
    return [int(idx[a]) for a in range(len(idx)) if reach[a].all()]


# ---------------------------------------------------------------------------------------------------------
#  Rules without veto
# ---------------------------------------------------------------------------------------------------------
def plurality(e):
    top = e.U == e.U.max(1, keepdims=True)
    return argmax_set((top / top.sum(1, keepdims=True)).sum(0))


def borda_rule(e):
    return argmax_set(borda(e))


def irv(e):
    """Instant-runoff: eliminate the option with the fewest first preferences (ties: lowest Borda score, then
    highest index) until one has a majority of the ballots."""
    alive = list(range(e.m))
    b = borda(e)
    while True:
        U = e.U[:, alive]
        top = U == U.max(1, keepdims=True)
        first = (top / top.sum(1, keepdims=True)).sum(0)
        if first.max() > e.n / 2 or len(alive) == 1:
            return [alive[int(np.argmax(first))]]
        loser = min(range(len(alive)), key=lambda k: (first[k], b[alive[k]], -alive[k]))
        alive.pop(loser)


def approval(e):
    return argmax_set(e.acc.sum(0))


def majority_judgment(e):
    """Majority Judgment (Balinski and Laraki, 2007) with the majority gauge: the lower median grade, then
    +p if the share p of grades above it exceeds the share q below it, else -q."""
    G = e.grades()
    med = np.sort(G, 0)[(e.n - 1) // 2]
    p, q = (G > med).mean(0), (G < med).mean(0)
    gauge = np.where(p > q, p, -q)
    best = [x for x in range(e.m) if med[x] == med.max()]   # highest median grade, then highest gauge
    return argmax_set(gauge, best)


def copeland(e):
    N = e.N()
    return argmax_set((N > N.T).sum(1) + 0.5 * ((N == N.T).sum(1) - 1))


def minimax(e):
    """Simpson-Kramer: the smallest largest defeat, margins."""
    N = e.N()
    M = N.T - N
    np.fill_diagonal(M, np.iinfo(M.dtype).min)
    return argmax_set(-M.max(1))


def schulze_rule(e):
    return schulze(e)


def split_cycle_rule(e):
    return split_cycle(e)


def ranked_pairs_rule(e):
    return ranked_pairs(e)


# ---------------------------------------------------------------------------------------------------------
#  Compromise rules
# ---------------------------------------------------------------------------------------------------------
def fallback_bargaining(e, impasse=False):
    """Brams and Kilgour (2001): every voter descends their ranking one level at a time; the first options
    reached by all voters win (ties: highest Borda score, in `resolve`). With impasse, a voter never goes
    below the options they find acceptable; if no option is acceptable to all, nothing passes."""
    r = e.ranks()
    ok = e.acc if impasse else np.ones_like(e.acc)
    for k in range(1, e.m + 1):
        support = ((r <= k) & ok).sum(0)
        if support.max() == e.n:
            return list(np.flatnonzero(support == e.n))
    return None                                          # impasse


def majoritarian_compromise(e):
    """Sertel: descend level by level until some option is in the top k of more than half of the voters;
    among those, the most supported at that level."""
    r = e.ranks()
    for k in range(1, e.m + 1):
        support = (r <= k).sum(0)
        if support.max() > e.n / 2:
            return argmax_set(support)
    return list(range(e.m))


def sequential_veto(e, order=None):
    """Voting by veto (Mueller, 1978), sincere: voters in turn strike their least preferred remaining option
    until one is left."""
    alive = list(range(e.m))
    order = list(range(e.n)) if order is None else order
    k = 0
    while len(alive) > 1:
        i = order[k % len(order)]
        worst = min(alive, key=lambda x: (e.U[i, x], -x))
        alive.remove(worst)
        k += 1
    return alive


# ---------------------------------------------------------------------------------------------------------
#  Veto rules
# ---------------------------------------------------------------------------------------------------------
def unanimity(e):
    """Unanimity with the status quo as default (Wicksell): a proposal passes only if every voter prefers it
    to the status quo; among those that pass, the Schulze winner; if none passes, the status quo stays."""
    sq = e.sq
    passing = [x for x in range(e.m) if x != sq and (e.U[:, x] > e.U[:, sq]).all()]
    if not passing:
        return None
    return schulze(e, passing)


def qvc(e, theta):
    """Condorcet with a blocking quota, QVC(theta): options vetoed by at least theta * n voters are excluded;
    if all are, the least-vetoed are kept (fallback); Schulze winner among the options kept.
    theta = 1/n: any single veto excludes (consensus with individual veto, plus the fallback)."""
    v = e.vetoes()
    admissible = np.flatnonzero(v < theta * e.n - 1e-9)
    fell_back = len(admissible) == 0
    if fell_back:
        admissible = np.flatnonzero(v == v.min())
    return schulze(e, admissible), fell_back


def pvc_member(e, x):
    """Is x in the proportional veto core (Moulin, 1981)? A coalition T can veto ceil(m|T|/n) - 1 options;
    x is blocked if some T unanimously prefers at least m - that many options to x. Equivalently (Hall's
    condition), x is in the core iff for every coalition T the options that some member of T ranks at or below
    x number at least m|T|/n: a max-flow test, source -> voter (m) -> options weakly below x (inf) ->
    sink (n), saturated iff x is in the core (Ianovski and Kondratev, 2021)."""
    n, m = e.n, e.m
    W = e.U <= e.U[:, [x]]                              # W[i, y]: i ranks y at or below x
    src, sink = 0, n + m + 1
    rows, cols, cap = [], [], []
    for i in range(n):
        rows.append(src); cols.append(1 + i); cap.append(m)
        for y in np.flatnonzero(W[i]):
            rows.append(1 + i); cols.append(1 + n + y); cap.append(m * n)
    for y in range(m):
        rows.append(1 + n + y); cols.append(sink); cap.append(n)
    g = csr_matrix((np.array(cap, dtype=np.int32), (rows, cols)), shape=(n + m + 2, n + m + 2))
    return maximum_flow(g, src, sink).flow_value == m * n


def pvc(e):
    if "pvc" not in e.cache:
        e.cache["pvc"] = [x for x in range(e.m) if pvc_member(e, x)]
    return e.cache["pvc"]


def pvc_member_bruteforce(e, x):
    """Definition of the proportional veto core, by enumeration of coalitions (small n only)."""
    n, m = e.n, e.m
    better = e.U > e.U[:, [x]]                          # better[i, y]: i strictly prefers y to x
    for t in range(1, n + 1):
        veto = -(-m * t // n) - 1
        for T in itertools.combinations(range(n), t):
            if better[list(T)].all(0).sum() >= m - veto:
                return False
    return True


# ---------------------------------------------------------------------------------------------------------
#  All rules, by name
# ---------------------------------------------------------------------------------------------------------
def run(e, rule):
    """Outcome of a rule (by name) on an election."""
    if rule == "Unanimity":
        w = unanimity(e)
        return resolve(e, [e.sq], deadlock=True) if w is None else resolve(e, w)
    if rule == "Fallback (impasse)":
        w = fallback_bargaining(e, impasse=True)
        return resolve(e, [e.sq], deadlock=True) if w is None else resolve(e, w)
    if rule.startswith("QVC"):
        theta = QVC_THETAS[rule]
        w, fb = qvc(e, 1 / e.n if theta == "1/n" else theta)
        return resolve(e, w, fallback=fb)
    if rule == "PVC + Schulze":
        return resolve(e, schulze(e, pvc(e)))
    return resolve(e, SIMPLE[rule](e))


SIMPLE = {
    "Plurality": plurality,
    "Borda": borda_rule,
    "IRV": irv,
    "Approval": approval,
    "Majority Judgment": majority_judgment,
    "Copeland": copeland,
    "Minimax": minimax,
    "Schulze": schulze_rule,
    "Ranked Pairs": ranked_pairs_rule,
    "Split Cycle": split_cycle_rule,
    "Fallback": fallback_bargaining,
    "Majoritarian compromise": majoritarian_compromise,
    "Sequential veto": sequential_veto,
}
QVC_THETAS = {"QVC individual": "1/n", "QVC 10%": 0.10, "QVC 25%": 0.25, "QVC 33%": 1 / 3, "QVC 50%": 0.50}
RULES = (["Plurality", "IRV", "Borda", "Approval", "Majority Judgment", "Copeland", "Minimax", "Schulze",
          "Ranked Pairs", "Split Cycle", "Fallback", "Fallback (impasse)", "Majoritarian compromise",
          "Sequential veto", "Unanimity", "PVC + Schulze"] + list(QVC_THETAS))


# ---------------------------------------------------------------------------------------------------------
#  Tables
# ---------------------------------------------------------------------------------------------------------
def write_table(name, header, rows, title, notes, source, script="simulations/python/voting.py",
                long_share=None, size="small"):
    """Write outputs/tables/<name>.csv and .tex, in the caption style of the note: a short title in the
    caption; under the table (\\tabnotes, manuscript/preamble/macros.tex) the notes (what the rows and
    columns are, sample, method) and the source (the simulation, and the script that computed the table)."""
    import csv
    os.makedirs(OUT, exist_ok=True)
    data_rows = [r for r in rows if r != "midrule"]     # "midrule" draws a rule in the TeX table only
    with open(os.path.join(OUT, f"{name}.csv"), "w", newline="", encoding="utf8") as fh:
        wr = csv.writer(fh)
        wr.writerow(header)
        wr.writerows(data_rows)
    tex_script = os.path.basename(script).replace("_", "\\_")
    with open(os.path.join(OUT, f"{name}.tex"), "w", encoding="utf8") as fh:
        fh.write(f"% Generated by {script} -- do not edit by hand\n")
        fh.write(f"\\begin{{table}}[htbp]\\centering\\{size}\n")
        if size == "footnotesize":
            fh.write("\\setlength{\\tabcolsep}{4pt}\n")
        fh.write(f"\\caption{{{title}}}\\label{{tab:{name}}}\n")
        n_long = sum(len(h) > 6 for h in header[1:])
        share = long_share or 0.62 - 0.04 * (len(header) - 1 - n_long)
        cap = share / max(n_long, 1)
        char_width = CHAR_WIDTH * (0.88 if size == "footnotesize" else 1.0)

        def spec(k):
            h = header[k]
            if len(h) <= 6:
                return "r"
            chars = max([len(str(r[k])) for r in data_rows if k < len(r)] + [max(map(len, h.split())), -(-len(h) // 2)])
            return f">{{\\raggedleft\\arraybackslash}}p{{{min(cap, char_width * chars + 0.015):.3f}\\linewidth}}"
        fh.write("\\sbox{\\tabbox}{\\begin{tabular}{l" + "".join(spec(k) for k in range(1, len(header)))
                 + "}\n\\toprule\n")
        fh.write(" & ".join(header).replace("%", "\\%") + " \\\\\n\\midrule\n")
        for r in rows:
            if r == "midrule":
                fh.write("\\midrule\n")
                continue
            fh.write(" & ".join(str(v) for v in r).replace("%", "\\%") + " \\\\\n")
        fh.write("\\bottomrule\n\\end{tabular}}\n\\usebox{\\tabbox}\n")
        fh.write(f"\\tabnotes{{{notes}}}\n{{{source}; \\texttt{{{tex_script}}}.}}\n\\end{{table}}\n")


# ---------------------------------------------------------------------------------------------------------
#  Checks
# ---------------------------------------------------------------------------------------------------------
def random_election(rng, n, m, ties=False):
    U = rng.integers(0, 4, (n, m)).astype(float) if ties else rng.random((n, m))
    tau = rng.uniform(0.2, 0.6, (n, 1)) * (3 if ties else 1)
    return Election(U, U >= tau, sq=0)


def check(reps=400, seed=1):
    """Brute-force and textbook checks of the rules."""
    rng = np.random.default_rng(seed)
    ok = True

    def report(name, bad, total):
        nonlocal ok
        ok &= bad == 0
        print(f"  {name:<62} {'ok' if bad == 0 else f'FAILED in {bad} of {total}'}")

    # 1. proportional veto core: max-flow test against the definition (small n), and non-emptiness
    bad = empty = 0
    for _ in range(reps):
        e = random_election(rng, int(rng.integers(2, 8)), int(rng.integers(2, 7)), ties=rng.random() < 0.3)
        flow = [x for x in range(e.m) if pvc_member(e, x)]
        brute = [x for x in range(e.m) if pvc_member_bruteforce(e, x)]
        bad += flow != brute
        empty += len(flow) == 0
    report("PVC: max-flow test = definition by enumeration", bad, reps)
    report("PVC: never empty (Moulin, 1981)", empty, reps)

    # 2. Condorcet consistency, Smith, Pareto of the majority rules; Schulze widest paths vs path enumeration
    bad_cw = bad_smith = bad_pareto = bad_paths = 0
    for _ in range(reps):
        e = random_election(rng, int(rng.integers(3, 30)), int(rng.integers(2, 7)), ties=rng.random() < 0.3)
        cw, smith = condorcet_winner(e), set(smith_set(e))
        N = e.N()
        for f in (schulze, split_cycle, ranked_pairs):
            w = f(e)
            if cw is not None and w != [cw]:
                bad_cw += 1
            if not set(w) <= smith:
                bad_smith += 1
            dominated = [x for x in w for y in range(e.m)
                         if (e.U[:, y] >= e.U[:, x]).all() and (e.U[:, y] > e.U[:, x]).any()]
            bad_pareto += len(dominated) > 0
        # Schulze strengths by enumerating simple paths
        D = np.where(N > N.T, N, 0)
        P = _widest(D)
        for a, b in itertools.permutations(range(e.m), 2):
            best = 0
            for k in range(0, e.m - 1):
                for mid in itertools.permutations([c for c in range(e.m) if c not in (a, b)], k):
                    path = (a, *mid, b)
                    best = max(best, min(D[path[j], path[j + 1]] for j in range(len(path) - 1)))
            bad_paths += best != P[a, b]
    report("Schulze, Split Cycle, Ranked Pairs elect the Condorcet winner", bad_cw, 3 * reps)
    report("... and choose within the Smith set", bad_smith, 3 * reps)
    report("... and never a Pareto-dominated option", bad_pareto, 3 * reps)
    report("Schulze: Floyd-Warshall strengths = enumeration of paths", bad_paths, reps)

    # 3. textbook examples
    # the classic 45-voter, five-option example of the Schulze method (e.g. the Wikipedia article): winner E
    ballots = [(5, "ACBED"), (5, "ADECB"), (8, "BEDAC"), (3, "CABED"), (7, "CAEBD"), (2, "CBADE"),
               (7, "DCEBA"), (8, "EBADC")]
    rows = []
    for k, order in ballots:
        rows += [[5 - order.index(c) for c in "ABCDE"]] * k
    e = Election(np.array(rows, float), np.ones((45, 5), bool))
    report("Schulze method, classic 45-voter example: winner E", schulze(e) != [4], 1)
    # Condorcet cycle of three: Schulze breaks it at the weakest link
    e = Election(np.array([[3, 2, 1]] * 35 + [[1, 3, 2]] * 33 + [[2, 1, 3]] * 32, float), np.ones((100, 3), bool))
    report("Cycle 35 ABC / 33 BCA / 32 CAB: Schulze elects A", schulze(e) != [0], 1)
    report("... Split Cycle elects A", split_cycle(e) != [0], 1)

    # 4. properties of QVC proved in the note (Propositions 4-6), on random elections
    bad_dec = bad_acc = bad_cw = bad_clone = 0
    for _ in range(reps):
        e = random_election(rng, int(rng.integers(3, 40)), int(rng.integers(2, 8)))
        theta = rng.choice([1 / e.n, 0.1, 0.25, 1 / 3, 0.5])
        w, fb = qvc(e, theta)
        bad_dec += len(w) == 0
        v = e.vetoes()
        if (v < theta * e.n).any() and not all(v[x] < theta * e.n for x in w):
            bad_acc += 1
        adm = np.flatnonzero(v < theta * e.n - 1e-9)
        cw = condorcet_winner(e, adm) if len(adm) else None
        if cw is not None and w != [cw]:
            bad_cw += 1
        # clone: copy a random option with a tiny perturbation that keeps it next to the original in every
        # ranking and with the same veto marks; the winner must not change, up to the clone set
        x = int(rng.integers(e.m))
        eps = 1e-9 * rng.random(e.n)
        e2 = Election(np.c_[e.U, e.U[:, x] - eps], np.c_[e.acc, e.acc[:, x]], sq=0)
        w2, _ = qvc(e2, theta)
        bad_clone += {y if y < e.m else x for y in w2} != set(w)
    report("QVC: always decides (Proposition 4)", bad_dec, reps)
    report("QVC: winner vetoed by fewer than theta*n if any option is (Prop. 5)", bad_acc, reps)
    report("QVC: Condorcet winner of the admissible options wins (Prop. 6)", bad_cw, reps)
    report("QVC: independent of clones that share veto marks (Prop. 7)", bad_clone, reps)
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        print("Checks of the voting rules")
        sys.exit(0 if check() else 1)
    print(__doc__)

"""Monte Carlo study of the note: the rules of voting.py on the random elections of cultures.py.

Every election is drawn from its own seed (SEED, culture, index), so that results do not depend on the
number of processes. Each table is written to outputs/tables/ (.csv and .tex, label tab:<name>):

    cw_probability    probability that a Condorcet winner exists, by culture and number of options
    perf_<culture>    each rule on 2,000 elections (101 voters, 8 options including the status quo):
                      Condorcet efficiency, utility and worst-off efficiency, acceptance, contest, deadlock
    manipulability    share of elections that a coalition can manipulate with simple strategies
    clones            share of elections whose outcome changes when an option is cloned
    theta_sweep       QVC(theta) for theta from 1/n to 1 (no veto): the trade-off, drawn by figures.py
    deadlock_n        unanimity with the status quo as default against QVC, as the assembly grows

Run from the repository root:
    python3 simulations/python/experiments.py            # all tables (about 15 minutes on 4 cores)
    python3 simulations/python/experiments.py --quick    # a tenth of the elections, for development
    python3 simulations/python/experiments.py --check    # checks against known results (below)
"""
import math
import os
import sys
from multiprocessing import Pool

import numpy as np
from scipy.spatial import Delaunay

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cultures import CULTURES, LABELS, add_clones, draw          # noqa: E402
from voting import RULES, Election, condorcet_winner, run, write_table   # noqa: E402

SEED = 20261021
N_VOTERS, N_OPTIONS = 101, 8
REPS = {"perf": 2000, "manip": 500, "clones": 1000, "theta": 1000, "theta_manip": 300, "cw": 4000,
        "deadlock": 1000}
SCRIPT = "simulations/python/experiments.py"
SOURCE = "Monte Carlo simulation, cultures of \\texttt{cultures.py}, rules of \\texttt{voting.py}"
GROUPS = [["Plurality", "IRV", "Borda", "Copeland", "Minimax", "Schulze", "Ranked Pairs", "Split Cycle"],
          ["Approval", "Majority Judgment"],
          ["Fallback", "Fallback (impasse)", "Majoritarian compromise", "Sequential veto"],
          ["Unanimity", "PVC + Schulze", "QVC individual", "QVC 10%", "QVC 25%", "QVC 33%", "QVC 50%"]]
assert sorted(sum(GROUPS, [])) == sorted(RULES)
LABEL = {"QVC individual": "QVC, any veto (1/n)", "QVC 10%": "QVC, 10%", "QVC 25%": "QVC, 25%",
         "QVC 33%": "QVC, 33%", "QVC 50%": "QVC, 50%"}
CULTURE_ID = {"spatial": 1, "polarised": 2, "impartial": 3, "spatial1d": 4}
CONTEST = 1 / 3                          # a winner vetoed by at least a third of the voters is "contested"
WORST_OFF = 0.10                         # the worst-off voters: the 10th percentile of utility
THETAS = ["1/n", 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 1 / 3, 0.40, 0.50, 1.0]


def rng_for(culture, k, salt=0):
    return np.random.default_rng([SEED, CULTURE_ID[culture], salt, k])


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


# ---------------------------------------------------------------------------------------------------------
#  Measures of one outcome
# ---------------------------------------------------------------------------------------------------------
def measures(e, out, cw):
    """Measures of the winner of one election (each a number or None when not defined)."""
    w = out.winner
    return {
        "condorcet": None if cw is None else float(w == cw),
        "sue": efficiency(e.U.sum(0), w),                                # Merrill (1984)
        "worst_off": efficiency(np.quantile(e.U, WORST_OFF, axis=0), w),
        "acceptance": e.acc[:, w].mean(),
        "contested": float((~e.acc[:, w]).mean() >= CONTEST - 1e-12),
        "deadlock": float(out.deadlock),
        "fallback": float(out.fallback),
    }


MEASURES = ["condorcet", "sue", "worst_off", "acceptance", "contested", "deadlock", "fallback"]
HEAD = {"condorcet": "Condorcet eff. (%)", "sue": "Utility eff. (%)", "worst_off": "Worst-off eff. (%)",
        "acceptance": "Accepted (%)", "contested": "Contested (%)", "deadlock": "Deadlock (%)",
        "fallback": "Fallback (%)"}
SHORT = {"spatial": "Spatial", "polarised": "Polarised", "impartial": "Impartial"}


def efficiency(score, w):
    """Score of the winner on a 0-100 scale: 0 for the average option, 100 for the best (Merrill, 1984)."""
    span = score.max() - score.mean()
    return 1.0 if span <= 1e-12 else (score[w] - score.mean()) / span


def manipulable(e, rule, out, size=None):
    """Can a coalition of voters who all prefer some y to the winner w get y elected by one of three simple
    joint strategies? (1) rank y first and w last, veto w; (2) the same and veto every option but y;
    (3) only rank w last and veto it. The coalition is every voter who prefers y to w or, with `size`, at
    most that many of them (the first in index order; voters are exchangeable in the cultures). A lower
    bound on coalitional manipulability (Green-Armytage, Tideman and Cosman, 2016, use the same kind of
    bound)."""
    w = out.winner
    top, bottom = e.U.max() + 1, e.U.min() - 1
    for y in range(e.m):
        if y == w:
            continue
        C = np.flatnonzero(e.U[:, y] > e.U[:, w])[:size]
        if len(C) == 0:
            continue
        U, acc = e.U[C].copy(), e.acc[C].copy()
        G = None if e.G is None else e.G[C].copy()
        U[:, w], acc[:, w] = bottom, False
        if G is not None:
            G[:, w] = 0
        strategies = []
        U1, acc1 = U.copy(), acc.copy()
        U1[:, y], acc1[:, y] = top, True
        G1 = None if G is None else G.copy()
        if G1 is not None:
            G1[:, y] = 5
        strategies.append((U1, acc1, G1))
        acc2 = np.zeros_like(acc1)
        acc2[:, y] = True
        G2 = None if G1 is None else np.where(acc2, G1, 0)
        strategies.append((U1, acc2, G2))
        strategies.append((U, acc, G))
        for Us, accs, Gs in strategies:
            if run(e.with_ballots(C, Us, accs, Gs), rule).winner == y:
                return True
    return False


# ---------------------------------------------------------------------------------------------------------
#  Workers (one election each, for the process pool)
# ---------------------------------------------------------------------------------------------------------
def work_perf(args):
    culture, k = args
    e = draw(culture, rng_for(culture, k), N_VOTERS, N_OPTIONS)
    cw = condorcet_winner(e)
    return {r: measures(e, run(e, r), cw) for r in RULES}


SMALL = N_VOTERS // 10                   # a small coalition: at most 10% of the voters


def work_manip(args):
    culture, k, rules = args
    e = draw(culture, rng_for(culture, k, salt=1), N_VOTERS, N_OPTIONS)
    out = {}
    for r in rules:
        o = run(e, r)
        out[r] = (float(manipulable(e, r, o)), float(manipulable(e, r, o, SMALL)))
    return out


def work_clones(args):
    culture, k = args
    rng = rng_for(culture, k, salt=2)
    e = draw(culture, rng, N_VOTERS, N_OPTIONS)
    res = {}
    for r in RULES:
        w = run(e, r).winner
        loser = int(rng.choice([x for x in range(e.m) if x != w]))
        res[r] = []
        for x in (loser, w):                  # clone a losing option (teaming), then the winner (splitting)
            e2 = add_clones(e, x, 3, rng)
            w2 = run(e2, r).winner
            w2 = x if w2 >= e.m else w2         # a clone of x counts as x
            res[r].append(float(w2 != w))
    return res


def theta_rule(theta):
    return "QVC individual" if theta == "1/n" else ("Schulze" if theta == 1.0 else f"theta={theta}")


def work_theta(args):
    culture, k, with_manip = args
    e = draw(culture, rng_for(culture, k, salt=3), N_VOTERS, N_OPTIONS)
    cw = condorcet_winner(e)
    out = {}
    from voting import QVC_THETAS
    for t in THETAS:
        name = theta_rule(t) if t in ("1/n", 1.0) else "QVC tmp"
        if name == "QVC tmp":
            QVC_THETAS["QVC tmp"] = t
        o = run(e, name)
        out[str(t)] = measures(e, o, cw)
        if with_manip:
            out[str(t)]["manip"] = float(manipulable(e, name, o))
            out[str(t)]["manip_small"] = float(manipulable(e, name, o, SMALL))
    return out


def in_hull(points, x):
    return Delaunay(points).find_simplex(x) >= 0


def work_deadlock(args):
    n, k = args
    rng = np.random.default_rng([SEED, 9, n, k])
    e, V, X = draw("spatial", rng, n, N_OPTIONS, positions=True)
    return {"hull": float(n > 2 and in_hull(V, X[-1])),
            "Unanimity": float(run(e, "Unanimity").deadlock),
            "QVC individual": float(run(e, "QVC individual").fallback),
            "QVC 25%": float(run(e, "QVC 25%").fallback),
            "QVC 33%": float(run(e, "QVC 33%").fallback)}


def mean_of(results, key, measure):
    vals = [r[key][measure] for r in results if r[key][measure] is not None]
    return float(np.mean(vals)) if vals else float("nan")


# ---------------------------------------------------------------------------------------------------------
#  Tables
# ---------------------------------------------------------------------------------------------------------
def rows_by_group(fn):
    rows = []
    for g, group in enumerate(GROUPS):
        if g:
            rows.append("midrule")
        rows += [[LABEL.get(r, r)] + fn(r) for r in group]
    return rows


def table_perf(pool, scale):
    reps = max(50, REPS["perf"] // scale)
    for culture in CULTURES:
        res = pool.map(work_perf, [(culture, k) for k in range(reps)], chunksize=20)
        cw_rate = np.mean([r["Schulze"]["condorcet"] is not None for r in res])
        header = ["Rule"] + [HEAD[m] for m in MEASURES]
        rows = rows_by_group(lambda r: [pct(mean_of(res, r, m)) for m in MEASURES])
        write_table(
            f"perf_{culture}", header, rows,
            f"The rules compared: {LABELS[culture][0].lower() + LABELS[culture][1:]}",
            f"{reps:,} elections, {N_VOTERS} voters, {N_OPTIONS} options of which one is the status quo. "
            f"Condorcet efficiency: share of the elections with a Condorcet winner (here {pct(cw_rate)}\\%) in "
            "which the rule elects it. Utility efficiency: total utility of the winner, 0 for the average option "
            "and 100 for the best \\citep{Merrill1984}. Worst-off efficiency: the same for the utility of the "
            "voter at the 10th percentile. Accepted: average share of the voters who do not veto the winner. "
            "Contested: share of the elections whose winner is vetoed by at least a third of the voters. "
            "Deadlock: the status quo stays because no "
            "proposal passes. Fallback: QVC excluded every option and kept the least vetoed. QVC, $x$: "
            "Condorcet with a blocking quota $\\theta = x$ (Section~\\ref{sec:procedure}). Monte Carlo standard "
            "errors are at most 1.1 points.",
            SOURCE, SCRIPT, long_share=0.61, size="footnotesize")
        print(f"  perf_{culture}: {reps} elections")


def table_manip(pool, scale):
    reps = max(30, REPS["manip"] // scale)
    cols = {}
    for culture in CULTURES:
        res = pool.map(work_manip, [(culture, k, RULES) for k in range(reps)], chunksize=5)
        cols[culture] = {r: np.mean([x[r] for x in res], 0) for r in RULES}
    header = ["Rule"] + [f"{SHORT[c]}: {who} (%)" for c in CULTURES for who in ("all", "10%")]
    rows = rows_by_group(lambda r: [pct(v) for c in CULTURES for v in cols[c][r]])
    write_table(
        "manipulability", header, rows,
        "Share of elections a coalition can manipulate",
        f"{reps:,} elections per culture, {N_VOTERS} voters, {N_OPTIONS} options. An election counts as "
        "manipulable if, for some option $y$, voters who prefer $y$ to the winner can elect $y$ by one of "
        "three joint strategies: rank $y$ first and the winner last, vetoing the winner; the same, vetoing "
        "every option but $y$; or rank the winner last and veto it. All: every voter who prefers $y$ to the "
        f"winner joins; 10\\%: at most {SMALL} of them. Other strategies may succeed where these fail: the "
        "shares are lower bounds. Monte Carlo standard errors at most 2.2 points.",
        SOURCE, SCRIPT, long_share=0.6, size="footnotesize")
    print(f"  manipulability: {reps} elections per culture")


def table_clones(pool, scale):
    reps = max(50, REPS["clones"] // scale)
    cols = {}
    for culture in CULTURES:
        res = pool.map(work_clones, [(culture, k) for k in range(reps)], chunksize=20)
        cols[culture] = {r: np.mean([x[r] for x in res], 0) for r in RULES}
    header = ["Rule"] + [f"{SHORT[c]}: {what} (%)" for c in CULTURES for what in ("loser", "winner")]
    rows = rows_by_group(lambda r: [pct(v) for c in CULTURES for v in cols[c][r]])
    write_table(
        "clones", header, rows, "Share of outcomes changed by three clones",
        f"{reps:,} elections per culture, {N_VOTERS} voters, {N_OPTIONS} options. Loser: three clones of a "
        "losing option, drawn at random, are added (teaming, or flooding the agenda); winner: three clones of "
        "the winner are added (vote splitting). A clone is a variant that every voter ranks next to the "
        "original, and grades and vetoes as the original \\citep{Tideman1987}. The outcome is unchanged if "
        "the winner is the same or a clone of it. Monte Carlo standard errors at most 1.6 points.",
        SOURCE, SCRIPT, long_share=0.6, size="footnotesize")
    print(f"  clones: {reps} elections per culture")


def table_theta(pool, scale):
    reps, reps_m = max(50, REPS["theta"] // scale), max(30, REPS["theta_manip"] // scale)
    header = (["Quota"] + [HEAD[m] for m in MEASURES if m != "deadlock"]
              + ["Manip. all (%)", "Manip. 10% (%)"])
    rows = []
    for culture in ("spatial", "polarised"):
        res = pool.map(work_theta, [(culture, k, k < reps_m) for k in range(reps)], chunksize=10)
        if rows:
            rows.append("midrule")
        for t in THETAS:
            key = str(t)
            label = "1/n (any veto)" if t == "1/n" else ("none (Schulze)" if t == 1.0 else f"{100 * t:.0f}%")
            vals = [pct(mean_of(res, key, m)) for m in MEASURES if m != "deadlock"]
            man = [np.mean([r[key][m] for r in res if m in r[key]]) for m in ("manip", "manip_small")]
            rows.append([f"{SHORT[culture]}, {label}"] + vals + [pct(v) for v in man])
    write_table(
        "theta_sweep", header, rows, "QVC: the blocking quota",
        f"{reps:,} elections per culture ({reps_m} for manipulability), {N_VOTERS} voters, {N_OPTIONS} options. "
        "Quota: the share $\\theta$ of the voters whose vetoes exclude an option; 1/n, a single veto; "
        "none, no veto (the Schulze rule). Measures as in Table~\\ref{tab:perf_spatial}; Manip.: manipulable "
        "by all the voters who prefer another option, or by at most 10\\% of the voters, as in "
        "Table~\\ref{tab:manipulability}.",
        SOURCE, SCRIPT, long_share=0.62, size="footnotesize")
    print(f"  theta_sweep: {reps} elections per culture")


def table_cw(pool, scale):
    reps = max(200, REPS["cw"] // scale)
    ms = [3, 4, 5, 6, 8, 12]
    limits = {3: 0.9123, 4: 0.8245, 5: 0.7487, 6: 0.6848}       # impartial culture, n -> infinity (Gehrlein)
    rows = []
    for culture in CULTURES + ["spatial1d"]:
        row = [LABELS[culture]]
        for m in ms:
            res = pool.map(cw_exists, [(culture, m, k) for k in range(reps)], chunksize=50)
            row.append(pct(np.mean(res)))
        rows.append(row)
    rows.append(["Impartial, $n\\to\\infty$"] + [pct(limits[m]) if m in limits else "" for m in ms])
    write_table(
        "cw_probability", ["Culture"] + [f"m = {m}" for m in ms], rows,
        "Probability that a Condorcet winner exists",
        f"{reps:,} elections per cell, {N_VOTERS} voters; $m$ options including the status quo. Last row: the "
        "limit for an infinite electorate under the impartial culture \\citep{GehrleinFishburn1976,Gehrlein2006}. "
        "Monte Carlo standard errors at most 0.8 points.",
        SOURCE + "; last row from the literature", SCRIPT)
    print(f"  cw_probability: {reps} elections per cell")


def cw_exists(args):
    culture, m, k = args
    rng = np.random.default_rng([SEED, CULTURE_ID[culture], 7, m, k])
    return float(condorcet_winner(draw(culture, rng, N_VOTERS, m)) is not None)


def table_deadlock(pool, scale):
    reps = max(100, REPS["deadlock"] // scale)
    ns = [3, 5, 11, 21, 51, 101, 201]
    rows = []
    for n in ns:
        res = pool.map(work_deadlock, [(n, k) for k in range(reps)], chunksize=20)
        rows.append([str(n)] + [pct(np.mean([r[c] for r in res])) for c in
                                ("hull", "Unanimity", "QVC individual", "QVC 25%", "QVC 33%")])
    write_table(
        "deadlock_n", ["Voters", "Status quo Pareto-optimal (%)", "Unanimity: deadlock (%)",
                       "QVC 1/n: fallback (%)", "QVC 25%: fallback (%)", "QVC 33%: fallback (%)"], rows,
        "Deadlock under unanimity as the assembly grows",
        f"{reps:,} elections per row, spatial culture (2D), {N_OPTIONS} options including the status quo. "
        "Status quo Pareto-optimal: the status quo lies in the convex hull of the voters' ideal points, so "
        "that no option whatsoever is preferred to it by every voter (Proposition~\\ref{prop:gridlock}). "
        "Unanimity: no proposal is preferred to the status quo by every voter, which stays. QVC: share of "
        "the elections in which every option is vetoed by the quota and the least-vetoed options are kept; "
        "QVC still decides. Monte Carlo standard errors at most 1.6 points.",
        SOURCE, SCRIPT, long_share=0.7)
    print(f"  deadlock_n: {reps} elections per row")


# ---------------------------------------------------------------------------------------------------------
#  Checks
# ---------------------------------------------------------------------------------------------------------
def check(pool):
    ok = True

    def report(name, good):
        nonlocal ok
        ok &= bool(good)
        print(f"  {name:<70} {'ok' if good else 'FAILED'}")

    # 1. impartial culture, large electorate: probability of a Condorcet winner near Gehrlein's limits
    reps = 20000
    for m, limit in ((3, 0.9123), (4, 0.8245), (5, 0.7487)):
        res = pool.map(cw_ic_large, [(m, k) for k in range(reps)], chunksize=200)
        p, se = np.mean(res), math.sqrt(limit * (1 - limit) / reps)
        report(f"IC, n = 1001, m = {m}: P(Condorcet winner) {p:.4f} vs limit {limit} (3 s.e.)",
               abs(p - limit) < 3 * se + 0.003)          # + finite-n bias, small and positive
    # 2. one dimension, odd n: a Condorcet winner always exists and is the option nearest the median voter
    good = True
    for k in range(300):
        e, V, X = draw("spatial1d", np.random.default_rng([SEED, 4, 99, k]), 101, 8, positions=True)
        med = np.median(V[:, 0])
        good &= condorcet_winner(e) == int(np.argmin(np.abs(X[:, 0] - med)))
    report("1D: the Condorcet winner is the option nearest the median voter (Black, 1948)", good)
    # 3. Proposition (gridlock): status quo in the hull of ideal points => unanimity deadlocks
    good = True
    for k in range(500):
        e, V, X = draw("spatial", np.random.default_rng([SEED, 1, 98, k]), 21, 8, positions=True)
        if in_hull(V, X[-1]):
            good &= run(e, "Unanimity").deadlock
    report("Status quo in the convex hull of ideal points => unanimity keeps it", good)
    # 4. measures: a Condorcet rule has Condorcet efficiency 1; QVC 33% winners contested only on fallback
    res = pool.map(work_perf, [("spatial", k) for k in range(200)], chunksize=20)
    report("Schulze: Condorcet efficiency = 100%", mean_of(res, "Schulze", "condorcet") == 1.0)
    report("QVC 33%: contested only when it falls back",
           all(r["QVC 33%"]["contested"] <= r["QVC 33%"]["fallback"] for r in res))
    report("Unanimity deadlocks in some elections, QVC never does",
           mean_of(res, "Unanimity", "deadlock") > 0 and all(r[q]["deadlock"] == 0 for r in res
                                                             for q in RULES if q.startswith("QVC")))
    return ok


def cw_ic_large(args):
    m, k = args
    rng = np.random.default_rng([SEED, 3, 77, m, k])
    U = rng.random((1001, m))
    return float(condorcet_winner(Election(U, np.ones_like(U, bool))) is not None)


if __name__ == "__main__":
    with Pool(int(os.environ.get("PROCESSES", os.cpu_count() or 1))) as pool:
        if "--check" in sys.argv:
            print("Checks of the Monte Carlo study")
            sys.exit(0 if check(pool) else 1)
        scale = 10 if "--quick" in sys.argv else 1
        only = [a for a in sys.argv[1:] if not a.startswith("--")]
        tables = {"perf": table_perf, "manip": table_manip, "clones": table_clones, "theta": table_theta,
                  "cw": table_cw, "deadlock": table_deadlock}
        for name, fn in tables.items():
            if not only or name in only:
                fn(pool, scale)

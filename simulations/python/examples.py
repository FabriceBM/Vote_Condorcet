"""Worked examples of the note (Section 6.4): small profiles that show, rule by rule, what is at stake.

    E1  majority or compromise: 51 voters A > B > C, 49 voters B > C > A; the minority vetoes A
    E2  flooding: E1 after the majority adds two variants of A (clones A2, A3)
    E3  a Condorcet cycle: 35 A > B > C, 33 B > C > A, 32 C > A > B; each bloc vetoes its last option
    E4  the status-quo trap: 99 voters X > Y > S, one voter S > Y > X who vetoes X and Y

Writes outputs/tables/examples.csv and .tex (label tab:examples). Run from the repository root:
    python3 simulations/python/examples.py
    python3 simulations/python/examples.py --check     # the winners stated in the note
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voting import Election, run, write_table     # noqa: E402

RULES = ["Plurality", "Borda", "Schulze", "Fallback", "PVC + Schulze", "Unanimity", "QVC 25%", "QVC 33%",
         "QVC 50%"]
SHORT = {"Plurality": "Plur.", "Borda": "Borda", "Schulze": "Schul.", "Fallback": "Fallb.",
         "PVC + Schulze": "PVC", "Unanimity": "Unan.", "QVC 25%": "Q 25%", "QVC 33%": "Q 33%",
         "QVC 50%": "Q 50%"}
TAG = {"E1": "compromise", "E2": "flooding", "E3": "cycle", "E4": "status quo"}


def profile(blocs, options, sq):
    """blocs: list of (size, ranking from best to worst, vetoed options)."""
    U, acc = [], []
    for size, ranking, vetoed in blocs:
        u = [len(options) - ranking.index(o) for o in options]
        a = [o not in vetoed for o in options]
        U += [u] * size
        acc += [a] * size
    return Election(np.array(U, float), np.array(acc), sq=options.index(sq), names=list(options))


EXAMPLES = {
    "E1": ("Majority or compromise",
           profile([(51, ["A", "B", "C"], ["C"]), (49, ["B", "C", "A"], ["A"])], ["A", "B", "C"], "C")),
    "E2": ("E1 flooded with two clones of A",
           profile([(51, ["A", "A2", "A3", "B", "C"], ["C"]), (49, ["B", "C", "A", "A2", "A3"], ["A", "A2", "A3"])],
                   ["A", "A2", "A3", "B", "C"], "C")),
    "E3": ("A Condorcet cycle",
           profile([(35, ["A", "B", "C"], ["C"]), (33, ["B", "C", "A"], ["A"]), (32, ["C", "A", "B"], ["B"])],
                   ["A", "B", "C"], "C")),
    "E4": ("The status-quo trap",
           profile([(99, ["X", "Y", "S"], ["S"]), (1, ["S", "Y", "X"], ["X", "Y"])], ["X", "Y", "S"], "S")),
}
EXPECTED = {   # the winners stated in Section 6.4 of the note
    "E1": {"Plurality": "A", "Borda": "B", "Schulze": "A", "Fallback": "B", "PVC + Schulze": "B",
           "Unanimity": "B", "QVC 25%": "B", "QVC 33%": "B", "QVC 50%": "A"},
    "E2": {"Plurality": "A", "Borda": "A", "Schulze": "A", "Fallback": "A", "PVC + Schulze": "A",
           "Unanimity": "B", "QVC 25%": "B", "QVC 33%": "B", "QVC 50%": "A"},
    "E3": {"Schulze": "A", "QVC 25%": "B", "QVC 33%": "A", "QVC 50%": "A"},
    "E4": {"Unanimity": "S", "QVC 25%": "X", "QVC 33%": "X", "QVC 50%": "X"},
}


def winners():
    out = {}
    for key, (_, e) in EXAMPLES.items():
        out[key] = {}
        for r in RULES:
            o = run(e, r)
            out[key][r] = e.names[o.winner] + (" (stuck)" if o.deadlock else "") + (" (fb)" if o.fallback else "")
    return out


def main():
    w = winners()
    rows = [[f"{k} ({TAG[k]})"] + [w[k][r] for r in RULES] for k in EXAMPLES]
    write_table(
        "examples", ["Example"] + [SHORT[r] for r in RULES], rows, "Winners in the worked examples",
        "E1: 51 voters rank A, B, C and veto C; 49 rank B, C, A and veto A. E2: E1 after the majority "
        "proposes two variants of A, ranked just below A by the majority and last by the minority, which "
        "vetoes them. E3: 35 voters rank A, B, C; 33 B, C, A; 32 C, A, B; each bloc vetoes its last option. "
        "E4: 99 voters rank X, Y, S and veto S; one voter ranks S, Y, X and vetoes X and Y. The status quo is "
        "C in E1--E3 and S in E4. Stuck: no proposal passes and the status quo stays; fb: every option is "
        "vetoed by the quota and QVC keeps the least-vetoed ones. Fallb.: fallback bargaining; PVC: Schulze "
        "within the proportional veto core; Unan.: unanimity with the status quo as default; Q $x$: QVC "
        "with a blocking quota $\\theta = x$.",
        "Profiles of Section~\\ref{sec:examples}", "simulations/python/examples.py", long_share=0.62,
        size="footnotesize")


def check():
    w = winners()
    ok = True
    for key, exp in EXPECTED.items():
        for r, x in exp.items():
            got = w[key][r].split(" ")[0]
            good = got == x
            ok &= good
            print(f"  {key} {r:<14} expected {x:<3} got {w[key][r]:<10} {'ok' if good else 'FAILED'}")
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        print("Checks of the worked examples")
        sys.exit(0 if check() else 1)
    main()
    for k, row in winners().items():
        print(k, row)

"""The explainer: a web page on the ideas of the note, with linked diagrams (inline SVG, no library).

Sections: the argument as a map (hover a box to follow its links), the procedure QVC(θ) step by step with the
propositions attached to their steps, Example E1 through the count, and three pictures: the status quo inside
the voters' convex hull (Proposition 2, interactive), flooding under proportional veto and under the blocking
quota (Propositions 3 and 7, computed from the ballots of E1 and E2), and the trade-off in the quota θ.

Numbers come from the generated outputs (outputs/tables/key_numbers_en.tex and theta_sweep.csv), never typed:
rerun this script after experiments.py and key_numbers.py.

Run from the repository root:
    python3 tools/explainer_page.py                   # summaries/en/explainer/voting-with-veto-rights.html
    python3 tools/explainer_page.py --fragment OUT    # the same page without <!doctype>, <head> and <body>,
                                                      # for hosts that add their own (a claude.ai artifact)
"""
import argparse
import csv
import html
import math
import re

REPO = "."
OUT = "summaries/en/explainer/voting-with-veto-rights.html"

KN = dict(re.findall(r"\\newcommand\{\\KN(\w+)\}\{([^}]*)\}",
                     open(f"{REPO}/outputs/tables/key_numbers_en.tex", encoding="utf8").read()))
SWEEP = list(csv.DictReader(open(f"{REPO}/outputs/tables/theta_sweep.csv", encoding="utf8")))


def esc(s):
    return html.escape(s, quote=True)


def rich(s):
    """Escape, then render A_θ as A with a subscript θ inside SVG text."""
    s = esc(s)
    return s.replace("A_θ", 'A<tspan class="sub" dy="3">θ</tspan><tspan dy="-3">\u200b</tspan>')


# ------------------------------------------------------------------------------------------------
#  Shared SVG helpers
# ------------------------------------------------------------------------------------------------
def rounded_path(points, r=8):
    """Polyline through points with rounded corners."""
    if len(points) == 2:
        (x1, y1), (x2, y2) = points
        return f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"
    d = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(1, len(points) - 1):
        (xa, ya), (xb, yb), (xc, yc) = points[i - 1], points[i], points[i + 1]
        la, lc = math.hypot(xb - xa, yb - ya), math.hypot(xc - xb, yc - yb)
        ra = min(r, la / 2, lc / 2)
        p1 = (xb - (xb - xa) / la * ra, yb - (yb - ya) / la * ra)
        p2 = (xb + (xc - xb) / lc * ra, yb + (yc - yb) / lc * ra)
        d += f" L{p1[0]:.1f},{p1[1]:.1f} Q{xb:.1f},{yb:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    d += f" L{points[-1][0]:.1f},{points[-1][1]:.1f}"
    return d


def bezier(x1, y1, x2, y2):
    dx = max(30, (x2 - x1) * 0.5)
    return f"M{x1:.1f},{y1:.1f} C{x1 + dx:.1f},{y1:.1f} {x2 - dx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"


def markers(prefix):
    return (f'<defs>'
            f'<marker id="{prefix}-ah" class="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>'
            f'<marker id="{prefix}-ah-hi" class="ah-hi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker>'
            f'</defs>')


# ------------------------------------------------------------------------------------------------
#  1. The argument map
# ------------------------------------------------------------------------------------------------
def argument_map():
    cols = ["The question", "What theory and evidence say", "Design principles", "The procedure",
            "What it guarantees", "Containing the price"]
    W, H, X0, STEP, Y0, ROW = 172, 44, 0, 202, 46, 54
    colx = [X0 + i * STEP for i in range(6)]
    # id: (col, row, title, sub, kind)
    N = {
        "H1": (0, 0.3, "H1 · Open agenda", "anyone proposes any number", "q"),
        "H2": (0, 1.6, "H2 · Full ballots", "all judge every option", "q"),
        "H3": (0, 2.9, "H3 · Veto rights", "voters can block options", "q"),
        "R1": (0, 4.2, "R1 · Best compromise", "one everyone can live with", "q"),
        "R2": (0, 5.5, "R2 · Never stuck", "always a decision, in time", "q"),

        "L5": (1, 0, "Prop. 3 · Flooding", "clones dilute vetoes", "e"),
        "L4": (1, 1, "Cycles are rare", "Condorcet winners abound", "e"),
        "L6": (1, 2, "Block ≠ approve", "Bouton et al. (2018)", "e"),
        "L2": (1, 3, "Prop. 1 · Majority vs veto", "its winner may be vetoed", "e"),
        "L3": (1, 4, "Prop. 2 · Deadlock", "unanimity stalls as n grows", "e"),
        "L8": (1, 5, "Agendas can be steered", "sequential votes (McKelvey)", "e"),
        "L7": (1, 6, "A default breeds inertia", "veto players (Tsebelis)", "e"),
        "L1": (1, 7, "No rule is strategy-proof", "Gibbard–Satterthwaite", "e"),

        "P5": (2, 0, "P5 · Clone-independent", "flooding gains nothing", "p"),
        "P2": (2, 1.2, "P2 · Rank, then block", "a ranking plus a line", "p"),
        "P3": (2, 2.4, "P3 · Coalitions veto", "a share θ, not one voter", "p"),
        "P6": (2, 3.6, "P6 · Always a decision", "never an empty choice", "p"),
        "P1": (2, 4.8, "P1 · Simultaneous ballot", "no agenda to steer", "p"),
        "P4": (2, 6.0, "P4 · Status quo = option", "never the default", "p"),

        "M5": (3, 0, "Schulze winner", "among admissible options", "m"),
        "M2": (3, 1.2, "Acceptability line", "below it: vetoed", "m"),
        "M3": (3, 2.4, "Blocking quota θ", "exclude x if v(x) ≥ θn", "m"),
        "M6": (3, 3.6, "Fallback", "keep the least vetoed", "m"),
        "M1": (3, 4.8, "One ballot, one round", "all options at once", "m"),
        "M4": (3, 6.0, "Status quo on the ballot", "ranked and vetoed like any", "m"),

        "G7": (4, 0, "Prop. 7 · Clone-proof", "clones inherit vetoes", "g"),
        "G6": (4, 1.2, "Prop. 6 · Majority decides", "Condorcet winner of A_θ wins", "g"),
        "G5": (4, 2.4, "Prop. 5 · Acceptable", "to > 1 − θ when possible", "g"),
        "G4": (4, 4.2, "Prop. 4 · Always decides", "one round, no default edge", "g"),
        "G8": (4, 6.0, "Prop. 8 · The price", "vetoes can be strategic", "w"),

        "S1": (5, 3.6, "Named, reasoned vetoes", "public, with a reason", "s"),
        "S4": (5, 4.6, "Quota of at least 1/4", "θ = 1/3 by default", "s"),
        "S2": (5, 5.6, "One revision round", "only after a fallback", "s"),
        "S3": (5, 6.6, "Veto budgets", "across decisions only", "s"),
    }
    E = [("H1", "L5"), ("H2", "L8"), ("H2", "L4"), ("H3", "L6"), ("H3", "L2"), ("H3", "L3"), ("R1", "L2"),
         ("R1", "L6"), ("R2", "L3"), ("R2", "L7"),
         ("L5", "P5"), ("L6", "P2"), ("L2", "P3"), ("L3", "P3"), ("L3", "P6"), ("L8", "P1"), ("L7", "P4"),
         ("L4", "M5"),
         ("P5", "M5"), ("P2", "M2"), ("P3", "M3"), ("P6", "M6"), ("P1", "M1"), ("P4", "M4"),
         ("M5", "G7"), ("M2", "G7"), ("M5", "G6"), ("M3", "G6"), ("M3", "G5"), ("M6", "G5"), ("M6", "G4"),
         ("M1", "G4"), ("M4", "G4"), ("M3", "G8"), ("L1", "G8"),
         ("G8", "S1"), ("G8", "S2"), ("G8", "S3"), ("G8", "S4")]
    pos = {k: (colx[c], Y0 + r * ROW) for k, (c, r, *_) in N.items()}
    width, height = colx[-1] + W + 4, Y0 + 7.0 * ROW + H + 8
    out = [f'<svg class="dg graph" id="argmap" viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
           f'aria-labelledby="argmap-t argmap-d">'
           f'<title id="argmap-t">The argument of the note as a map</title>'
           f'<desc id="argmap-d">From the hypotheses and requirements, through the results of theory and '
           f'evidence, to the design principles, the steps of the procedure, its guarantees, its price and '
           f'the safeguards that contain it.</desc>', markers("am")]
    for i, name in enumerate(cols):
        out.append(f'<text class="colhead" x="{colx[i]}" y="18">{esc(name.upper())}</text>')
    for a, b in E:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        long_jump = N[b][0] - N[a][0] > 1
        x1, y1, x2, y2 = xa + W, ya + H / 2, xb - 2, yb + H / 2
        d = bezier(x1, y1, x2, y2)
        cls = "edge long" if long_jump else "edge"
        out.append(f'<path class="{cls}" data-from="{a}" data-to="{b}" d="{d}" marker-end="url(#am-ah)"/>')
    for k, (c, r, title, sub, kind) in N.items():
        x, y = pos[k]
        out.append(f'<g class="node k-{kind}" data-id="{k}" tabindex="0">'
                   f'<rect class="box" x="{x}" y="{y}" width="{W}" height="{H}" rx="5"/>'
                   f'<text x="{x + 9}" y="{y + 18}" class="t">{rich(title)}</text>'
                   f'<text x="{x + 9}" y="{y + 34}" class="s">{rich(sub)}</text></g>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------------------------------------
#  2. The procedure, step by step
# ------------------------------------------------------------------------------------------------
def flowchart():
    MX, MW = 380, 300          # main column
    BX, BW = 740, 250          # branch column
    AX, AW = 150, 200          # annotation column
    LH = 16                    # line height
    out = []

    def box(x, y, w, lines, kind="step", pill=False):
        h = 16 + LH * len(lines) + 4
        rx = h / 2 if pill else 6
        g = [f'<g class="fnode k-{kind}"><rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>']
        for i, (text, cls) in enumerate(lines):
            anchor = ' text-anchor="middle"' if pill else ""
            tx = x + w / 2 if pill else x + 12
            g.append(f'<text x="{tx}" y="{y + 22 + i * LH}" class="{cls}"{anchor}>{rich(text)}</text>')
        g.append("</g>")
        out.append("".join(g))
        return h

    def diamond(cx, cy, w, h, lines):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        g = [f'<g class="fnode k-q"><polygon class="box" points="{pts}"/>']
        y0 = cy - (len(lines) - 1) * LH / 2 + 4
        for i, t in enumerate(lines):
            g.append(f'<text x="{cx}" y="{y0 + i * LH}" class="t" text-anchor="middle">{rich(t)}</text>')
        g.append("</g>")
        out.append("".join(g))

    def arrow(points, dashed=False, label=None, lx=None, ly=None):
        cls = "edge dashed" if dashed else "edge"
        out.append(f'<path class="{cls}" d="{rounded_path(points)}" marker-end="url(#fc-ah)"/>')
        if label:
            out.append(f'<text class="elabel" x="{lx}" y="{ly}">{esc(label)}</text>')

    def note(y_mid, lines, target_y):
        h = 12 + 15 * len(lines)
        y = y_mid - h / 2
        g = [f'<g class="fnote"><rect class="box" x="{AX}" y="{y}" width="{AW}" height="{h}" rx="5"/>']
        for i, (text, cls) in enumerate(lines):
            g.append(f'<text x="{AX + 10}" y="{y + 19 + i * 15}" class="{cls}">{rich(text)}</text>')
        g.append("</g>")
        out.append("".join(g))
        out.append(f'<path class="link" d="M{AX + AW},{y_mid} L{MX - 4},{target_y}"/>')

    cx = MX + MW / 2
    # phases (bands) -- drawn first
    phases = [("Before the vote", 8, 132), ("Nomination", 132, 236), ("Ballot", 236, 360),
              ("Count", 360, 900), ("Result", 900, 1176)]
    bands = []
    for i, (name, y0, y1) in enumerate(phases):
        bands.append(f'<rect class="band{" alt" if i % 2 else ""}" x="0" y="{y0}" width="1100" height="{y1 - y0}"/>'
                     f'<text class="phase" x="10" y="{y0 + 22}">{esc(name.upper())}</text>')
    # nodes
    y = 22
    h1 = box(MX, y, MW, [("Fix the parameters", "t"), ("quota θ: one third, ⌈n/3⌉ voters", "s"),
                         ("status quo protected? no, by default", "s"), ("nomination period, revision round", "s")])
    n1b = y + h1
    y2 = 146
    h2 = box(MX, y2, MW, [("Nomination", "t"), ("anyone proposes any number of options", "s"),
                          ("the status quo is on the ballot", "s")])
    y3 = 250
    h3 = box(MX, y3, MW, [("Ballot", "t"), ("rank every option, ties allowed", "s"),
                          ("draw the acceptability line: below it, a veto", "s"),
                          ("each veto named and reasoned", "s")])
    y4 = 376
    h4 = box(MX, y4, MW, [("Count the vetoes", "t"), ("v(x): how many voters veto option x", "s")])
    d1y = 500
    diamond(cx, d1y, MW, 100, ["Some option with", "v(x) < θn ?"])
    y5 = 590
    h5 = box(MX, y5, MW, [("Admissible options", "t"), ("A_θ = { x : v(x) < θn }", "m")], kind="m")
    y5b = d1y - 37
    h5b = box(BX, y5b, BW, [("Fallback", "t"), ("A_θ = the options with", "s"), ("the fewest vetoes", "s")], kind="m")
    y6 = 676
    h6 = box(MX, y6, MW, [("Schulze among A_θ", "t"), ("pairwise counts N(x, y), strongest paths", "s")], kind="m")
    d2y = 806
    diamond(cx, d2y, MW, 92, ["One Schulze", "winner?"])
    y6b = d2y - 45
    h6b = box(BX, y6b, BW, [("Tie-break", "t"), ("1. fewest vetoes", "s"), ("2. Schulze on the tied options", "s"),
                            ("3. order drawn before the vote", "s")], kind="m")
    y7 = 912
    h7 = box(MX, y7, MW, [("Winner, published", "t"), ("with the veto counts, A_θ and the matrix N,", "s"),
                          ("so that anyone can check the count", "s")], kind="g")
    d3y = 1052
    diamond(cx, d3y, MW, 96, ["Fallback used and", "revision round adopted?"])
    y8 = 1126
    box(MX + 60, y8, MW - 120, [("Final decision", "t")], kind="g", pill=True)
    y7b = d3y - 45
    h7b = box(BX, y7b, BW, [("Revision round", "t"), ("nominations reopen briefly", "s"),
                            ("for compromise proposals; one", "s"), ("more ballot, whose result is final", "s")], kind="w")
    # arrows on the main line
    arrow([(cx, n1b), (cx, y2 - 2)])
    arrow([(cx, y2 + h2), (cx, y3 - 2)])
    arrow([(cx, y3 + h3), (cx, y4 - 2)])
    arrow([(cx, y4 + h4), (cx, d1y - 50 - 2)])
    arrow([(cx, d1y + 50), (cx, y5 - 2)], label="yes", lx=cx + 8, ly=d1y + 66)
    arrow([(MX + MW, d1y), (BX - 2, d1y)], label="no", lx=MX + MW + 14, ly=d1y - 8)
    arrow([(BX + BW / 2, y5b + h5b), (BX + BW / 2, y6 + 28), (MX + MW + 2, y6 + 28)])
    arrow([(cx, y5 + h5), (cx, y6 - 2)])
    arrow([(cx, y6 + h6), (cx, d2y - 46 - 2)])
    arrow([(cx, d2y + 46), (cx, y7 - 2)], label="yes", lx=cx + 8, ly=d2y + 62)
    arrow([(MX + MW, d2y), (BX - 2, d2y)], label="no", lx=MX + MW + 14, ly=d2y - 8)
    arrow([(BX + BW / 2, y6b + h6b), (BX + BW / 2, y7 + 36), (MX + MW + 2, y7 + 36)])
    arrow([(cx, y7 + h7), (cx, d3y - 48 - 2)])
    arrow([(cx, d3y + 48), (cx, y8 - 2)], label="no", lx=cx + 8, ly=d3y + 64)
    arrow([(MX + MW, d3y), (BX - 2, d3y)], label="yes", lx=MX + MW + 14, ly=d3y - 8)
    loop_x = BX + BW + 50
    arrow([(BX + BW, d3y), (loop_x, d3y), (loop_x, y2 + h2 / 2), (MX + MW + 2, y2 + h2 / 2)], dashed=True,
          label="once", lx=loop_x + 8, ly=(d3y + y2) / 2)
    # the guarantees, attached where they bite
    note(y3 + h3 / 2, [("Prop. 8 · the price", "t"), ("a blocking third can also", "s"),
                       ("veto strategically: hence", "s"), ("named vetoes, θ ≥ 1/4", "s")], y3 + h3 / 2)
    note(y4 + h4 / 2 + 22, [("Prop. 7 · clones", "t"), ("a variant carries the same", "s"),
                            ("vetoes as its original", "s")], y4 + h4 / 2)
    note(y5 + h5 / 2 + 6, [("Prop. 5 · acceptability", "t"), ("the winner is acceptable to", "s"),
                           ("> 1 − θ if any option is", "s")], y5 + h5 / 2)
    note(y6 + h6 / 2 + 62, [("Prop. 6 · majority", "t"), ("in the Smith set of A_θ,", "s"),
                            ("never Pareto-dominated", "s")], y6 + h6 / 2)
    note(y7 + h7 / 2 + 30, [("Prop. 4 · decisive", "t"), ("one option, one round, any", "s"),
                            ("profile, no default edge", "s")], y7 + h7 / 2)
    height = 1176
    svg = (f'<svg class="dg flow" viewBox="0 0 1100 {height}" role="img" aria-labelledby="flow-t flow-d">'
           f'<title id="flow-t">QVC(θ), step by step</title><desc id="flow-d">The procedure from the choice of '
           f'parameters to the final decision: nomination, ballot, veto counts, admissible options or fallback, '
           f'Schulze winner and tie-break, publication, and an optional revision round. The propositions of the '
           f'note are attached to the steps they concern.</desc>{markers("fc")}{"".join(bands)}{"".join(out)}</svg>')
    return svg


# ------------------------------------------------------------------------------------------------
#  3. Flooding: proportional veto against the blocking quota (Examples E1 and E2)
# ------------------------------------------------------------------------------------------------
def flooding():
    """E1 and E2 under the proportional veto core and under QVC(1/3), computed from the ballots."""
    n = 100
    profiles = {
        "E1": [(51, ["A", "B", "C"], {"C"}), (49, ["B", "C", "A"], {"A"})],
        "E2": [(51, ["A", "A₂", "A₃", "B", "C"], {"C"}), (49, ["B", "C", "A", "A₂", "A₃"], {"A", "A₂", "A₃"})],
    }
    winners = {("pvc", "E1"): "B", ("pvc", "E2"): "A", ("qvc", "E1"): "B", ("qvc", "E2"): "B"}  # Table 4 of the note

    def pvc_blocker(bloc, x, m):
        """The bloc that blocks x in the proportional veto core, if any (each bloc is a coalition)."""
        for t, ranking, _ in sorted(bloc, key=lambda b: -b[0]):
            preferred = ranking.index(x)          # options this bloc ranks above x
            if preferred >= m - math.ceil(m * t / n) + 1:
                return "maj" if t > n / 2 else "min"
        return None

    def qvc_blocker(bloc, x):
        for t, _, vetoes in bloc:
            if x in vetoes and t >= n / 3:
                return "maj" if t > n / 2 else "min"
        return None

    out = [f'<svg class="dg flood" viewBox="0 0 800 340" role="img" aria-labelledby="fl-t fl-d">'
           f'<title id="fl-t">Flooding the agenda</title><desc id="fl-d">Examples E1 and E2. Under the '
           f'proportional veto core, the minority blocks A in E1; in E2 the majority has added two variants of '
           f'A, the minority’s vetoes no longer reach A, and A wins. Under the blocking quota, every variant of A '
           f'inherits 49 vetoes and is excluded, and B wins in both.</desc>']
    cols = [(60, "pvc", "Proportional veto core"), (450, "qvc", "Blocking quota, θ = 1/3")]
    for cx0, _, head in cols:
        out.append(f'<text class="colhead" x="{cx0}" y="20">{esc(head.upper())}</text>')
    for ry, ex in ((44, "E1"), (196, "E2")):
        bloc = profiles[ex]
        opts = bloc[0][1]
        m = len(opts)
        out.append(f'<text class="phase" x="0" y="{ry + 32}">{ex}</text>')
        for cx0, rule, _ in cols:
            for j, o in enumerate(opts):
                x = cx0 + j * 54
                by = pvc_blocker(bloc, o, m) if rule == "pvc" else qvc_blocker(bloc, o)
                cls = "tok" + (f" blocked by-{by}" if by else "") + (" win" if winners[(rule, ex)] == o else "")
                out.append(f'<g class="{cls}"><rect x="{x}" y="{ry + 8}" width="44" height="38" rx="6"/>'
                           f'<text x="{x + 22}" y="{ry + 33}" text-anchor="middle">{esc(o)}</text></g>')
            out.append(f'<text class="t" x="{cx0 + m * 54 + 4}" y="{ry + 33}">→ {winners[(rule, ex)]}</text>')
            if rule == "pvc":
                v_min, v_maj = math.ceil(m * 49 / n) - 1, math.ceil(m * 51 / n) - 1
                lines = [f"{m} options. The 49% minority vetoes {v_min} of them,",
                         f"the 51% majority {v_maj}."]
                lines.append("The minority's veto reaches A." if ex == "E1" else
                             "Two vetoes cannot cover three copies of A.")
            else:
                lines = ["An option is out once θn = 33.3 voters veto it.",
                         "v(A) = 49, v(C) = 51: both out." if ex == "E1" else
                         "Each copy of A inherits 49 vetoes: all out."]
            for i, line in enumerate(lines):
                out.append(f'<text class="s" x="{cx0}" y="{ry + 70 + i * 16}">{esc(line)}</text>')
    out.append(f'<g class="tok blocked by-min"><rect x="60" y="314" width="16" height="14" rx="3"/></g>'
               f'<text class="s" x="82" y="325">blocked by the minority</text>'
               f'<g class="tok blocked by-maj"><rect x="250" y="314" width="16" height="14" rx="3"/></g>'
               f'<text class="s" x="272" y="325">blocked by the majority</text>'
               f'<g class="tok win"><rect x="440" y="314" width="16" height="14" rx="3"/></g>'
               f'<text class="s" x="462" y="325">winner</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------------------------------------
#  4. The θ dial: the trade-off, from the simulation's θ sweep
# ------------------------------------------------------------------------------------------------
def theta_chart():
    series = [("Condorcet eff. (%)", "Condorcet efficiency", "c1"), ("Worst-off eff. (%)", "Worst-off efficiency", "c2"),
              ("Fallback (%)", "Fallback used", "c3"), ("Manip. 10% (%)", "Manipulable by 10% of voters", "c4")]
    X0, X1, Y0, Y1 = 64, 600, 66, 320          # plot area
    def xs(t):                                   # θ in percent, 0..50, linear
        return X0 + (t / 50) * (X1 - X0)
    def ys(v):
        return Y1 - v / 100 * (Y1 - Y0)
    groups = []
    for culture in ("Polarised", "Spatial"):
        rows = [r for r in SWEEP if r["Quota"].startswith(culture + ",")]
        pts = []
        for r in rows:
            q = r["Quota"].split(", ", 1)[1]
            if q.startswith("1/n"):
                t = 1.0
            elif q.startswith("none"):
                continue
            else:
                t = float(q.rstrip("%"))
            pts.append((t, r))
        g = [f'<g class="culture" data-culture="{culture.lower()}"{" hidden" if culture == "Spatial" else ""}>']
        for col, label, cls in series:
            path = " ".join(f"{'M' if i == 0 else 'L'}{xs(t):.1f},{ys(float(r[col])):.1f}" for i, (t, r) in enumerate(pts))
            g.append(f'<path class="line {cls}" d="{path}"/>')
            for t, r in pts:
                v = float(r[col])
                g.append(f'<circle class="dot {cls}" cx="{xs(t):.1f}" cy="{ys(v):.1f}" r="2.6">'
                         f'<title>{esc(label)}, θ = {esc(r["Quota"].split(", ", 1)[1])}: {v:.1f}%</title></circle>')
            # end label
            t_end, r_end = pts[-1]
            g.append(f'<text class="endlab {cls}" x="{X1 + 8}" y="{ys(float(r_end[col])) + 4:.1f}">{esc(label)}</text>')
        g.append("</g>")
        groups.append("".join(g))
    axes = []
    for v in range(0, 101, 20):
        axes.append(f'<line class="grid" x1="{X0}" x2="{X1}" y1="{ys(v)}" y2="{ys(v)}"/>'
                    f'<text class="tick" x="{X0 - 8}" y="{ys(v) + 4}" text-anchor="end">{v}</text>')
    for t in (0, 10, 20, 30, 40, 50):
        axes.append(f'<text class="tick" x="{xs(t)}" y="{Y1 + 18}" text-anchor="middle">{t}%</text>')
    axes.append(f'<text class="axis" x="{(X0 + X1) / 2}" y="{Y1 + 40}" text-anchor="middle">Blocking quota θ, '
                f'share of voters whose veto excludes an option</text>')
    axes.append(f'<text class="axis" x="{X0 - 8}" y="{Y0 - 14}" text-anchor="end">%</text>')
    # regimes and markers
    regimes = [(0, 20, ["fallback decides,", "the veto is a negative vote"], ""),
               (25, 40, ["the veto filters,", "the majority decides"], " sweet"),
               (40, 50, ["the veto", "rarely binds"], "")]
    reg = []
    for a, b, lab, extra in regimes:
        reg.append(f'<rect class="regime{extra}" x="{xs(a)}" y="{Y0}" width="{xs(b) - xs(a)}" height="{Y1 - Y0}"/>')
        for i, line in enumerate(lab):
            reg.append(f'<text class="reglab" x="{(xs(a) + xs(b)) / 2}" y="{16 + i * 14}" text-anchor="middle">{esc(line)}</text>')
    marks = [(100 / 3, "θ = 1/3", "mark main"), (35, "EU blocking minority 35%", "mark"),
             (49, "E1 flips: B below, A above", "mark")]
    mk = []
    for t, lab, cls in marks:
        mk.append(f'<line class="{cls}" x1="{xs(t):.1f}" x2="{xs(t):.1f}" y1="{Y0}" y2="{Y1}"/>')
    mk.append(f'<text class="marklab main" x="{xs(100 / 3) - 4:.1f}" y="{Y0 - 8}" text-anchor="end">θ = 1/3</text>')
    mk.append(f'<text class="marklab" x="{xs(35) + 4:.1f}" y="{Y0 - 8}">EU 35%</text>')
    mk.append(f'<text class="marklab" x="{xs(49) + 4:.1f}" y="{Y0 - 22}" text-anchor="middle">E1 flips at 49%</text>')
    return (f'<svg class="dg chart" viewBox="0 0 800 370" role="img" aria-labelledby="th-t th-d">'
            f'<title id="th-t">What the blocking quota buys and costs</title><desc id="th-d">As the quota θ rises '
            f'from a single veto to half of the voters, Condorcet efficiency rises, worst-off efficiency falls, the '
            f'fallback disappears above about 30 percent, and manipulability by small coalitions falls steeply. '
            f'The recommended quota is one third.</desc>{"".join(reg)}{"".join(axes)}{"".join(mk)}'
            f'{"".join(groups)}</svg>')


# ------------------------------------------------------------------------------------------------
#  Page
# ------------------------------------------------------------------------------------------------
STYLE = r"""
/* Layout: an argument told in pictures. A connected map of the note's ideas first, then the procedure as a
   flowchart, then three geometric pictures (hull, flooding, the θ dial). Colour encodes the role of an idea:
   blue = question, grey = what theory and evidence say, ink = principles, teal = the procedure's mechanism,
   green = guarantees, orange = the price. */
:root {
  --bg: #F6F8FB;
  --surface: #FFFFFF;
  --ink: #111722;
  --muted: #586174;
  --line: #D9DFE9;
  --edge: #9AA5B8;
  --accent: #2A78D6;
  --accent-soft: #E8F1FC;
  --mech: #0F7C8C;
  --mech-soft: #E3F3F5;
  --good: #16825C;
  --good-soft: #E5F4EE;
  --warn: #C25A1A;
  --warn-soft: #FBEEE5;
  --band: #EEF2F8;
  --c1: #2A78D6; --c2: #16825C; --c3: #8C6A00; --c4: #C25A1A;
  --font-display: "IBM Plex Sans Condensed", "Arial Narrow", "Helvetica Neue", Arial, sans-serif;
  --font-body: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --radius: 6px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0D121B; --surface: #151C29; --ink: #E4E9F2; --muted: #9AA4B8; --line: #2A3448; --edge: #56627A;
    --accent: #5D9EF2; --accent-soft: #17263D; --mech: #4CC3D2; --mech-soft: #102A2E; --good: #43BE8F;
    --good-soft: #12291F; --warn: #EE8E52; --warn-soft: #33200F; --band: #121926;
    --c1: #5D9EF2; --c2: #43BE8F; --c3: #E0B84A; --c4: #EE8E52; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #0D121B; --surface: #151C29; --ink: #E4E9F2; --muted: #9AA4B8; --line: #2A3448; --edge: #56627A;
  --accent: #5D9EF2; --accent-soft: #17263D; --mech: #4CC3D2; --mech-soft: #102A2E; --good: #43BE8F;
  --good-soft: #12291F; --warn: #EE8E52; --warn-soft: #33200F; --band: #121926;
  --c1: #5D9EF2; --c2: #43BE8F; --c3: #E0B84A; --c4: #EE8E52; color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: 1rem; line-height: 1.55;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 4rem;
}
.wrap { max-width: 1120px; margin: 0 auto; }
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; line-height: 1.15; margin: 0; }
h1 { font-size: clamp(1.9rem, 4.6vw, 2.7rem); font-weight: 700; letter-spacing: -0.01em; }
h2 { font-size: 1.55rem; font-weight: 600; }
h3 { font-size: 1.1rem; font-weight: 600; }
p { margin: 0; max-width: 70ch; }
a { color: var(--accent); }
a:focus-visible, button:focus-visible, [tabindex]:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.eyebrow { font-family: var(--font-display); font-weight: 600; font-size: 0.78rem; letter-spacing: 0.09em;
  text-transform: uppercase; color: var(--muted); }
section { display: grid; gap: 1rem; padding-block: 2.6rem 0; }
.hint { font-size: 0.88rem; color: var(--muted); }
.narrow-hint { display: none; }

header { display: grid; gap: 1rem; padding-block: 2.6rem 1.4rem; border-bottom: 1px solid var(--line); }
header .lead { font-size: 1.08rem; }
.answer { display: grid; gap: 0.5rem; background: var(--surface); border: 1px solid var(--line);
  border-left: 3px solid var(--mech); border-radius: var(--radius); padding: 1rem 1.1rem; max-width: 820px; }
.answer ol { margin: 0; padding-left: 1.3rem; display: grid; gap: 0.15rem; }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.8rem; }
.fact { border-top: 2px solid var(--ink); padding-top: 0.5rem; display: grid; gap: 0.2rem; align-content: start; }
.fact b { font-family: var(--font-display); font-size: 1.45rem; font-weight: 600; font-variant-numeric: tabular-nums; }
.fact span { font-size: 0.88rem; color: var(--muted); }
.fact.warn { border-top-color: var(--warn); }
.fact.good { border-top-color: var(--good); }
nav.toc { display: flex; flex-wrap: wrap; gap: 0.4rem 0.6rem; }
nav.toc a { font-family: var(--font-display); font-weight: 500; font-size: 0.92rem; text-decoration: none; color: var(--ink);
  border: 1px solid var(--line); border-radius: 999px; padding: 0.2rem 0.75rem; background: var(--surface); }
nav.toc a:hover { border-color: var(--accent); color: var(--accent); }

.figure { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 1rem; overflow-x: auto; }
.figure svg { display: block; width: 100%; height: auto; }
.figure.wide svg { min-width: 900px; }
.legend { display: flex; flex-wrap: wrap; gap: 0.4rem 1.1rem; font-size: 0.86rem; color: var(--muted); }
.legend span::before { content: ""; display: inline-block; width: 0.75em; height: 0.75em; border-radius: 2px;
  margin-right: 0.4em; vertical-align: -0.05em; background: var(--k); border: 1px solid var(--kb, transparent); }

/* ---- SVG diagrams ---- */
.dg text { font-family: var(--font-body); fill: var(--ink); }
.dg .t { font-family: var(--font-display); font-weight: 600; font-size: 13px; }
.dg .s { font-size: 11.5px; fill: var(--muted); }
.dg .m { font-family: var(--font-mono); font-size: 12px; }
.dg .sub { font-size: 80%; }
.dg .colhead { font-family: var(--font-display); font-weight: 600; font-size: 11px; letter-spacing: 0.08em; fill: var(--muted); }
.dg .phase { font-family: var(--font-display); font-weight: 600; font-size: 11px; letter-spacing: 0.08em; fill: var(--muted); }
.dg .box { fill: var(--surface); stroke: var(--line); stroke-width: 1.2; }
.dg .k-q .box { fill: var(--accent-soft); stroke: var(--accent); }
.dg .k-e .box { fill: var(--surface); stroke: var(--edge); }
.dg .k-p .box { fill: var(--surface); stroke: var(--ink); }
.dg .k-m .box { fill: var(--mech-soft); stroke: var(--mech); }
.dg .k-g .box { fill: var(--good-soft); stroke: var(--good); }
.dg .k-w .box { fill: var(--warn-soft); stroke: var(--warn); }
.dg .k-s .box { fill: var(--surface); stroke: var(--warn); stroke-dasharray: 4 3; }
.dg .edge { fill: none; stroke: var(--edge); stroke-width: 1.3; }
.dg .edge.long { stroke-dasharray: 5 4; }
.dg .edge.dashed { stroke-dasharray: 6 5; }
.dg .ah path { fill: var(--edge); }
.dg .ah-hi path { fill: var(--accent); }
.dg .elabel { font-family: var(--font-display); font-size: 12px; font-weight: 600; fill: var(--muted); }
.dg .band { fill: var(--band); } .dg .band.alt { fill: transparent; }
.dg .fnote .box { fill: var(--surface); stroke: var(--line); stroke-dasharray: 3 3; }
.dg .link { stroke: var(--edge); stroke-dasharray: 2 3; fill: none; }
.graph .node { cursor: pointer; transition: opacity 0.15s; }
.graph .edge { transition: opacity 0.15s, stroke 0.15s; }
.graph.focusing .node { opacity: 0.22; }
.graph.focusing .node.lit { opacity: 1; }
.graph.focusing .edge { opacity: 0.08; }
.graph.focusing .edge.lit { opacity: 1; stroke: var(--accent); stroke-width: 2.2; marker-end: url(#am-ah-hi); }

/* flooding */
.flood .tok rect { fill: var(--surface); stroke: var(--edge); stroke-width: 1.2; }
.flood .tok text { font-family: var(--font-display); font-weight: 600; font-size: 15px; }
.flood .tok.blocked.by-min rect { fill: var(--warn-soft); stroke: var(--warn); }
.flood .tok.blocked.by-min text { fill: var(--warn); text-decoration: line-through; }
.flood .tok.blocked.by-maj rect { fill: var(--band); stroke: var(--edge); stroke-dasharray: 3 2; }
.flood .tok.blocked.by-maj text { fill: var(--muted); text-decoration: line-through; }
.flood .tok.win rect { fill: var(--good-soft); stroke: var(--good); stroke-width: 2; }

/* the θ chart */
.chart .grid { stroke: var(--line); stroke-width: 1; }
.chart .tick { font-size: 11px; fill: var(--muted); font-variant-numeric: tabular-nums; }
.chart .axis { font-size: 11.5px; fill: var(--muted); }
.chart .line { fill: none; stroke-width: 2.2; }
.chart .line.c1, .chart .dot.c1 { stroke: var(--c1); } .chart .dot.c1, .chart .endlab.c1 { fill: var(--c1); }
.chart .line.c2, .chart .dot.c2 { stroke: var(--c2); } .chart .dot.c2, .chart .endlab.c2 { fill: var(--c2); }
.chart .line.c3, .chart .dot.c3 { stroke: var(--c3); } .chart .dot.c3, .chart .endlab.c3 { fill: var(--c3); }
.chart .line.c4, .chart .dot.c4 { stroke: var(--c4); } .chart .dot.c4, .chart .endlab.c4 { fill: var(--c4); }
.chart .endlab { font-family: var(--font-display); font-weight: 600; font-size: 12px; }
.chart .regime { fill: var(--band); }
.chart .regime.sweet { fill: var(--good-soft); }
.chart .reglab { font-family: var(--font-display); font-size: 11.5px; font-weight: 600; fill: var(--muted); }
.chart .mark { stroke: var(--edge); stroke-dasharray: 3 3; }
.chart .mark.main { stroke: var(--ink); stroke-dasharray: none; stroke-width: 1.4; }
.chart .marklab { font-family: var(--font-display); font-size: 11.5px; fill: var(--muted); }
.chart .marklab.main { fill: var(--ink); font-weight: 600; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 999px; overflow: hidden; background: var(--surface); }
.seg button { font-family: var(--font-display); font-size: 0.9rem; border: 0; background: transparent; color: var(--ink);
  padding: 0.25rem 0.9rem; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--ink); color: var(--bg); }

/* hull */
.hullbox { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 1.2rem; align-items: start; }
.hull { width: 100%; height: auto; display: block; touch-action: none; cursor: crosshair; }
.hull .frame { fill: var(--surface); stroke: var(--line); }
.hull .hullpoly { fill: var(--accent-soft); stroke: var(--accent); stroke-width: 1.4; }
.hull .halfplane { fill: var(--good-soft); opacity: 0.8; }
.hull .bisector { stroke: var(--good); stroke-dasharray: 5 4; stroke-width: 1.4; }
.hull .voter { fill: var(--surface); stroke: var(--ink); stroke-width: 1.3; }
.hull .voter.keeps { fill: var(--warn); stroke: var(--warn); }
.hull .sq { fill: var(--ink); }
.hull .prop { fill: var(--good); }
.hull text { font-family: var(--font-display); font-size: 13px; font-weight: 600; fill: var(--ink); }
.readout { display: grid; gap: 0.7rem; align-content: start; }
.readout .big { font-family: var(--font-display); font-size: 1.25rem; font-weight: 600; }
.readout .big.stuck { color: var(--warn); }
.readout .big.passes { color: var(--good); }
.controls { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; }
.controls label { font-size: 0.9rem; color: var(--muted); }
.controls input[type=range] { width: 160px; accent-color: var(--accent); }
.btn { font-family: var(--font-display); font-size: 0.9rem; border: 1px solid var(--line); border-radius: 999px;
  background: var(--surface); color: var(--ink); padding: 0.25rem 0.9rem; cursor: pointer; }
.btn:hover { border-color: var(--accent); color: var(--accent); }

/* example E1 */
.trace { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 0.8rem; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 0.9rem 1rem;
  display: grid; gap: 0.45rem; align-content: start; }
.card table { border-collapse: collapse; font-size: 0.92rem; }
.card td, .card th { padding: 0.2rem 0.6rem 0.2rem 0; text-align: left; font-variant-numeric: tabular-nums; }
.card th { font-family: var(--font-display); font-weight: 600; font-size: 0.8rem; color: var(--muted); letter-spacing: 0.05em; text-transform: uppercase; }
.out-b { color: var(--good); font-weight: 600; } .out-a { color: var(--accent); font-weight: 600; }
.x { color: var(--warn); text-decoration: line-through; }

.open { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.8rem; }
.open .card h3 { font-size: 1rem; }
.open .card p { font-size: 0.92rem; color: var(--muted); }
footer { padding-block: 2.4rem 0; color: var(--muted); font-size: 0.85rem; }

@media (max-width: 760px) {
  .hullbox { grid-template-columns: 1fr; }
  .narrow-hint { display: block; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""


def page():
    k = KN
    facts = f"""
  <div class="facts">
    <div class="fact warn"><b>{k['deadlockUnanimity']}%</b><span>of 101-voter elections in which unanimity keeps the status quo</span></div>
    <div class="fact good"><b>{k['contestedSchulze']}% → {k['contestedQVC']}%</b><span>outcomes vetoed by a third: Schulze, then QVC(1/3), polarised electorate</span></div>
    <div class="fact good"><b>{k['worstoffSchulze']} → {k['worstoffQVC']}</b><span>worst-off efficiency, with total utility {k['utilitySchulze']} → {k['utilityQVC']}</span></div>
    <div class="fact"><b>{k['clonesQVC']}%</b><span>of elections in which clones change the QVC winner; up to {k['clonesPVC']}% for the proportional veto core</span></div>
    <div class="fact warn"><b>{k['manipQVCSpatial']}–{k['manipQVCPolarised']}%</b><span>manipulable by 10% coalitions under QVC(1/3), against {k['manipSchulzeSpatial']}–{k['manipSchulzePolarised']}% under Schulze: the price</span></div>
  </div>"""
    body = f"""
<title>Voting with Veto Rights</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>{STYLE}</style>

<div class="wrap">
<header>
  <span class="eyebrow">A state-of-the-art note · v0.1.1</span>
  <h1>Voting for a consensus with veto rights</h1>
  <p class="lead">A group must choose one option. Anyone may propose as many options as they wish (H1), everyone
  judges every option (H2), and everyone can veto (H3). The procedure must reach the best compromise (R1) and never
  get stuck (R2). The two requirements pull against each other: a veto protects minorities and blocks decisions.</p>
  <div class="answer">
    <span class="eyebrow">The answer: QVC(θ), Condorcet with a blocking quota, θ = 1/3</span>
    <ol>
      <li>Each voter ranks every option and marks the unacceptable ones.</li>
      <li>Options vetoed by at least a share θ of the voters are excluded.</li>
      <li>If that excludes every option, the least-vetoed ones are kept.</li>
      <li>The Schulze winner among the options left is elected.</li>
    </ol>
  </div>
  {facts}
  <nav class="toc" aria-label="Sections">
    <a href="#map">The argument</a>
    <a href="#steps">Step by step</a>
    <a href="#example">Example E1</a>
    <a href="#deadlock">Why unanimity deadlocks</a>
    <a href="#flooding">Why flooding matters</a>
    <a href="#dial">The θ dial</a>
    <a href="#open">Open questions</a>
  </nav>
</header>

<section id="map" aria-labelledby="map-h">
  <h2 id="map-h">The argument in one map</h2>
  <p>Each column answers the one before it. The requirements meet results that no procedure escapes; these fix
  six design principles; each principle becomes one part of the procedure; the parts give four guarantees, and
  one price, which the safeguards contain. Dashed links skip a column.</p>
  <div class="legend">
    <span style="--k: var(--accent-soft); --kb: var(--accent)">Question</span>
    <span style="--k: var(--surface); --kb: var(--edge)">Theory and evidence</span>
    <span style="--k: var(--surface); --kb: var(--ink)">Principle</span>
    <span style="--k: var(--mech-soft); --kb: var(--mech)">Mechanism</span>
    <span style="--k: var(--good-soft); --kb: var(--good)">Guarantee</span>
    <span style="--k: var(--warn-soft); --kb: var(--warn)">Price</span>
  </div>
  <p class="hint">Hover over or tap a box to follow everything it rests on and everything that rests on it. Tap
  again to release it.</p>
  <p class="hint narrow-hint">Scroll the diagram sideways.</p>
  <div class="figure wide">{argument_map()}</div>
</section>

<section id="steps" aria-labelledby="steps-h">
  <h2 id="steps-h">QVC(θ), step by step</h2>
  <p>One ballot round, one count, and at most one revision round. The boxes on the left are the propositions of
  the note, attached to the step where they apply.</p>
  <p class="hint narrow-hint">Scroll the diagram sideways.</p>
  <div class="figure wide">{flowchart()}</div>
</section>

<section id="example" aria-labelledby="ex-h">
  <h2 id="ex-h">Example E1 through the count</h2>
  <p>The example behind Proposition 1. A majority's favourite that a large minority cannot accept, and a
  compromise that everyone ranks first or second. The quota decides between them.</p>
  <div class="trace">
    <div class="card">
      <h3>The ballots, 100 voters</h3>
      <table>
        <tr><th>Voters</th><th>Ranking</th><th>Veto</th></tr>
        <tr><td>51</td><td>A ≻ B ≻ C</td><td>C</td></tr>
        <tr><td>49</td><td>B ≻ C ≻ A</td><td>A</td></tr>
      </table>
      <p class="hint">A beats B and C, 51 to 49: it is the Condorcet winner.</p>
    </div>
    <div class="card">
      <h3>Veto counts</h3>
      <table>
        <tr><th>Option</th><th>v(x)</th></tr>
        <tr><td>A</td><td>49</td></tr>
        <tr><td>B</td><td>0</td></tr>
        <tr><td>C</td><td>51</td></tr>
      </table>
    </div>
    <div class="card">
      <h3>The outcome depends on θ</h3>
      <table>
        <tr><th>Quota</th><th>θn</th><th>Admissible</th><th>Winner</th></tr>
        <tr><td>1/4</td><td>25</td><td><span class="x">A</span> B <span class="x">C</span></td><td class="out-b">B</td></tr>
        <tr><td>1/3</td><td>33.3</td><td><span class="x">A</span> B <span class="x">C</span></td><td class="out-b">B</td></tr>
        <tr><td>1/2</td><td>50</td><td>A B <span class="x">C</span></td><td class="out-a">A</td></tr>
        <tr><td>none</td><td>–</td><td>A B C</td><td class="out-a">A</td></tr>
      </table>
      <p class="hint">Below 49%, the minority's veto excludes A and the compromise B wins. From 49% up, the
      majority's A wins. Choosing θ is choosing between them.</p>
    </div>
  </div>
</section>

<section id="deadlock" aria-labelledby="dl-h">
  <h2 id="dl-h">Why unanimity deadlocks: the status quo inside the hull</h2>
  <p>Each voter prefers options closer to their ideal point. A proposal y beats the status quo s for a voter on
  y's side of the perpendicular bisector of s and y. If s lies inside the convex hull of the ideal points, every
  such half-plane misses at least one voter: someone always prefers s, and under unanimity s stays
  (Proposition 2). With more voters, the hull covers s almost surely. In the simulations, unanimity keeps the
  status quo in {k['deadlockUnanimityThree']}% of elections with 3 voters, {k['deadlockUnanimityEleven']}% with 11
  and {k['deadlockUnanimity']}% with 101.</p>
  <div class="hullbox">
    <div class="figure"><svg class="hull" id="hull" viewBox="0 0 520 400" role="img" aria-labelledby="hull-t">
      <title id="hull-t">Voters' ideal points, their convex hull, the status quo and a proposal</title></svg></div>
    <div class="readout">
      <div class="controls">
        <label for="nvoters">Voters: <b id="nval">11</b></label>
        <input type="range" id="nvoters" min="3" max="60" value="11">
        <button class="btn" type="button" id="redraw">Draw new voters</button>
      </div>
      <p class="hint">Tap or drag anywhere in the picture to move the proposal y.</p>
      <div class="big" id="verdict"></div>
      <p id="detail"></p>
      <div class="legend">
        <span style="--k: var(--accent-soft); --kb: var(--accent)">Convex hull of the voters</span>
        <span style="--k: var(--good-soft)">Side where y is preferred</span>
        <span style="--k: var(--warn)">Voters who keep s</span>
      </div>
    </div>
  </div>
</section>

<section id="flooding" aria-labelledby="fl-h">
  <h2 id="fl-h">Why flooding matters: proportional veto against the blocking quota</h2>
  <p>Under an open agenda, a faction can add variants of its favourite. The proportional veto core gives a
  coalition a share of vetoes equal to its share of voters, counted in options, so every variant the majority
  adds dilutes the minority's vetoes (Proposition 3). Under the blocking quota a variant inherits the vetoes of
  its original, so it is excluded with it (Proposition 7). Examples E1 and E2: the majority adds A₂ and A₃,
  which it ranks just below A and the minority ranks last and vetoes.</p>
  <div class="figure">{flooding()}</div>
  <p class="hint">In the simulations, three clones of a losing option change the winner of the proportional veto
  core in up to {k['clonesPVC']}% of elections, of fallback bargaining in up to {k['clonesFallback']}%, of Borda
  in up to {k['clonesBorda']}%, and of Schulze and QVC in {k['clonesSchulze']}%.</p>
</section>

<section id="dial" aria-labelledby="dial-h">
  <h2 id="dial-h">The θ dial: majority at one end, minority protection at the other</h2>
  <p>A low quota gives every small group a veto: the fallback decides most elections, the result is close to
  approval voting, and small coalitions can steer it. A high quota never binds and leaves the majority alone.
  Between 25% and 40%, the veto excludes what a substantial minority rejects and the majority decides among the
  rest. One third sits there, close to the European Union's 35% blocking minority.</p>
  <div class="controls">
    <div class="seg" role="group" aria-label="Electorate">
      <button type="button" aria-pressed="true" data-culture="polarised">Polarised, 55/45</button>
      <button type="button" aria-pressed="false" data-culture="spatial">Spatial</button>
    </div>
  </div>
  <div class="figure">{theta_chart()}</div>
  <p class="hint">Simulation of the note: 101 voters, 8 options, 1,000 elections per electorate (300 for
  manipulability). Efficiency: 0 for the average option, 100 for the best; worst-off: the voter at the 10th
  percentile. A single veto is plotted at 1%.</p>
</section>

<section id="open" aria-labelledby="open-h">
  <h2 id="open-h">What remains open</h2>
  <div class="open">
    <div class="card"><h3>A clone-proof proportional veto?</h3><p>The proportional veto core resists strategic
    blocking but not flooding; the blocking quota resists flooding but not strategic blocking. Can one rule have
    clone independence, veto power proportional to size and a non-empty core?</p></div>
    <div class="card"><h3>Fast procedures with hard vetoes</h3><p>One- and two-round proposal procedures reach the
    Condorcet winner quickly with single-peaked preferences. With binding vetoes and several dimensions, nobody
    knows yet.</p></div>
    <div class="card"><h3>Do named vetoes work?</h3><p>Responsibility changes votes in committees, and tacit consent
    keeps formal vetoes in check. A laboratory test of QVC with and without named, reasoned vetoes would settle
    it.</p></div>
    <div class="card"><h3>Real ballots</h3><p>The simulations use stylised electorates. Ranked ballots with an
    acceptability line exist, in Debian's general resolutions among others, and would test the conclusions on
    observed preferences.</p></div>
  </div>
</section>

<footer>From the note "Voting for a consensus with veto rights", v0.1.1, October 2026. Numbers from its
simulations; propositions as numbered in the note.</footer>
</div>
"""
    return body + SCRIPT


SCRIPT = r"""
<script>
(function () {
  /* ---- the argument map: follow a box's chain both ways ---- */
  var svg = document.getElementById("argmap");
  if (svg) {
    var nodes = {}, out = {}, inn = {}, edges = [];
    svg.querySelectorAll(".node").forEach(function (n) { nodes[n.dataset.id] = n; out[n.dataset.id] = []; inn[n.dataset.id] = []; });
    svg.querySelectorAll(".edge").forEach(function (e) {
      var a = e.dataset.from, b = e.dataset.to; edges.push(e); out[a].push(b); inn[b].push(a);
    });
    var pinned = null;
    function reach(start, adj) {
      var seen = {}, stack = [start];
      while (stack.length) { var x = stack.pop(); (adj[x] || []).forEach(function (y) { if (!seen[y]) { seen[y] = 1; stack.push(y); } }); }
      return seen;
    }
    function light(id) {
      var down = reach(id, out), up = reach(id, inn);
      svg.classList.add("focusing");
      Object.keys(nodes).forEach(function (k) { nodes[k].classList.toggle("lit", k === id || down[k] || up[k]); });
      edges.forEach(function (e) {
        var a = e.dataset.from, b = e.dataset.to;
        var onDown = (a === id || down[a]) && down[b];
        var onUp = (b === id || up[b]) && up[a];
        e.classList.toggle("lit", !!(onDown || onUp));
      });
    }
    function clear() {
      svg.classList.remove("focusing");
      svg.querySelectorAll(".lit").forEach(function (x) { x.classList.remove("lit"); });
    }
    Object.keys(nodes).forEach(function (k) {
      var n = nodes[k];
      n.addEventListener("mouseenter", function () { if (!pinned) light(k); });
      n.addEventListener("mouseleave", function () { if (!pinned) clear(); });
      n.addEventListener("focus", function () { if (!pinned) light(k); });
      n.addEventListener("blur", function () { if (!pinned) clear(); });
      n.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (pinned === k) { pinned = null; clear(); } else { pinned = k; light(k); }
      });
      n.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); n.dispatchEvent(new MouseEvent("click")); }
      });
    });
    svg.addEventListener("click", function () { pinned = null; clear(); });
  }

  /* ---- the θ chart: switch electorate ---- */
  document.querySelectorAll(".seg button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".seg button").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      document.querySelectorAll(".chart .culture").forEach(function (g) { g.hidden = g.dataset.culture !== b.dataset.culture; });
    });
  });

  /* ---- the hull: Proposition 2 ---- */
  var hs = document.getElementById("hull");
  if (!hs) return;
  var NS = "http://www.w3.org/2000/svg", W = 520, H = 400, S = { x: 250, y: 205 }, Y = { x: 400, y: 110 };
  var seed = 7, pts = [];
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  function gauss() { var u = 0, v = 0; while (u === 0) u = rnd(); v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  function draw(n) {
    pts = [];
    for (var i = 0; i < n; i++) {
      var x = S.x + gauss() * 85, y = S.y + gauss() * 70;
      pts.push({ x: Math.max(16, Math.min(W - 16, x)), y: Math.max(16, Math.min(H - 16, y)) });
    }
  }
  function hull(p) {
    var a = p.slice().sort(function (u, v) { return u.x - v.x || u.y - v.y; });
    function cross(o, u, v) { return (u.x - o.x) * (v.y - o.y) - (u.y - o.y) * (v.x - o.x); }
    var lo = [], up = [];
    a.forEach(function (q) { while (lo.length >= 2 && cross(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); });
    a.slice().reverse().forEach(function (q) { while (up.length >= 2 && cross(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q); });
    return lo.slice(0, -1).concat(up.slice(0, -1));
  }
  function inside(poly, q) {
    if (poly.length < 3) return false;
    var sign = 0;
    for (var i = 0; i < poly.length; i++) {
      var a = poly[i], b = poly[(i + 1) % poly.length];
      var c = (b.x - a.x) * (q.y - a.y) - (b.y - a.y) * (q.x - a.x);
      if (c !== 0) { if (sign === 0) sign = Math.sign(c); else if (Math.sign(c) !== sign) return false; }
    }
    return true;
  }
  function el(tag, attrs, text) {
    var e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text) e.textContent = text;
    return e;
  }
  /* the half-plane where y is preferred to s, clipped to the frame */
  function halfPlane() {
    var mx = (S.x + Y.x) / 2, my = (S.y + Y.y) / 2, dx = Y.x - S.x, dy = Y.y - S.y;
    var poly = [{ x: 0, y: 0 }, { x: W, y: 0 }, { x: W, y: H }, { x: 0, y: H }], res = [];
    function side(p) { return (p.x - mx) * dx + (p.y - my) * dy; }
    for (var i = 0; i < poly.length; i++) {
      var a = poly[i], b = poly[(i + 1) % poly.length], sa = side(a), sb = side(b);
      if (sa > 0) res.push(a);
      if ((sa > 0) !== (sb > 0)) { var t = sa / (sa - sb); res.push({ x: a.x + t * (b.x - a.x), y: a.y + t * (b.y - a.y) }); }
    }
    return { poly: res, side: side, mx: mx, my: my, dx: dx, dy: dy };
  }
  function render() {
    while (hs.lastChild && hs.lastChild.tagName !== "title") hs.removeChild(hs.lastChild);
    hs.appendChild(el("rect", { class: "frame", x: 0.5, y: 0.5, width: W - 1, height: H - 1, rx: 6 }));
    var hp = halfPlane();
    if (hp.poly.length) hs.appendChild(el("polygon", { class: "halfplane", points: hp.poly.map(function (p) { return p.x + "," + p.y; }).join(" ") }));
    var L = 1000, nx = -hp.dy, ny = hp.dx, len = Math.hypot(nx, ny) || 1;
    hs.appendChild(el("line", { class: "bisector", x1: hp.mx - nx / len * L, y1: hp.my - ny / len * L, x2: hp.mx + nx / len * L, y2: hp.my + ny / len * L }));
    var hv = hull(pts);
    hs.appendChild(el("polygon", { class: "hullpoly", points: hv.map(function (p) { return p.x + "," + p.y; }).join(" ") }));
    var keep = 0;
    pts.forEach(function (p) {
      var prefersS = Math.hypot(p.x - S.x, p.y - S.y) <= Math.hypot(p.x - Y.x, p.y - Y.y);
      if (prefersS) keep++;
      hs.appendChild(el("circle", { class: "voter" + (prefersS ? " keeps" : ""), cx: p.x, cy: p.y, r: 4.5 }));
    });
    hs.appendChild(el("circle", { class: "sq", cx: S.x, cy: S.y, r: 7 }));
    hs.appendChild(el("text", { x: S.x + 11, y: S.y + 5 }, "s"));
    hs.appendChild(el("circle", { class: "prop", cx: Y.x, cy: Y.y, r: 7 }));
    hs.appendChild(el("text", { x: Y.x + 11, y: Y.y + 5 }, "y"));
    var inHull = inside(hv, S), n = pts.length;
    var v = document.getElementById("verdict"), d = document.getElementById("detail");
    if (keep > 0) {
      v.textContent = keep + " of " + n + " voters prefer s: unanimity keeps the status quo.";
      v.className = "big stuck";
    } else {
      v.textContent = "All " + n + " voters prefer y: it passes, even under unanimity.";
      v.className = "big passes";
    }
    d.textContent = inHull
      ? "s lies inside the hull of the voters, so wherever you put y, someone prefers s. Try it."
      : "s lies outside the hull of the voters, so some proposal can beat it unanimously: move y towards the voters, away from s.";
  }
  function setY(ev) {
    var r = hs.getBoundingClientRect();
    Y = { x: (ev.clientX - r.left) / r.width * W, y: (ev.clientY - r.top) / r.height * H };
    render();
  }
  var dragging = false;
  hs.addEventListener("pointerdown", function (ev) { dragging = true; try { hs.setPointerCapture(ev.pointerId); } catch (e) {} setY(ev); });
  hs.addEventListener("pointermove", function (ev) { if (dragging) setY(ev); });
  hs.addEventListener("pointerup", function () { dragging = false; });
  var slider = document.getElementById("nvoters"), nval = document.getElementById("nval");
  slider.addEventListener("input", function () { nval.textContent = slider.value; seed = 7; draw(+slider.value); render(); });
  document.getElementById("redraw").addEventListener("click", function () { seed = (seed * 48271 + 11) % 2147483647 || 3; draw(+slider.value); render(); });
  draw(11); render();
})();
</script>
"""

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font: 14px system-ui, sans-serif; } img { max-width: 100%; } [hidden] { display: none !important; }</style>
</head>
<body>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fragment", metavar="OUT", help="write the page without <!doctype>, <head> and <body> to OUT")
    args = ap.parse_args()
    if args.fragment:
        out, text = args.fragment, page()
    else:
        head, body = page().split('<div class="wrap">', 1)            # title, fonts and styles go to <head>
        text = HEAD.replace("</head>", head.strip() + "\n</head>") + '<div class="wrap">' + body + "</body>\n</html>\n"
        out = OUT
    with open(out, "w", encoding="utf8") as fh:
        fh.write(text)
    print(f"  {out}: {len(text) // 1024} KB")


if __name__ == "__main__":
    main()

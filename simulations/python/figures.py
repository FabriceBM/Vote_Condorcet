"""Figures of the note, drawn from the tables written by experiments.py (outputs/tables/*.csv).

    fig_theta     QVC: what the blocking quota theta buys and costs (table theta_sweep), two panels;
                  also fig_theta_fr, the same with French labels, for the French executive summary
    fig_deadlock  unanimity with the status quo as default against QVC as the assembly grows (deadlock_n)

Writes outputs/figures/<name>.pdf (label fig:<name without fig_>). Run from the repository root, after
experiments.py:
    python3 simulations/python/figures.py
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt     # noqa: E402

TABLES = os.environ.get("TAB_DIR", "outputs/tables")
FIGURES = os.environ.get("FIG_DIR", "outputs/figures")

# categorical slots 1-4 of the reference palette (validated for adjacent-pair CVD separation); markers and
# direct labels carry identity too, for print and colour-blind readers
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MARKERS = ["o", "s", "^", "D"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
    "pdf.fonttype": 42,
})


def read(name):
    with open(os.path.join(TABLES, f"{name}.csv"), encoding="utf8") as fh:
        rows = list(csv.reader(fh))
    return rows[0], rows[1:]


def direct_labels(ax, ends, x):
    """Label each line at its right end, spreading labels that would overlap."""
    ends = sorted(ends, key=lambda t: t[0])
    placed = []
    for y, text in ends:
        if placed and y - placed[-1] < 11:
            y = placed[-1] + 11
        placed.append(y)
        ax.annotate(text, (x, y), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8,
                    color=INK, annotation_clip=False)


THETA_TEXT = {
    "en": {"series": ["Condorcet efficiency", "Worst-off efficiency", "Fallback", "Manipulable (10%)"],
           "titles": ["Spatial", "Polarised"], "xlabel": r"Blocking quota $\theta$ (%)", "name": "fig_theta"},
    "fr": {"series": ["Efficacité de Condorcet", "Efficacité (moins bien lotis)", "Repli",
                      "Manipulable (10 %)"],
           "titles": ["Spatial", "Polarisé"], "xlabel": r"Quota $\theta$ (en %)",
           "name": "fig_theta_fr"},
}


def fig_theta(lang="en"):
    text = THETA_TEXT[lang]
    header, rows = read("theta_sweep")
    col = {h: k for k, h in enumerate(header)}
    series = list(zip(["Condorcet eff. (%)", "Worst-off eff. (%)", "Fallback (%)", "Manip. 10% (%)"],
                      text["series"]))
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0), sharey=True)
    for ax, culture, title in zip(axes, ("Spatial", "Polarised"), text["titles"]):
        sub = [r for r in rows if r[0].startswith(culture) and "none" not in r[0]]
        theta = [100 / 101 if "1/n" in r[0] else float(r[0].split(", ")[1].rstrip("%")) for r in sub]
        ends = []
        for k, (h, label) in enumerate(series):
            y = [float(r[col[h]]) for r in sub]
            ax.plot(theta, y, color=SERIES[k], lw=1.6, marker=MARKERS[k], ms=3.5, mec="white", mew=0.6,
                    label=label, solid_capstyle="round")
            ends.append((y[-1], label))
        ax.axvline(100 / 3, color=MUTED, lw=0.8)
        ax.text(100 / 3, 103, r"$\theta=1/3$", ha="center", va="bottom", fontsize=8, color=MUTED)
        ax.set_title(title, fontsize=9, color=INK, loc="left", pad=12)
        ax.set_xlim(0, 50)
        ax.set_ylim(0, 100)
        ax.set_xticks([0, 10, 20, 30, 40, 50])
        ax.set_xlabel(text["xlabel"])
    axes[0].set_ylabel("%")
    direct_labels(axes[1], ends, 50)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.07, 0.86 if lang == "en" else 0.82, 1))
    save(fig, text["name"])


def fig_deadlock():
    header, rows = read("deadlock_n")
    n = [int(r[0]) for r in rows]
    series = [(1, "Status quo Pareto-optimal"), (2, "Unanimity: deadlock"), (4, "QVC 25%: fallback"),
              (5, "QVC 33%: fallback")]
    fig, ax = plt.subplots(figsize=(5.8, 2.8))
    ends = []
    for k, (c, label) in enumerate(series):
        y = [float(r[c]) for r in rows]
        ax.plot(n, y, color=SERIES[k], lw=1.6, marker=MARKERS[k], ms=3.5, mec="white", mew=0.6, label=label)
        ends.append((y[-1], label))
    ax.set_xscale("log")
    ax.set_xticks(n)
    ax.set_xticklabels([str(v) for v in n])
    ax.minorticks_off()
    ax.set_ylim(0, 100)
    ax.set_xlabel("Number of voters (log scale)")
    ax.set_ylabel("% of elections")
    direct_labels(ax, ends, n[-1])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=8)
    fig.tight_layout(rect=(0, 0, 0.78, 1))
    save(fig, "fig_deadlock")


def save(fig, name):
    os.makedirs(FIGURES, exist_ok=True)
    fig.savefig(os.path.join(FIGURES, f"{name}.pdf"), bbox_inches="tight",
                metadata={"CreationDate": None})                                    # reproducible file
    fig.savefig(os.path.join(FIGURES, f"{name}.png"), bbox_inches="tight", dpi=150)   # preview only
    plt.close(fig)
    print(f"  {name}")


if __name__ == "__main__":
    fig_theta()
    fig_theta("fr")
    fig_deadlock()

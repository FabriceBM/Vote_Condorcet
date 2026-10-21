"""Random elections ("cultures") for the Monte Carlo study of the note.

Every culture draws one decision: n voters, m options of which the last is the status quo. Options other
than the status quo are open proposals: each is put forward by a voter drawn at random, near that voter's
ideal point, so that active blocs propose more and near-duplicates (clones) arise naturally.

    spatial      voters' ideal points N(0, I_2); proposals at the proposer's ideal point + N(0, 0.25^2 I_2);
                 the status quo N(0, I_2). Utility = minus the Euclidean distance.
    polarised    two blocs, 55% around (-1.2, 0) and 45% around (+1.2, 0), within-bloc sd 0.6; otherwise as
                 spatial. Most proposals sit near a bloc; the few made by voters between the blocs are
                 compromises.
    impartial    utilities i.i.d. U(0, 1) (the impartial culture, no structure): the worst case for majority
                 rule, a benchmark only.
    spatial1d    as spatial on a line: preferences are single-peaked, a Condorcet winner always exists (odd n).

Vetoes: voter i finds option x acceptable if its utility is at least a personal threshold, fixed before the
proposals are known (a tolerance, not a share of the menu): distance <= rho_i with rho_i ~ U(1.25, 2.25)
in the spatial cultures (U(0.6, 1.1) on the line), utility >= tau_i with tau_i ~ U(0.2, 0.6) in the impartial
culture. A voter therefore vetoes about half of the options on average, and never an option ranked above
one they accept. Grades for Majority Judgment: 0 for a vetoed option; acceptable options graded 1-5 by
their utility relative to the threshold (an absolute scale, as Majority Judgment asks).
"""
import numpy as np

from voting import Election

CULTURES = ["spatial", "polarised", "impartial"]
LABELS = {"spatial": "Spatial (2D)", "polarised": "Polarised (55/45)", "impartial": "Impartial culture",
          "spatial1d": "Spatial (1D)"}


def _spatial(rng, n, m, centres=None, weights=None, sd=1.0, dim=2, rho=(1.5, 2.5)):
    if centres is None:
        V = rng.normal(0, sd, (n, dim))
    else:
        bloc = rng.choice(len(centres), size=n, p=weights)
        V = np.asarray(centres, float)[bloc] + rng.normal(0, sd, (n, dim))
    proposers = rng.integers(0, n, m - 1)
    X = np.vstack([V[proposers] + rng.normal(0, 0.25, (m - 1, dim)),   # open proposals
                   rng.normal(0, 1.0, (1, dim))])                       # status quo, last
    dist = np.linalg.norm(V[:, None, :] - X[None, :, :], axis=2)
    r = rng.uniform(*rho, (n, 1))
    acc = dist <= r
    G = np.where(acc, 1 + np.minimum(4, np.floor(5 * (1 - dist / r))).astype(int), 0)
    return Election(-dist, acc, sq=m - 1, G=G), V, X


def draw(culture, rng, n=101, m=8, positions=False):
    """One random election; with positions=True also the voters' and options' coordinates (spatial only)."""
    if culture == "spatial":
        e, V, X = _spatial(rng, n, m)
    elif culture == "polarised":
        e, V, X = _spatial(rng, n, m, centres=[(-1.2, 0), (1.2, 0)], weights=[0.55, 0.45], sd=0.6)
    elif culture == "spatial1d":
        e, V, X = _spatial(rng, n, m, dim=1, rho=(0.75, 1.25))
    elif culture == "impartial":
        U = rng.random((n, m))
        tau = rng.uniform(0.2, 0.5, (n, 1))
        acc = U >= tau
        G = np.where(acc, 1 + np.minimum(4, np.floor(5 * (U - tau) / (1 - tau))).astype(int), 0)
        e, V, X = Election(U, acc, sq=m - 1, G=G), None, None
    else:
        raise ValueError(culture)
    return (e, V, X) if positions else e


def add_clones(e, x, k, rng):
    """The election with k clones of option x added after the others: variants that every voter ranks next
    to x (above or below it, at random) and grades and vetoes as x (Tideman, 1987)."""
    Uc = e.U[:, [x]] + 1e-9 * (rng.random((e.n, k)) - 0.5)
    acc_c = np.repeat(e.acc[:, [x]], k, axis=1)
    G = None if e.G is None else np.c_[e.G, np.repeat(e.G[:, [x]], k, axis=1)]
    return Election(np.c_[e.U, Uc], np.c_[e.acc, acc_c], sq=e.sq, G=G)

#!/usr/bin/env python3
"""
Three slides for equations (8)-(10) on REAL data — the G01 -> G09
block of the 62-neuron hDelta->FB run (configuration 87ef7c02), the
largest gold edge of the run and the pathway slide's worked example.

  Slide 1: P_AB = 0.7 R_AB + 0.3 M_AB in full, then R (equation 8):
           the full W (group-sorted, viridis as on the SVD slide) with
           a connector from the gold-outlined block to the same block
           opened up with its 42 real weights and row sums. R = -15.18.
  Slide 2: M (equation 9): where omega comes from (the real Sigma
           diagonal, squared and shared out), mode 1 in full detail
           (u_1 / v_1 strips, the layer, the numbered block, its
           contribution -6.00), modes 2-9 as a table (together -0.01),
           and the blend M = -6.01.
  Slide 3: the payoff: the three equations with the real numbers
           substituted, P = -12.43, and the gold edge it buys.

Notation: R and the inner sum of M use the single summation over
ordered pairs, sum_{(a,b) in A x B} — one sum over the block's cells,
not a nested pair of sums. The outer sum of M (over modes) stays: it
does a different job (a weighted blend, sum_m omega_m = 1).

Heatmaps use the viridis colour scheme of the SVD slide so the
figures read as a continuation of it. Every number is computed from
the run's stored artifacts; slide 1's build asserts that G01 -> G09
really is the largest |P| of the 132 ordered group pairs.

DATA LOCATION: the script reads two files from the run's
processed-data folder -- z_matrix.42d6ad4c.npz and
eigen.42d6ad4c.json. It finds them in one of four ways (first match
wins):
  1. --data-dir <folder> on the command line, or
  2. the EIGEN_RUN_DIR environment variable, or
  3. the two files beside this script, or in the current working
     directory, or
  4. a data/processed/<dataset>/ folder beside this script (or beside
     its parent folder, or in the current working directory) -- i.e.
     drop the script into your eigen-decomposition project, or copy
     that processed folder next to it.
If none of those is found, the script stops with a message naming
the two files it needs instead of guessing a path. No path in this
file points at any one machine — same rule as
make_mode_block_eq9_real.py.

Outputs (in an output/ folder beside this script, created if needed):
  eq8-9-slide1.png, eq8-9-slide2.png, eq8-9-slide3.png
Run:    python make_eq8_9_slides.py [1|2|3|all] [--data-dir <folder>]
        (bare run = slide 1)
Needs:  matplotlib, numpy
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

DATASET = "hDelta_ABH_FB_15pre_001_merged_data_v1"
NEEDED = ("z_matrix.42d6ad4c.npz", "eigen.42d6ad4c.json")


def resolve_data_dir(cli_dir):
    """First folder holding both run files, or stop with directions."""
    here = Path(__file__).resolve().parent
    candidates = []
    if cli_dir:
        candidates.append(Path(cli_dir))
    if os.environ.get("EIGEN_RUN_DIR"):
        candidates.append(Path(os.environ["EIGEN_RUN_DIR"]))
    candidates += [here, Path.cwd()]
    rel = Path("data") / "processed" / DATASET
    candidates += [here / rel, here.parent / rel, Path.cwd() / rel]
    for cand in candidates:
        if all((cand / name).is_file() for name in NEEDED):
            return cand
    tried = "\n  ".join(str(c) for c in candidates)
    sys.exit(
        "make_eq8_9_slides.py: could not find the run data.\n"
        f"Needed files: {NEEDED[0]} and {NEEDED[1]}\n"
        "Point the script at the folder holding them, one of:\n"
        "  python make_eq8_9_slides.py all --data-dir <folder>\n"
        "  EIGEN_RUN_DIR=<folder> python make_eq8_9_slides.py all\n"
        "  or put the two files beside this script (or in the folder\n"
        "  you run it from), or in data/processed/" + DATASET + "/\n"
        "  beside this script.\n"
        f"Folders tried:\n  {tried}"
    )

OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BG = "#1E1E1E"
INK = "#D4D4D4"
DIM = "#9A9A9A"
FAINT = "#6A6A6A"
GOLD = "#E8A33D"
TEAL = "#4EC9B0"
PURPLE = "#C586C0"
TEAL_BG = "#12312B"
PURPLE_BG = "#2E1A2E"
VIRIDIS = plt.get_cmap("viridis")

GROUPS = {
    "G01": ["FB4F_b", "FB4I", "FB4K", "FB4P_a", "FB4X", "FB4Y(EB/NO1)", "FB5X"],
    "G02": ["FB4P_b", "hDeltaB0", "hDeltaB1", "hDeltaB20", "hDeltaB3",
            "hDeltaB4", "hDeltaB5", "hDeltaB9"],
    "G03": ["FB2F_b", "FB5A", "FB5D", "FB5E", "FB5K", "FB5O"],
    "G04": ["FB4B(NO2)", "FB4C(NO2)", "FB4G", "FB4J", "FB4N", "hDeltaB2",
            "hDeltaB42", "hDeltaB7", "hDeltaB8"],
    "G05": ["FB4F_a", "FB4M(PPM3-FB3/4-NO-DAN)", "FB4Q_a", "hDeltaA20"],
    "G06": ["FB5H", "FB5R", "FB5S", "FB5U", "hDeltaH2", "hDeltaH7", "hDeltaH8"],
    "G07": ["FB3A", "FB4D", "hDeltaB31", "hDeltaB6"],
    "G08": ["FB4Z", "hDeltaA31", "hDeltaA4", "hDeltaA7", "hDeltaA8"],
    "G09": ["hDeltaA0", "hDeltaA1", "hDeltaA2", "hDeltaA3", "hDeltaA42",
            "hDeltaA5"],
    "G10": ["FB1H(NO2/3)", "FB4L(PPM3-FB3/4-DAN)", "FB4R"],
    "G11": ["hDeltaH1", "hDeltaH3", "hDeltaH4"],
}
SRC, TGT = "G01", "G09"
SHORT = {"FB4Y(EB/NO1)": "FB4Y"}

FOOTER = ("Real data throughout: 62-neuron hDelta\u2192FB run, configuration "
          "87ef7c02 \u2014 $W$ from Phase 03; $U$, $\\Sigma$, $V^{T}$ from the "
          "Phase 04 SVD ($k$ = 9).")


def fmt(v, digits=2):
    return f"{v:+.{digits}f}".replace("-", "\u2212")


def fmt_small(v):
    if abs(v) < 0.005:
        return "\u2248 0.00"
    return fmt(v)

def fmt3(v):
    """Three-decimal signed value (the contribution column)."""
    s = f"{v:.3f}"
    if s in ("-0.000", "0.000"):
        return "0.000"
    s = s.replace("-", "\u2212")
    return ("+" + s) if v > 0 else s


def chain(fig, ax, cx, y, segments, fontsize, left=None):
    """Draw (text, kwargs) segments side by side, centred at cx
    (or starting at `left` when given). Returns each segment's
    (x0, x1, y_bottom, y_top) in data coords."""
    objs = [ax.text(0, y, t, fontsize=fontsize, ha="left", va="center",
                    **kw) for t, kw in segments]
    rend = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    spans = []
    for o in objs:
        bb = o.get_window_extent(renderer=rend)
        (xa, ya), (xb, yb) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        spans.append((xb - xa, ya, yb))
    x = left if left is not None else cx - sum(w for w, _, _ in spans) / 2
    out = []
    for o, (w, ya, yb) in zip(objs, spans):
        o.set_x(x)
        out.append((x, x + w, ya, yb))
        x += w
    return out



class Data:
    def __init__(self, data_dir):
        DATA_DIR = data_dir
        z = np.load(DATA_DIR / "z_matrix.42d6ad4c.npz", allow_pickle=True)
        self.W = z["matrix"]
        order = [str(x) for x in z["neuron_order"]]
        self.idx = {n: i for i, n in enumerate(order)}
        eig = json.loads((DATA_DIR / "eigen.42d6ad4c.json").read_text())
        modes = eig["modes"]
        self.sig = np.array([m["value"] for m in modes])
        self.U = np.column_stack([m["left"] for m in modes])
        self.Vt = np.row_stack([m["right"] for m in modes])
        self.layers = [self.sig[m] * np.outer(self.U[:, m], self.Vt[m])
                       for m in range(9)]
        self.omega = self.sig ** 2 / (self.sig ** 2).sum()
        self.A = [self.idx[n] for n in GROUPS[SRC]]
        self.B = [self.idx[n] for n in GROUPS[TGT]]
        self.block = self.W[np.ix_(self.A, self.B)]
        self.R = self.block.sum()
        self.row_sums = self.block.sum(axis=1)
        self.layer_blocks = [lay[np.ix_(self.A, self.B)] for lay in self.layers]
        self.block_sums = np.array([lb.sum() for lb in self.layer_blocks])
        self.contribs = self.omega * self.block_sums
        self.M = self.contribs.sum()
        self.P = 0.7 * self.R + 0.3 * self.M
        self.perm = [self.idx[n] for g in GROUPS.values() for n in g]
        self.col_off = sum(len(GROUPS[g]) for g in
                           list(GROUPS)[:list(GROUPS).index(TGT)])
        self.wnorm = Normalize(self.W.min(), self.W.max())

    def check(self):
        best = (None, 0.0)
        for ga, ma in GROUPS.items():
            for gb, mb in GROUPS.items():
                if ga == gb:
                    continue
                ia = [self.idx[n] for n in ma]
                ib = [self.idx[n] for n in mb]
                r = self.W[np.ix_(ia, ib)].sum()
                mm = sum(self.omega[m] * self.layers[m][np.ix_(ia, ib)].sum()
                         for m in range(9))
                p = abs(0.7 * r + 0.3 * mm)
                if p > best[1]:
                    best = ((ga, gb), p)
        assert best[0] == (SRC, TGT), f"largest |P| is {best}"
        print(f"verified: R={self.R:.2f} M={self.M:.2f} P={self.P:.2f} "
              f"is the largest |P| of the 132 ordered group pairs")


def canvas():
    fig = plt.figure(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_facecolor(BG)
    ax.axis("off")
    return fig, ax


def inset(fig, x, y, w, h):
    a = fig.add_axes([x / 16, y / 9, w / 16, h / 9])
    a.set_xticks([])
    a.set_yticks([])
    for s in a.spines.values():
        s.set_color("#3C3C3C")
    return a


def heat(a, mat, norm):
    a.imshow(mat, cmap=VIRIDIS, norm=norm, aspect="auto",
             interpolation="nearest")


def footer(ax, tag):
    ax.text(8, 0.16, FOOTER, ha="center", va="center", fontsize=8.5,
            color=FAINT)
    ax.text(15.72, 8.78, tag, ha="right", va="center", fontsize=9.5,
            color=FAINT)



def group_tile(ax, x, y, w, h, title, rows, title_fs=10.5, pill_fs=8.5):
    """A group box in the combined graph's style: dark rounded tile,
    group title, and the member neurons as pale pills inside."""
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.09",
                                facecolor="#141A22", edgecolor="#5A6B82",
                                linewidth=1.2))
    ax.text(x + 0.18, y + h - 0.24, title, fontsize=title_fs, color=INK,
            va="center", fontweight="bold")
    top = y + h - 0.50
    ph = 0.38
    for r, row in enumerate(rows):
        cy = top - r * (ph + 0.12) - ph / 2
        n = len(row)
        gap = 0.08
        pw = (w - 0.30 - (n - 1) * gap) / n
        for c, name in enumerate(row):
            px = x + 0.15 + c * (pw + gap)
            ax.add_patch(FancyBboxPatch(
                (px, cy - ph / 2), pw, ph,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                facecolor="#DDE3EC", edgecolor="none"))
            ax.text(px + pw / 2, cy, name, ha="center", va="center",
                    fontsize=pill_fs, color="#141A22")


# ---------------------------------------------------------------- slide 1
def slide1(d):
    fig, ax = canvas()
    spans = chain(fig, ax, 8, 8.58,
                  [(r"$P_{AB} \;=\; 0.7\,$", dict(color=INK)),
                   (r"$R_{AB}$", dict(color=GOLD, fontweight="bold")),
                   (r"$\;+\; 0.3\,M_{AB}$", dict(color=INK))], 23)
    ux0, ux1, uyb, _ = spans[1]
    ax.plot([ux0 + 0.02, ux1 - 0.02], [uyb - 0.05, uyb - 0.05],
            color=GOLD, lw=2.5, solid_capstyle="round")
    ax.text(8, 8.06, "the pathway weight behind the gold edges, worked on "
            "one block \u2014 G01 \u2192 G09, the strongest pair in the run",
            ha="center", va="center", fontsize=11.5, color=DIM)

    # the R definition, boxed (equation 9 belongs to slide 2)
    ax.add_patch(Rectangle((1.55, 7.36), 9.35, 0.52, facecolor="#26221A",
                           edgecolor=GOLD, linewidth=1.2))
    ax.text(1.85, 7.62, r"$R_{AB} = \sum_{(a,b)\,\in\,A \times B} w_{ab}$",
            fontsize=15.5, color=INK, va="center")
    ax.text(8.15, 7.62, "(raw block sum)", fontsize=11.5, color=DIM,
            va="center")
    ax.text(11.15, 7.62, "(8)", fontsize=11.5, color=FAINT, va="center")

    # the two groups, as tiles in the combined graph's style
    group_tile(ax, 0.45, 6.22, 7.15, 1.02, "G01 \u00b7 Mode 1 \u00b7 (F01)",
               [[SHORT.get(n, n) for n in GROUPS[SRC]]],
               title_fs=10, pill_fs=8.5)
    group_tile(ax, 8.40, 6.22, 7.15, 1.02, "G09 \u00b7 Mode 1 \u00b7 (F01)",
               [GROUPS[TGT]], title_fs=10, pill_fs=8.5)
    ax.add_patch(FancyArrowPatch((7.68, 6.73), (8.32, 6.73),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=GOLD, lw=2.0))

    # ---- W, group-sorted, with the block outlined
    wx, wy, ws = 0.45, 1.42, 4.30
    ax.text(wx + ws / 2, 5.92, "$W$ \u2014 the directed functional "
            "connectivity matrix, sorted by group",
            ha="center", va="center", fontsize=11, color=INK)
    aW = inset(fig, wx, wy, ws, ws)
    heat(aW, d.W[np.ix_(d.perm, d.perm)], d.wnorm)
    aW.add_patch(Rectangle((d.col_off - 0.5, -0.5), len(d.B), len(d.A),
                           facecolor="none", edgecolor=GOLD, linewidth=2.0))
    ax.text(wx + ws / 2, wy - 0.30, "gold box: rows of G01 \u00d7 columns "
            "of G09, top-right of $W$", ha="center", va="center",
            fontsize=9.5, color=FAINT)

    # ---- connector from the box to the opened-up block
    y_link = wy + ws - (3.5 / 62) * ws
    ax.add_patch(FancyArrowPatch((wx + ws + 0.03, y_link), (6.02, y_link),
                                 arrowstyle="-|>", mutation_scale=20,
                                 color=GOLD, lw=2.0))
    ax.text((wx + ws + 6.02) / 2, y_link + 0.24, "opened up",
            ha="center", va="center", fontsize=10, color=GOLD)

    # ---- the block, with numbers
    bx, by, bw, bh = 6.15, 2.08, 3.60, 3.36
    ax.text(bx + bw / 2, 5.92, "the block itself \u2014 G01's "
            "neurons \u2192 G09's neurons", ha="center", va="center",
            fontsize=11, color=INK)
    aB = inset(fig, bx, by, bw, bh)
    heat(aB, d.block, d.wnorm)
    for i in range(len(d.A)):
        for j in range(len(d.B)):
            aB.text(j, i, fmt(d.block[i, j]), ha="center", va="center",
                    fontsize=8.5, color="white")
    for i, n in enumerate(GROUPS[SRC]):
        ax.text(bx - 0.10, by + bh - (i + 0.5) * bh / len(d.A),
                SHORT.get(n, n), ha="right", va="center", fontsize=10,
                color=TEAL)
    for j, n in enumerate(GROUPS[TGT]):
        ax.text(bx + (j + 0.5) * bw / len(d.B), by + bh + 0.10,
                n.replace("hDelta", ""), ha="center", va="bottom",
                fontsize=10, color=PURPLE)
    ax.text(bx + bw + 0.42, by + bh + 0.10, "row \u03a3", ha="center",
            va="bottom", fontsize=10, color=DIM)
    for i in range(len(d.A)):
        ax.text(bx + bw + 0.42, by + bh - (i + 0.5) * bh / len(d.A),
                fmt(d.row_sums[i]), ha="center", va="center", fontsize=10,
                color=GOLD)
    ax.text(bx, by - 0.34, "columns: hDeltaA0 \u00b7 A1 \u00b7 A2 \u00b7 "
            "A3 \u00b7 A42 \u00b7 A5 \u2014 all of G09",
            fontsize=9.5, color=FAINT, va="center")
    ax.text(bx, by - 0.72,
            r"$\sum_{(a,b)\,\in\,A \times B} w_{ab} \;=\; R$"
            f" = the sum of all 42 cells = {fmt(d.R)}",
            fontsize=13.5, color=GOLD, va="center", fontweight="bold")

    # ---- reading notes, right (no omega, no forward references)
    nx = 11.05
    ax.text(nx, 5.92, "reading $R$", fontsize=12.5, color=INK, va="center")
    ax.text(nx, 5.54, "$R$ needs nothing but $W$ \u2014 add the\n"
            "wiring in the rectangle, signs included.",
            fontsize=10.5, color=DIM, va="top", linespacing=1.55)
    ax.text(nx, 4.72, "Every one of the 42 weights is negative,\n"
            "so the block is pre-dominant as a whole\n"
            "\u2014 nothing cancels.",
            fontsize=10.5, color=DIM, va="top", linespacing=1.55)
    ax.text(nx, 3.72, "FB4X is the faint row (\u22120.09\u2026\u22120.14);\n"
            "FB4P_a and FB4I carry the block\n"
            f"(row sums {fmt(d.row_sums[3])} and {fmt(d.row_sums[1])}).",
            fontsize=10.5, color=DIM, va="top", linespacing=1.55)
    ax.text(nx, 2.62, "The mirror block is a different sum:\n"
            "G09 \u2192 G01 reads the rectangle below\n"
            "the diagonal, with its own value \u2014\n"
            "direction is kept, never merged.",
            fontsize=10.5, color=DIM, va="top", linespacing=1.55)

    footer(ax, "equations (8)\u2013(10) \u00b7 slide 1 of 3")
    out = OUT_DIR / "eq8-9-slide1.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")


def strip_cells(ax, x, y, w, h, values, horizontal, bg, edge):
    """Toy-figure style u/v strips: solid cells with the value inside.
    (x, y) is the bottom-left of the whole strip."""
    n = len(values)
    for k, v in enumerate(values):
        if horizontal:
            cx, cy = x + k * w / n, y
            cw, ch = w / n, h
        else:
            cx, cy = x, y + h - (k + 1) * h / n
            cw, ch = w, h / n
        ax.add_patch(Rectangle((cx, cy), cw, ch, facecolor=bg,
                               edgecolor=edge, linewidth=0.9))
        ax.text(cx + cw / 2, cy + ch / 2, fmt(v), ha="center", va="center",
                fontsize=8.5, color="white")


# ---------------------------------------------------------------- slide 2
def slide2(d):
    fig, ax = canvas()
    ax.text(8, 8.66, "The mode block sum $M$ (equation 9) \u2014 the same "
            "block, read through the modes",
            ha="center", va="center", fontsize=17.5, color=INK)
    ax.text(8, 7.92, r"$M_{AB} = \sum_{m=1}^{9} \omega_m "
            r"\sum_{(a,b)\,\in\,A \times B} \sigma_m\, u_{am} v_{bm}$,"
            r"     $\omega_m = \dfrac{\sigma_m^2}{\sum_{j=1}^{9} \sigma_j^2}$",
            ha="center", va="center", fontsize=14.5, color=INK)
    ax.text(15.35, 7.92, "(9)", fontsize=11, color=FAINT, va="center")

    # ---- left: where omega comes from
    ax.text(0.40, 7.34, "where \u03c9 comes from \u2014 the \u03a3 diagonal",
            fontsize=12.5, color=INK, va="center")
    ax.text(1.36, 7.06, r"$\sigma_m$", fontsize=19, color=GOLD,
            ha="center", va="center")
    aS = inset(fig, 0.55, 5.22, 1.62, 1.62)
    heat(aS, np.diag(d.sig), Normalize(0, d.sig[0]))
    ax.add_patch(FancyArrowPatch((1.00, 6.96), (0.68, 6.78),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=GOLD, lw=1.6))
    ax.text(2.40, 7.10, "\u03c3\u2081 = 3.85 is the bright\ncorner cell; "
            "each step\ndown the diagonal is a\nweaker mode. Square\n"
            "the diagonal, share it\nout \u2014 that is \u03c9.",
            fontsize=10, color=DIM, va="top", linespacing=1.5)
    ax.text(0.55, 4.98, "the \u03a3 matrix: only the diagonal is non-zero",
            fontsize=9.5, color=FAINT, va="center")
    cols = (0.60, 1.45, 2.45, 3.45)
    for x, h in zip(cols, ("m", r"$\sigma_m$", r"$\sigma_m^2$",
                           r"$\omega_m$")):
        ax.text(x, 4.62, h, fontsize=9.5, color=FAINT, va="center")
    for m in range(9):
        y = 4.28 - m * 0.30
        c = GOLD if m == 0 else INK
        w = "bold" if m == 0 else "normal"
        ax.text(cols[0], y, str(m + 1), fontsize=11, color=c, va="center",
                fontweight=w)
        ax.text(cols[1], y, f"{d.sig[m]:.2f}", fontsize=11, color=c,
                va="center", fontweight=w)
        ax.text(cols[2], y, f"{d.sig[m] ** 2:.2f}", fontsize=11, color=c,
                va="center", fontweight=w)
        ax.text(cols[3], y, f"{d.omega[m]:.2f}", fontsize=11, color=c,
                va="center", fontweight=w)
    ax.text(0.40, 1.52, f"retained \u03c3\u00b2 total = "
            f"{(d.sig ** 2).sum():.2f} of $W$'s {(d.W ** 2).sum():.2f} (91%)",
            fontsize=9.5, color=DIM, va="center")
    ax.text(0.40, 1.24, "\u03c9\u2081 = 14.85 / 36.55 = 0.41 \u2014 mode 1 "
            "counts \u2248 16\u00d7 mode 9", fontsize=9.5, color=DIM,
            va="center")

    # ---- centre: mode 1 in full
    ax.text(4.75, 7.34, "mode 1 in full \u2014 the block inside "
            r"$\sigma_1 u_1 v_1^{T}$", fontsize=12.5, color=INK, va="center")
    aU = inset(fig, 5.05, 3.30, 0.66, 2.38)
    heat(aU, d.U, Normalize(d.U.min(), d.U.max()))
    aU.add_patch(Rectangle((-0.5, -0.5), 1, 62, facecolor="none",
                           edgecolor=GOLD, linewidth=1.8))
    ax.text(5.38, 3.04, "$U$ (yuu)", ha="center", va="center",
            fontsize=10.5, color=INK)
    ax.text(5.38, 2.78, "first column outlined", ha="center",
            va="center", fontsize=8.5, color=FAINT)
    ax.text(5.38, 2.54, "shown on its own scale", ha="center",
            va="center", fontsize=8.5, color=FAINT)
    ax.add_patch(FancyArrowPatch((5.76, 5.50), (6.83, 5.50),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=GOLD, lw=1.8))
    ax.text(6.35, 6.45, "\u00d7 \u03c3\u2081 = 3.85", ha="center",
            va="center", fontsize=11.5, color=GOLD)
    aV = inset(fig, 7.55, 6.42, 2.88, 0.48)
    heat(aV, d.Vt, Normalize(d.Vt.min(), d.Vt.max()))
    aV.add_patch(Rectangle((-0.5, -0.5), 62, 1, facecolor="none",
                           edgecolor=GOLD, linewidth=1.8))
    ax.text(7.55, 7.08, "$V^{T}$ (vee) \u2014 first row outlined",
            fontsize=9.5, color=PURPLE, va="center")
    ax.add_patch(FancyArrowPatch((10.15, 6.40), (10.15, 6.17),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=GOLD, lw=1.8))
    # strips + numbered block (the toy figure's arrangement, real numbers)
    bx, by, bw, bh = 7.55, 3.30, 2.88, 2.38
    strip_cells(ax, 6.88, by, 0.58, bh, d.U[d.A, 0], False, TEAL_BG, TEAL)
    strip_cells(ax, bx, by + bh + 0.08, bw, 0.38, d.Vt[0, d.B], True,
                PURPLE_BG, PURPLE)
    ax.text(7.17, by - 0.24, "$u_1$ \u2014 G01 rows", ha="center",
            va="center", fontsize=9.5, color=TEAL)
    ax.text(bx, by + bh + 0.56, "$v_1$ \u2014 G09 columns",
            va="center", fontsize=9.5, color=PURPLE)
    aB = inset(fig, bx, by, bw, bh)
    heat(aB, d.layer_blocks[0], d.wnorm)
    for i in range(len(d.A)):
        for j in range(len(d.B)):
            aB.text(j, i, fmt(d.layer_blocks[0][i, j]), ha="center",
                    va="center", fontsize=8, color="white")
    ax.add_patch(Rectangle((bx, by), bw, bh, facecolor="none",
                           edgecolor=GOLD, linewidth=1.6))
    ax.text(7.60, by - 1.08,
            f"$M_1$ = $\\omega_1$ × block sum = "
            f"{d.omega[0]:.2f} × ({fmt(d.block_sums[0])}) = "
            f"{fmt(d.contribs[0])}",
            ha="center", fontsize=12.5, color=GOLD, va="center",
            fontweight="bold")

    # ---- right: modes 2-9
    ax.text(10.75, 7.34, "modes 2\u20139 \u2014 the supporting cast",
            fontsize=12.5, color=INK, va="center")
    ax.add_patch(Rectangle((14.20, 3.62), 1.52, 3.62,
                           facecolor="#26221A", edgecolor=GOLD,
                           linewidth=1.2))
    for x, h in ((10.90, "m"), (11.75, r"$\omega_m$"), (12.85, "block sum"),
                 (14.35, "contribution")):
        ax.text(x, 7.04, h, fontsize=9.5, color=FAINT, va="center")
    for k, m in enumerate(range(1, 9)):
        y = 6.66 - k * 0.345
        ax.text(10.90, y, str(m + 1), fontsize=11, color=INK, va="center")
        ax.text(11.75, y, f"{d.omega[m]:.2f}", fontsize=11, color=INK,
                va="center")
        ax.text(12.85, y, fmt_small(d.block_sums[m]), fontsize=11,
                color=INK, va="center")
        ax.text(14.35, y, fmt3(d.contribs[m]), fontsize=11, color=INK,
                va="center")
    ax.plot([10.90, 15.60], [4.06, 4.06], color=DIM, lw=0.8)
    ax.text(10.90, 3.84, "2\u20139 together", fontsize=11, color=GOLD,
            va="center")
    ax.text(12.85, 3.84, "\u2014", fontsize=11, color=FAINT,
            va="center")
    ax.text(14.35, 3.84, fmt3(d.contribs[1:].sum()), fontsize=11,
            color=GOLD, va="center", fontweight="bold")
    ax.add_patch(Rectangle((10.75, 1.50), 4.95, 1.95, facecolor="#26221A",
                           edgecolor=GOLD, linewidth=1.4))
    ax.text(11.00, 3.14, "the blend", fontsize=12, color=GOLD, va="center")
    ax.text(11.00, 2.70, f"$M$ = {d.omega[0]:.2f}\u00d7"
            f"({fmt(d.block_sums[0])}) + ({fmt(d.M - d.contribs[0])})",
            fontsize=12.5, color=INK, va="center")
    ax.text(11.00, 2.26, f"= {fmt(d.M)}", fontsize=14.5, color=GOLD,
            va="center", fontweight="bold")
    ax.text(11.00, 1.84, f"mode 1: {fmt(d.contribs[0])} \u00b7 modes "
            f"2\u20139: {fmt(d.M - d.contribs[0])}",
            fontsize=9.5, color=DIM, va="center")

    ax.text(0.40, 1.06, "Why mode 1 owns this block: G01 is mode 1's home "
            "group and G09 sits inside mode 1's target pattern, so mode "
            "1's layer rebuilds the block almost\n"
            f"exactly ({fmt(d.block_sums[0])} of $R$'s {fmt(d.R)}). Most "
            "blocks blend several modes; this one is nearly a single-mode "
            "reading.", fontsize=10, color=DIM, va="top", linespacing=1.55)

    footer(ax, "equations (8)\u2013(10) \u00b7 slide 2 of 3")
    out = OUT_DIR / "eq8-9-slide2.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")


# ---------------------------------------------------------------- slide 3
def slide3(d):
    fig, ax = canvas()
    chain(fig, ax, 8, 8.52, [
        (r"$\mathbf{P_{AB}\;=\;0.7\,R_{AB}\;+\;0.3\,M_{AB}}$",
         dict(color=GOLD)),
        ("  \u2014  one block, three numbers", dict(color=INK)),
    ], 19)

    x0 = 1.05
    ax.text(x0, 7.70, r"$R_{AB} = \sum_{(a,b)\,\in\,A \times B} w_{ab}$"
            "     (8)", fontsize=16, color=INK, va="center")
    ax.text(8.35, 7.70, f"= {fmt(d.R)}", fontsize=16, color=GOLD,
            va="center", fontweight="bold")
    ax.text(x0, 7.30, "slide 1 \u2014 the 42 real weights of the G01 "
            "\u2192 G09 block, added as they stand",
            fontsize=10.5, color=DIM, va="center")
    ax.text(x0, 6.52, r"$M_{AB} = \sum_{m=1}^{9} \omega_m "
            r"\sum_{(a,b)\,\in\,A \times B} \sigma_m\, u_{am} v_{bm}$"
            "     (9)", fontsize=16, color=INK, va="center")
    ax.text(8.35, 6.52, f"= {fmt(d.M)}", fontsize=16, color=GOLD,
            va="center", fontweight="bold")
    ax.text(x0, 6.12, "slide 2 \u2014 mode 1 contributes "
            f"{fmt(d.contribs[0])}; modes 2\u20139 together "
            f"{fmt(d.M - d.contribs[0])}",
            fontsize=10.5, color=DIM, va="center")
    ax.text(x0, 5.34, r"$P_{AB} = 0.7\,R_{AB} + 0.3\,M_{AB}$     (10)",
            fontsize=16, color=INK, va="center")
    ax.text(x0, 4.94, "the blend \u2014 the raw wiring counts 0.7, the "
            "mode reading 0.3", fontsize=10.5, color=DIM, va="center")
    part_r, part_m = 0.7 * d.R, 0.3 * d.M
    sign = "+" if part_m >= 0 else "\u2212"
    chain(fig, ax, 0, 4.30,
          [("= 0.7\u00d7(", dict(color=INK)),
           (fmt(d.R), dict(color=GOLD, fontweight="bold")),
           (") + 0.3\u00d7(", dict(color=INK)),
           (fmt(d.M), dict(color=GOLD, fontweight="bold")),
           (f") = {fmt(part_r)} {sign} {abs(part_m):.2f}",
            dict(color=INK))],
          15.5, left=x0)
    ax.text(x0, 3.62, f"$P$ = {fmt(d.P)}", fontsize=26, color=GOLD,
            va="center", fontweight="bold")
    ax.text(x0, 3.14, "the same three numbers as the pathway slide's "
            "Check-it box \u2014 now with their workings shown",
            fontsize=10.5, color=TEAL, va="center")

    # ---- right: where this edge sits
    rx = 10.55
    ax.text(rx, 7.70, "where this edge sits", fontsize=12.5, color=INK,
            va="center")
    ax.text(rx, 7.28, "\u00b7 strongest of the 132 ordered group pairs\n"
            "\u00b7 10 of the 11 drawn gold edges are negative;\n"
            "   the one positive edge is G11 \u2192 G06, +1.44\n"
            "\u00b7 no gold edge \u2260 no interaction: signed\n"
            "   blocks cancel, and pairs inside one group\n"
            "   never receive a gold edge at all",
            fontsize=10.5, color=DIM, va="top", linespacing=1.6)

    # ---- the edge itself, groups drawn as in the combined graph
    group_tile(ax, 2.05, 1.42, 4.30, 1.62, "G01 \u00b7 Mode 1 \u00b7 (F01)",
               [[SHORT.get(n, n) for n in GROUPS[SRC][:4]],
                [SHORT.get(n, n) for n in GROUPS[SRC][4:]]],
               title_fs=11, pill_fs=8.5)
    group_tile(ax, 9.65, 1.42, 4.30, 1.62, "G09 \u00b7 Mode 1 \u00b7 (F01)",
               [GROUPS[TGT][:3], GROUPS[TGT][3:]],
               title_fs=11, pill_fs=8.5)
    ax.add_patch(FancyArrowPatch((6.50, 2.23), (9.50, 2.23),
                                 arrowstyle="-|>", mutation_scale=30,
                                 color=GOLD, lw=3.5, linestyle=(0, (6, 3))))
    ax.text(8.0, 2.72, f"$P$ = {fmt(d.P)}", ha="center", va="center",
            fontsize=15, color=GOLD, fontweight="bold")
    ax.text(8, 1.18, r"drawn gold because $|P| \geq 0.10 \times "
            r"\max|P|$ — and this pair is the max, so it sets "
            r"the cutoff (1.24)", ha="center", va="center",
            fontsize=10.5, color=DIM)
    ax.text(8, 0.88, "11 of the 132 ordered pairs are drawn; this one is "
            "the strongest", ha="center", va="center", fontsize=10.5,
            color=DIM)

    footer(ax, "equations (8)\u2013(10) \u00b7 slide 3 of 3")
    out = OUT_DIR / "eq8-9-slide3.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")




if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Three slides for equations (8)-(10) on real data.")
    ap.add_argument("which", nargs="?", default="1",
                    help="slide to build: 1, 2, 3, or all (default: 1)")
    ap.add_argument("--data-dir", default=None,
                    help="folder holding z_matrix.42d6ad4c.npz and "
                         "eigen.42d6ad4c.json (or set EIGEN_RUN_DIR)")
    args = ap.parse_args()
    d = Data(resolve_data_dir(args.data_dir))
    d.check()
    which = args.which
    if which in ("1", "all"):
        slide1(d)
    if which in ("2", "all"):
        slide2(d)
    if which in ("3", "all"):
        slide3(d)

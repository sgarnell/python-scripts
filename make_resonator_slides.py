#!/usr/bin/env python3
"""Resonator-score slides (S = G x E).

Journal structure (Definition / Proposition, numbered equations) typeset
in Computer Modern math (matplotlib mathtext, fontset 'cm') with
Liberation Serif text on Saul's dark slide ground (#1E1E1E, VS Code
Dark+ accents). Colour code, held across all three slides:
  G = teal #4EC9B0,  E = yellow #DCDCAA,  S = purple #C586C0,  w = #9CDCFE.

Usage: python3 make_resonator_slides.py [1|2|3|all]
"""
import sys

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

BG = "#1E1E1E"
PANEL = "#26262B"
INK = "#EDEDED"
GREY = "#A9A9A9"
BLUE = "#569CD6"
TEAL = "#4EC9B0"   # G
YELL = "#DCDCAA"   # E
PURP = "#C586C0"   # S
LBLUE = "#9CDCFE"  # w

plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Liberation Serif", "DejaVu Serif"]

FIG_W, FIG_H, DPI = 13.333, 7.5, 200


def out_path(name):
    """PNGs go into an output/ folder beside this script, created if needed."""
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def new_slide():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")
    return fig, ax


def math_row(fig, ax, x, y, segments, va="center"):
    """Draw a horizontal row of (text, colour, fontsize, weight) segments,
    chaining each segment to the previous one's rendered width.
    A segment is math if wrapped in $...$, plain serif text otherwise."""
    cur = x
    for text, color, fontsize, weight in segments:
        t = ax.text(cur, y, text, fontsize=fontsize, color=color,
                    va=va, ha="left", fontweight=weight)
        fig.canvas.draw()
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        x1, _ = ax.transData.inverted().transform((bb.x1, bb.y1))
        cur = x1
    return cur


def slide1():
    fig, ax = new_slide()

    # ---- title ------------------------------------------------------
    math_row(fig, ax, 0.55, 7.08, [
        ("The resonator score   ", INK, 25, "bold"),
        (r"$S$", PURP, 25, "normal"),
        ("  =  ", INK, 25, "normal"),
        (r"$G$", TEAL, 25, "normal"),
        ("  ×  ", INK, 25, "normal"),
        (r"$E$", YELL, 25, "normal"),
    ])
    ax.plot([0.55, 12.78], [6.80, 6.80], color=BLUE, lw=1.2)

    # ---- 2-cycle figure (top right) ---------------------------------
    fx = fig.add_axes([0.672, 0.600, 0.305, 0.265])
    fx.set_xlim(0, 12)
    fx.set_ylim(0, 5.86)
    fx.set_aspect("equal")
    fx.axis("off")
    for cx, lab in ((3.0, "a"), (9.0, "b")):
        fx.add_patch(Circle((cx, 2.93), 1.02, facecolor=BG,
                            edgecolor=BLUE, lw=1.6))
        fx.text(cx, 2.93, lab, fontsize=21, color=INK, ha="center",
                va="center", style="italic")
    fx.add_patch(FancyArrowPatch((3.78, 3.55), (8.22, 3.55),
                                 connectionstyle="arc3,rad=-0.38",
                                 arrowstyle="-|>", mutation_scale=22,
                                 color=INK, lw=1.6))
    fx.add_patch(FancyArrowPatch((8.22, 2.31), (3.78, 2.31),
                                 connectionstyle="arc3,rad=-0.38",
                                 arrowstyle="-|>", mutation_scale=22,
                                 color=INK, lw=1.6))
    fx.text(6.0, 5.55, r"$w_{a\to b}$", fontsize=16, color=LBLUE,
            ha="center", va="center")
    fx.text(6.0, 0.32, r"$w_{b\to a}$", fontsize=16, color=LBLUE,
            ha="center", va="center")
    ax.text(10.90, 4.28, "a reciprocal pair (2-cycle)", fontsize=11.5,
            color=GREY, ha="center", style="italic")

    # ---- Definition 1 -----------------------------------------------
    ax.text(0.55, 6.50, "Definition 1.", fontsize=14.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(0.55, 6.16,
            r"Let $a \to b$ and $b \to a$ both be present — a reciprocal pair — with sender- and",
            fontsize=12.3, color=INK, va="center")
    ax.text(0.55, 5.90,
            r"receiver-side z-scores $z^{pre},\, z^{post} \in [0.1,\,1]$ as exported. Define:",
            fontsize=12.3, color=INK, va="center")

    def eq_number(y, n):
        ax.text(8.42, y, f"({n})", fontsize=12, color=GREY, va="center")

    # (1) the unified weight w
    math_row(fig, ax, 0.85, 5.42, [
        (r"$w_{ab}$", LBLUE, 15.5, "normal"),
        (r"$= s_{ab}\,\tanh\left(\alpha\,\log\frac{z^{post}_{a\to b}}"
         r"{z^{pre}_{a\to b} + \varepsilon}\right)$", INK, 15.5, "normal"),
    ])
    eq_number(5.42, 1)
    ax.text(0.85, 5.06,
            r"the unified weight of $a \to b$ (Phase 02), with "
            r"$s_{ab} = \frac{1}{2}\left(z^{pre}_{a\to b} + z^{post}_{a\to b}\right)$"
            r" the mean prominence, $\alpha = 1$, $\varepsilon = 0.1$;",
            fontsize=10.8, color=GREY, va="center", style="italic")
    ax.text(0.85, 4.82,
            r"$\mathrm{sign}(w_{ab})$ records pre- vs post-dominance — not excitation or inhibition.",
            fontsize=10.8, color=GREY, va="center", style="italic")

    # (2) G
    math_row(fig, ax, 0.85, 4.34, [
        (r"$G_{ab}$", TEAL, 16.5, "normal"),
        (r"$= \sqrt{|w_{ab}|\;|w_{ba}|}$", INK, 16.5, "normal"),
    ])
    eq_number(4.34, 2)
    ax.text(0.85, 3.99,
            "the intensity of the pair (Onnela et al. 2005) — both legs must be strong.",
            fontsize=10.8, color=GREY, va="center", style="italic")

    # (3) E
    math_row(fig, ax, 0.85, 3.56, [
        (r"$E_{ab}$", YELL, 16.5, "normal"),
        (r"$= \sqrt{z^{post}_{a\to b}\;z^{post}_{b\to a}}$", INK, 16.5, "normal"),
    ])
    eq_number(3.56, 3)
    ax.text(0.85, 3.21,
            "receiver-side prominence — each receiver must weight its incoming leg highly.",
            fontsize=10.8, color=GREY, va="center", style="italic")

    # (4) S, the anchor equation
    math_row(fig, ax, 0.85, 2.66, [
        (r"$S_{ab}$", PURP, 23, "normal"),
        (r"$\;=\;$", INK, 23, "normal"),
        (r"$G_{ab}$", TEAL, 23, "normal"),
        (r"$\;\times\;$", INK, 23, "normal"),
        (r"$E_{ab}$", YELL, 23, "normal"),
    ])
    eq_number(2.66, 4)

    # ---- Proposition 1 ----------------------------------------------
    ax.add_patch(FancyBboxPatch((0.55, 0.78), 12.23, 1.28,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=PANEL, edgecolor=BLUE, lw=1.1))
    ax.text(0.85, 1.86, "Proposition 1.", fontsize=13.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(2.62, 1.86, r"For every reciprocal pair $\{a, b\}$:",
            fontsize=12, color=INK, va="center")
    math_row(fig, ax, 0.85, 1.47, [
        (r"$\mathrm{(i)}\;\; S_{ab} = S_{ba}$", INK, 13, "normal"),
        ("      symmetry", GREY, 11.5, "normal"),
    ])
    math_row(fig, ax, 0.85, 1.08, [
        (r"$\mathrm{(iii)}\;\; S_{ab}$", INK, 13, "normal"),
        ("  strictly increases in each leg's ", INK, 11.5, "normal"),
        (r"$|w|$", INK, 13, "normal"),
        ("  and  ", INK, 11.5, "normal"),
        (r"$z^{post}$", INK, 13, "normal"),
        ("      monotonicity", GREY, 11.5, "normal"),
    ])
    math_row(fig, ax, 6.95, 1.47, [
        (r"$\mathrm{(ii)}\;\; S_{ab} = 0 \Longleftrightarrow \min(|w_{ab}|,\, |w_{ba}|) = 0$",
         INK, 13, "normal"),
        ("      annihilation — no leg, no loop", GREY, 11.5, "normal"),
    ])
    math_row(fig, ax, 6.95, 1.08, [
        (r"$\mathrm{(iv)}\;\; 0 \leq S_{ab} < 1$", INK, 13, "normal"),
        ("      bounded", GREY, 11.5, "normal"),
    ])

    # ---- footer -------------------------------------------------------
    ax.text(0.55, 0.47,
            "Domain: reciprocal pairs only — 127 of the 590 directed pairs (62-neuron run). "
            "For a non-reciprocal pair S is undefined, not zero: the missing leg has no z-scores.",
            fontsize=10.3, color=INK, va="center")
    ax.text(0.55, 0.18,
            "Each property in Proposition 1 is immediate from Definition 1.   ·   "
            "G after Onnela, Saramäki, Kertész & Kaski, Phys. Rev. E 71, 065103 (2005).",
            fontsize=9.8, color=GREY, va="center", style="italic")

    out = out_path("resonator-slide1-definition.png")
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print("wrote", out)


def _head(ax, y, text):
    ax.text(0.55, y, text, fontsize=14.5, color=BLUE,
            fontweight="bold", va="center")


def _gloss(ax, y, text, size=10.8):
    ax.text(0.85, y, text, fontsize=size, color=GREY, va="center",
            style="italic")


def _eqnum(ax, y, label):
    ax.text(8.42, y, label, fontsize=12, color=GREY, va="center")


def slide2():
    fig, ax = new_slide()

    # ---- title ------------------------------------------------------
    math_row(fig, ax, 0.55, 7.08, [
        ("The factor   ", INK, 25, "bold"),
        (r"$E$", YELL, 25, "normal"),
        ("   —   receiver-side prominence", INK, 25, "bold"),
    ])
    ax.plot([0.55, 12.78], [6.80, 6.80], color=BLUE, lw=1.2)

    # ---- A: the adopted factor --------------------------------------
    _head(ax, 6.46, r"The adopted factor: $E^{post}$  (Definition 1, eq. 3)")
    math_row(fig, ax, 0.85, 6.02, [
        (r"$E_{ab}$", YELL, 17, "normal"),
        (r"$= \sqrt{z^{post}_{a\to b}\;z^{post}_{b\to a}}$", INK, 17, "normal"),
    ])
    _eqnum(ax, 6.02, "(3)")
    _gloss(ax, 5.66,
           "for each direction, the connection's z-score as seen from the receiving side — the side where a loop's "
           "returning signal lands; both receivers must rank the incoming leg highly.")
    _gloss(ax, 5.40,
           r"$E_{ab} \in [0.1,\,1]$: the export floor keeps $E$ strictly positive, so $E$ can attenuate a score but "
           r"never annihilate it — annihilation is carried by $G$ alone (Proposition 1(ii)).")

    # ---- B: the sender-side control ----------------------------------
    _head(ax, 4.74, r"The sender-side control: $E^{pre}$")
    math_row(fig, ax, 0.85, 4.32, [
        (r"$E^{pre}_{ab}$", GREY, 16.5, "normal"),
        (r"$= \sqrt{z^{pre}_{a\to b}\;z^{pre}_{b\to a}}$", INK, 16.5, "normal"),
    ])
    _eqnum(ax, 4.32, "(5)")
    _gloss(ax, 3.96,
           "the same construction on the sender side — a legitimate alternative a priori, kept for comparison. "
           "As a score it fails the test the adopted factor passes:")
    _gloss(ax, 3.70,
           r"Glu–ACh pairs in the top 12: $E^{post}$ finds 7 of 12 ($p = 0.0002$); $E^{pre}$ finds 1 of 12 "
           r"($p = 0.85$). The two scores correlate 0.96 over all 127 pairs, yet their top-12 lists overlap in only 5 —")
    _gloss(ax, 3.44,
           "the receiver-side signal lives at the top of the list, where candidacy is decided.")

    # ---- C: the predecessor ------------------------------------------
    _head(ax, 2.62, r"The predecessor: $E^{I}$  (share-based, after Bascompte)")
    math_row(fig, ax, 0.85, 2.22, [
        (r"$E^{I}_{ab}$", GREY, 16, "normal"),
        (r"$= \sqrt{s_{a\to b}\;s_{b\to a}}$", INK, 16, "normal"),
        ("      with      ", GREY, 12, "normal"),
        (r"$s_{a\to b} = |w_{ab}|/I_b$", INK, 16, "normal"),
        (" ,       ", GREY, 12, "normal"),
        (r"$I_a = \sum_u |w_{ua}|$", INK, 16, "normal"),
    ])
    _eqnum(ax, 2.22, "(6)")
    _gloss(ax, 1.86,
           r"whence the closed form $S^{I}_{ab} = |w_{ab}|\,|w_{ba}|/\sqrt{I_a I_b}$ — the pair's leg product "
           r"discounted by the two neurons' total incoming budgets (Bascompte et al. 2006).")
    _gloss(ax, 1.60,
           r"the flaw is $I$: a within-set budget over only the exported neurons — change the export and "
           r"the same pair scores differently: one pair, two exports, two scores. $E^{post}$ depends on the pair alone.")


    # ---- footer ---------------------------------------------------------
    ax.text(0.55, 0.40,
            r"$E$ grades prominence; $G$ gates existence.",
            fontsize=10.3, color=INK, va="center")
    ax.text(0.55, 0.13,
            "Bascompte, Jordano & Olesen, Science 312, 431–433 (2006).",
            fontsize=9.8, color=GREY, va="center", style="italic")

    out = out_path("resonator-slide2-E.png")
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print("wrote", out)


def slide3():
    fig, ax = new_slide()

    # ---- title ------------------------------------------------------
    math_row(fig, ax, 0.55, 7.08, [
        ("The factor   ", INK, 25, "bold"),
        (r"$G$", TEAL, 25, "normal"),
        ("   —   loop intensity", INK, 25, "bold"),
    ])
    ax.plot([0.55, 12.78], [6.80, 6.80], color=BLUE, lw=1.2)

    # ---- A: the adopted factor --------------------------------------
    _head(ax, 6.46, r"The adopted factor  (Definition 1, eq. 2)")
    math_row(fig, ax, 0.85, 6.02, [
        (r"$G_{ab}$", TEAL, 17, "normal"),
        (r"$= \sqrt{|w_{ab}|\;|w_{ba}|}$", INK, 17, "normal"),
    ])
    _eqnum(ax, 6.02, "(2)")
    _gloss(ax, 5.66,
           "Onnela et al. (2005): the intensity of a weighted motif is the geometric mean of its link weights. "
           "A reciprocal pair is the smallest motif containing a cycle — the 2-cycle — and G is its intensity.")
    _gloss(ax, 5.40,
           "both legs enter as magnitudes: G measures how strongly the loop is wired, irrespective of dominance direction.")

    # ---- B: loop gain --------------------------------------------------
    _head(ax, 4.74, r"Remark: $G$ and loop gain")
    math_row(fig, ax, 0.85, 4.32, [
        (r"$\Lambda_{ab}$", INK, 16.5, "normal"),
        (r"$= |w_{ab}|\;|w_{ba}| = $", INK, 16.5, "normal"),
        (r"$G_{ab}^2$", TEAL, 16.5, "normal"),
    ])
    _eqnum(ax, 4.32, "(7)")
    _gloss(ax, 3.96,
           "the product around a cycle is its loop gain; G is that gain's per-step geometric mean, "
           r"$\sqrt{\Lambda_{ab}}$. A resonator requires loop gain together with an E–I sign structure —")
    _gloss(ax, 3.70,
           r"and $G$ supplies only the magnitude. The sign structure is not in $\mathrm{sign}(w)$ (dominance, not coupling sign): "
           "it is read from the transmitters — ACh excitatory, Glu inhibitory — the pair's E–I grade.")

    # ---- C: why geometric ----------------------------------------------
    _head(ax, 2.88, "Why the geometric mean: the imbalance tax")
    math_row(fig, ax, 0.85, 2.48, [
        (r"$G_{ab} \leq \frac{|w_{ab}| + |w_{ba}|}{2}$", INK, 16, "normal"),
    ])
    _eqnum(ax, 2.48, "(AM–GM)")
    _gloss(ax, 2.12,
           "by AM–GM, with equality iff the legs are equal. The arithmetic mean pays an unbalanced pair for one strong leg; "
           "the geometric mean taxes imbalance — replacing geometric by arithmetic")
    _gloss(ax, 1.86,
           "inflates an unbalanced pair, paying one strong leg as if the loop were strong; balanced pairs barely move. "
           "Zero test: legs 0.9 and 0 — arithmetic claims 0.45, a half-loop; geometric says 0.")


    # ---- footer ------------------------------------------------------------
    ax.text(0.55, 0.40,
            r"$G$ gates existence; $E$ grades prominence.",
            fontsize=10.3, color=INK, va="center")
    ax.text(0.55, 0.13,
            "Onnela, Saramäki, Kertész & Kaski, Phys. Rev. E 71, 065103 (2005).   ·   "
            "Thomas (1981), negative-loop necessity; Buzsáki & Wang, Annu. Rev. Neurosci. 35 (2012).",
            fontsize=9.8, color=GREY, va="center", style="italic")

    out = out_path("resonator-slide3-G.png")
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print("wrote", out)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "1"
    if which in ("1", "all"):
        slide1()
    if which in ("2", "all"):
        slide2()
    if which in ("3", "all"):
        slide3()

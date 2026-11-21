#!/usr/bin/env python3
"""Single dense overview slide for the Bruno anesthetic experiment.

Layout (top to bottom): title, hypothesis strip, the ExR7 fork circuit
(with tool markers and ASAP5 recording dots), a row of four leg boxes,
and the decision strip ('What would count as the cognitive link').

Dark #1E1E1E ground, VS Code Dark+ palette, matching the resonator
slides. Run: python3 make_experiment_overview.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle

BG = "#1E1E1E"
PANEL = "#252526"
INK = "#FFFFFF"
BODY = "#D4D4D4"
GREY = "#9A9A9A"
BLUE = "#569CD6"
TEAL = "#4EC9B0"     # ACh / excitatory / ON switch
PURPLE = "#C586C0"   # Glu / inhibitory
YELL = "#DCDCAA"     # ASAP5 dots / S family
ORANGE = "#CE9178"   # shibire / OFF switch
LBLUE = "#9CDCFE"    # circuit arrows

for cand in ("Liberation Serif", "DejaVu Serif"):
    if any(cand in f.name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break
plt.rcParams["mathtext.fontset"] = "cm"

FIG_W, FIG_H, DPI = 13.333, 7.5, 200


def arrow(ax, p1, p2, color=LBLUE, lw=1.7, rad=0.0, dashed=False):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=(0, (4, 3)) if dashed else "-",
                                shrinkA=1, shrinkB=1,
                                connectionstyle=f"arc3,rad={rad}"),
                zorder=3)


def node(ax, cx, cy, label, w=1.5, h=0.58, size=12.5, edge=BLUE,
         dashed=False, italic=False, dot=False):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.09",
                                facecolor=PANEL, edgecolor=edge, lw=1.3,
                                linestyle=(0, (4, 3)) if dashed else "-",
                                zorder=4))
    ax.text(cx, cy, label, fontsize=size, color=INK, ha="center",
            va="center", fontweight="bold" if not italic else "normal",
            style="italic" if italic else "normal", zorder=5)
    if dot:
        ax.add_patch(Circle((cx + w / 2 - 0.13, cy + h / 2 - 0.13), 0.055,
                            facecolor=YELL, edgecolor="none", zorder=6))


def build():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")
    ax.set_facecolor(BG)

    # ---- title (auto-fit) -------------------------------------------
    title = ("Does anesthesia silence cognition by cutting excitatory "
             "drive to the fan-shaped body?")
    size = 20.5
    t = ax.text(0.55, 7.16, title, fontsize=size, color=INK,
                fontweight="bold", va="center")
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    while t.get_window_extent(renderer=rend).width / DPI > 12.23 and size > 12:
        size -= 0.5
        t.set_fontsize(size)
        fig.canvas.draw()
    ax.plot([0.55, 12.78], [6.90, 6.90], color=BLUE, lw=1.2)

    # ---- hypothesis strip --------------------------------------------
    ax.text(0.55, 6.62, "Hypothesis:", fontsize=11.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(1.95, 6.62,
            "anesthetics abolish cognition by preferentially suppressing excitatory (cholinergic) transmission,",
            fontsize=10.8, color=BODY, va="center", style="italic")
    ax.text(1.95, 6.36,
            "leaving inhibitory (glutamatergic) transmission intact. The catch: both ExR7 branches are cholinergic —",
            fontsize=10.8, color=BODY, va="center", style="italic")
    ax.text(1.95, 6.10,
            "the drug alone cannot separate them; any dissociation must emerge downstream, in the FB network.",
            fontsize=10.8, color=BODY, va="center", style="italic")

    # ---- circuit -------------------------------------------------------
    # FB panel
    ax.add_patch(FancyBboxPatch((7.30, 4.72), 3.75, 1.26,
                                boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="#202022", edgecolor=GREY, lw=0.9,
                                linestyle=(0, (5, 4)), zorder=1))
    ax.text(10.92, 5.86, "fan-shaped body", fontsize=9, color=GREY,
            va="center", ha="right", style="italic", zorder=2)

    # nodes
    node(ax, 1.55, 5.03, "EPG")
    node(ax, 3.75, 5.03, "ExR7", dot=True)
    node(ax, 6.05, 5.60, "FB4Y", dot=True)
    node(ax, 8.15, 5.38, "FB5R/U", dot=True)
    node(ax, 10.15, 5.38, "hDeltaH3/7/8", size=10.5, dot=True)
    node(ax, 6.05, 4.32, "LAL013", dot=True)
    node(ax, 12.05, 5.38, "cognitive assay", w=1.42, size=10.5,
         edge=GREY, dashed=True, italic=True)
    node(ax, 8.75, 4.32, "exploratory turning", w=1.95, size=10.5,
         edge=GREY, dashed=True, italic=True)

    # wiring
    arrow(ax, (2.32, 5.03), (2.97, 5.03))                       # EPG -> ExR7
    arrow(ax, (4.52, 5.18), (5.28, 5.50), rad=-0.15)            # ExR7 -> FB4Y
    arrow(ax, (4.52, 4.88), (5.28, 4.44), rad=-0.15)            # ExR7 -> LAL013
    arrow(ax, (6.82, 5.56), (7.38, 5.44))                       # FB4Y -> FB5
    arrow(ax, (9.42, 5.52), (8.88, 5.52), color=TEAL, rad=-0.4)   # hDelta -> FB5 (ACh)
    arrow(ax, (8.88, 5.24), (9.42, 5.24), color=PURPLE, rad=-0.4)  # FB5 -> hDelta (Glu)
    arrow(ax, (11.07, 5.38), (11.32, 5.38), color=GREY, dashed=True)  # loop -> cognition
    arrow(ax, (6.82, 4.32), (7.75, 4.32), color=GREY, dashed=True)    # LAL013 -> turning

    # transmitter labels on the fork + loop
    ax.text(4.88, 5.74, "ACh", fontsize=10, color=TEAL, ha="center",
            va="center", fontweight="bold")
    ax.text(4.90, 4.26, "ACh", fontsize=10, color=TEAL, ha="center",
            va="center", fontweight="bold")
    ax.text(9.15, 5.85, "ACh", fontsize=9.5, color=TEAL, ha="center",
            va="center", fontweight="bold")
    ax.text(9.15, 4.93, "Glu", fontsize=9.5, color=PURPLE, ha="center",
            va="center", fontweight="bold")

    # tool tags
    ax.text(1.55, 4.56, "heading input", fontsize=9, color=GREY,
            ha="center", va="center", style="italic")
    ax.text(3.75, 4.56, "Chrimson · ON switch", fontsize=9, color=TEAL,
            ha="center", va="center", fontweight="bold")
    ax.text(6.05, 5.10, "shibire^ts · OFF switch", fontsize=9,
            color=ORANGE, ha="center", va="center", fontweight="bold")
    ax.text(8.15, 4.90, "shibire^ts · OFF", fontsize=8.5, color=ORANGE,
            ha="center", va="center", fontweight="bold")

    # circuit caption
    ax.text(0.55, 3.86,
            "Yellow dot = ASAP5 recording site. The anesthetic is bath-applied to the whole preparation — "
            "the genetic cuts draw the boundaries the drug cannot, one cell type at a time.   ·   Decision criteria: slide 2.",
            fontsize=10, color=GREY, va="center", style="italic")

    # ---- the four legs ---------------------------------------------------
    legs = [
        ("Leg 1 — Baseline", [
            "ASAP5 recording of every NOI",
            "under defined stimulation",
            "(Chrimson drive of ExR7), plus",
            "both behaviors.",
            "The two behavioral metrics are",
            "fixed here and never redefined —",
            "every later effect is a percentage",
            "of these no-drug baseline values.",
        ]),
        ("Leg 2 — Deactivation", [
            "shibire^ts silencing: FB4Y first",
            "(the entry point), then FB5.",
            "hDeltaH3/7/8 are recorded in",
            "every condition — FB5's loop",
            "partners are where its loss",
            "is read.",
            "Effects are read downstream,",
            "never in the soma of the",
            "deactivated neuron.",
        ]),
        ("Leg 3 — Graded anesthetic", [
            "Dose–response curve for every NOI,",
            "ExR7 co-recorded as internal",
            "standard; randomized dose order,",
            "washout to baseline between doses",
            "(recovery proves reversibility).",
            "Axis anchored to the behavioral",
            "EC50. References: mecamylamine",
            "(ACh off), ivermectin (Glu off).",
            "Prediction: FB5 falls early — the",
            "loop dies by its cholinergic leg,",
            "hDelta→FB5.",
        ]),
        ("Leg 4 — Combined", [
            "Graded anesthetic × each NOI",
            "deactivated in turn (FB4Y, FB5,",
            "ExR7, LAL013, hDelta partners).",
            "Three tests: phenocopy — does",
            "the cut alone copy the drug",
            "state? Occlusion — does the",
            "drug add anything on top of",
            "the cut? EC50 shift — does the",
            "cut move the dose curve?",
            "LAL013 off is the specificity",
            "control.",
        ]),
    ]
    box_w, gap, top = 2.98, 0.10, 3.62
    for i, (head, lines) in enumerate(legs):
        x = 0.55 + i * (box_w + gap)
        ax.add_patch(FancyBboxPatch((x, top - 3.27), box_w, 3.27,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    facecolor=PANEL, edgecolor=BLUE, lw=1.0))
        ax.text(x + 0.15, top - 0.30, head, fontsize=12, color=BLUE,
                fontweight="bold", va="center")
        for j, ln in enumerate(lines):
            ax.text(x + 0.15, top - 0.70 - j * 0.245, ln, fontsize=9.7,
                    color=BODY, va="center")

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "bruno-experiment-overview.png")
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print("wrote", out)


if __name__ == "__main__":
    build()

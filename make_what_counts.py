#!/usr/bin/env python3
"""Slide 2 for the Bruno anesthetic experiment: the decision criteria.

'What would count as the cognitive link' — shared EC50, phenocopy, and
occlusion / the two-route dissociation, each with a worked illustration
and its failure mode, plus the expected dose ordering.

Dark #1E1E1E ground, VS Code Dark+ palette, matching the overview slide.
Run: python3 make_what_counts.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

BG = "#1E1E1E"
PANEL = "#252526"
INK = "#FFFFFF"
BODY = "#D4D4D4"
GREY = "#9A9A9A"
BLUE = "#569CD6"
TEAL = "#4EC9B0"

for cand in ("Liberation Serif", "DejaVu Serif"):
    if any(cand in f.name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break
plt.rcParams["mathtext.fontset"] = "cm"

FIG_W, FIG_H, DPI = 13.333, 7.5, 200
CLAIM = dict(fontsize=10.2, color=BODY, va="center")
FENCE = dict(fontsize=10.2, color=GREY, va="center", style="italic")


def block(ax, head_y, heading, lines):
    """lines: list of (text, style) with style 'claim' or 'fence'."""
    ax.text(0.55, head_y, heading, fontsize=13.5, color=BLUE,
            fontweight="bold", va="center")
    for j, (text, style) in enumerate(lines):
        ax.text(0.85, head_y - 0.28 - j * 0.235, text,
                **(CLAIM if style == "claim" else FENCE))


def build():
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")
    ax.set_facecolor(BG)

    # ---- title ---------------------------------------------------------
    title = "What would count as the cognitive link"
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

    ax.text(0.55, 6.58,
            "The decision criteria for the anesthetic program — three tests, agreed in advance. "
            "The legs may adapt as results come in; these criteria do not.",
            fontsize=10.8, color=GREY, va="center", style="italic")

    # ---- (i) shared EC50 -------------------------------------------------
    block(ax, 6.16, "(i)   Shared EC50", [
        ("FB5's evoked activity and the cognitive readout fall along the same dose curve: each reaches 50% of its Leg 1 baseline at the same anesthetic dose.", "claim"),
        ("That shared dose must differ from the dose at which LAL013's response and exploratory turning fall — otherwise the curves separate nothing.", "claim"),
        ("Illustration: cognition and FB5 both reach half-baseline at about 1% isoflurane, while LAL013 and turning hold out to about 2%.", "fence"),
        ("If it fails: if FB5's dose curve instead tracks LAL013's curve, the fan-shaped body is not the site where cognition is lost.", "fence"),
    ])

    # ---- (ii) phenocopy ----------------------------------------------------
    block(ax, 4.92, "(ii)   Phenocopy", [
        ("Silence FB5 with shibire^ts, with no anesthetic present. If the fly lands in the same state the anesthetic produces — same physiology, same behavior —", "claim"),
        ("the genetic cut has copied the drug's state. 'Same state' means the whole pattern: the cognitive readout degraded by the same amount, turning intact, LAL013 intact.", "claim"),
        ("Illustration: at its EC50 the drug leaves cognition at 50% and turning at 100%; FB5 off alone should then leave cognition at ≈50% and turning at ≈100%.", "fence"),
        ("If it fails: FB5 off degrades cognition only slightly, or also kills turning — the pattern does not match, and the drug must act beyond FB5.", "fence"),
    ])

    # ---- (iii) occlusion / two routes ---------------------------------------
    block(ax, 3.68, "(iii)   Occlusion, and the two-route dissociation", [
        ("Deactivate first, then add the graded anesthetic. The same arms answer two claims, and each claim is read off its own readout:", "claim"),
        ("The narrow claim (the cognitive readout): if FB5 is already off and the drug adds nothing further, the drug's cognitive action runs through FB5. That is occlusion.", "claim"),
        ("The target claim (both routes): FB off degrades the cognitive readout, and FB off + drug degrades it most — the drug then removes the remaining route,", "claim"),
        ("the fast ExR7→LAL013 action channel — 'shoot first, ask questions later' — while the FB route is the one that evaluates.", "claim"),
        ("The drug's extra effect on top of the cut counts as the LAL route only if it appears at the doses where LAL013's own dose–response curve falls.", "claim"),
        ("Boundary cases, outside both claims: FB off leaving the readout fully intact means FB5 is not necessary for that behavior; FB off abolishing", "fence"),
        ("the readout entirely floors the test, and occlusion cannot be judged — occlusion is claimable only on partial degradation.", "fence"),
        ("Specificity control: with LAL013 off, the prediction is no occlusion on the cognitive readout.", "fence"),
    ])

    # ---- closing strip -------------------------------------------------------
    ax.add_patch(FancyBboxPatch((0.55, 0.28), 12.23, 1.27,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=PANEL, edgecolor=TEAL, lw=1.1))
    ax.text(0.85, 1.33, "Expected ordering, if the hypothesis holds",
            fontsize=12, color=TEAL, fontweight="bold", va="center")
    ax.text(0.85, 1.05,
            "The cognitive readout's EC50 sits below turning's EC50: cognition is lost at doses where the fast ExR7→LAL013 route still works.",
            **CLAIM)
    ax.text(0.85, 0.80,
            "The same ordering as clinical anesthesia, where awareness is lost at doses below those that abolish movement.",
            **CLAIM)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_qbi")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "bruno-what-counts.png")
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print("wrote", out)


if __name__ == "__main__":
    build()

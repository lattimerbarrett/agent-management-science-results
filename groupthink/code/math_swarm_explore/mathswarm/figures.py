"""Figures for a run. To the point: axes, lines, a legend. Anything else to say goes in the caption, which is
returned and written beside the image, not drawn on it.

Two measures on two scales get two panels, never two axes on one. Arms take the colours in a fixed order, so
an arm keeps its colour whichever arms are plotted with it. The palette is the validated reference one of the
chart guidelines in use here (colour-blind separation checked on neighbouring arms); three of its colours are
light against the background, so each line also carries its arm's name at its end.

`pairs` is the figure an approach is judged by (Barrett, 2026-10-13): a bar for each arm, of how the pairs of a
problem's agents ended. There the colours are the kinds of a pair, the same in every figure: both right at the
foot and on the same wrong answer at the top, so that each of the two is read from an edge that does not move.
"""
from __future__ import annotations

from .report import baseline_of, in_words, shared_only, summary_of
from .tracking import Run

SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
SURFACE, INK, QUIET, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
KINDS = (("both_right", "both right", "#2e7d32", "white"), ("right_and_wrong", "one right, one wrong", "#9e9e9e", INK),
         ("no_answer", "one has no answer", "#e0e0e0", INK), ("different_wrong", "different wrong answers", "#f4a6a0", INK),
         ("same_wrong", "same wrong answer", "#b71c1c", "white"))       # a pair's kinds from the foot of a bar up: colour, and ink on it


def steps(run: Run) -> str:
    """After each step, the share of agents on the right answer and how many different answers were held, one
    line per arm. Writes steps.png and steps.md (the caption) into the run's folder and returns the caption."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    episodes = run.read("episodes")
    shared = shared_only(episodes)             # arms are drawn on the problems all of them played
    summary = summary_of(shared, baseline_of(run.config["settings"]))
    if not summary:
        raise SystemExit(f"{run.folder} has no problems that every arm has played to plot")
    if len(summary) > len(SERIES):
        raise SystemExit(f"{len(summary)} arms is more than one figure can tell apart ({len(SERIES)}): plot fewer")
    panels = (("right", "agents on the right answer (%)", 100.0), ("distinct", "different answers held", 1.0))
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8), facecolor=SURFACE)
    for ax, (key, label, scale) in zip(axes, panels):
        ax.set_facecolor(SURFACE)
        longest, lines = 0, {}
        for colour, (arm, entry) in zip(SERIES, summary.items()):
            values = [scale * r[key] for r in entry["all"]["by_round"]]
            longest = max(longest, len(values))
            ax.plot(range(1, len(values) + 1), values, color=colour, linewidth=2, marker="o", markersize=6, clip_on=False,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, solid_capstyle="round", solid_joinstyle="round", label=arm)
            lines[arm] = values
        ax.set_xticks(range(1, longest + 1))
        ax.set_xlim(0.8, longest + 0.2 + 0.22 * longest * (len(summary) <= 4))
        ax.set_ylim(bottom=0, top=100 if key == "right" else None)
        ax.set_xlabel("step", color=QUIET, fontsize=10)
        if len(summary) <= 4:                  # each line's name at its end, moved up off other names
            def height(y):
                return ax.transData.transform((0, y))[1] * 72 / fig.dpi
            names: list[float] = []
            for arm, values in sorted(lines.items(), key=lambda line: line[1][-1]):
                at, shift = height(values[-1]), 0.0
                while any(abs(at + shift - busy) < 11 for busy in names):
                    shift += 1.0
                names.append(at + shift)
                ax.annotate(arm, (len(values), values[-1]), xytext=(9, shift), textcoords="offset points", va="center", color=QUIET, fontsize=9)
        ax.set_ylabel(label, color=QUIET, fontsize=10)
        ax.grid(axis="y", color=GRID, linewidth=1)
        ax.set_axisbelow(True)
        ax.tick_params(colors=QUIET, length=0, labelsize=9)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
    if len(summary) > 1:
        axes[0].legend(frameon=False, fontsize=9, labelcolor=INK, loc="best")
    fig.tight_layout()
    fig.savefig(run.path("steps.png"), dpi=160, facecolor=SURFACE)
    plt.close(fig)

    problems = max(entry["all"]["problems"] for entry in summary.values())
    which = f"the {problems} problems every arm has played" if len(shared) < len(episodes) else f"{problems} problems"
    caption = (f"Figure: {run.config['experiment']} / {run.config['run']}, {which}. Left: share of agents holding the "
               "right answer after each of their steps (an agent that has stopped keeps its answer). Right: how many "
               "different answers a problem's agents held. Each point is a mean over problems. The numbers are in summary.md.")
    run.path("steps.md").write_text(f"![steps](steps.png)\n\n{caption}\n")
    return f"wrote {run.path('steps.png')}\n{caption}"


def pairs(run: Run) -> str:
    """How the pairs of a problem's agents ended, a bar for each arm: both right, one right and one wrong, one with
    no answer, on different wrong answers, on the same wrong answer, as percents of a problem's pairs averaged
    over problems. Writes pairs.png and pairs.md (the caption) into the run's folder and returns the caption."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    episodes = run.read("episodes")
    shared = shared_only(episodes)             # arms are drawn on the problems all of them played
    summary = summary_of(shared, baseline_of(run.config["settings"]))
    if not summary:
        raise SystemExit(f"{run.folder} has no problems that every arm has played to plot")
    saved = {arm["name"]: arm for key, arm in run.config["settings"].items() if key.startswith("arm:")}
    words = [in_words(saved[arm]) if arm in saved else arm for arm in summary]
    words = words if len(set(words)) == len(words) else list(summary)        # two arms that read alike: by their names
    fig, ax = plt.subplots(figsize=(2.2 + 1.7 * len(summary) + 2.6, 4.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    at, foot = range(len(summary)), [0.0] * len(summary)
    for kind, label, colour, ink in KINDS:
        heights = [100 * entry["all"]["pairs"][kind]["mean"] for entry in summary.values()]
        ax.bar(at, heights, 0.62, bottom=foot, color=colour, edgecolor=SURFACE, linewidth=1, label=label)
        for x, (height, below) in enumerate(zip(heights, foot)):
            if height >= 4:                    # a share too thin to hold its number is read off the table
                ax.text(x, below + height / 2, f"{height:.0f}%", ha="center", va="center", fontsize=10, color=ink)
        foot = [below + height for below, height in zip(foot, heights)]
    ax.set_xticks(list(at))
    ax.set_xticklabels(words, color=INK, fontsize=10)
    ax.set_xlim(-0.6, len(summary) - 0.4)
    ax.set_ylim(0, 100)
    ax.set_ylabel("pairs of a problem's agents (%)", color=QUIET, fontsize=10)
    ax.tick_params(colors=QUIET, length=0, labelsize=9)
    ax.tick_params(axis="x", labelsize=10, labelcolor=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], frameon=False, fontsize=9.5, labelcolor=INK, loc="center left", bbox_to_anchor=(1.0, 0.5))
    fig.tight_layout()
    fig.savefig(run.path("pairs.png"), dpi=160, facecolor=SURFACE)
    plt.close(fig)

    entries = list(summary.values())
    problems, agents = max(entry["all"]["problems"] for entry in entries), sorted({arm["agents"] for arm in saved.values() if arm["name"] in summary})
    which = f"the {problems} problems every arm has played" if len(shared) < len(episodes) else f"{problems} problems"
    bars = ", ".join(f"{' '.join(word.split())} (`{arm}`)" for word, arm in zip(words, summary) if word != arm) or ", ".join(f"`{arm}`" for arm in summary)
    caption = (f"Figure: {run.config['experiment']} / {run.config['run']}, {which}, {' or '.join(map(str, agents))} agents a problem. "
               "Every pair of a problem's agents, by how the two ended, as a percent of the problem's pairs averaged "
               f"over problems. Bars: {bars}. The numbers: `uv run lab show {run.config['experiment']}/{run.config['run']}`.")
    run.path("pairs.md").write_text(f"![pairs](pairs.png)\n\n{caption}\n")
    return f"wrote {run.path('pairs.png')}\n{caption}"

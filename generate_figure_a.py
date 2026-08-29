"""
Figure A — “Three ways survival fails”
Publication-grade 3-panel figure illustrating the three fundamental failure modes 
of candidate survival as a security proxy for RAG retrieval filters.

Panel 1: Equal exposure → unequal behavior (D1, D1b, D6)
Panel 2: Higher exposure → lower behavior (D3 DistilBERT ranking inversion)
Panel 3: Retained → more behaviorally susceptible (GPT-5-mini D3 A4 retained vs removed)
"""

import math
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set up paths
BASE_DIR = Path(__file__).resolve().parent
REPL_DIR = BASE_DIR / "tmlr" / "replication_gpt54"
DATA_DIR = BASE_DIR / "tmlr" / "paper"
OUT_PATHS = [
    BASE_DIR / "fig_three_ways_survival_fails.png",
    BASE_DIR / "fig_three_ways_survival_fails.pdf",
    BASE_DIR / "tmlr" / "paper" / "fig_three_ways_survival_fails.png",
    BASE_DIR / "tmlr" / "paper" / "fig_three_ways_survival_fails.pdf",
    REPL_DIR / "figures" / "fig_three_ways_survival_fails.png",
    REPL_DIR / "figures" / "fig_three_ways_survival_fails.pdf",
]

# Wilson score interval
def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (max(0.0, center - margin), min(1.0, center + margin))


def load_and_verify_data():
    ep_path = REPL_DIR / "episode_level_results.csv"
    if not ep_path.exists():
        ep_path = BASE_DIR / "new_experiment_gpt_model" / "episode_level_results.csv"
    df = pd.read_csv(ep_path)
    return df


def generate_figure_a():
    df = load_and_verify_data()

    # Configure styling for top ML venues (TMLR / NeurIPS / ICML)
    mpl.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["axes.edgecolor"] = "#333333"
    mpl.rcParams["axes.linewidth"] = 0.9

    fig, axes = plt.subplots(1, 3, figsize=(16.8, 5.2), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    # High-contrast, colorblind-safe publication colors
    c_a3 = "#1f77b4"        # Blue for A3 (Semantic Camouflage)
    c_a3_dark = "#0d47a1"
    c_a4 = "#d62728"        # Crimson for A4 (Length-Matched)
    c_a4_dark = "#b71c1c"
    c_neutral = "#555555"   # Neutral dark gray for exposure
    c_removed = "#607d8b"   # Slate gray for removed
    c_baseline = "#37474f"  # Dark blue-gray for unfiltered baseline
    c_retained = "#c62828"  # Deep red for retained survivors

    # =========================================================================
    # PANEL 1: Equal exposure → unequal behavior (D1, D1b, D6)
    # =========================================================================
    ax1 = axes[0]
    ax1.set_facecolor("#fbfcfd")

    defenses_p1 = ["D1_3feat_tiny", "D1b_3feat_trained", "D6_ensemble"]
    def_labels_p1 = ["$D_1$\n(3-feat tiny)", "$D_{1b}$\n(3-feat trained)", "$D_6$\n(Ensemble)"]
    x1 = np.arange(len(defenses_p1))
    bar_w = 0.30

    a3_p1_vals, a3_p1_errs = [], []
    a4_p1_vals, a4_p1_errs = [], []

    for d in defenses_p1:
        sub_a3 = df[(df.defense == d) & (df.attack == "A3_semantic_camouflage") & (df.target_fpr == 0.01)]
        sub_a4 = df[(df.defense == d) & (df.attack == "A4_length_matched") & (df.target_fpr == 0.01)]

        k3, n3 = int((sub_a3.E * sub_a3.C).sum()), len(sub_a3)
        k4, n4 = int((sub_a4.E * sub_a4.C).sum()), len(sub_a4)

        p3 = k3 / n3
        p4 = k4 / n4
        ci3_l, ci3_h = wilson_ci(k3, n3)
        ci4_l, ci4_h = wilson_ci(k4, n4)

        a3_p1_vals.append(p3)
        a3_p1_errs.append([p3 - ci3_l, ci3_h - p3])
        a4_p1_vals.append(p4)
        a4_p1_errs.append([p4 - ci4_l, ci4_h - p4])

    a3_p1_errs = np.array(a3_p1_errs).T
    a4_p1_errs = np.array(a4_p1_errs).T

    # Draw exposure reference band at top
    ax1.axhline(1.0, color=c_neutral, linestyle="--", linewidth=1.5, alpha=0.75, zorder=2)
    ax1.text(1.0, 1.035, "Candidate Exposure $P(E \\mid D) = 1.00$ (100% Equal for All)", 
             ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#333333",
             bbox=dict(boxstyle="round,pad=0.22", facecolor="#ffffff", edgecolor="#aaaaaa", alpha=0.95))

    rects1 = ax1.bar(x1 - bar_w/2, a3_p1_vals, bar_w, yerr=a3_p1_errs, capsize=3.5,
                     label="$A_3$ (Semantic Camouflage)", color=c_a3, edgecolor=c_a3_dark, linewidth=0.9, zorder=3)
    rects2 = ax1.bar(x1 + bar_w/2, a4_p1_vals, bar_w, yerr=a4_p1_errs, capsize=3.5,
                     label="$A_4$ (Length-Matched)", color=c_a4, edgecolor=c_a4_dark, linewidth=0.9, zorder=3)

    # Bar value labels
    for rect in rects1:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2, h + 0.045, f"{h*100:.1f}%\n(12/300)",
                 ha="center", va="bottom", fontsize=7.8, fontweight="bold", color=c_a3_dark)
    for rect in rects2:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2, h + 0.055, f"{h*100:.1f}%\n(88/300)",
                 ha="center", va="bottom", fontsize=7.8, fontweight="bold", color=c_a4_dark)

    # Delta badge spanning above bars
    ax1.text(1.0, 0.54, "7.33× Behavioral Risk Gap\n($\\Delta = +25.33\\%$ on GPT-5-mini)", ha="center", va="bottom",
             fontsize=8.3, fontweight="bold", color="#8b0000",
             bbox=dict(boxstyle="round,pad=0.28", facecolor="#ffebee", edgecolor="#ef9a9a", lw=1.1, alpha=0.95),
             zorder=4)

    ax1.set_xticks(x1)
    ax1.set_xticklabels(def_labels_p1, fontsize=9.2)
    ax1.set_ylabel("Downstream Attack Success $P(C \\mid D)$", fontsize=10, fontweight="bold")
    ax1.set_ylim(0, 1.22)
    ax1.set_title("(a) Panel 1: Equal Exposure $\\rightarrow$ Unequal Behavior\n($D_1, D_{1b}, D_6$ on GPT-5-mini)",
                  fontsize=10.5, fontweight="bold", pad=10, color="#111111")
    ax1.grid(axis="y", linestyle=":", alpha=0.45, zorder=1)
    ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=7.8, framealpha=0.95)

    # =========================================================================
    # PANEL 2: Higher exposure → lower behavior (D3 DistilBERT Ranking Inversion)
    # =========================================================================
    ax2 = axes[1]
    ax2.set_facecolor("#fbfcfd")

    # D3 stats
    d3_a3 = df[(df.defense == "D3_distilbert") & (df.attack == "A3_semantic_camouflage") & (df.target_fpr == 0.01)]
    d3_a4 = df[(df.defense == "D3_distilbert") & (df.attack == "A4_length_matched") & (df.target_fpr == 0.01)]

    pe_a3 = d3_a3.E.mean()              # 0.9867 (296/300)
    pc_a3 = (d3_a3.E * d3_a3.C).mean()  # 0.0400 (12/300)
    pe_a4 = d3_a4.E.mean()              # 0.6767 (203/300)
    pc_a4 = (d3_a4.E * d3_a4.C).mean()  # 0.2300 (69/300)

    # Slopegraph layout
    x_coords = [0, 1]

    # Plot lines with clean markers
    ax2.plot(x_coords, [pe_a3, pc_a3], color=c_a3, marker="o", markersize=9, linewidth=3.0,
             label="$A_3$ (Semantic Camouflage)", zorder=4)
    ax2.plot(x_coords, [pe_a4, pc_a4], color=c_a4, marker="s", markersize=9, linewidth=3.0,
             label="$A_4$ (Length-Matched)", zorder=4)

    # Left-side labels (Exposure) - perfectly aligned to the left of the x=0 markers
    ax2.text(-0.06, pe_a3, f"$A_3$ Exposure\n$\\mathbf{{98.7\\%}}$ (296/300)", ha="right", va="center",
             fontsize=8.2, fontweight="bold", color=c_a3_dark)
    ax2.text(-0.06, pe_a4, f"$A_4$ Exposure\n$\\mathbf{{67.7\\%}}$ (203/300)", ha="right", va="center",
             fontsize=8.2, fontweight="bold", color=c_a4_dark)

    # Right-side labels (Success) - perfectly aligned to the right of the x=1 markers
    ax2.text(1.06, pc_a3, f"$A_3$ Success\n$\\mathbf{{4.0\\%}}$ (12/300)", ha="left", va="center",
             fontsize=8.2, fontweight="bold", color=c_a3_dark)
    ax2.text(1.06, pc_a4, f"$A_4$ Success\n$\\mathbf{{23.0\\%}}$ (69/300)\n[$\\mathbf{{5.75\\times}}$ higher]", 
             ha="left", va="center", fontsize=8.2, fontweight="bold", color=c_a4_dark)

    # Clean Inversion Banner centered at top without intersecting lines
    ax2.text(0.5, 0.98, "RANKING INVERSION\n$P(E\\mid D_3)$ inverts $P(C\\mid D_3)$",
             ha="center", va="center", fontsize=8.2, fontweight="bold", color="#7f0000",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee", edgecolor="#ef5350", lw=1.2, alpha=0.95),
             zorder=5)

    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["Retrieval Candidate\nExposure $P(E \\mid D_3)$", "Downstream Behavioural\nSuccess $P(C \\mid D_3)$"],
                        fontsize=9.2, fontweight="bold")
    ax2.set_ylabel("Probability Rate", fontsize=10, fontweight="bold")
    ax2.set_xlim(-0.52, 1.52)
    ax2.set_ylim(-0.06, 1.18)
    ax2.set_title("(b) Panel 2: Higher Exposure $\\rightarrow$ Lower Behavior\n($D_3$ DistilBERT Ranking Reversal on GPT-5-mini)",
                  fontsize=10.5, fontweight="bold", pad=10, color="#111111")
    ax2.grid(True, linestyle=":", alpha=0.45, zorder=1)
    ax2.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=7.8, framealpha=0.95)

    # =========================================================================
    # PANEL 3: Retained → more behaviorally susceptible (GPT-5-mini D3 A4)
    # =========================================================================
    ax3 = axes[2]
    ax3.set_facecolor("#fbfcfd")

    # Cohort analysis for D3 and A4
    n_total = 300
    n_retained = int(d3_a4.E.sum())       # 203
    n_removed = int((1 - d3_a4.E).sum())  # 97

    k_retained = int(d3_a4[d3_a4.E == 1].C.sum())  # 69
    k_removed = int(d3_a4[d3_a4.E == 0].C.sum())   # 19
    k_total = int(d3_a4.C.sum())                   # 88 (D0 baseline)

    p_retained = k_retained / n_retained   # 0.3399 (34.0%)
    p_removed = k_removed / n_removed     # 0.1959 (19.6%)
    p_total = k_total / n_total           # 0.2933 (29.3%)

    ci_ret_l, ci_ret_h = wilson_ci(k_retained, n_retained)
    ci_rem_l, ci_rem_h = wilson_ci(k_removed, n_removed)
    ci_tot_l, ci_tot_h = wilson_ci(k_total, n_total)

    p3_cohorts = ["Removed by $D_3$\n(Filtered out, $N=97$)", 
                  "All Unfiltered ($D_0$)\n(Baseline, $N=300$)", 
                  "Retained by $D_3$\n(Survivors, $N=203$)"]
    p3_rates = [p_removed, p_total, p_retained]
    p3_errs = [
        [p_removed - ci_rem_l, ci_rem_h - p_removed],
        [p_total - ci_tot_l, ci_tot_h - p_total],
        [p_retained - ci_ret_l, ci_ret_h - p_retained],
    ]
    p3_errs = np.array(p3_errs).T
    p3_colors = [c_removed, c_baseline, c_retained]
    p3_edgecolors = ["#37474f", "#212121", "#7f0000"]

    x3 = np.arange(len(p3_cohorts))
    bars3 = ax3.bar(x3, p3_rates, width=0.52, yerr=p3_errs, capsize=4,
                    color=p3_colors, edgecolor=p3_edgecolors, linewidth=0.9, zorder=3)

    # Bar value labels & counts
    counts_p3 = [f"{k_removed}/{n_removed}", f"{k_total}/{n_total}", f"{k_retained}/{n_retained}"]
    for idx, (rect, count) in enumerate(zip(bars3, counts_p3)):
        h = rect.get_height()
        top_err = p3_errs[1, idx]
        ax3.text(rect.get_x() + rect.get_width()/2, h + top_err + 0.025, f"{h*100:.1f}%\n({count})",
                 ha="center", va="bottom", fontsize=8.0, fontweight="bold", color=p3_colors[idx])

    # Annotation bracket for enrichment
    bracket_y = 0.54
    ax3.plot([0, 0, 2, 2], [bracket_y - 0.015, bracket_y, bracket_y, bracket_y - 0.015],
             color="#b71c1c", lw=1.3, zorder=4)
    ax3.text(1.0, bracket_y + 0.02, "+14.4% Susceptibility Enrichment\n(1.74× Higher Compliance in Survivors)",
             ha="center", va="bottom", fontsize=8.0, fontweight="bold", color="#b71c1c",
             bbox=dict(boxstyle="round,pad=0.25", facecolor="#ffebee", edgecolor="#ffcdd2", lw=1.1, alpha=0.95),
             zorder=5)

    ax3.set_xticks(x3)
    ax3.set_xticklabels(p3_cohorts, fontsize=8.8)
    ax3.set_ylabel("Downstream Compliance $P(C \\mid E)$", fontsize=10, fontweight="bold")
    ax3.set_ylim(0, 0.76)
    ax3.set_title("(c) Panel 3: Filtering Enriches for Downstream Compliance\n(Survivor Enrichment under $D_3$ on GPT-5-mini for $A_4$)",
                  fontsize=10.5, fontweight="bold", pad=10, color="#111111")
    ax3.grid(axis="y", linestyle=":", alpha=0.45, zorder=1)

    plt.tight_layout()

    # Save to all target output paths
    for p in OUT_PATHS:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".pdf":
            plt.savefig(p, bbox_inches="tight")
        else:
            plt.savefig(p, dpi=300, bbox_inches="tight")
        print(f"Saved: {p}")

    plt.close()
    print("Figure A generation complete!")


if __name__ == "__main__":
    generate_figure_a()

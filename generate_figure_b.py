"""
Generate publication-quality 2-panel Figure B
Panel (a): Global Parameter Space (Delta E vs Delta B)
Panel (b): Detail of Cluster Near Equal Exposure (x in [-0.06, 0.13])
With zero overlapping text, zero overlapping lines, and proper canvas margins.
"""

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
REPL_DIR = BASE_DIR / "tmlr" / "replication_gpt54"
DATA_DIR = BASE_DIR / "tmlr" / "paper"
OUT_PATHS = [
    BASE_DIR / "fig_exposure_vs_behavioral_ordering.png",
    BASE_DIR / "fig_exposure_vs_behavioral_ordering.pdf",
    BASE_DIR / "tmlr" / "paper" / "fig_exposure_vs_behavioral_ordering.png",
    BASE_DIR / "tmlr" / "paper" / "fig_exposure_vs_behavioral_ordering.pdf",
    REPL_DIR / "figures" / "fig_exposure_vs_behavioral_ordering.png",
    REPL_DIR / "figures" / "fig_exposure_vs_behavioral_ordering.pdf",
]

def load_data():
    sum_path = REPL_DIR / "attack_detector_summary.csv"
    if not sum_path.exists():
        sum_path = BASE_DIR / "new_experiment_gpt_model" / "attack_detector_summary.csv"
    df = pd.read_csv(sum_path)
    
    a3 = df[df.attack == "A3_semantic_camouflage"].copy()
    a4 = df[df.attack == "A4_length_matched"].copy()

    merged = pd.merge(a3, a4, on=["defense", "target_fpr", "model"], suffixes=("_A3", "_A4"))
    cells18 = merged[~merged.defense.isin(["D0_none", "D4_guard_zeroshot"])].copy()

    cells18["dx"] = cells18["P_E_given_D_A3"] - cells18["P_E_given_D_A4"]
    cells18["dy"] = cells18["P_C_given_D_A3"] - cells18["P_C_given_D_A4"]
    return cells18

def generate_figure_b():
    cells18 = load_data()

    # Styling for TMLR publication
    mpl.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["axes.edgecolor"] = "#334155"
    mpl.rcParams["axes.linewidth"] = 0.85

    det_style = {
        "D1_3feat_tiny": {"label": "$D_1$ (3-feat tiny)", "color": "#1f77b4", "marker": "o"},
        "D1b_3feat_trained": {"label": "$D_{1b}$ (3-feat trained)", "color": "#0d9488", "marker": "D"},
        "D2_embed_probe": {"label": "$D_2$ (Embed probe)", "color": "#16a34a", "marker": "s"},
        "D3_distilbert": {"label": "$D_3$ (DistilBERT)", "color": "#dc2626", "marker": "P"},
        "D5_perplexity": {"label": "$D_5$ (Perplexity)", "color": "#ea580c", "marker": "^"},
        "D6_ensemble": {"label": "$D_6$ (Ensemble)", "color": "#7c3aed", "marker": "X"},
    }

    fpr_size = {0.001: 70, 0.01: 130, 0.05: 200}
    fpr_label = {0.001: "0.1%", 0.01: "1.0%", 0.05: "5.0%"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.2, 5.8), dpi=300,
                                   gridspec_kw={"width_ratios": [1.15, 1.0], "wspace": 0.28})
    fig.patch.set_facecolor("#ffffff")

    # =========================================================================
    # PANEL (a): Global Landscape (Delta E vs Delta B)
    # =========================================================================
    ax1.set_facecolor("#ffffff")
    ax1.fill_between([0, 1.15], -0.34, 0, color="#fff1f2", alpha=0.85, zorder=0)
    ax1.fill_between([0, 1.15], 0, 0.10, color="#f0fdf4", alpha=0.6, zorder=0)
    ax1.fill_between([-0.20, 0], -0.34, 0, color="#f8fafc", alpha=0.6, zorder=0)

    ax1.axhline(0, color="#64748b", linestyle="-", linewidth=0.9, zorder=1)
    ax1.axvline(0, color="#64748b", linestyle="-", linewidth=0.9, zorder=1)

    # Plot all 18 points in Panel 1
    for idx, r in cells18.iterrows():
        d = r["defense"]
        fpr = r["target_fpr"]
        st = det_style[d]
        sz = fpr_size[fpr]
        ax1.scatter(r["dx"], r["dy"], color=st["color"], marker=st["marker"], s=sz,
                    edgecolor="#0f172a", linewidth=0.75, alpha=0.92, zorder=4)

    # Clean text labels only for the separated points
    ax1.text(0.31 - 0.025, -0.195, "$D_3$ (1% FPR)\n$\\Delta E=+0.31, \\Delta B=-0.19$",
             fontsize=7.5, fontweight="bold", color="#dc2626", ha="right", va="center", zorder=5)

    ax1.text(0.337 + 0.025, -0.165, "$D_5$ (1% FPR)\n$\\Delta E=+0.34, \\Delta B=-0.17$",
             fontsize=7.5, fontweight="bold", color="#ea580c", ha="left", va="center", zorder=5)

    ax1.text(0.59 + 0.025, -0.077, "$D_3$ (5% FPR)\n$\\Delta E=+0.59, \\Delta B=-0.08$",
             fontsize=7.5, fontweight="bold", color="#dc2626", ha="left", va="center", zorder=5)

    ax1.text(0.917 - 0.025, 0.027 + 0.015, "$D_5$ (5% FPR)\n$\\Delta E=+0.92, \\Delta B=+0.03$",
             fontsize=7.5, fontweight="bold", color="#ea580c", ha="right", va="bottom", zorder=5)

    # Quadrant Headers (Separated cleanly from data points)
    ax1.text(0.50, -0.035, "STRICT RANKING REVERSAL ZONE ($x > 0,\\, y < 0$)\n"
                          "Exposure ranks $A_3$ above $A_4$, but behavior ranks $A_4$ above $A_3$ (8 cells)",
             ha="center", va="top", fontsize=8.0, fontweight="bold", color="#991b1b", zorder=2)

    ax1.text(0.45, 0.065, "Concordant Zone ($x > 0, y > 0$)\n1 cell ($D_5$ @ 5% FPR)",
             ha="center", va="center", fontsize=7.2, color="#166534", zorder=2)

    ax1.text(-0.09, -0.04, "Concordant Zone\n($x < 0, y < 0$)\n2 cells",
             ha="center", va="top", fontsize=7.0, color="#334155", zorder=2)

    # Highlight box around cluster
    rect = plt.Rectangle((-0.07, -0.27), 0.20, 0.055, fill=False, edgecolor="#2563eb",
                         linestyle="--", linewidth=1.2, zorder=3)
    ax1.add_patch(rect)
    ax1.text(0.03, -0.285, "Cluster near $x=0$ (13 cells)\n(See Detail View in Panel b $\\longrightarrow$)",
             fontsize=7.4, fontweight="bold", color="#2563eb", ha="center", va="top", zorder=5)

    ax1.set_xlim(-0.18, 1.05)
    ax1.set_ylim(-0.33, 0.09)
    ax1.set_xlabel("Candidate Exposure Difference: $\\Delta E = P(E \\mid D, A_3) - P(E \\mid D, A_4)$\n"
                   "$\\longleftarrow$ $A_4$ Higher Exposure  $\\vert$  $A_3$ Higher Exposure $\\longrightarrow$",
                   fontsize=8.5, fontweight="bold", labelpad=6)
    ax1.set_ylabel("Behavioral Attack Success Difference: $\\Delta B = P(C \\mid D, A_3) - P(C \\mid D, A_4)$\n"
                   "$\\longleftarrow$ $A_4$ Higher Behavioral Success  $\\vert$  $A_3$ Higher Behavioral Success $\\longrightarrow$",
                   fontsize=8.5, fontweight="bold", labelpad=6)
    ax1.set_title("(a) Global Exposure vs. Behavioral Ordering (18 Filter Cells)", fontsize=9.8, fontweight="bold", pad=8)
    ax1.grid(True, linestyle=":", alpha=0.35, zorder=0)

    # =========================================================================
    # PANEL (b): Detail View of the 13 Cells near x=0
    # =========================================================================
    ax2.set_facecolor("#ffffff")
    ax2.fill_between([0, 0.14], -0.275, -0.215, color="#fff1f2", alpha=0.85, zorder=0)
    ax2.fill_between([-0.07, 0], -0.275, -0.215, color="#f8fafc", alpha=0.6, zorder=0)
    ax2.axvline(0, color="#64748b", linestyle="-", linewidth=1.0, zorder=1)

    # In Panel (b), spread the 7 points at x=0 vertically so every single marker is 100% visible
    zoom_cells = cells18[cells18.dx <= 0.12].copy().sort_values(by=["dx", "defense", "target_fpr"])
    
    # 7 points at x=0
    eq_rows = zoom_cells[zoom_cells.dx == 0.0]
    y_spreads = np.linspace(-0.258, -0.248, len(eq_rows))
    
    for (idx, r), y_plot in zip(eq_rows.iterrows(), y_spreads):
        d = r["defense"]
        fpr = r["target_fpr"]
        st = det_style[d]
        sz = fpr_size[fpr]
        ax2.scatter(0.0, y_plot, color=st["color"], marker=st["marker"], s=sz,
                    edgecolor="#0f172a", linewidth=0.8, alpha=0.95, zorder=4)

    # Plot other points in zoom at their exact coordinates
    for idx, r in zoom_cells[zoom_cells.dx != 0.0].iterrows():
        d = r["defense"]
        fpr = r["target_fpr"]
        st = det_style[d]
        sz = fpr_size[fpr]
        ax2.scatter(r["dx"], r["dy"], color=st["color"], marker=st["marker"], s=sz,
                    edgecolor="#0f172a", linewidth=0.8, alpha=0.95, zorder=4)

    # Clean, non-overlapping labels in zoom
    ax2.text(-0.025, -0.268, "Equal Exposure ($x = 0$):\n$\\mathbf{7\\ cells}$ at $\\Delta B = -0.2533$\n"
                             "$D_1, D_{1b}, D_5, D_6$ (@ 0.1%, 1% FPR)\n"
                             "$A_4$ is $7.3\\times$ more potent downstream",
             fontsize=7.0, fontweight="bold", color="#1e293b", ha="center", va="top",
             bbox=dict(boxstyle="round,pad=0.22", facecolor="#ffffff", edgecolor="#cbd5e1", alpha=0.95), zorder=5)

    ax2.text(-0.0433, -0.224, "$D_{1b}$ (5% FPR)\n$\\Delta E=-0.043$",
             fontsize=7.0, color="#0d9488", ha="center", va="bottom", zorder=5)

    ax2.text(0.0167, -0.224, "$D_2$ (5% FPR)\n$\\Delta E=+0.017$",
             fontsize=7.0, color="#16a34a", ha="center", va="bottom", zorder=5)

    ax2.text(0.0267 + 0.005, -0.237, "$D_1$ (5% FPR)\n$\\Delta E=+0.027$",
             fontsize=7.0, color="#1f77b4", ha="left", va="center", zorder=5)

    ax2.text(0.0434, -0.258, "$D_3$ (0.1% FPR)\n$\\Delta E=+0.043$",
             fontsize=7.0, color="#dc2626", ha="center", va="top", zorder=5)

    ax2.text(0.110, -0.226, "$D_6$ (5% FPR)\n$\\Delta E=+0.110$",
             fontsize=7.0, color="#7c3aed", ha="center", va="bottom", zorder=5)

    ax2.set_xlim(-0.065, 0.130)
    ax2.set_ylim(-0.278, -0.218)
    ax2.set_xlabel("Candidate Exposure Difference: $\\Delta E = P(E \\mid D, A_3) - P(E \\mid D, A_4)$",
                   fontsize=8.5, fontweight="bold", labelpad=6)
    ax2.set_ylabel("Behavioral Attack Success Difference: $\\Delta B$",
                   fontsize=8.5, fontweight="bold", labelpad=6)
    ax2.set_title("(b) Detail View: Cluster Near Equal Exposure ($\\Delta E \\approx 0$)", fontsize=9.8, fontweight="bold", pad=8)
    ax2.grid(True, linestyle=":", alpha=0.35, zorder=0)

    # Shared Legend at Bottom with ample spacing
    legend_handles = []
    for d, st in det_style.items():
        h = ax1.scatter([], [], color=st["color"], marker=st["marker"], s=85,
                        edgecolor="#0f172a", linewidth=0.75, label=st["label"])
        legend_handles.append(h)
    
    for fpr, sz in fpr_size.items():
        h = ax1.scatter([], [], color="#475569", marker="o", s=sz,
                        edgecolor="#0f172a", linewidth=0.75, label=f"FPR = {fpr_label[fpr]}")
        legend_handles.append(h)

    fig.legend(handles=legend_handles, loc="lower center", bbox_to_anchor=(0.5, 0.01),
               ncol=5, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=7.8)

    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.22, top=0.92)

    # Save to all target paths
    for p in OUT_PATHS:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".pdf":
            plt.savefig(p, bbox_inches="tight")
        else:
            plt.savefig(p, dpi=300, bbox_inches="tight")
        print(f"Saved: {p}")

    plt.close()
    print("2-Panel Figure B generation complete!")

if __name__ == "__main__":
    generate_figure_b()

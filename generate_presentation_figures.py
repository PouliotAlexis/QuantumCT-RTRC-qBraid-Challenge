"""
Generate premium presentation figures for the Quantum CVRP Hackathon.
Outputs high-resolution PNG files in results/figures/.
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.gridspec import GridSpec
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

# ── Global Style ──────────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "figure.facecolor": "#0D1117",
    "axes.facecolor":   "#0D1117",
    "axes.edgecolor":   "#30363D",
    "axes.labelcolor":  "#C9D1D9",
    "xtick.color":      "#8B949E",
    "ytick.color":      "#8B949E",
    "text.color":       "#C9D1D9",
    "grid.color":       "#21262D",
    "grid.linestyle":   "--",
    "grid.alpha":       0.6,
    "font.family":      "DejaVu Sans",
    "figure.dpi":       150,
    "savefig.dpi":      200,
    "savefig.facecolor": "#0D1117",
})

QUANTUM_PURPLE = "#7C3AED"
QUANTUM_CYAN   = "#22D3EE"
QUANTUM_GREEN  = "#10B981"
QUANTUM_ORANGE = "#F59E0B"
QUANTUM_PINK   = "#EC4899"
QUANTUM_RED    = "#EF4444"
ACCENT_GOLD    = "#F5C518"
BG_COLOR       = "#0D1117"

ROUTE_COLORS = ["#22D3EE", "#10B981", "#F59E0B", "#EC4899", "#7C3AED"]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Instance data ──────────────────────────────────────────────────────────────
INSTANCES = {
    1: {"nodes": [(0,0), (-2,2), (-5,8), (2,3)],            "vehicles": 2, "capacity": 5},
    2: {"nodes": [(0,0), (-2,2), (-5,8), (2,3)],            "vehicles": 2, "capacity": 2},
    3: {"nodes": [(0,0), (-2,2), (-5,8), (2,3), (5,7), (2,4), (2,-3)], "vehicles": 3, "capacity": 2},
    4: {"nodes": [(0,0), (-2,2), (-5,8), (6,3), (4,4), (3,2), (0,2),
                  (-2,3), (-4,3), (2,3), (2,7), (-2,5), (-1,4)],         "vehicles": 4, "capacity": 3},
    5: {"nodes": [(0,0), (0,5), (-1,2), (1,2), (-2.5,1), (-1.5,1),
                  (-2,0.5), (2.5,1), (1.5,1), (2,0.5), (0.5,-1),
                  (-0.5,-1), (0,-1.5)],                                   "vehicles": 4, "capacity": 3},
}

# Best results per instance (from all_run_results.csv)
BEST_RESULTS = {
    1: {"calc": 21.74, "opt": 21.74,  "qubits": 16, "gates": 63,  "depth": 18,  "time": 5.97},
    2: {"calc": 26.18, "opt": 26.18,  "qubits": 9,  "gates": 50,  "depth": 11,  "time": 3.76},
    3: {"calc": 50.70, "opt": 49.50,  "qubits": 9,  "gates": 105, "depth": 11,  "time": 7.17},
    4: {"calc": 59.66, "opt": 58.18,  "qubits": 16, "gates": 500, "depth": 24,  "time": 188.92},
    5: {"calc": 25.96, "opt": None,   "qubits": 16, "gates": 376, "depth": 21,  "time": 672.43},
}

# Best routes per instance
BEST_ROUTES = {
    1: [[0,3,2,1,0]],
    2: [[0,2,1,0], [0,3,0]],
    3: [[0,6,4,0], [0,5,3,0], [0,1,2,0]],
    4: [[0,9,10,6,0], [0,12,11,2,0], [0,7,8,1,0], [0,3,4,5,0]],
    5: [[0,7,8,9,0], [0,3,1,2,0], [0,4,5,6,0], [0,11,12,10,0]],
}


def add_gradient_background(ax, color="#7C3AED", alpha=0.05):
    """Subtle vignette / gradient effect on the axes background."""
    ax.set_facecolor("#0D1117")


def draw_quantum_decorations(ax, alpha=0.15):
    """Decorative circuit-like lines."""
    for _ in range(5):
        x = np.random.uniform(*ax.get_xlim())
        y = np.random.uniform(*ax.get_ylim())
        ax.plot([x, x], ax.get_ylim(), color=QUANTUM_PURPLE, alpha=alpha*0.5, lw=0.4)
        ax.plot(ax.get_xlim(), [y, y], color=QUANTUM_CYAN, alpha=alpha*0.5, lw=0.4)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 – Solution Coverage: Calculated vs Optimal distances (bar chart)
# ══════════════════════════════════════════════════════════════════════════════
def fig_distance_comparison():
    instances = [1, 2, 3, 4]
    calc = [BEST_RESULTS[i]["calc"] for i in instances]
    opt  = [BEST_RESULTS[i]["opt"]  for i in instances]

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.suptitle("Quantum CVRP – Solution Quality", fontsize=18, fontweight="bold",
                 color=QUANTUM_CYAN, y=1.01)

    x = np.arange(len(instances))
    w = 0.35

    bars_opt  = ax.bar(x - w/2, opt,  w, label="Optimal (Classical)",
                       color=QUANTUM_CYAN, alpha=0.85, zorder=3)
    bars_calc = ax.bar(x + w/2, calc, w, label="Quantum Result",
                       color=QUANTUM_PURPLE, alpha=0.85, zorder=3)

    # Glow effect
    ax.bar(x - w/2, opt,  color=QUANTUM_CYAN,   alpha=0.2, zorder=2, width=w+0.05)
    ax.bar(x + w/2, calc, color=QUANTUM_PURPLE, alpha=0.2, zorder=2, width=w+0.05)

    for bar in bars_opt:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.2f}", ha="center", va="bottom",
                fontsize=10, color=QUANTUM_CYAN, fontweight="bold")
    for bar in bars_calc:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.2f}", ha="center", va="bottom",
                fontsize=10, color="#C9D1D9", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([f"Instance {i}" for i in instances], fontsize=12)
    ax.set_ylabel("Total Route Distance", fontsize=12)
    ax.set_title("Calculated vs Optimal Distance", fontsize=14, color=QUANTUM_CYAN, pad=10)
    ax.legend(fontsize=11, framealpha=0.3)
    ax.grid(axis="y", zorder=0)
    ax.set_ylim(0, max(calc) * 1.2)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig1_distance_comparison.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 – Quantum Circuit Complexity (Qubits, Gates, Depth)
# ══════════════════════════════════════════════════════════════════════════════
def fig_circuit_complexity():
    instances = [1, 2, 3, 4]
    qubits = [BEST_RESULTS[i]["qubits"] for i in instances]
    gates  = [BEST_RESULTS[i]["gates"]  for i in instances]
    depths = [BEST_RESULTS[i]["depth"]  for i in instances]

    fig, axes = plt.subplots(1, 3, figsize=(16, 9))
    fig.suptitle("Quantum Circuit Complexity Across Instances", fontsize=17,
                 fontweight="bold", color=QUANTUM_CYAN, y=1.03)

    labels = [f"Inst.\n{i}" for i in instances]
    metrics = [
        (axes[0], qubits, "# Qubits",          QUANTUM_PURPLE),
        (axes[1], gates,  "# Gate Operations",  QUANTUM_CYAN),
        (axes[2], depths, "Circuit Depth",       QUANTUM_ORANGE),
    ]

    for ax, data, ylabel, color in metrics:
        x = np.arange(len(instances))
        bars = ax.bar(x, data, color=color, alpha=0.80, zorder=3, width=0.6)
        ax.bar(x, data, color=color, alpha=0.15, zorder=2, width=0.7)  # glow

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data)*0.01,
                    str(int(bar.get_height())), ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color="#C9D1D9")

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(ylabel, fontsize=13, color=color, pad=8)
        ax.set_ylim(0, max(data) * 1.22)
        ax.grid(axis="y", zorder=0)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig2_circuit_complexity.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – Execution Time vs Circuit Depth (scatter + trend)
# ══════════════════════════════════════════════════════════════════════════════
def fig_time_vs_depth():
    instances = [1, 2, 3, 4, 5]
    times  = [BEST_RESULTS[i]["time"]  for i in instances]
    depths = [BEST_RESULTS[i]["depth"] for i in instances]
    gates  = [BEST_RESULTS[i]["gates"] for i in instances]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle("Execution Time vs Circuit Depth", fontsize=17,
                 fontweight="bold", color=QUANTUM_CYAN)

    # Bubble size proportional to gate count
    sizes = [g / max(gates) * 1200 + 80 for g in gates]
    colors_inst = [ROUTE_COLORS[i % len(ROUTE_COLORS)] for i in range(len(instances))]

    for i, (d, t, s, c, inst) in enumerate(zip(depths, times, sizes, colors_inst, instances)):
        ax.scatter(d, t, s=s, color=c, alpha=0.85, zorder=4, edgecolors="white", linewidths=0.8)
        ax.scatter(d, t, s=s*1.4, color=c, alpha=0.12, zorder=3)  # glow
        ax.annotate(f" Inst. {inst}", (d, t), fontsize=10, color=c,
                    fontweight="bold", va="center")

    # Trend line (log fit)
    x_fit = np.linspace(min(depths)-1, max(depths)+2, 200)
    poly  = np.polyfit(depths, np.log(times), 1)
    y_fit = np.exp(np.polyval(poly, x_fit))
    ax.plot(x_fit, y_fit, "--", color=QUANTUM_PURPLE, alpha=0.7, lw=1.8,
            label="Exponential trend")

    ax.set_xlabel("Circuit Depth", fontsize=12)
    ax.set_ylabel("Execution Time (s)", fontsize=12)
    ax.set_yscale("log")
    ax.legend(fontsize=10, framealpha=0.3)
    ax.grid(True, zorder=0)

    # Legend for bubble size
    for g_val, label in [(63, "63 gates"), (252, "252 gates"), (500, "500 gates")]:
        s = g_val / max(gates) * 1200 + 80
        ax.scatter([], [], s=s, color="#8B949E", alpha=0.7, label=label)
    ax.legend(fontsize=9, framealpha=0.3, loc="upper left")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig3_time_vs_depth.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 – CVRP Route Maps (premium version, 2×2 grid for Inst 1–4)
# ══════════════════════════════════════════════════════════════════════════════
def plot_instance_map(ax, inst_id, title_detail=""):
    inst  = INSTANCES[inst_id]
    nodes = inst["nodes"]  # node 0 = depot
    routes = BEST_ROUTES[inst_id]

    xs = [n[0] for n in nodes]
    ys = [n[1] for n in nodes]
    limit = max(max(abs(x) for x in xs), max(abs(y) for y in ys)) + 2.5

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, zorder=0, alpha=0.25)
    ax.axhline(0, color="#21262D", lw=0.8)
    ax.axvline(0, color="#21262D", lw=0.8)

    for ri, route in enumerate(routes):
        color = ROUTE_COLORS[ri % len(ROUTE_COLORS)]
        rx = [nodes[n][0] for n in route]
        ry = [nodes[n][1] for n in route]

        # Route line with glow
        ax.plot(rx, ry, "-", color=color, lw=2.5, alpha=0.9, zorder=3)
        ax.plot(rx, ry, "-", color=color, lw=6, alpha=0.1, zorder=2)

        # Arrows
        for j in range(len(rx) - 1):
            dx = rx[j+1] - rx[j]
            dy = ry[j+1] - ry[j]
            ax.annotate("", xy=(rx[j+1], ry[j+1]), xytext=(rx[j], ry[j]),
                        arrowprops=dict(arrowstyle="->", color=color,
                                        lw=1.5, mutation_scale=14),
                        zorder=5)

    # Customer nodes
    for idx in range(1, len(nodes)):
        ax.scatter(*nodes[idx], s=130, color="#C9D1D9", zorder=6, edgecolors="#0D1117", lw=1.2)
        ax.text(nodes[idx][0]+0.25, nodes[idx][1]+0.25, str(idx),
                fontsize=8, fontweight="bold", color="#C9D1D9", zorder=7)

    # Depot
    ax.scatter(0, 0, s=260, marker="*", color=ACCENT_GOLD, zorder=8,
               edgecolors="#0D1117", lw=1)
    ax.text(0.2, -0.6, "Depot", fontsize=7.5, color=ACCENT_GOLD, fontweight="bold", zorder=9)

    # Route legend
    patches = [mpatches.Patch(color=ROUTE_COLORS[i % len(ROUTE_COLORS)],
                               label=f"Vehicle {i+1}")
               for i in range(len(routes))]
    ax.legend(handles=patches, fontsize=7, loc="lower right", framealpha=0.35,
              facecolor="#0D1117", edgecolor="#30363D")

    best = BEST_RESULTS[inst_id]
    ax.set_title(f"Instance {inst_id} — Distance: {best['calc']:.2f}",
                 fontsize=10, color=QUANTUM_CYAN, pad=6)


def fig_route_maps():
    fig, axes = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Quantum CVRP — Optimized Routes (Instances 1–4)",
                 fontsize=17, fontweight="bold", color=QUANTUM_CYAN, y=1.01)

    for idx, inst_id in enumerate([1, 2, 3, 4]):
        ax = axes[idx // 2][idx % 2]
        plot_instance_map(ax, inst_id)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig4_route_maps.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 – Instance 5 route map (standalone, larger)
# ══════════════════════════════════════════════════════════════════════════════
def fig_instance5_map():
    fig, ax = plt.subplots(figsize=(9, 8))
    fig.suptitle("Quantum CVRP — Instance 5 (Best Result: 25.96)",
                 fontsize=15, fontweight="bold", color=QUANTUM_CYAN)
    plot_instance_map(ax, 5)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig5_instance5_map.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 – Summary dashboard (KPI cards)
# ══════════════════════════════════════════════════════════════════════════════
def fig_summary_dashboard():
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor("#0D1117")
    gs = GridSpec(2, 4, figure=fig, hspace=0.55, wspace=0.4)

    # Top: headline stats
    kpis = [
        ("5",           "Instances\nSolved",     QUANTUM_CYAN),
        ("100%",        "Inst. 1 & 2\nOptimal",  QUANTUM_GREEN),
        ("≤8.1%",       "Max Gap\nfrom Optimal", QUANTUM_ORANGE),
        ("6–748\nGates","Circuit\nRange",         QUANTUM_PURPLE),
    ]
    for i, (val, label, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor("#161B22")
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
        ax.text(0.5, 0.62, val, ha="center", va="center", fontsize=22,
                fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.22, label, ha="center", va="center", fontsize=10,
                color="#8B949E", transform=ax.transAxes)

    # Bottom-left: time bar (log scale)
    ax_time = fig.add_subplot(gs[1, :2])
    instances = [1, 2, 3, 4, 5]
    times = [BEST_RESULTS[i]["time"] for i in instances]
    labels = [f"Inst. {i}" for i in instances]
    x = np.arange(len(instances))

    bar_colors = [ROUTE_COLORS[i % len(ROUTE_COLORS)] for i in range(len(instances))]
    bars = ax_time.bar(x, times, color=bar_colors, alpha=0.85, zorder=3, width=0.6)
    ax_time.bar(x, times, color=bar_colors, alpha=0.15, zorder=2, width=0.7)
    ax_time.set_yscale("log")
    ax_time.set_xticks(x)
    ax_time.set_xticklabels(labels)
    ax_time.set_ylabel("Execution Time (s, log scale)", fontsize=10)
    ax_time.set_title("Execution Time per Instance", fontsize=12, color=QUANTUM_CYAN, pad=8)
    ax_time.grid(axis="y", zorder=0)
    for bar in bars:
        ax_time.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.1,
                     f"{bar.get_height():.1f}s", ha="center", va="bottom",
                     fontsize=8, color="#C9D1D9")

    # Bottom-right: radar-like quality plot
    ax_r = fig.add_subplot(gs[1, 2:])
    instance_labels = [f"Inst. {i}" for i in [1,2,3,4]]
    calc = [BEST_RESULTS[i]["calc"] for i in [1,2,3,4]]
    opt  = [BEST_RESULTS[i]["opt"]  for i in [1,2,3,4]]
    gaps = [(c/o - 1)*100 for c,o in zip(calc, opt)]

    x2 = np.arange(4)
    ax_r.bar(x2, gaps, color=[QUANTUM_GREEN if g < 2 else QUANTUM_ORANGE if g < 5 else QUANTUM_RED
                               for g in gaps],
             alpha=0.85, zorder=3, width=0.5)
    ax_r.axhline(0, color=QUANTUM_GREEN, lw=1.5, linestyle="--", label="Optimal gap (0%)")
    ax_r.set_xticks(x2)
    ax_r.set_xticklabels(instance_labels)
    ax_r.set_ylabel("Gap from Optimal (%)", fontsize=10)
    ax_r.set_title("Optimality Gap", fontsize=12, color=QUANTUM_CYAN, pad=8)
    ax_r.grid(axis="y", zorder=0)
    ax_r.legend(fontsize=9, framealpha=0.3)

    for i, g in enumerate(gaps):
        ax_r.text(i, g + 0.05, f"{g:.2f}%", ha="center", va="bottom",
                  fontsize=9, fontweight="bold", color="#C9D1D9")

    fig.suptitle("Quantum CVRP — Results Summary Dashboard",
                 fontsize=18, fontweight="bold", color=QUANTUM_CYAN, y=1.02)

    plt.savefig(os.path.join(OUTPUT_DIR, "fig6_dashboard.png"), bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved {os.path.join(OUTPUT_DIR, 'fig6_dashboard.png')}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 – Quantum Pipeline / Architecture diagram (matplotlib-drawn)
# ══════════════════════════════════════════════════════════════════════════════
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#0D1117")

    steps = [
        ("CVRP\nInstance", "#22D3EE",   1.0),
        ("K-Means\nClustering", "#7C3AED", 3.2),
        ("TSP sub-\nproblems", "#F59E0B",  5.4),
        ("VQE /\nQAOA", "#EC4899",         7.6),
        ("Route\nDecoding", "#10B981",     9.8),
        ("Solution\n& Metrics", "#F5C518", 12.0),
    ]

    box_w, box_h = 1.6, 1.4
    for label, color, cx in steps:
        # Glowing box
        fancy = mpatches.FancyBboxPatch((cx - box_w/2, 1.3), box_w, box_h,
                                         boxstyle="round,pad=0.12",
                                         linewidth=2, edgecolor=color,
                                         facecolor="#161B22", zorder=3)
        ax.add_patch(fancy)
        # Glow behind
        glow = mpatches.FancyBboxPatch((cx - box_w/2 - 0.05, 1.25), box_w+0.1, box_h+0.1,
                                        boxstyle="round,pad=0.12",
                                        linewidth=0, facecolor=color, alpha=0.08, zorder=2)
        ax.add_patch(glow)
        ax.text(cx, 2.0, label, ha="center", va="center", fontsize=10,
                fontweight="bold", color=color, zorder=5)

    # Arrows between steps
    arrow_y = 2.0
    for i in range(len(steps) - 1):
        x0 = steps[i][2]   + box_w/2
        x1 = steps[i+1][2] - box_w/2
        ax.annotate("", xy=(x1, arrow_y), xytext=(x0, arrow_y),
                    arrowprops=dict(arrowstyle="->", color="#8B949E",
                                   lw=1.8, mutation_scale=18),
                    zorder=4)

    ax.text(7, 3.7, "Quantum CVRP Solver Pipeline",
            ha="center", va="center", fontsize=15,
            fontweight="bold", color=QUANTUM_CYAN, zorder=6)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig7_pipeline.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 8 – Instance 4 repeated runs (spread/stability)
# ══════════════════════════════════════════════════════════════════════════════
def fig_instance4_runs():
    """Show the variability across multiple Instance 4 runs."""
    # From all_run_results.csv – Instance 4 rows
    runs_18 = [63.05, 61.03, 63.18, 60.22, 62.21, 60.47]   # depth 18
    runs_21 = [63.38, 60.06, 60.22, 62.34, 62.21, 58.42]   # depth 21
    runs_24 = [53.26, 52.93, 51.24, 62.57, 59.66, 59.66]   # depth 24 (inc. some with depth 24)
    opt = 58.18

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle("Instance 4 – Multi-Run Stability Analysis", fontsize=16,
                 fontweight="bold", color=QUANTUM_CYAN)

    groups = [("Depth 18", runs_18, QUANTUM_CYAN),
              ("Depth 21", runs_21, QUANTUM_ORANGE),
              ("Depth 24", runs_24, QUANTUM_PURPLE)]

    x_offsets = [-0.25, 0, 0.25]
    for i, (label, data, color) in enumerate(groups):
        xpos = np.arange(len(data)) + x_offsets[i]*0.5 + i*0.3 - 0.3
        ax.scatter(xpos, data, s=90, color=color, alpha=0.85,
                   zorder=4, edgecolors="#0D1117", label=label)
        mean_val = np.mean(data)
        ax.hlines(mean_val, xpos[0]-0.1, xpos[-1]+0.1,
                  color=color, lw=1.5, linestyle="--", alpha=0.5)

    ax.axhline(opt, color=QUANTUM_GREEN, lw=2.0, linestyle="-",
               label=f"Optimal = {opt}", zorder=5)
    ax.fill_between([-0.5, len(runs_18)+1.0], opt*0.98, opt*1.02,
                    color=QUANTUM_GREEN, alpha=0.06)

    ax.set_ylabel("Calculated Total Distance", fontsize=11)
    ax.set_xlabel("Run index", fontsize=11)
    ax.set_title("Variability across circuit depths — closer to optimal is better",
                 fontsize=11, color="#8B949E", pad=6)
    ax.legend(fontsize=10, framealpha=0.3)
    ax.grid(True, zorder=0)
    ax.set_xticks([])

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig8_instance4_runs.png")
    plt.savefig(path)
    plt.close()
    print(f"  ✓ Saved {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 9 – 3D Route Demo (N-dimensional generalization)
# ══════════════════════════════════════════════════════════════════════════════
def fig_3d_demo():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    # --- Synthetic 3D CVRP data ---
    np.random.seed(42)
    depot = np.array([0.0, 0.0, 0.0])
    n_clients = 10
    clients = np.random.uniform(-7, 7, size=(n_clients, 3))

    # Pre-defined routes (node IDs 1-based, 0 = depot)
    routes = [
        [0, 1, 4, 7, 0],
        [0, 2, 5, 8, 0],
        [0, 3, 6, 9, 10, 0],
    ]
    route_colors = [QUANTUM_CYAN, QUANTUM_GREEN, QUANTUM_ORANGE]
    route_labels = ["Vehicle 1", "Vehicle 2", "Vehicle 3"]

    all_pts = np.vstack([depot, clients])  # index 0 = depot

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection="3d")

    # Dark background for 3D panes
    ax.set_facecolor(BG_COLOR)
    fig.patch.set_facecolor(BG_COLOR)
    ax.xaxis.pane.set_facecolor(BG_COLOR)
    ax.yaxis.pane.set_facecolor(BG_COLOR)
    ax.zaxis.pane.set_facecolor(BG_COLOR)
    ax.xaxis.pane.set_edgecolor("#30363D")
    ax.yaxis.pane.set_edgecolor("#30363D")
    ax.zaxis.pane.set_edgecolor("#30363D")
    ax.grid(True, color="#30363D", alpha=0.4)

    # Tick colors
    ax.tick_params(axis="x", colors="#8B949E")
    ax.tick_params(axis="y", colors="#8B949E")
    ax.tick_params(axis="z", colors="#8B949E")
    ax.xaxis.label.set_color("#8B949E")
    ax.yaxis.label.set_color("#8B949E")
    ax.zaxis.label.set_color("#8B949E")

    # Draw routes
    for route, color, label in zip(routes, route_colors, route_labels):
        pts = np.array([all_pts[i] for i in route])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                color=color, linewidth=2.5, alpha=0.85, label=label, zorder=3)
        # Arrows via quiver on each segment
        for k in range(len(pts) - 1):
            d = pts[k + 1] - pts[k]
            mid = pts[k] + d * 0.55
            ax.quiver(mid[0], mid[1], mid[2],
                      d[0] * 0.001, d[1] * 0.001, d[2] * 0.001,
                      color=color, alpha=0.7, arrow_length_ratio=80, linewidth=0)

    # Client nodes
    ax.scatter(clients[:, 0], clients[:, 1], clients[:, 2],
               s=120, c="#C9D1D9", edgecolors="white", linewidths=0.8,
               zorder=5, depthshade=True)

    # Node labels
    for i in range(n_clients):
        ax.text(clients[i, 0] + 0.4, clients[i, 1] + 0.4, clients[i, 2] + 0.4,
                str(i + 1), fontsize=9, color=QUANTUM_ORANGE, fontweight="bold")

    # Depot
    ax.scatter(*depot, s=300, c="#FFA657", marker="*", edgecolors="white",
               linewidths=1.2, zorder=6, depthshade=False)
    ax.text(depot[0] + 0.5, depot[1] + 0.5, depot[2] + 0.5,
            "Depot", fontsize=11, color="#FFA657", fontweight="bold")

    # Calculate total distance
    total_dist = 0.0
    for route in routes:
        for k in range(len(route) - 1):
            total_dist += np.linalg.norm(all_pts[route[k + 1]] - all_pts[route[k]])

    ax.set_xlabel("X-axis", fontsize=14, labelpad=15)
    ax.set_ylabel("Y-axis", fontsize=14, labelpad=15)
    ax.set_zlabel("Z-axis", fontsize=14, labelpad=15)

    # Set box aspect to better fit 16:9 horizontal space
    ax.set_box_aspect((2.0, 1.2, 0.8))

    fig.suptitle("3D CVRP — N-Dimensional Coordinate Support",
                 fontsize=24, fontweight="bold", color=QUANTUM_CYAN, y=0.96)
    ax.set_title(f"Synthetic 3D Instance — Total Distance: {total_dist:.2f}",
                 fontsize=16, color=QUANTUM_CYAN, pad=30)

    ax.legend(fontsize=13, framealpha=0.3, loc="upper left", bbox_to_anchor=(0.05, 0.9))
    ax.view_init(elev=22, azim=135)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    path = os.path.join(OUTPUT_DIR, "fig9_3d_demo.png")
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"  ✓ Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n🔬  Generating Quantum CVRP Presentation Figures …\n")
    fig_distance_comparison()
    fig_circuit_complexity()
    fig_route_maps()
    fig_3d_demo()
    print(f"\n✅  All figures saved to: {OUTPUT_DIR}\n")


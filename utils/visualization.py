import matplotlib.pyplot as plt
import numpy as np


def plot_nodes(data_instance: dict):
    """
    Plots the coordinates of nodes (depot and customers) in a central graph.

    Args:
        data_instance: Instance with 'nodes' and 'id'.
    """
    nodes = [(0, 0)] + data_instance["nodes"]
    x = np.array([p[0] for p in nodes])
    y = np.array([p[1] for p in nodes])

    limit = max(np.max(np.abs(x)), np.max(np.abs(y))) + 2
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.scatter(x[0], y[0], c="red", s=200, marker="X", label="Depot (0,0)", zorder=5)
    plt.scatter(x[1:], y[1:], c="blue", s=100, label="Customers", alpha=0.8)

    for i, (px, py) in enumerate(nodes):
        plt.text(px + 0.3, py + 0.3, str(i), fontsize=10, fontweight="bold")

    plt.title(f"Instance {data_instance['id']} - Centered on Depot")
    plt.legend()
    plt.axis("equal")
    plt.show()


def plot_solution(data_instance: dict, all_routes: list):
    """
    Visualizes the CVRP solution, drawing vehicle routes between nodes.

    Args:
        data_instance: Original instance with 'nodes'.
        all_routes: List of routes, each a list of node indices starting/ending at 0.
    """
    nodes = [(0, 0)] + data_instance["nodes"]
    x_coords = np.array([p[0] for p in nodes])
    y_coords = np.array([p[1] for p in nodes])

    limit = max(np.max(np.abs(x_coords)), np.max(np.abs(y_coords))) + 2
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, linestyle=":", alpha=0.5)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, route in enumerate(all_routes):
        route_x = [nodes[node_idx][0] for node_idx in route]
        route_y = [nodes[node_idx][1] for node_idx in route]

        color = colors[i % len(colors)]
        plt.plot(
            route_x,
            route_y,
            marker="o",
            linestyle="-",
            linewidth=2,
            color=color,
            label=f"Vehicle {i+1}",
            zorder=2,
        )

        for j in range(len(route_x) - 1):
            plt.annotate(
                "",
                xy=(route_x[j + 1], route_y[j + 1]),
                xytext=(route_x[j], route_y[j]),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
            )

    plt.scatter(0, 0, c="red", s=250, marker="X", label="Depot (0,0)", zorder=5)

    for idx, (px, py) in enumerate(nodes):
        plt.text(px + 0.3, py + 0.3, str(idx), fontsize=12, fontweight="bold", zorder=10)

    plt.title(
        f"CVRP Solution - Instance {data_instance['id']}\nRoutes optimized with VQE",
        pad=20,
    )
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=3,
        fancybox=True,
        shadow=True,
    )
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

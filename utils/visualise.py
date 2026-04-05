import matplotlib.pyplot as plt
import numpy as np


def plot_instance(instance):
    nodes = [(0, 0)] + instance["nodes"]
    x = np.array([p[0] for p in nodes])
    y = np.array([p[1] for p in nodes])

    # Calcul des limites symétriques pour voir le négatif
    limit = max(np.max(np.abs(x)), np.max(np.abs(y))) + 2

    fig, ax = plt.subplots(figsize=(8, 8))

    # Configurer les axes au centre (0,0)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, linestyle=":", alpha=0.5)

    # Dessiner les points
    plt.scatter(x[0], y[0], c="red", s=200, marker="X", label="Dépôt (0,0)", zorder=5)
    plt.scatter(x[1:], y[1:], c="blue", s=100, label="Clients", alpha=0.8)

    # Étiquettes des nœuds
    for i, (px, py) in enumerate(nodes):
        plt.text(px + 0.3, py + 0.3, str(i), fontsize=10, fontweight="bold")

    plt.title(f"Instance {instance['id']} - Centrée sur le dépôt")
    plt.legend()
    plt.axis("equal")
    plt.show()


def visualize_solution(instance: dict, all_routes: list):
    """
    Affiche les clients et trace les routes des véhicules.

    Args:
        instance (dict): L'instance contenant les 'nodes'.
        all_routes (list): Liste de listes d'indices (ex: [[0, 1, 2, 0], [0, 3, 0]])
    """
    # 1. Préparation des points (Dépôt + Clients)
    nodes = [(0, 0)] + instance["nodes"]
    x_coords = np.array([p[0] for p in nodes])
    y_coords = np.array([p[1] for p in nodes])

    # 2. Configuration du graphique centré
    limit = max(np.max(np.abs(x_coords)), np.max(np.abs(y_coords))) + 2
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.grid(True, linestyle=":", alpha=0.5)

    # 3. Tracer les routes (Lignes reliant les points)
    # Palette de couleurs pour différencier les véhicules
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, route in enumerate(all_routes):
        # Récupérer les coordonnées pour chaque étape de la route
        route_x = [nodes[node_idx][0] for node_idx in route]
        route_y = [nodes[node_idx][1] for node_idx in route]

        color = colors[i % len(colors)]
        # Tracer la ligne avec une flèche pour indiquer le sens du trajet
        plt.plot(
            route_x,
            route_y,
            marker="o",
            linestyle="-",
            linewidth=2,
            color=color,
            label=f"Véhicule {i+1}",
            zorder=2,
        )

        # Optionnel : Ajouter des petites flèches pour le sens
        for j in range(len(route_x) - 1):
            plt.annotate(
                "",
                xy=(route_x[j + 1], route_y[j + 1]),
                xytext=(route_x[j], route_y[j]),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
            )

    # 4. Afficher le dépôt et les clients par-dessus
    plt.scatter(0, 0, c="red", s=250, marker="X", label="Dépôt (0,0)", zorder=5)

    # Étiquettes des nœuds
    for idx, (px, py) in enumerate(nodes):
        plt.text(
            px + 0.3, py + 0.3, str(idx), fontsize=12, fontweight="bold", zorder=10
        )

    plt.title(
        f"Solution CVRP - Instance {instance['id']}\nRoutes optimisées par VQE", pad=20
    )

    # MODIFICATION ICI : On place la légende en bas pour ne rien couper
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=3,
        fancybox=True,
        shadow=True,
    )

    plt.axis("equal")

    # TRÈS IMPORTANT : Ajuste le layout pour que la légende soit visible
    plt.tight_layout()
    plt.show()

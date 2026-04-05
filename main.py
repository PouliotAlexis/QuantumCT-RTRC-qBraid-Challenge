import sys
from time import time

from utils.clustering import cluster_nodes_by_sweep
from utils.data_loader import CVRPDataLoader
from utils.distance import compute_distance_matrix_with_mapping, map_indices_to_node_ids
from utils.metrics import calculate_total_distance, log_metrics_to_csv
from utils.solution_storage import save_solution_to_txt
from utils.tsp_solver import solve_tsp_with_vqe
from utils.visualization import plot_solution


def main(instance_id: int) -> None:
    """
    Runs a Capacitated Vehicle Routing Problem (CVRP) quantum solver instance.
    Executes the quantum circuit and saves results in the official hackathon format.

    Args:
        instance_id (int): The problem instance number (1-4).

    Returns:
        None. Saves solution and metrics to files.
    """
    loader = CVRPDataLoader()
    data_instance: dict = loader.load_instance(instance_id)

    # Initial plot of the instance (optional)
    # from utils.visualization import plot_nodes
    # plot_nodes(data_instance)

    nb_total_gate = 0
    max_nb_qubits = 0
    all_routes: list[list[int]] = []

    start_time = time()

    # 1. Clustering based on angular sweep
    clusters: list[dict] = cluster_nodes_by_sweep(data_instance)

    # 2. Solve TSP for each cluster using VQE
    for cluster in clusters:
        distance_matrix, node_ids = compute_distance_matrix_with_mapping(cluster)
        route_indices: list[int] = solve_tsp_with_vqe(distance_matrix)
        route: list[int] = map_indices_to_node_ids(route_indices, node_ids)
        all_routes.append(route)

    # 3. Format routes for official hackathon compliance
    # Map index to node ID (+1) and ensure it starts/ends at depot (0)
    all_routes = [[node_id + 1 for node_id in route] for route in all_routes]
    all_routes = [r[r.index(0) :] + r[: r.index(0)] + [0] for r in all_routes]

    # Calculate total Euclidean distance for all routes
    total_distance = calculate_total_distance(all_routes, data_instance["nodes"])

    # Fill missing vehicle routes with [0, 0] if capacity allows more vehicles than used
    num_vehicles = data_instance.get("m_vehicles", len(all_routes))
    while len(all_routes) < num_vehicles:
        all_routes.append([0, 0])

    # 4. Save results in the official format
    save_solution_to_txt(
        instance_id,
        all_routes,
        data_dir="data",
    )

    # 5. Log metrics and performance data
    log_metrics_to_csv(
        instance_id,
        max_nb_qubits,
        nb_total_gate,
        time() - start_time,
        "data/run_results.csv",
        total_distance,
        all_routes,
        data_instance,
    )

    # 6. Visualize the final routes
    plot_solution(data_instance, all_routes)
    print(f"Final Routes: {all_routes}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <instance_id>")
        sys.exit(1)
    main(int(sys.argv[1]))

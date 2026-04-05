from time import time

from utils.CVRPDataLoader import CVRPDataLoader
from utils.get_cluster import get_cluster_with_optimised_sweep
from utils.get_distance_matrix import get_distance_matrix_with_ids, remap_route_indices
from utils.save_crp_solutions import save_cvrp_solution
from utils.save_instance_results import get_total_distance, save_instance_results
from utils.visualise import plot_instance, visualize_solution
from utils.vqe import solve_tsp


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
    data_instance: dict = loader.get_instance(instance_id)

    # plot_instance(data_instance)

    nb_total_gate = 0
    max_nb_qubits = 0
    all_routes: list[list[int]] = []

    start_time = time()

    clusters: list[dict] = get_cluster_with_optimised_sweep(data_instance)

    for cluster in clusters:
        distance_matrix, node_ids = get_distance_matrix_with_ids(cluster)
        route_indices: list[int] = solve_tsp(distance_matrix)
        route: list[int] = remap_route_indices(route_indices, node_ids)
        all_routes.append(route)

    # Modify routes in correct format
    all_routes = [[node_id + 1 for node_id in route] for route in all_routes]
    all_routes = [r[r.index(0) :] + r[: r.index(0)] + [0] for r in all_routes]

    # Calculate total Euclidean distance
    total_distance = get_total_distance(all_routes, data_instance["nodes"])

    # Save results in the official format
    save_cvrp_solution(
        instance_id,
        all_routes,
        data_dir="data",
    )

    # Save overall data with total distance
    save_instance_results(
        instance_id,
        max_nb_qubits,
        nb_total_gate,
        time() - start_time,
        "data/data.csv",
        total_distance,
    )

    # Commented out to avoid tkinter threading issues
    visualize_solution(data_instance, all_routes)
    print(all_routes)


if __name__ == "__main__":
    INSTANCE_ID = 3  # Between 1 and 4
    main(INSTANCE_ID)

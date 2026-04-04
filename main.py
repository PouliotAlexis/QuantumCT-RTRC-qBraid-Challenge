from time import time

from utils.CVRPDataLoader import CVRPDataLoader
from utils.get_cluster import get_cluster_with_optimised_sweep
from utils.get_distance_matrix import get_distance_matrix
from utils.qaoa import qaoa_adaptation
from utils.save_crp_solutions import clean_route, save_cvrp_solution
from utils.save_instance_results import save_instance_results


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

    nb_total_gate = 0
    max_nb_qubits = 0
    all_routes = []

    start_time = time()

    clusters: list[dict] = get_cluster_with_optimised_sweep(data_instance)
    print(clusters)

    for cluster in clusters:
        distance_matrix = get_distance_matrix(cluster)
        route, _ = qaoa_adaptation(distance_matrix, p=1)
        print(route)
        all_routes.append(route)

    # Save results in the official format
    save_cvrp_solution(
        instance_id,
        all_routes,
        data_dir="data",
    )

    # Save overall data
    save_instance_results(
        instance_id, max_nb_qubits, nb_total_gate, time() - start_time, "data/data.csv"
    )

    print(all_routes)


if __name__ == "__main__":
    INSTANCE_ID = 3  # Between 1 and 4
    main(INSTANCE_ID)

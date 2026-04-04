from time import time

from utils.CVRPDataLoader import CVRPDataLoader
from utils.save_crp_solutions import save_cvrp_solution
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
    data_instance = loader.get_instance(instance_id)

    nb_total_gate = 0
    max_nb_qubits = 0

    start_time = time()

    # TODO: Implement logic to load instance, run quantum circuit, and compute results (nb_total_gate and max_nb_qubits)

    # Save results in the official format
    save_cvrp_solution(
        instance_id,
        routes=[
            [0, 2, 3, 0],
            [0, 1, 4, 0],
        ],
        data_dir="data",
    )

    # Save overall data
    save_instance_results(
        instance_id, max_nb_qubits, nb_total_gate, time() - start_time, "data/data.csv"
    )


if __name__ == "__main__":
    INSTANCE_ID = 1  # Between 1 and 4
    main(INSTANCE_ID)

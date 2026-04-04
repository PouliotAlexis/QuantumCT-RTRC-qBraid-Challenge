from time import time

from utils.CVRPDataLoader import CVRPDataLoader
from utils.save_crp_solutions import save_cvrp_solution
from utils.save_instance_results import save_instance_results


def main(instance_id: int) -> None:
    """
    Runs a Capacitated Vehicle Routing Problem (CVRP) instance.
    Executes the quantum circuit and saves results in the official hackathon format.

    Args:
        None

    Returns:
        None
    """
    loader = CVRPDataLoader()
    data_instance = loader.get_instance(instance_id)

    nb_total_gate = 0
    max_nb_qubits = 0

    start_time = time()

    # TODO : Implement the logic to load the instance, run the quantum circuit and compute the results, nb_total_gate and max_nb_qubits

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

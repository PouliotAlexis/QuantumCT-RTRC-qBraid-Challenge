import csv
import os
from typing import Union


def save_instance_results(
    instance_id: Union[int, str],
    nb_qubits: int,
    nb_gates: int,
    exec_time: float,
    file_path: str,
) -> None:
    """
    Saves quantum execution metrics for a CVRP instance to a CSV file.
    Automatically creates the CSV header if the file does not exist.

    Args:
        instance_id (int or str): The problem instance number.
        nb_qubits (int): The number of qubits used in the quantum circuit.
        nb_gates (int): The total number of gate operations executed.
        exec_time (float): The execution time in seconds.
        file_path (str): The path to the CSV file where data will be appended.

    Returns:
        None. Prints a success message and writes to CSV file.
    """
    header = [
        "CVRP Instance #",
        "# of Qubits",
        "# of Gate Operations",
        "Execution Time",
    ]
    row = [instance_id, nb_qubits, nb_gates, f"{exec_time:.4f}"]

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(header)

        writer.writerow(row)

    print(f"✅ Données de l'instance {instance_id} ajoutées à {file_path}")

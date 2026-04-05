import csv
import os
from typing import Union

import numpy as np


def get_total_distance(all_routes: list[list[int]], nodes: list) -> float:
    """
    Calculates the total Euclidean distance of all routes.

    Args:
        all_routes (list[list[int]]): List of routes, each route is a list of node IDs (1-based, where 0 is depot).
        nodes (list): List of node coordinates [(x, y), ...] where index 0 is the first customer node.

    Returns:
        float: Total Euclidean distance across all routes.
    """
    total_distance = 0.0
    depot = (0, 0)  # Depot is always at origin

    for route in all_routes:
        for i in range(len(route) - 1):
            node1_id = route[i]
            node2_id = route[i + 1]

            # Get coordinates for each node
            # node_id 0 = depot, node_id 1+ = customers in nodes list
            coord1 = depot if node1_id == 0 else nodes[node1_id - 1]
            coord2 = depot if node2_id == 0 else nodes[node2_id - 1]

            x1, y1 = coord1
            x2, y2 = coord2
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance += distance

    return total_distance


def save_instance_results(
    instance_id: Union[int, str],
    nb_qubits: int,
    nb_gates: int,
    exec_time: float,
    file_path: str,
    total_distance: float = 0.0,
) -> None:
    """
    Saves quantum execution metrics for a CVRP instance to a CSV file.
    Automatically creates the CSV header if the file does not exist.

    Args:
        instance_id (Union[int, str]): The problem instance number (1-4).
        nb_qubits (int): The number of qubits used in the quantum circuit.
        nb_gates (int): The total number of gate operations executed.
        exec_time (float): The execution time in seconds.
        file_path (str): The path to the CSV file where data will be appended.
        total_distance (float): The total Euclidean distance of all routes.

    Returns:
        None. Prints success message and writes to CSV file.
    """
    header = [
        "CVRP Instance #",
        "# of Qubits",
        "# of Gate Operations",
        "Execution Time",
        "Total Euclidean Distance",
    ]
    row = [
        instance_id,
        nb_qubits,
        nb_gates,
        f"{exec_time:.4f}",
        f"{total_distance:.4f}",
    ]

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(header)

        writer.writerow(row)

    print(f"✅ Instance {instance_id} metrics saved to {file_path}")

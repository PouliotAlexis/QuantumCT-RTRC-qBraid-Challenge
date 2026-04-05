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


def format_routes(all_routes: list[list[int]]) -> str:
    """
    Formats routes like: r1: 0, 1, 2, 0 | r2: 0, 3, 0

    Args:
        all_routes (list[list[int]]): List of routes.

    Returns:
        str: Formatted routes string.
    """
    route_strs = []
    for i, route in enumerate(all_routes, 1):
        route_str = ", ".join(str(node) for node in route)
        route_strs.append(f"r{i}: {route_str}")
    return " | ".join(route_strs)


def load_optimal_data(optimal_file: str = "data/optimal_results.csv") -> dict:
    """
    Loads optimal results from the optimal_results.csv file.

    Args:
        optimal_file (str): Path to optimal_results.csv.

    Returns:
        dict: Dictionary mapping instance_id to (optimal_distance, optimal_routes).
    """
    optimal_data = {}
    if os.path.isfile(optimal_file):
        with open(optimal_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instance_id = int(row["Instance"])
                optimal_distance = float(row["Distance"])
                optimal_routes = row["Routes"]
                optimal_data[instance_id] = (optimal_distance, optimal_routes)
    return optimal_data


def save_run_results(
    instance_id: Union[int, str],
    nb_qubits: int,
    nb_gates: int,
    exec_time: float,
    file_path: str,
    total_distance: float = 0.0,
    all_routes: list[list[int]] = None,
    data_instance: dict = None,
) -> None:
    """
    Saves quantum execution metrics for a CVRP instance to a CSV file.
    Automatically creates the CSV header if the file does not exist.
    Fills missing vehicle routes with empty routes [0, 0].

    Args:
        instance_id (Union[int, str]): The problem instance number (1-4).
        nb_qubits (int): The number of qubits used in the quantum circuit.
        nb_gates (int): The total number of gate operations executed.
        exec_time (float): The execution time in seconds.
        file_path (str): The path to the CSV file where data will be appended.
        total_distance (float): The total Euclidean distance of all routes.
        all_routes (list[list[int]]): The calculated routes.
        data_instance (dict): The instance data containing m_vehicles.

    Returns:
        None. Prints success message and writes to CSV file.
    """
    instance_id = int(instance_id)
    optimal_data = load_optimal_data()

    # Fill missing vehicle routes with [0, 0]
    if data_instance and all_routes:
        num_vehicles = data_instance.get("m_vehicles", len(all_routes))
        while len(all_routes) < num_vehicles:
            all_routes.append([0, 0])

    header = [
        "Instance",
        "# of Qubits",
        "# of Gate Operations",
        "Execution Time",
        "Calculated Distance",
        "Optimal Distance",
        "Calculated Routes",
        "Optimal Routes",
    ]

    # Get optimal values if available
    if instance_id in optimal_data:
        opt_distance, opt_routes = optimal_data[instance_id]
    else:
        opt_distance = "N/A"
        opt_routes = "N/A"

    # Format calculated routes
    routes_str = format_routes(all_routes) if all_routes else "N/A"

    row = [
        instance_id,
        nb_qubits,
        nb_gates,
        f"{exec_time:.4f}",
        f"{total_distance:.4f}",
        f"{opt_distance}" if opt_distance != "N/A" else "N/A",
        routes_str,
        opt_routes,
    ]

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(header)

        writer.writerow(row)

    print(f"✅ Instance {instance_id} metrics saved to {file_path}")

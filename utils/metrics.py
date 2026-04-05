import csv
import os
from typing import Union

import numpy as np


def calculate_total_distance(all_routes: list[list[int]], nodes: list) -> float:
    """
    Calculates the total Euclidean distance of all vehicle routes.

    Args:
        all_routes (list[list[int]]): Node IDs for each route (0 is depot).
        nodes (list): Coordinates for each node [(x, y), ...].

    Returns:
        float: Total Euclidean distance.
    """
    total_distance = 0.0
    depot = (0, 0)

    for route in all_routes:
        for i in range(len(route) - 1):
            n1_id, n2_id = route[i], route[i + 1]

            coord1 = depot if n1_id == 0 else nodes[n1_id - 1]
            coord2 = depot if n2_id == 0 else nodes[n2_id - 1]

            x1, y1 = coord1
            x2, y2 = coord2
            total_distance += np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return total_distance


def _format_routes_as_string(all_routes: list[list[int]]) -> str:
    """
    Internal helper to format routes for CSV storage.
    """
    route_strs = []
    for i, route in enumerate(all_routes, 1):
        route_str = ", ".join(str(node) for node in route)
        route_strs.append(f"r{i}: {route_str}")
    return " | ".join(route_strs)


def _load_optimal_data(optimal_file: str = "data/optimal_results.csv") -> dict:
    """
    Helper to load optimal results for comparison from CSV.
    """
    optimal_data = {}
    if os.path.isfile(optimal_file):
        with open(optimal_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instance_id = int(row["Instance"])
                optimal_data[instance_id] = (float(row["Distance"]), row["Routes"])
    return optimal_data


def log_metrics_to_csv(
    instance_id: Union[int, str],
    nb_qubits: int,
    nb_gates: int,
    circuit_depth: int,
    exec_time: float,
    file_path: str,
    total_distance: float = 0.0,
    all_routes: list[list[int]] = None,
    data_instance: dict = None,
) -> None:
    """
    Saves quantum metrics and calculated distance to a CSV file for a CVRP instance.

    Args:
        instance_id: ID of the problem (1-4).
        nb_qubits: Number of qubits in the circuit.
        nb_gates: Number of gates executed.
        circuit_depth: Depth of the circuit.
        exec_time: Runtime in seconds.
        file_path: Target CSV path.
        total_distance: Total distance calculated from routes.
        all_routes: Computed vehicle routes.
        data_instance: Original data containing vehicle count if needed.
    """
    instance_id = int(instance_id)
    optimal_data = _load_optimal_data()

    # Fill empty/missing routes up to total vehicle count
    if data_instance and all_routes:
        num_vehicles = data_instance.get("m_vehicles", len(all_routes))
        while len(all_routes) < num_vehicles:
            all_routes.append([0, 0])

    header = [
        "Instance",
        "# of Qubits",
        "# of Gate Operations",
        "Circuit Depth",
        "Execution Time",
        "Calculated Distance",
        "Optimal Distance",
        "Calculated Routes",
        "Optimal Routes",
    ]

    opt_distance, opt_routes = optimal_data.get(instance_id, ("N/A", "N/A"))
    routes_str = _format_routes_as_string(all_routes) if all_routes else "N/A"

    row = [
        instance_id,
        nb_qubits,
        nb_gates,
        circuit_depth,
        f"{exec_time:.4f}",
        f"{total_distance:.4f}",
        f"{opt_distance}",
        routes_str,
        opt_routes,
    ]

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

    print(f"✅ Metrics for Instance {instance_id} logged to '{file_path}'.")

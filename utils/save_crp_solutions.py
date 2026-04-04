from typing import List, Union


def save_cvrp_solution(
    instance_id: Union[int, str], routes: List[List[int]], data_dir: str
) -> None:
    """
    Generates and saves a CVRP solution file in the official hackathon format.
    Each route is written as a line in the format: r1: 0, 2, 3, 0

    Args:
        instance_id (int or str): The problem instance number (e.g., 1, 2, 3, or 4).
        routes (list of lists): A list of vehicle routes. Each route is a list of node IDs.
                                Example: [[0, 2, 3, 0], [0, 1, 4, 0]]
        data_dir (str): The directory path where the solution file will be saved.

    Returns:
        None. Prints a success message and writes to file.
    """
    filename = f"{data_dir}/Instance{instance_id}.txt"

    with open(filename, "w") as f:
        for i, route in enumerate(routes, start=1):
            # Transforme la liste [0, 2, 3, 0] en chaîne "0, 2, 3, 0"
            route_str = ", ".join(map(str, route))
            # Écrit la ligne au format r1: 0, ...
            f.write(f"r{i}: {route_str}\n")

    print(f"✅ Fichier de solution '{filename}' généré avec succès.")

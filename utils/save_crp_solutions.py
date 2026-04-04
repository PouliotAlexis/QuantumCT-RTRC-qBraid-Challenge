from typing import List, Union


def save_cvrp_solution(
    instance_id: Union[int, str], routes: List[List[int]], data_dir: str
) -> None:
    """
    Generates and saves a CVRP solution file in the official hackathon format.
    Each route is written as a line in the format: r1: 0, 2, 3, 0

    Args:
        instance_id (Union[int, str]): The problem instance number (1-4).
        routes (List[List[int]]): A list of vehicle routes. Each route is a list of node IDs.
                                  Example: [[0, 2, 3, 0], [0, 1, 4, 0]]
        data_dir (str): The directory path where the solution file will be saved.

    Returns:
        None. Prints success message and writes to file.
    """
    filename = f"{data_dir}/Instance{instance_id}.txt"

    with open(filename, "w") as f:
        for i, route in enumerate(routes, start=1):
            # Clean route to remove empty lists and flatten nested structures
            cleaned_route = clean_route(route)
            # Convert list [0, 2, 3, 0] to string "0, 2, 3, 0"
            route_str = ", ".join(map(str, cleaned_route))
            # Write line in format r1: 0, ...
            f.write(f"r{i}: {route_str}\n")

    print(f"✅ Solution file '{filename}' generated successfully.")

from typing import List, Union


def save_solution_to_txt(
    instance_id: Union[int, str], routes: List[List[int]], data_dir: str
) -> None:
    """
    Saves the final CVRP solution for a given instance into a text file 
    using the official hackathon format.

    Args:
        instance_id (Union[int, str]): Problem instance (1-4).
        routes (List[List[int]]): Calculated routes starting and ending with 0 (depot).
        data_dir (str): Destination directory for the solution file.
    """
    filename = f"{data_dir}/Instance{instance_id}.txt"

    with open(filename, "w") as f:
        for i, route in enumerate(routes, start=1):
            route_str = ", ".join(map(str, route))
            f.write(f"r{i}: {route_str}\n")

    print(f"✅ Solution saved to '{filename}'.")

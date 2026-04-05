import numpy as np


def get_distance_matrix(nodes: dict[int, tuple[float, float]]) -> np.ndarray:
    """
    Computes the Euclidean distance matrix for a set of nodes.

    Args:
        nodes (dict): A dictionary {id: (x, y)} representing the nodes.

    Returns:
        ndarray: A NumPy distance matrix of shape (n, n) where element [i, j] is the Euclidean distance
                 between node i and node j.
    """
    # Convert coordinates to NumPy array (n, 2)
    coords = np.array(list(nodes.values()))

    # Calculate the difference between each pair of points (n, n, 2)
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]

    # Calculate the Euclidean norm on the last axis
    dist_matrix = np.linalg.norm(diff, axis=2)

    return dist_matrix


def get_distance_matrix_with_ids(
    nodes: dict[int, tuple[float, float]],
) -> tuple[np.ndarray, list[int]]:
    """
    Computes the Euclidean distance matrix and returns the mapping of indices to node IDs.

    Args:
        nodes (dict): A dictionary {id: (x, y)} representing the nodes.

    Returns:
        tuple: (distance_matrix, node_ids_list) where:
               - distance_matrix: NumPy distance matrix of shape (n, n)
               - node_ids_list: List of node IDs in the same order as the matrix rows/columns
    """
    node_ids = list(nodes.keys())
    dist_matrix = get_distance_matrix(nodes)
    return dist_matrix, node_ids


def remap_route_indices(route: list[int], node_ids: list[int]) -> list[int]:
    """
    Remaps route indices from matrix indices to actual node IDs.

    Args:
        route (list[int]): Route with indices relative to the distance matrix (0 to n-1)
        node_ids (list[int]): List of node IDs in the same order as matrix rows/columns

    Returns:
        list[int]: Route with actual node IDs
    """
    return [node_ids[idx] for idx in route]

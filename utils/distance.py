import numpy as np


def compute_distance_matrix(nodes: dict[int, tuple[float, ...]]) -> np.ndarray:
    """
    Computes the Euclidean distance matrix for a set of nodes in N-dimensional space.

    Args:
        nodes (dict): A dictionary {id: (coord1, coord2, ...)} representing the nodes.

    Returns:
        ndarray: A NumPy distance matrix of shape (n, n) where element [i, j] 
                 is the Euclidean distance between node i and node j.
    """
    # Convert coordinates to NumPy array (n, D)
    coords = np.array(list(nodes.values()))

    # Calculate the difference between each pair of points (n, n, D)
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]

    # Calculate the Euclidean norm on the last axis (dimension axis)
    dist_matrix = np.linalg.norm(diff, axis=-1)

    return dist_matrix


def compute_distance_matrix_with_mapping(
    nodes: dict[int, tuple[float, ...]],
) -> tuple[np.ndarray, list[int]]:
    """
    Computes Euclidean distance matrix and returns index-to-node ID mapping.

    Args:
        nodes (dict): A dictionary {id: (coord1, coord2, ...)} representing the nodes.

    Returns:
        tuple: (distance_matrix, node_ids_list) where:
               - distance_matrix: NumPy distance matrix of shape (n, n)
               - node_ids_list: List of node IDs in matrix row/column order
    """
    node_ids = list(nodes.keys())
    dist_matrix = compute_distance_matrix(nodes)
    return dist_matrix, node_ids


def map_indices_to_node_ids(route_indices: list[int], node_ids: list[int]) -> list[int]:
    """
    Maps matrix indices in a route back to their original node IDs.

    Args:
        route_indices (list[int]): Route with matrix-relative indices (0 to n-1)
        node_ids (list[int]): Ordered list of node IDs corresponding to matrix indices

    Returns:
        list[int]: Route updated with actual node IDs
    """
    try:
        return [node_ids[int(idx)] for idx in route_indices]
    except (TypeError, ValueError) as e:
        # Handle potentially nested structure or non-integer indices
        flat_route = []
        for item in route_indices:
            if isinstance(item, (list, tuple)):
                flat_route.extend(item)
            else:
                flat_route.append(item)
        return [node_ids[int(idx)] for idx in flat_route]

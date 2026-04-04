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

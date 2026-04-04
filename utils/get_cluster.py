import math

DEPOT_NODE = (0, 0)


def get_cluster_with_optimised_sweep(data_instance: dict) -> list[dict]:
    """
    Solves the Capacitated Vehicle Routing Problem (CVRP) using an optimized sweep algorithm.

    This algorithm assigns customers to vehicles by calculating the polar angle of each node
    relative to the depot, then rotates through different starting angles to find the partition
    that minimizes the angular spread across all routes (vehicles).

    Args:
        data_instance (dict): A dictionary containing problem data with keys:
                             - "nodes" (list): A list of node coordinates.
                             - "capacity" (int): Maximum number of customers per vehicle.

    Returns:
        list[dict]: A list of clusters, where each cluster is a dictionary {id: (x, y)}.
                    Each cluster represents a route for one vehicle.
    """
    nodes: list = data_instance["nodes"]
    capacity: int = data_instance["capacity"]

    # Calculate polar angle for each customer node relative to the depot
    nodes_angle = []
    for node_id, coords in enumerate(nodes):
        angle = math.atan2(coords[1] - DEPOT_NODE[1], coords[0] - DEPOT_NODE[0])
        nodes_angle.append({"id": node_id, "angle": angle})

    # Sort nodes by angle
    nodes_angle.sort(key=lambda x: x["angle"])
    n_nodes = len(nodes_angle)
    lowest_angle_sum = float("inf")
    best_clusters = []

    # Try all possible rotations to find the optimal partition
    for start_idx in range(n_nodes):
        rotated_nodes = [nodes_angle[(start_idx + i) % n_nodes] for i in range(n_nodes)]
        current_clusters = []
        current_angle_sum = 0

        # Create clusters respecting the vehicle capacity constraint
        for i in range(0, n_nodes, capacity):
            cluster = rotated_nodes[i : i + capacity]
            current_clusters.append(cluster)
            # Calculate angular spread (gap) for this cluster
            angle_start = cluster[0]["angle"]
            angle_end = cluster[-1]["angle"]
            spread = (angle_end - angle_start) % (2 * math.pi)
            current_angle_sum += spread

        # Keep the partition with the minimum total angular spread
        if current_angle_sum < lowest_angle_sum:
            lowest_angle_sum = current_angle_sum
            best_clusters = current_clusters

    # Return clusters as list of dictionaries {id: (x, y)}
    # Include the depot (id: 0) in every cluster
    result = []
    for cluster in best_clusters:
        cluster_dict = {-1: tuple(DEPOT_NODE)}  # Start with depot
        cluster_dict.update({node["id"]: tuple(nodes[node["id"]]) for node in cluster})
        result.append(cluster_dict)

    return result

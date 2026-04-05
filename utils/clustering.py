import math

DEPOT_NODE = (0, 0)


def cluster_nodes_by_sweep(data_instance: dict) -> list[dict]:
    """
    Solves the Capacitated Vehicle Routing Problem (CVRP) by clustering customers 
    using an optimized sweep algorithm.

    Assigns customers to vehicles by calculating the polar angle of each node 
    relative to the depot, then finds the partition that minimizes the angular spread 
    across all vehicles.

    Args:
        data_instance (dict): Problem data (nodes, capacity).

    Returns:
        list[dict]: List of clusters (node ID mapping to coordinates), 
                   where each cluster represents a vehicle route.
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

    # Prepare final clusters with the depot (id: -1 to represent depot at 0,0)
    result = []
    for cluster in best_clusters:
        cluster_dict = {-1: tuple(DEPOT_NODE)}  # Start with depot
        cluster_dict.update({node["id"]: tuple(nodes[node["id"]]) for node in cluster})
        result.append(cluster_dict)

    return result

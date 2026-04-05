import sys
import itertools
import numpy as np
from typing import List, Tuple, Dict
from utils.data_loader import CVRPDataLoader

DEPOT = (0, 0)

def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_route_distance(route: List[int], all_nodes: List[Tuple[float, float]]) -> float:
    """
    Calculates total distance for a single route [0, n1, n2, ..., 0].
    """
    total = 0.0
    current_pos = DEPOT
    for node_id in route[1:-1]: # Skip the 0 at start/end
        node_coords = all_nodes[node_id - 1]
        total += calculate_distance(current_pos, node_coords)
        current_pos = node_coords
    total += calculate_distance(current_pos, DEPOT)
    return total

def solve_bruteforce(instance_id: int):
    loader = CVRPDataLoader()
    data = loader.load_instance(instance_id)
    nodes = data["nodes"]
    capacity = data["capacity"]
    num_customers = len(nodes)
    customer_ids = list(range(1, num_customers + 1))

    print(f"--- Brute-forcing Instance {instance_id} ---")
    print(f"Customers: {num_customers}, Capacity: {capacity}")

    best_distance = float('inf')
    best_routes = []

    # Iterate through all permutations of customers
    # For small n (up to 8-9), this is fast.
    for perm in itertools.permutations(customer_ids):
        # Find optimal way to split this permutation into routes
        # We use a simple recursive/DP approach for splitting
        # dp[i] = min distance to cover first i customers in the permutation
        n = len(perm)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        parent = [-1] * (n + 1)

        for i in range(1, n + 1):
            current_load = 0
            for j in range(i, 0, -1):
                current_load += 1 # Each stop is 1 unit
                if current_load > capacity:
                    break
                
                # Distance of route starting with depot, visiting perm[j-1:i], ending at depot
                route = [0] + list(perm[j-1:i]) + [0]
                d = get_route_distance(route, nodes)
                
                if dp[j-1] + d < dp[i]:
                    dp[i] = dp[j-1] + d
                    parent[i] = j - 1

        if dp[n] < best_distance:
            best_distance = dp[n]
            # Reconstruct routes
            best_routes = []
            curr = n
            while curr > 0:
                prev = parent[curr]
                best_routes.insert(0, [0] + list(perm[prev:curr]) + [0])
                curr = prev

    print(f"Best Distance Found: {best_distance:.4f}")
    print(f"Optimal Routes: {best_routes}")
    return best_distance, best_routes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utils/bruteforce_optimizer.py <instance_id>")
        sys.exit(1)
    
    solve_bruteforce(int(sys.argv[1]))

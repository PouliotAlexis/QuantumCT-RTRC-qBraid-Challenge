import sys
import itertools
import numpy as np
from typing import List, Tuple, Dict
from utils.data_loader import CVRPDataLoader

DEPOT = (0, 0)

def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_best_tour_distance(subset: List[int], all_nodes: List[Tuple[float, float]]) -> Tuple[float, List[int]]:
    """
    Finds the best tour for a subset of nodes starting/ending at depot.
    """
    if not subset:
        return 0, [0, 0]
    
    best_d = float('inf')
    best_p = []
    
    # Check all permutations (max 3! = 6)
    for perm in itertools.permutations(subset):
        d = 0
        curr = DEPOT
        for node_id in perm:
            node_coords = all_nodes[node_id - 1]
            d += calculate_distance(curr, node_coords)
            curr = node_coords
        d += calculate_distance(curr, DEPOT)
        
        if d < best_d:
            best_d = d
            best_p = [0] + list(perm) + [0]
            
    return best_d, best_p

def solve_instance4_exact():
    loader = CVRPDataLoader()
    data = loader.load_instance(4)
    nodes = data["nodes"]
    capacity = data["capacity"] # Capacity is 3
    num_customers = len(nodes)
    customer_ids = list(range(1, num_customers + 1)) # [1, 2, ..., 12]

    # Pre-calculate all possible single-vehicle routes (max 3 customers)
    # Store them as a list of (mask, distance, path)
    sub_routes = []
    for r_size in range(1, capacity + 1):
        for combo in itertools.combinations(range(num_customers), r_size):
            subset_ids = [customer_ids[i] for i in combo]
            dist, path = get_best_tour_distance(subset_ids, nodes)
            
            mask = 0
            for i in combo:
                mask |= (1 << i)
            
            sub_routes.append((mask, dist, path))

    # DP on subsets
    # dp[mask] = min distance to cover customers in mask
    num_masks = 1 << num_customers
    dp = [float('inf')] * num_masks
    parent_mask = [-1] * num_masks
    parent_route = [None] * num_masks
    
    dp[0] = 0
    
    for mask in range(num_masks):
        if dp[mask] == float('inf'):
            continue
            
        # Try to add a new route from sub_routes
        for r_mask, r_dist, r_path in sub_routes:
            if not (mask & r_mask): # No overlap
                new_mask = mask | r_mask
                if dp[mask] + r_dist < dp[new_mask]:
                    dp[new_mask] = dp[mask] + r_dist
                    parent_mask[new_mask] = mask
                    parent_route[new_mask] = r_path

    # Extract result
    final_mask = num_masks - 1
    total_dist = dp[final_mask]
    
    routes = []
    curr = final_mask
    while curr > 0:
        routes.append(parent_route[curr])
        curr = parent_mask[curr]
        
    print(f"--- Exact Solution for Instance 4 ---")
    print(f"Optimal Distance: {total_dist:.4f}")
    print(f"Optimal Routes: {routes[::-1]}")
    return total_dist, routes[::-1]

if __name__ == "__main__":
    solve_instance4_exact()

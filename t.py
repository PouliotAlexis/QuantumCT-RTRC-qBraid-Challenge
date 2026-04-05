import numpy as np
from scipy.spatial import distance_matrix

from tsp import solve_tsp
from utils.qaoa import qaoa_adaptation

coords = np.array([(0, 0), (2, 1), (1, 2), (2, 2)])
adj_matrix = distance_matrix(coords, coords)
print(adj_matrix)

# Passez cette adj_matrix à votre fonction
# route, energy = qaoa_adaptation(adj_matrix)
route = solve_tsp(adj_matrix)
print("Route:", route)

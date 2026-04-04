import numpy as np
from scipy.spatial import distance_matrix

from utils.qaoa import qaoa_adaptation

coords = np.array([(0, 0), (3, 4), (8, 13)])  # Vos points -1, 5, 3
adj_matrix = distance_matrix(coords, coords)
print(adj_matrix)

# Passez cette adj_matrix à votre fonction
route, energy = qaoa_adaptation(adj_matrix)
print("Route:", route)

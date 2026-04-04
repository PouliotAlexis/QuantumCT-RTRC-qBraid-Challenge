import pytest
import numpy as np
from utils.get_distance_matrix import get_distance_matrix

class TestGetDistanceMatrix:
    @pytest.mark.parametrize("nodes, expected_shape, val_01", [
        ({0: (0, 0), 1: (3, 4)}, (2, 2), 5.0),
        ({0: (1, 1), 1: (1, 3), 2: (1, 5)}, (3, 3), 2.0),
        ([(0, 0), (0, 3), (4, 0)], (3, 3), 3.0),
        ([(0, 0), (1, 1), (2, 2), (3, 3)], (4, 4), np.sqrt(2)),
    ])
    def test_distance_matrix_shapes_and_values(self, nodes, expected_shape, val_01):
        matrix = get_distance_matrix(nodes)
        assert matrix.shape == expected_shape
        assert np.isclose(matrix[0, 1], val_01)
        assert np.isclose(matrix[1, 0], val_01)
        assert np.isclose(matrix[0, 0], 0.0)

    def test_single_node(self):
        matrix = get_distance_matrix([(0, 0)])
        assert matrix.shape == (1, 1)
        assert matrix[0, 0] == 0.0

    def test_large_number_of_nodes(self):
        nodes = {i: (float(i), float(i)) for i in range(100)}
        matrix = get_distance_matrix(nodes)
        assert matrix.shape == (100, 100)
        assert np.isclose(matrix[0, 99], np.sqrt(2) * 99)

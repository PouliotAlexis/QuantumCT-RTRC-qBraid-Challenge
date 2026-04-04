import pytest
from utils.get_cluster import get_cluster_with_optimised_sweep

@pytest.fixture
def circular_data():
    return {
        "capacity": 2,
        "nodes": {
            0: [0, 0],   
            1: [1, 1],   
            2: [-1, 1],  
            3: [-1, -1], 
            4: [1, -1]   
        }
    }

@pytest.fixture
def linear_data():
    return {
        "capacity": 3,
        "nodes": {
            0: [0, 0],
            1: [1, 0],
            2: [2, 0],
            3: [3, 0],
            4: [-1, 0],
            5: [-2, 0],
            6: [-3, 0],
        }
    }

class TestGetCluster:
    def test_basic_sweep_clustering(self, circular_data):
        clusters = get_cluster_with_optimised_sweep(circular_data)
        assert len(clusters) == 2
        for cluster in clusters:
            assert 0 in cluster
            assert cluster[0] == (0, 0)
            assert len(cluster) <= 3

    def test_linear_sweep_clustering(self, linear_data):
        clusters = get_cluster_with_optimised_sweep(linear_data)
        assert len(clusters) == 2
        for cluster in clusters:
            assert 0 in cluster
            assert len(cluster) <= 4

    def test_empty_customers(self):
        data = {
            "capacity": 5,
            "nodes": {0: [0, 0]}
        }
        clusters = get_cluster_with_optimised_sweep(data)
        assert len(clusters) == 0

    @pytest.mark.parametrize("capacity, expected_clusters", [
        (1, 4),
        (2, 2),
        (4, 1),
        (5, 1)
    ])
    def test_capacity_variations(self, circular_data, capacity, expected_clusters):
        circular_data["capacity"] = capacity
        clusters = get_cluster_with_optimised_sweep(circular_data)
        assert len(clusters) == expected_clusters
        for cluster in clusters:
            assert len(cluster) <= capacity + 1

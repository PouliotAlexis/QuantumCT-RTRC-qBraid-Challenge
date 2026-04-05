import pytest
from utils.CVRPDataLoader import CVRPDataLoader

class TestCVRPDataLoader:
    @pytest.fixture
    def loader(self):
        return CVRPDataLoader()

    def test_init(self, loader):
        assert loader.depot == (0, 0)

    @pytest.mark.parametrize("instance_id, expected_vehicles, expected_capacity, num_nodes", [
        (1, 2, 5, 4),
        (2, 2, 2, 4),
        (3, 3, 2, 7),
        (4, 4, 3, 13)
    ])
    def test_get_valid_instances(self, loader, instance_id, expected_vehicles, expected_capacity, num_nodes):
        instance = loader.get_instance(instance_id)
        assert instance["id"] == instance_id
        assert instance["m_vehicles"] == expected_vehicles
        assert instance["capacity"] == expected_capacity
        assert len(instance["nodes"]) == num_nodes
        assert 0 in instance["nodes"]
        assert instance["nodes"][0] == (0, 0)

    @pytest.mark.parametrize("invalid_id", [0, 5, -1, 100])
    def test_get_invalid_instance(self, loader, invalid_id):
        with pytest.raises(ValueError):
            loader.get_instance(invalid_id)

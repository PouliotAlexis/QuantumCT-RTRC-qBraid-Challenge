import pytest
import os
import shutil
from utils.save_crp_solutions import clean_route, save_cvrp_solution

class TestSaveCRPSolutions:
    @pytest.fixture
    def test_dir(self):
        dir_name = "test_cvrp_data_dir"
        os.makedirs(dir_name, exist_ok=True)
        yield dir_name
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

    @pytest.mark.parametrize("route, expected", [
        ([0, [1, 2], [], None, 3, "4", 0], [0, 1, 2, 3, 4, 0]),
        ([0, 1, 2, 3, 0], [0, 1, 2, 3, 0]),
        ([[0], [1], [2], [0]], [0, 1, 2, 0]),
        ([0, "invalid", 1, None, 2, 0], [0, 1, 2, 0]),
        ([], []),
        ([[], [], []], [])
    ])
    def test_clean_route(self, route, expected):
        assert clean_route(route) == expected

    @pytest.mark.parametrize("instance_id, routes, expected_content", [
        ("999", [[0, 1, 2, 0], [0, 3, 4, 0]], "r1: 0, 1, 2, 0\nr2: 0, 3, 4, 0\n"),
        (1, [[0, 5, 0]], "r1: 0, 5, 0\n"),
        ("abc", [[0, 0]], "r1: 0, 0\n"),
        (2, [[0, [1, 2], 0], [0, 3, None, 0]], "r1: 0, 1, 2, 0\nr2: 0, 3, 0\n")
    ])
    def test_save_cvrp_solution(self, test_dir, instance_id, routes, expected_content):
        save_cvrp_solution(instance_id, routes, data_dir=test_dir)
        filepath = os.path.join(test_dir, f"Instance{instance_id}.txt")
        assert os.path.exists(filepath)
        
        with open(filepath, "r") as f:
            content = f.read()
            
        assert content == expected_content

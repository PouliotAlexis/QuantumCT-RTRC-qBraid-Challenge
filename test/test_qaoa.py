import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from utils.qaoa import qaoa_adaptation

class TestQAOA:
    @patch('utils.qaoa.QAOA')
    @patch('utils.qaoa.Tsp')
    @patch('utils.qaoa.QuadraticProgramToQubo')
    @patch('utils.qaoa.StatevectorSampler')
    def test_qaoa_adaptation(self, mock_sampler, mock_qubo, mock_tsp, mock_qaoa_class):
        # Setup mocks
        mock_tsp_instance = mock_tsp.return_value
        mock_tsp_instance.sample_most_likely.return_value = [1, 0, 0, 1]
        mock_tsp_instance.interpret.return_value = [0, 2, 1]
        
        mock_qubo_instance = mock_qubo.return_value.convert.return_value
        mock_qubo_instance.to_ising.return_value = (MagicMock(), 0.0)
        
        mock_qaoa_instance = mock_qaoa_class.return_value
        mock_result = MagicMock()
        mock_result.eigenstate = MagicMock()
        mock_result.eigenvalue = 14.5
        mock_qaoa_instance.compute_minimum_eigenvalue.return_value = mock_result
        
        adjacency_matrix = np.array([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0]
        ])
        
        route, energy = qaoa_adaptation(adjacency_matrix, p=1)
        
        assert route == [0, 2, 1]
        assert energy == 14.5
        mock_tsp.assert_called_once()
        mock_qaoa_class.assert_called_once()

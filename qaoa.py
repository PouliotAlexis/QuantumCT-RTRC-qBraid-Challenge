from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA
from qiskit.primitives import Sampler
import numpy as np
from qiskit_algorithms.optimizers import Optimizer

def qaoa(adjacency_matrix: np.ndarray, optimizer: Optimizer, p: int):
    """
    Solves the Traveling Salesperson Problem (TSP) for a given sector using QAOA.
    
    Args:
        adjacency_matrix (np.ndarray): The distance matrix of the sub-graph.
        optimizer (Optimizer): The classical optimizer to adjust QAOA parameters (e.g., COBYLA).
        p (int): The number of QAOA layers (depth/reps).
        
    Returns:
        tuple: A tuple containing the optimal route (list of nodes) and the quantum energy (eigenvalue).
    """
    # 1. Mathematical preparation (TSP -> Quadratic Program -> QUBO -> Ising)
    tsp = Tsp(adjacency_matrix)
    qp = tsp.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)
    qubitOp, offset = qubo.to_ising()

    # 3. Algorithm execution
    qaoa_instance = QAOA(sampler=Sampler(), optimizer=optimizer, reps=p)
    result = qaoa_instance.compute_minimum_eigenvalue(qubitOp)

    # 4. Decoding the quantum result into a classical route (crucial step!)
    x = tsp.sample_most_likely(result.eigenstate)
    optimal_route = tsp.interpret(x)

    # Return the route (e.g., [0, 2, 1]) and the quantum energy
    return optimal_route, result.eigenvalue
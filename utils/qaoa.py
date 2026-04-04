import numpy as np
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA  # L'optimiseur classique
from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo


def qaoa_adaptation(adjacency_matrix: np.ndarray, p: int = 1):
    """
    Solves the Traveling Salesman Problem (TSP) for a given sector using QAOA with COBYLA optimizer.

    Args:
        adjacency_matrix (np.ndarray): The distance/cost matrix for TSP.
        p (int): The number of QAOA layers (default: 1).

    Returns:
        tuple: A tuple containing:
            - optimal_route: The best route found (list of node indices).
            - eigenvalue: The energy value associated with the route.
    """
    tsp = Tsp(adjacency_matrix)
    qp = tsp.to_quadratic_program()
    qubo = QuadraticProgramToQubo().convert(qp)
    qubitOp, _ = qubo.to_ising()
    print(qubitOp.to_matrix())
    optimizer = COBYLA(maxiter=30)

    sampler = StatevectorSampler()
    qaoa_instance = QAOA(sampler=sampler, optimizer=optimizer, reps=p)
    result = qaoa_instance.compute_minimum_eigenvalue(qubitOp)

    x = tsp.sample_most_likely(result.eigenstate)
    optimal_route = tsp.interpret(x)

    return optimal_route, result.eigenvalue

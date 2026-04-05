import numpy as np
from qiskit import transpile
from qiskit.circuit.library import RealAmplitudes
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.applications import Tsp


def solve_tsp_with_vqe(distance_matrix: np.ndarray) -> list[int]:
    """
    Solves the Traveling Salesman Problem (TSP) using a Quantum VQE algorithm.

    Args:
        distance_matrix (np.ndarray): The matrix of Euclidean distances between nodes.

    Returns:
        list[int]: The optimal order of node indices found by the quantum solver.
    """
    # Initialize TSP application and convert to Quadratic Program
    tsp_app = Tsp(distance_matrix)
    quadratic_program = tsp_app.to_quadratic_program()

    # 1. Setup Backend
    backend = AerSimulator()

    # 2. Create Ansatz
    num_qubits = quadratic_program.get_num_vars()
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=2)

    # 3. Transpilation (CRITICAL for performance)
    ansatz_transpiled = transpile(ansatz, backend=backend)

    # 4. Configure Sampler and SamplingVQE
    sampler = AerSampler()
    vqe = SamplingVQE(
        sampler=sampler, 
        ansatz=ansatz_transpiled, 
        optimizer=COBYLA(maxiter=200)
    )

    # 5. Solve using Minimum Eigen Optimizer
    quantum_optimizer = MinimumEigenOptimizer(vqe)
    result = quantum_optimizer.solve(quadratic_program)

    # 6. Interpret results to node indices
    solution = tsp_app.interpret(result)

    # Handle various return types from interpret
    if hasattr(solution, "tolist"):
        return solution.tolist()
    return list(solution)

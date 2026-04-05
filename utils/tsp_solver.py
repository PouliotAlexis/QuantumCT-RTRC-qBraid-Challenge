import numpy as np
from qiskit import transpile
from qiskit.circuit.library import RealAmplitudes
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.applications import Tsp


def solve_tsp_with_vqe(distance_matrix: np.ndarray) -> tuple[list[int], int, int, int]:
    """
    Solves the Traveling Salesman Problem (TSP) using a Quantum VQE algorithm.

    Args:
        distance_matrix (np.ndarray): The matrix of Euclidean distances between nodes.

    Returns:
        tuple: (route, num_qubits, num_gates, depth)
            - route (list[int]): The optimal order of node indices.
            - num_qubits (int): Total qubits in the transpiled circuit.
            - num_gates (int): Total gate operations in the transpiled circuit.
            - depth (int): Total depth of the transpiled circuit.
    """
    # Initialize TSP application and convert to Quadratic Program
    tsp_app = Tsp(distance_matrix)
    quadratic_program = tsp_app.to_quadratic_program()

    # 1. Setup Backend
    backend = AerSimulator()

    # 2. Create Ansatz
    num_qubits = quadratic_program.get_num_vars()
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=3)

    # 3. Transpilation (CRITICAL for performance)
    ansatz_transpiled = transpile(ansatz, backend=backend)

    # 4. Configure Sampler and SamplingVQE
    sampler = AerSampler()
    vqe = SamplingVQE(
        sampler=sampler, 
        ansatz=ansatz_transpiled, 
        optimizer=COBYLA(maxiter=500)
    )

    # 5. Solve using Minimum Eigen Optimizer
    quantum_optimizer = MinimumEigenOptimizer(vqe)
    result = quantum_optimizer.solve(quadratic_program)

    # 6. Interpret results to node indices
    solution = tsp_app.interpret(result)

    # Extract metrics from the transpiled circuit
    n_qubits = ansatz_transpiled.num_qubits
    n_gates = ansatz_transpiled.size()
    depth = ansatz_transpiled.depth()

    # Handle various return types from interpret
    if hasattr(solution, "tolist"):
        return solution.tolist(), n_qubits, n_gates, depth
    return list(solution), n_qubits, n_gates, depth

import numpy as np
from qiskit import transpile
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import QAOAAnsatz
from qiskit_aer import AerSimulator
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA  # Classical optimizer
from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo


def solve_tsp_with_qaoa(distance_matrix: np.ndarray, p: int = 3) -> tuple[list[int], int, int, int]:
    """
    Solves the Traveling Salesman Problem (TSP) for a given sector using QAOA with COBYLA optimizer.

    Args:
        distance_matrix (np.ndarray): The distance/cost matrix for TSP.
        p (int): The number of QAOA layers (default: 3).

    Returns:
        tuple: A tuple containing:
            - optimal_route: The best route found (list of node indices).
            - num_qubits: Total qubits used in the QAOA mapping.
            - num_gates: Total gate operations.
            - depth: Circuit depth.
    """
    tsp = Tsp(distance_matrix)
    qp = tsp.to_quadratic_program()

    # 2. QUBO Conversion
    # Penalties can be adjusted if routes are invalid,
    # but Qiskit's default calculation is generally precise.
    qubo = QuadraticProgramToQubo().convert(qp)
    qubitOp, offset = qubo.to_ising()

    # --- IMPORTANT: Do not print(qubitOp.to_matrix()) here ---

    # 3. Robust Optimizer
    # tol=1e-3 prevents COBYLA from stopping too early
    optimizer = COBYLA(maxiter=150, tol=1e-3)

    # 4. Aer Sampler (Fast simulation)
    sampler = StatevectorSampler()

    # 5. QAOA with p layers for better precision
    qaoa_instance = QAOA(sampler=sampler, optimizer=optimizer, reps=p)

    # Execution
    result = qaoa_instance.compute_minimum_eigenvalue(qubitOp)

    # 6. Strict Interpretation
    # sample_most_likely converts the quantum state into the most probable bitstring
    most_likely_bitstring = tsp.sample_most_likely(result.eigenstate)

    # interpret converts these bits into a list of cities [0, 1, 2]
    optimal_route = tsp.interpret(most_likely_bitstring)

    # Metric calculation with the explicit QAOA circuit
    ansatz = QAOAAnsatz(cost_operator=qubitOp, reps=p)
    backend = AerSimulator()
    ansatz_transpiled = transpile(ansatz, backend=backend)
    n_gates = ansatz_transpiled.size()
    depth = ansatz_transpiled.depth()

    # Calculation of true distance
    total_distance = result.eigenvalue + offset

    # Return the optimal route and metrics
    return optimal_route, qubitOp.num_qubits, n_gates, depth

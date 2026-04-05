import numpy as np
from qiskit import transpile
from qiskit.circuit.library import RealAmplitudes
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.applications import Tsp


def solve_tsp(distance_matrix: np.ndarray):
    """
    Solves the Traveling Salesman Problem (TSP) for a given sector using VQE.

    Args:
        distance_matrix (np.ndarray): The distance matrix for TSP.

    Returns:
        list: The optimal route found (list of node indices).
    """
    tsp_app = Tsp(distance_matrix)
    quadratic_program = tsp_app.to_quadratic_program()

    # 1. Configurer le backend
    backend = AerSimulator()

    # 2. Créer l'Ansatz
    num_qubits = quadratic_program.get_num_vars()
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=2)

    # --- ÉTAPE CRUCIALE : La Transpilation ---
    # On transforme le circuit RealAmplitudes en portes de base (cx, ry, etc.)
    ansatz_transpiled = transpile(ansatz, backend=backend)
    # ------------------------------------------

    # 3. Configurer le Sampler et VQE
    sampler = AerSampler()

    # Utilisez ansatz_transpiled ici
    vqe = SamplingVQE(
        sampler=sampler, ansatz=ansatz_transpiled, optimizer=COBYLA(maxiter=200)
    )

    optimizer_quantique = MinimumEigenOptimizer(vqe)
    resultat = optimizer_quantique.solve(quadratic_program)

    # Extract the solution and convert to list of node indices
    solution = tsp_app.interpret(resultat)

    # Handle numpy array or other iterable types
    if hasattr(solution, "tolist"):
        return solution.tolist()
    elif isinstance(solution, (list, tuple)):
        return list(solution)
    else:
        # If it's something else, try to convert it
        return list(solution)

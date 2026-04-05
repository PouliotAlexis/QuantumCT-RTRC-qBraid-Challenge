import numpy as np
from qiskit import transpile
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import QAOAAnsatz
from qiskit_aer import AerSimulator
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA  # L'optimiseur classique
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

    # 2. Conversion en QUBO
    # On peut ajuster la pénalité si les routes sont invalides,
    # mais par défaut Qiskit la calcule assez bien.
    qubo = QuadraticProgramToQubo().convert(qp)
    qubitOp, offset = qubo.to_ising()

    # --- IMPORTANT: Retire le print(qubitOp.to_matrix()) ici ---

    # 3. Optimiseur plus robuste
    # tol=1e-3 aide COBYLA à ne pas s'arrêter trop tôt
    optimizer = COBYLA(maxiter=150, tol=1e-3)

    # 4. Sampler Aer (Rapide)
    sampler = StatevectorSampler()

    # 5. QAOA avec p=2 ou 3 pour plus de précision
    qaoa_instance = QAOA(sampler=sampler, optimizer=optimizer, reps=p)

    # Exécution
    result = qaoa_instance.compute_minimum_eigenvalue(qubitOp)

    # 6. Interprétation stricte
    # sample_most_likely convertit l'état quantique en la chaîne de bits la plus probable
    most_likely_bitstring = tsp.sample_most_likely(result.eigenstate)

    # interpret convertit ces bits en liste de villes [0, 1, 2]
    optimal_route = tsp.interpret(most_likely_bitstring)

    # Calcul des métriques avec le circuit QAOA explicit
    ansatz = QAOAAnsatz(cost_operator=qubitOp, reps=p)
    backend = AerSimulator()
    ansatz_transpiled = transpile(ansatz, backend=backend)
    n_gates = ansatz_transpiled.size()
    depth = ansatz_transpiled.depth()

    # Calcul de la distance réelle
    total_distance = result.eigenvalue + offset

    # On retourne la route optimale et les métriques
    return optimal_route, qubitOp.num_qubits, n_gates, depth

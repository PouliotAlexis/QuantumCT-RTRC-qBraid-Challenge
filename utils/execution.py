from typing import Tuple

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def execute_circuit(circuit: QuantumCircuit) -> Tuple:
    """
    Executes a quantum circuit using AerSimulator and collects metrics.

    Args:
        circuit (QuantumCircuit): The quantum circuit to execute.

    Returns:
        tuple: (result, num_qubits, total_gates)
    """
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1024).result()

    return (
        result,
        circuit.num_qubits,
        circuit.size(),
    )

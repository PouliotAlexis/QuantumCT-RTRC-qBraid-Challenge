from typing import Tuple

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def run_qc(circuit: QuantumCircuit) -> Tuple:
    """
    Executes a quantum circuit using AerSimulator and collects metrics.

    Args:
        circuit (QuantumCircuit): The quantum circuit to execute.

    Returns:
        tuple: A tuple containing:
            - result: The execution result from the simulator.
            - int: The number of qubits used in the circuit.
            - int: The total number of gate operations in the circuit.
    """
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1024).result()

    return (
        result,
        circuit.num_qubits,
        circuit.size(),
    )

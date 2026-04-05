# Quantum Courier: CVRP Solver (Yale Hackathon 2026)

Welcome to the **Quantum Courier** project, a specialized solver for the **Capacitated Vehicle Routing Problem (CVRP)**, developed for the Yale Hackathon 2026 sponsored by **RTX (RTRC)**, **QuantumCT**, and **qBraid**.

This implementation combines classical geometric heuristics with modern quantum optimization to solve complex logistics routing challenges.

## The Strategy: "Cluster-First, Route-Second"

To handle the complexity of CVRP (which is NP-hard), this solver employs a robust two-stage decomposition strategy:

1.  **Decomposition (Classical Clustering)**: Partitioning customers into groups (clusters) that a single vehicle can serve without exceeding its capacity limit.
2.  **Optimization (Quantum Routing)**: Determining the optimal sequence of stops within each cluster using quantum algorithms.

## Why This Approach?

Our hybrid methodology was chosen to maximize the potential of near-term quantum systems while maintaining practical scalability:

*   **Dimensionality Reduction**: Solving a large CVRP directly on a quantum computer would require an impractical number of qubits. By clustering first, we break the problem into smaller Traveling Salesman Problems (TSPs) that fit within the limits of NISQ (Noisy Intermediate-Scale Quantum) simulators and hardware.
*   **Heuristic Synergy**: The **Sweep algorithm** is exceptionally fast at handling capacity constraints classically. This allows the **QAOA** to focus exclusively on finding the best route within each sector, where quantum optimization truly shines.
*   **Geometric Compactness**: Our "Optimized Sweep" ensures that vehicles operate in distinct, non-overlapping geographic sectors. This naturally reduces the search space for the routing phase and leads to more intuitive, fuel-efficient solutions.
*   **Future-Proofing**: While we currently solve sub-problems, this modular architecture is designed to scale; as quantum hardware matures, we can increase the cluster size or eventually solve the global problem directly.

---

## Phase 1: Optimized Sweep Clustering

We use an **Optimized Sweep Algorithm** to perform the initial partitioning. Unlike a standard sweep, our implementation rotates the starting point to find the global minimum for geometric dispersion.

*   **Polar Transformation**: Customers are mapped to polar coordinates $(r, \theta)$ relative to the central depot at $(0,0)$.
*   **Rotation Optimization**: The algorithm iterates through all possible starting angles to partition the sorted customers according to vehicle capacity ($C$).
*   **Cost Metric**: It selects the partition that minimizes the total **angular spread** across all clusters, ensuring each vehicle operates in a geometrically compact sector.

---

## Phase 2: Quantum Routing with QAOA

Once clusters are defined, the routing for each vehicle is treated as a **Traveling Salesman Problem (TSP)** and solved using the **Quantum Approximate Optimization Algorithm (QAOA)**.

### Technical Implementation
*   **Framework**: Built using `qiskit-algorithms` and `qiskit-optimization`.
*   **Formulation**: The TSP is mapped to a **Quadratic Unconstrained Binary Optimization (QUBO)** problem.
*   **Quantum Circuit**:
    *   **Layers ($p$)**: We use $p=3$ for an optimal balance between circuit depth and approximation accuracy.
    *   **Simulator**: Executed on high-performance simulators provided by qBraid.
*   **Classical Loop**: The **COBYLA** optimizer is used for parameter training, with a fine-tuned tolerance ($10^{-3}$) to ensure convergence.

---

## Repository Structure

*   [`main.py`](main.py): Entry point to run the solver on different CVRP instances.
*   [`utils/`](utils/):
    *   [`get_cluster.py`](utils/get_cluster.py): Implementation of the Optimized Sweep algorithm.
    *   [`qaoa.py`](utils/qaoa.py): Quantum circuit logic and TSP-to-QUBO mapping.
    *   [`CVRPDataLoader.py`](utils/CVRPDataLoader.py): Handles standard challenge instances (Sets 1-4).
    *   [`save_crp_solutions.py`](utils/save_crp_solutions.py): Formats output for judging.
*   [`data/`](data/): Contains output solution files (e.g., `Instance1.txt`) and metric CSVs.
*   [`challenge/`](challenge/): Original hackathon instructions, rules, and notebook.

---

## Setup & Usage

### Prerequisites
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### Running the Solver
To execute the solver for a specific instance, modify the `INSTANCE_ID` in `main.py` and run:
```bash
python main.py
```

Results will be generated in the `data/` directory according to the hackathon's required format:
```text
r1: 0, 2, 3, 0
r2: 0, 1, 4, 0
```

---

## Insights & Scalability
Our approach leverages geometric intuition to reduce the search space of the quantum optimizer. By decomposing the large CVRP into smaller TSPs, we can maintain high solution quality while respecting current hardware (NISQ) limitations on qubit count and gate depth.


---

## Development Team

*   [**Alexis Pouliot**](https://github.com/PouliotAlexis)
*   [**Amarey Farris Hajouji Idrissi Rios**](https://github.com/haja8956)
*   [**Gabriel Michaud**](https://github.com/GabMichaud)
*   [**Jasmin Pelletier**](https://github.com/Jas-pel)
*   [**Laurier Perron**](https://github.com/perl2548)

---

*Developed for the Yale Hackathon 2026.*

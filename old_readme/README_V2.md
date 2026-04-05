# Quantum Courier: CVRP Solver (Yale Hackathon 2026)

Welcome to the **Quantum Courier** project, a specialized solver for the **Capacitated Vehicle Routing Problem (CVRP)**, developed for the Yale Hackathon 2026 sponsored by **RTX (RTRC)**, **QuantumCT**, and **qBraid**.

This implementation combines classical geometric heuristics with modern quantum optimization to solve complex logistics routing challenges.

---

## The Strategy: "Cluster-First, Route-Second"

To handle the complexity of CVRP (which is NP-hard), this solver employs a robust two-stage decomposition strategy:

1. **Decomposition (Classical Clustering)**: Partitioning customers into groups (clusters) that a single vehicle can serve without exceeding its capacity limit.
2. **Optimization (Quantum Routing)**: Determining the optimal sequence of stops within each cluster using quantum algorithms.

## Why This Approach?

Our hybrid methodology was chosen to maximize the potential of near-term quantum systems while maintaining practical scalability:

- **Dimensionality Reduction**: Solving a large CVRP directly on a quantum computer would require an impractical number of qubits. By clustering first, we break the problem into smaller Traveling Salesman Problems (TSPs) that fit within the limits of NISQ (Noisy Intermediate-Scale Quantum) simulators and hardware.
- **Heuristic Synergy**: The **Sweep algorithm** is exceptionally fast at handling capacity constraints classically. This allows the **QAOA** to focus exclusively on finding the best route within each sector, where quantum optimization truly shines.
- **Geometric Compactness**: Our "Optimized Sweep" ensures that vehicles operate in distinct, non-overlapping geographic sectors. This naturally reduces the search space for the routing phase and leads to more intuitive, fuel-efficient solutions.
- **Future-Proofing**: While we currently solve sub-problems, this modular architecture is designed to scale — as quantum hardware matures, we can increase the cluster size or eventually solve the global problem directly.

---

## Phase 1: Optimized Sweep Clustering

We use an **Optimized Sweep Algorithm** to perform the initial partitioning. Unlike a standard sweep, our implementation **rotates the starting angle across all possible values** to find the global minimum for geometric dispersion — a novel enhancement over the naive fixed-start sweep.

- **Polar Transformation**: Customers are mapped to polar coordinates $(r, \theta)$ relative to the central depot at $(0,0)$.
- **Rotation Optimization**: The algorithm iterates through all possible starting angles to partition the sorted customers according to vehicle capacity ($C$).
- **Cost Metric**: It selects the partition that minimizes the total **angular spread** across all clusters, ensuring each vehicle operates in a geometrically compact sector.

This approach consistently outperforms a fixed-start sweep in terms of cluster compactness, reducing unnecessary route crossings before the quantum phase even begins.

---

## Phase 2: Quantum Routing with QAOA

Once clusters are defined, the routing for each vehicle is treated as a **Traveling Salesman Problem (TSP)** and solved using the **Quantum Approximate Optimization Algorithm (QAOA)**.

### Technical Implementation

- **Framework**: Built using `qiskit-algorithms` and `qiskit-optimization`.
- **Formulation**: The TSP is mapped to a **Quadratic Unconstrained Binary Optimization (QUBO)** problem via `QuadraticProgramToQubo`.
- **Quantum Circuit**:
  - **Layers ($p$)**: We use $p=3$ for an optimal balance between circuit depth and approximation accuracy.
  - **Sampler**: `StatevectorSampler` for high-fidelity simulation.
  - **Simulator**: Executed on high-performance simulators provided by qBraid.
- **Classical Loop**: The **COBYLA** optimizer is used for parameter training (`maxiter=150`, `tol=1e-3`) to ensure robust convergence without overfitting to noise.

### Qubit Scaling

For a cluster of $n$ customers, the TSP-to-QUBO mapping requires $n^2$ binary variables, hence $n^2$ qubits. Our clustering strategy keeps $n$ small (typically 2–4 nodes per cluster), making the approach feasible on current NISQ hardware.

| Cluster size (n) | Qubits required ($n^2$) |
|-----------------|------------------------|
| 2               | 4                      |
| 3               | 9                      |
| 4               | 16                     |

---

## Results Summary

| Instance | Known Optimal | Our Solution | Approximation Ratio | Qubits Used | Gate Operations | Execution Time |
|----------|--------------|--------------|---------------------|-------------|-----------------|----------------|
| 1        | 26.18        | _TBD_        | _TBD_               | _TBD_       | _TBD_           | _TBD_ s        |
| 2        | 26.18        | _TBD_        | _TBD_               | _TBD_       | _TBD_           | _TBD_ s        |
| 3        | 49.50        | _TBD_        | _TBD_               | _TBD_       | _TBD_           | _TBD_ s        |
| 4        | _N/A_        | _TBD_        | _TBD_               | _TBD_       | _TBD_           | _TBD_ s        |

> **Approximation Ratio** = Our Solution Distance / Known Optimal Distance. A value of 1.00 means optimal; the closer to 1.00, the better.

**Best routes found:**

```
# Instance 1
r1: TBD
r2: TBD

# Instance 2
r1: TBD
r2: TBD

# Instance 3
r1: TBD
r2: TBD
r3: TBD

# Instance 4
r1: TBD
r2: TBD
r3: TBD
r4: TBD
```

---

## Repository Structure

```
.
├── main.py                        # Entry point — run solver on a given instance
├── requirements.txt               # Python dependencies
├── utils/
│   ├── get_cluster.py             # Optimized Sweep clustering algorithm
│   ├── qaoa.py                    # QAOA circuit, TSP-to-QUBO mapping, COBYLA loop
│   ├── CVRPDataLoader.py          # Loads challenge instances (Sets 1–4)
│   ├── get_distance_matrix.py     # Builds adjacency matrix from cluster nodes
│   ├── save_crp_solutions.py      # Formats output for hackathon submission
│   └── save_instance_results.py   # Records qubit count, gate count, execution time
├── data/
│   ├── Instance1.txt              # Solution file — instance 1
│   ├── Instance3.txt              # Solution file — instance 3
│   ├── data.csv                   # Quantum resource metrics per run
│   └── optimal_results.csv        # Known optimal solutions for comparison
├── test/                          # Unit tests for each module
└── challenge/
    ├── README.md                  # Original challenge description
    └── qCourier-YaleHackathon-2026.ipynb
```

---

## Setup & Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Solver

```bash
# Set INSTANCE_ID in main.py (1–4), then:
python main.py
```

**Full example — solving Instance 3:**

```python
# In main.py, set:
INSTANCE_ID = 3
# Then run:
# python main.py
#
# Expected output in data/:
#   Instance3.txt  →  routes in hackathon format
#   data.csv       →  qubit count, gate count, execution time appended
```

Output format (per hackathon spec):
```
r1: 0, 2, 3, 0
r2: 0, 1, 4, 0
```

### Running Tests

```bash
python -m pytest test/
```

---

## Insights & Scalability

Our approach leverages geometric intuition to reduce the search space of the quantum optimizer. By decomposing the large CVRP into smaller TSPs, we can maintain high solution quality while respecting current hardware (NISQ) limitations on qubit count and gate depth.

The key insight is that **geometric compactness of clusters directly correlates with TSP route quality**: a compact cluster produces a near-planar distance matrix, which is easier for QAOA to optimize at low circuit depth. Our rotation-optimized sweep is designed precisely to maximize this property.

As quantum hardware scales, this architecture allows straightforward upgrades: increasing $p$ (QAOA layers), growing cluster sizes, or eventually solving the full CVRP in a single quantum pass.

---

## Development Team

- [**Alexis Pouliot**](https://github.com/PouliotAlexis)
- [**Amarey Farris Hajouji Idrissi Rios**](https://github.com/haja8956)
- [**Gabriel Michaud**](https://github.com/GabMichaud)
- [**Jasmin Pelletier**](https://github.com/Jas-pel)
- [**Laurier Perron**](https://github.com/perl2548)

---

*Developed for the Yale Hackathon 2026 — RTX (RTRC) × QuantumCT × qBraid.*
# Quantum Courier — Hybrid Quantum-Classical CVRP Solver
### Yale Hackathon 2026 · RTX (RTRC) × QuantumCT × qBraid

> A **NISQ-aware hybrid solver** for the Capacitated Vehicle Routing Problem, combining a novel rotation-optimized sweep algorithm with QAOA-based quantum routing — built to run efficiently on today's quantum hardware while scaling gracefully as it matures.

---

## Table of Contents

1. [Problem & Motivation](#1-problem--motivation)
2. [Architecture Overview](#2-architecture-overview)
3. [Key Innovations](#3-key-innovations)
4. [Phase 1 — Rotation-Optimized Sweep Clustering](#4-phase-1--rotation-optimized-sweep-clustering)
5. [Phase 2 — Quantum Routing with QAOA](#5-phase-2--quantum-routing-with-qaoa)
6. [Quantum Resource Analysis](#6-quantum-resource-analysis)
7. [Results](#7-results)
8. [Repository Structure](#8-repository-structure)
9. [Setup & Usage](#9-setup--usage)
10. [Scalability & Future Work](#10-scalability--future-work)
11. [Development Team](#11-development-team)

---

## 1. Problem & Motivation

The **Capacitated Vehicle Routing Problem (CVRP)** asks: *given a depot and a set of customers with known demands, find the minimum-cost set of routes for a fleet of capacity-limited vehicles.*

It is **NP-hard** — solution space grows exponentially with problem size, making it intractable for classical exact solvers at scale. Even a **0.5% improvement** in route quality translates to millions of dollars in annual logistics savings for companies like RTX.

Quantum algorithms offer a fundamentally different search strategy over the combinatorial solution space. Our goal is to demonstrate a **practical, resource-efficient hybrid approach** that produces high-quality solutions while staying within the qubit and gate-depth budgets of current NISQ devices.

---

## 2. Architecture Overview

We employ a **"Cluster-First, Route-Second"** decomposition strategy — a principled divide-and-conquer approach that breaks the global CVRP into a series of small Traveling Salesman Problems (TSPs), each solvable by a quantum circuit.

```
┌─────────────────────────────────────────────────────┐
│                   CVRP Instance                     │
│            (customers + depot + capacity)           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         Phase 1 — Classical Clustering              │
│      Rotation-Optimized Sweep Algorithm             │
│   → Partitions customers into compact sectors       │
│   → Each sector ≤ vehicle capacity (n ≤ 4 nodes)   │
└────────────────────┬────────────────────────────────┘
                     │  One TSP sub-problem per cluster
                     ▼
┌─────────────────────────────────────────────────────┐
│         Phase 2 — Quantum Routing (QAOA)            │
│   TSP → QUBO → Ising Hamiltonian → Quantum Circuit  │
│   Optimized with COBYLA (classical outer loop)      │
│   → Optimal route per cluster                       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            Full CVRP Solution                       │
│     Merged routes in hackathon submission format    │
└─────────────────────────────────────────────────────┘
```

This hybrid design is **intentional**: classical computers are extremely good at geometric partitioning; quantum computers offer a search advantage on discrete combinatorial optimization. We let each do what it does best.

---

## 3. Key Innovations

### 🔄 Novel: Rotation-Optimized Sweep
Standard sweep algorithms use a fixed starting angle, which can produce suboptimal cluster boundaries by accident of geometry. Our implementation **exhaustively searches all possible starting angles** and selects the partition that minimizes total angular spread across all clusters. This guarantees the globally optimal sweep partition — not just a locally good one — at negligible additional cost ($O(n)$ extra iterations).

### 📐 NISQ-Aware Cluster Sizing
Cluster sizes are deliberately kept at $n \leq 4$ customers, requiring at most $n^2 = 16$ qubits per sub-problem. This is not a limitation — it is a **conscious hardware-aware design choice** that ensures the quantum circuits remain feasible on current NISQ simulators and real hardware without needing error correction.

### 🔗 Modular, Upgradeable Architecture
Each component (clustering, QUBO mapping, quantum execution) is independently swappable. Increasing QAOA depth $p$, adopting a different optimizer, or scaling cluster sizes requires changes in a single module — enabling painless upgrades as hardware matures.

---

## 4. Phase 1 — Rotation-Optimized Sweep Clustering

### How It Works

Customers are mapped to **polar coordinates** $(r, \theta)$ relative to the central depot at $(0, 0)$, then sorted by angle $\theta$. A sweep groups consecutive customers into clusters of size $\leq C$ (vehicle capacity).

The innovation is in how the sweep's starting angle is chosen:

```python
for start_idx in range(n_nodes):                          # Try every starting angle
    rotated_nodes = [nodes_angle[(start_idx + i) % n_nodes]
                     for i in range(n_nodes)]
    ...
    spread = (angle_end - angle_start) % (2 * math.pi)   # Angular spread per cluster
    current_angle_sum += spread

if current_angle_sum < lowest_angle_sum:                  # Keep global minimum
    best_clusters = current_clusters
```

By minimizing **total angular spread**, we ensure each vehicle operates in a geometrically compact, non-overlapping sector — which directly reduces the search space for the QAOA phase and leads to better routes.

### Why Angular Spread?

A compact cluster (small angular spread) produces a nearly planar distance matrix. QAOA is known to perform better on structured, near-planar TSP instances at low circuit depth — meaning our clustering directly improves quantum solution quality.

---

## 5. Phase 2 — Quantum Routing with QAOA

Each cluster is treated as a **Traveling Salesman Problem** and solved via the Quantum Approximate Optimization Algorithm.

### Pipeline

```
Cluster distance matrix
        │
        ▼
   Tsp (Qiskit)          → Quadratic Program
        │
        ▼
QuadraticProgramToQubo   → QUBO formulation
        │
        ▼
   to_ising()            → Pauli Hamiltonian (qubitOp)
        │
        ▼
   QAOA (p=3 layers)     → Parameterized quantum circuit
        │
        ▼
   COBYLA optimizer       → Classical parameter training
   (maxiter=150, tol=1e-3)
        │
        ▼
sample_most_likely()     → Most probable bitstring
        │
        ▼
   tsp.interpret()        → Optimal route
```

### Design Choices & Rationale

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| QAOA layers $p$ | 3 | Balances circuit depth vs. approximation quality; $p=1$ rarely escapes local minima for TSP |
| Optimizer | COBYLA | Derivative-free, handles noisy landscapes well; robust for variational circuits |
| `maxiter` | 150 | Sufficient convergence budget without overfitting to noise |
| `tol` | 1e-3 | Prevents premature termination while avoiding wasted iterations |
| Sampler | `StatevectorSampler` | High-fidelity simulation; exact state vector avoids sampling noise |

### Qubit Scaling

For a cluster of $n$ customers, the TSP-to-QUBO mapping encodes each city-at-each-timestep as a binary variable, requiring $n^2$ qubits:

| Cluster size $n$ | Qubits ($n^2$) | Gate depth (approx.) |
|-----------------|----------------|----------------------|
| 2 | 4 | Low |
| 3 | 9 | Moderate |
| 4 | 16 | Manageable on NISQ |
| 5 | 25 | Pushing NISQ limits |

Our cluster size cap of $n \leq 4$ keeps every sub-problem under 16 qubits — comfortably within NISQ hardware budgets.

---

## 6. Quantum Resource Analysis

### Classical vs. Quantum Responsibility

| Task | Method | Why |
|------|--------|-----|
| Capacity partitioning | Classical sweep | Trivially solved classically; no quantum advantage |
| Route optimization within sector | QAOA | Discrete combinatorial search — quantum advantage domain |
| Parameter training | COBYLA (classical) | Outer loop; handles parameter landscape classically |

### Resource Efficiency by Design

Solving the full CVRP directly on a quantum computer with $N$ customers would require $O(N^2)$ qubits for the QUBO encoding — quickly exceeding any current hardware's coherent qubit count. By decomposing into clusters of size $\leq 4$, we bound qubit usage at **16 qubits per sub-problem**, regardless of total problem size.

This means the quantum resource cost scales with **cluster size** (fixed by design), not with **total problem size** — a crucial distinction for practical NISQ deployment.

---

## 7. Results

| Instance | Known Optimal | Our Solution | Approximation Ratio | Qubits Used | Gate Operations | Execution Time |
|----------|--------------|--------------|---------------------|-------------|-----------------|----------------|
| 1 | 26.18 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ s |
| 2 | 26.18 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ s |
| 3 | 49.50 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ s |
| 4 | _N/A_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ s |

> **Approximation Ratio** = Our Solution / Known Optimal. Closer to 1.00 is better; 1.00 = optimal.

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

## 8. Repository Structure

```
.
├── main.py                        # Entry point — runs the full solver on a given instance
├── requirements.txt               # Python dependencies
├── utils/
│   ├── get_cluster.py             # Rotation-Optimized Sweep clustering algorithm
│   ├── qaoa.py                    # QAOA circuit, TSP→QUBO mapping, COBYLA training loop
│   ├── CVRPDataLoader.py          # Loads challenge instances (Sets 1–4)
│   ├── get_distance_matrix.py     # Builds adjacency matrix from cluster nodes
│   ├── save_crp_solutions.py      # Formats routes for hackathon submission
│   └── save_instance_results.py   # Records qubit count, gate count, execution time
├── data/
│   ├── Instance1.txt              # Solution file — instance 1
│   ├── Instance3.txt              # Solution file — instance 3
│   ├── data.csv                   # Quantum resource metrics per run
│   └── optimal_results.csv        # Known optimal solutions for benchmarking
├── test/                          # Unit tests for all modules (pytest)
│   ├── test_cvrp_dataloader.py
│   ├── test_get_cluster.py
│   ├── test_get_distance_matrix.py
│   ├── test_qaoa.py
│   ├── test_save_crp_solutions.py
│   └── test_save_instance_results.py
└── challenge/
    ├── README.md                  # Original challenge description
    └── qCourier-YaleHackathon-2026.ipynb
```

---

## 9. Setup & Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Solver

Set `INSTANCE_ID` in `main.py` (1–4), then:

```bash
python main.py
```

**Full example — solving Instance 3:**

```python
# In main.py:
INSTANCE_ID = 3
# Then:
# python main.py
#
# Outputs written to data/:
#   Instance3.txt  →  routes in hackathon format
#   data.csv       →  qubit count, gate count, execution time (appended)
```

**Output format** (per hackathon spec):
```
r1: 0, 2, 3, 0
r2: 0, 1, 4, 0
```

### Running Tests

```bash
python -m pytest test/
```

---

## 10. Scalability & Future Work

Our architecture is explicitly designed to evolve alongside quantum hardware:

| Hardware generation | Supported upgrade |
|---------------------|-------------------|
| Current NISQ (today) | Cluster size $n \leq 4$, $p=3$, StatevectorSampler |
| Near-term NISQ (2–3 years) | Increase $n$ to 5–6, increase $p$, use real hardware samplers |
| Fault-tolerant era | Solve full CVRP in a single quantum pass, no decomposition needed |

The key insight driving our design: **geometric compactness of clusters directly correlates with QAOA solution quality**. A compact cluster yields a near-planar distance matrix, which QAOA can optimize effectively at low circuit depth ($p=3$). Our rotation-optimized sweep is specifically engineered to maximize this property — making the quantum phase as easy as possible to solve well.

---

## 11. Development Team

- [**Alexis Pouliot**](https://github.com/PouliotAlexis)
- [**Amarey Farris Hajouji Idrissi Rios**](https://github.com/haja8956)
- [**Gabriel Michaud**](https://github.com/GabMichaud)
- [**Jasmin Pelletier**](https://github.com/Jas-pel)
- [**Laurier Perron**](https://github.com/perl2548)

---

*Developed for the Yale Hackathon 2026 — RTX (RTRC) × QuantumCT × qBraid.*
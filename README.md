# 🍃 BioPath Optimizer
> **Ant Colony Optimization for carbon-neutral delivery route planning**
> AlgoFest Hackathon 2026 · AI/ML + Sustainable Technology

---

## The Problem

Global logistics accounts for ~8% of worldwide CO₂ emissions. The root cause is inefficient routing — most delivery systems rely on greedy algorithms that leave massive fuel savings untapped.

**BioPath Optimizer solves this using a mechanism nature already perfected: ant colonies.**

---

## The Biomimicry Insight

When ants forage, they deposit pheromone trails. Shorter paths get traversed more often, accumulating stronger trails, attracting more ants. Over generations, the colony converges on the optimal route — no central controller, no global knowledge needed.

This is Ant Colony Optimization (ACO), and it maps directly onto the Travelling Salesman Problem at the heart of every delivery network.

---

## Measured Results

| Network | ACO Cost | Greedy Cost | Improvement |
|---------|----------|-------------|-------------|
| 5-city  | 70.00    | 70.00       | Matched optimal |
| 10-city | 156.34   | 208.47      | **25.01% better** |

> A 25% fuel reduction across a mid-sized logistics fleet (100 vehicles, 50,000 km/year each)
> eliminates approximately **375,000 litres of fuel** and **~1,000 tonnes of CO₂ annually**.

---

## Technical Implementation

### Transition probability

```
P(i→j) = [τ(i,j)^α × η(i,j)^β] / Σ_k [τ(i,k)^α × η(i,k)^β]

τ(i,j) = pheromone intensity on edge (i,j)
η(i,j) = 1/distance(i,j)   heuristic desirability
α = pheromone weight  (default 1.0)
β = heuristic weight  (default 2.5)
```

### Pheromone update

```
evaporation:    τ(i,j) ← τ(i,j) × (1 - ρ)
reinforcement:  τ(i,j) ← τ(i,j) + Q/L_k   for each ant k using edge (i,j)

ρ = evaporation rate (default 0.4)
Q = deposit constant (100.0)
L_k = total tour cost of ant k
```

### Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Single ant tour | O(n²) | O(n) |
| One generation (m ants) | O(m·n²) | O(n²) |
| Full run (t iterations) | **O(t·m·n²)** | **O(n²)** |

With defaults (t=150, m=30): scales to 50+ cities in under 1 second.
Brute force is O(n!) — 10 cities = 3,628,800 routes. ACO finds near-optimal in 4,500 targeted evaluations.

### Stack

| Layer | Technology |
|-------|------------|
| Core engine | C++17, zero external dependencies |
| Selection | Roulette-wheel proportional probability |
| Visualization | HTML5 Canvas + Chart.js |
| Demo | Standalone index.html — open in any browser, no install |

---

## How to Run

**Web demo (no install):**
```
Open index.html in any browser → adjust sliders → click Run
```

**C++ engine:**
```bash
g++ -O2 -std=c++17 -o biopath biopath_optimizer.cpp
./biopath
```

---

## Project Structure

```
BioPath-Optimizer/
├── biopath_optimizer.cpp   # Core C++ ACO engine
├── index.html              # Interactive web demo
├── results_5city.json      # C++ output
├── results_10city.json     # C++ output
└── README.md
```

---

## Team

| Name | Role |
|------|------|
| Areeba Qammar | C++ engine, ACO algorithm, architecture |
| Hifza Sultan | Web demo, visualization, presentation |

**Tracks: Artificial Intelligence & Machine Learning · Sustainable Technology**

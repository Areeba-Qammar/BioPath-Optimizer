# 🍃 BioPath Optimizer

> **Ant Colony Optimization for carbon-neutral delivery route planning**
> AlgoFest Hackathon 2026 · Track: AI/ML + Sustainable Technology

---

## 🐜 The Biomimicry Idea

Ant colonies solve the Travelling Salesman Problem every time they forage.
They deposit pheromone on paths — shorter paths get stronger trails,
more ants follow them, colony converges on the optimal route over generations.

**BioPath Optimizer translates this exact mechanism into C++ to minimize
fuel consumption and CO₂ emissions in real-world delivery networks.**

---

## 🚀 Features

| Feature | Detail |
|---------|--------|
| C++ ACO Engine | Full Ant Colony Optimization — roulette-wheel selection, pheromone evaporation & reinforcement |
| Interactive Web Demo | `index.html` — no install needed, open in any browser |
| Live Convergence Chart | Watch the colony learn in real time |
| Tunable Parameters | α, β, evaporation, ant count, generations |
| JSON Export | C++ engine exports `results_Ncity.json` for further analysis |
| Two Test Cases | 5-city and 10-city networks included |

---

## 📁 Project Structure

```
BioPath-Optimizer/
├── biopath_optimizer.cpp   # Core C++ ACO engine
├── index.html              # Interactive web demo (open directly in browser)
├── results_5city.json      # Output from C++ (auto-generated on run)
├── results_10city.json     # Output from C++ (auto-generated on run)
└── README.md
```

---

## ⚙️ How to Run

### Option 1 — Web Demo (no install)
```
Open index.html in any browser
Adjust sliders → click Run Bio-Optimization
```

### Option 2 — C++ Engine
```bash
g++ -O2 -std=c++17 -o biopath biopath_optimizer.cpp
./biopath
```
Outputs best route, fuel cost, and exports JSON for both test cases.

---

## 🧠 Algorithm

```
For each generation:
  Each ant builds a tour using roulette-wheel selection:
    P(i→j) = [pheromone(i,j)^α × (1/distance(i,j))^β] / Σ all unvisited

  Pheromone update:
    evaporation:    pheromone[i][j] *= (1 - ρ)
    reinforcement:  pheromone[i][j] += Q / tour_cost   (for each edge used)

  Track global best tour across all generations
```

| Parameter | Symbol | Default | Effect |
|-----------|--------|---------|--------|
| Pheromone weight | α | 1.0 | Higher = exploit known trails more |
| Heuristic weight | β | 2.5 | Higher = prefer shorter edges greedily |
| Evaporation | ρ | 0.4 | Higher = forget faster, explore more |
| Ants | — | 30 | More ants = better coverage per generation |
| Generations | — | 150 | More = closer to global optimum |

---

## 🌍 Real-World Impact

A 10–15% fuel reduction across a mid-sized logistics fleet
eliminates thousands of tonnes of CO₂ annually.
BioPath shows that **the solution already exists in nature**.

---

## 👥 Team

| Name | Role |
|------|------|
| Areeba Qamar | C++ engine, algorithm, presentation|
| Hifza Sultan | Web demo, visualization, architecture |

---

## 🏷️ Tracks

**Artificial Intelligence & Machine Learning · Sustainable Technology**

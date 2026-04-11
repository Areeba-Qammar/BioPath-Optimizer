# 🍃 BioPath Optimizer

> **Nature-inspired route optimization for carbon-neutral logistics**
> Built for AlgoFest Hackathon 2026

---

## 🐜 The Biomimicry Idea

Ant colonies solve the Travelling Salesman Problem every time they find food.
They leave pheromone trails — the shorter the path, the stronger the trail,
the more ants follow it. Over generations, the colony converges on the optimal route.

**BioPath Optimizer applies this exact mechanism — Ant Colony Optimization (ACO) —
to real-world delivery route planning**, minimizing fuel consumption and CO₂ emissions.

---

## 🚀 Features

- **ACO Engine in Python** — fully vectorized with NumPy for speed
- **Reference implementation in C++** — demonstrating algorithmic correctness
- **Interactive Streamlit UI** — configure ant population, generations, pheromone weights
- **Live convergence chart** — watch the colony learn in real time
- **Route visualization** — Plotly map of the optimized delivery network
- **Efficiency metric** — shows % improvement vs. naive random routing

---

## 📁 Project Structure

```
BioPath-Optimizer/
├── core/
│   └── optimizer.py        # ACO engine (Python/NumPy)
├── biopath_optimizer.cpp   # Reference C++ implementation
├── app.py                  # Streamlit web interface
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

**C++ (optional, for reference):**
```bash
g++ -O2 -o biopath biopath_optimizer.cpp
./biopath
```

---

## 📦 Requirements

```
streamlit
numpy
plotly
```

Save as `requirements.txt`.

---

## 🧠 Algorithm — How ACO Works

| Parameter | Meaning | Default |
|-----------|---------|---------|
| α (alpha) | Pheromone weight — how much ants trust existing trails | 1.0 |
| β (beta)  | Heuristic weight — how much ants prefer shorter edges | 2.0 |
| Evaporation | Trail decay rate — prevents getting stuck in local optima | 0.5 |
| Ants | Number of agents exploring per generation | 20 |

**Each generation:**
1. Every ant constructs a full route using roulette-wheel probabilistic selection
2. Pheromones evaporate by `(1 - evaporation_rate)`
3. Ants reinforce edges on their route proportional to `Q / route_cost`
4. Best route so far is tracked across all generations

---

## 🌍 Real-World Impact

Optimizing delivery routes by even 10–15% across a mid-sized logistics company
reduces thousands of tonnes of CO₂ annually. BioPath demonstrates that
**solutions already exist in nature** — we just need to translate them into code.

---

## 👥 Team

| Name | Role |
|------|------|
| Areeba Qammar | Core algorithm, C++ implementation, presentation|
| Hifza Sultan | UI/UX, visualization, architecture  |

---

## 🏷️ Track

**Artificial Intelligence & Machine Learning** · **Sustainable Technology**

*AlgoFest Hackathon 2026*

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <numeric>
#include <limits>
#include <fstream>
#include <sstream>
#include <iomanip>
using namespace std;

// ─── Hyperparameters ────────────────────────────────────────────────
const int    NUM_ANTS    = 30;
const int    ITERATIONS  = 150;
const double ALPHA       = 1.0;   // Pheromone importance
const double BETA        = 2.5;   // Fuel efficiency importance
const double EVAPORATION = 0.4;
const double Q           = 100.0; // Pheromone deposit factor
const double INIT_PHER   = 0.1;

// ─── Ant ─────────────────────────────────────────────────────────────
struct Ant {
    vector<int> path;
    double total_fuel_cost = 0.0;
};

// ─── BioPathOptimizer ────────────────────────────────────────────────
class BioPathOptimizer {
private:
    int num_nodes;
    vector<vector<double>> fuel_matrix;
    vector<vector<double>> pheromones;
    mt19937 rng;

    // History for convergence output
    vector<double> best_cost_history;

public:
    BioPathOptimizer(int n, vector<vector<double>> matrix, unsigned seed = 42)
        : num_nodes(n), fuel_matrix(matrix), rng(seed) {
        pheromones.assign(n, vector<double>(n, INIT_PHER));
    }

    // ── Roulette Wheel Selection ──────────────────────────────────────
    int select_next_node(int current, vector<bool>& visited) {
        vector<double> probs(num_nodes, 0.0);
        double total = 0.0;

        for (int j = 0; j < num_nodes; j++) {
            if (!visited[j] && fuel_matrix[current][j] > 1e-9) {
                double pher     = pow(pheromones[current][j], ALPHA);
                double heuristic = pow(1.0 / fuel_matrix[current][j], BETA);
                probs[j]         = pher * heuristic;
                total           += probs[j];
            }
        }

        // Fallback: pick any unvisited
        if (total < 1e-12) {
            for (int j = 0; j < num_nodes; j++)
                if (!visited[j]) return j;
            return -1;
        }

        // Spin the wheel
        uniform_real_distribution<double> dist(0.0, total);
        double spin       = dist(rng);
        double cumulative = 0.0;
        for (int j = 0; j < num_nodes; j++) {
            cumulative += probs[j];
            if (spin <= cumulative) return j;
        }
        for (int j = num_nodes - 1; j >= 0; j--)
            if (!visited[j]) return j;
        return -1;
    }

    // ── Pheromone Update ─────────────────────────────────────────────
    void update_pheromones(vector<Ant>& colony) {
        // Evaporation
        for (int i = 0; i < num_nodes; i++)
            for (int j = 0; j < num_nodes; j++)
                pheromones[i][j] *= (1.0 - EVAPORATION);

        // Reinforcement: shorter routes deposit more pheromone
        for (auto& ant : colony) {
            if (ant.total_fuel_cost < 1e-9) continue;
            double deposit = Q / ant.total_fuel_cost;
            for (int k = 0; k < (int)ant.path.size() - 1; k++) {
                int i = ant.path[k];
                int j = ant.path[k + 1];
                pheromones[i][j] += deposit;
                pheromones[j][i] += deposit; // symmetric roads
            }
            // Return edge (last city back to start)
            int last  = ant.path.back();
            int first = ant.path.front();
            pheromones[last][first] += deposit;
            pheromones[first][last] += deposit;
        }
    }

    // ── Main Run ─────────────────────────────────────────────────────
    pair<vector<int>, double> run(bool verbose = true) {
        double         global_best_fuel = numeric_limits<double>::max();
        vector<int>    global_best_path;

        for (int t = 0; t < ITERATIONS; t++) {
            vector<Ant> colony(NUM_ANTS);

            // Each ant builds a complete tour
            for (auto& ant : colony) {
                vector<bool> visited(num_nodes, false);
                ant.path.push_back(0); // all ants start at city 0
                visited[0] = true;

                while ((int)ant.path.size() < num_nodes) {
                    int curr = ant.path.back();
                    int next = select_next_node(curr, visited);
                    if (next == -1) break;
                    ant.total_fuel_cost += fuel_matrix[curr][next];
                    ant.path.push_back(next);
                    visited[next] = true;
                }
                // Return to start
                ant.total_fuel_cost += fuel_matrix[ant.path.back()][ant.path[0]];

                if (ant.total_fuel_cost < global_best_fuel) {
                    global_best_fuel = ant.total_fuel_cost;
                    global_best_path = ant.path;
                }
            }

            update_pheromones(colony);
            best_cost_history.push_back(global_best_fuel);

            if (verbose && (t % 15 == 0 || t == ITERATIONS - 1)) {
                cout << "  Iter " << setw(3) << t
                     << "  |  Best Fuel Cost: " << fixed << setprecision(2)
                     << global_best_fuel << "\n";
            }
        }

        return {global_best_path, global_best_fuel};
    }

    // ── Export convergence data for HTML chart ────────────────────────
    void export_json(const string& filename,
                     const vector<int>& best_path,
                     double best_cost) {
        ofstream f(filename);
        f << "{\n";
        f << "  \"best_cost\": " << fixed << setprecision(4) << best_cost << ",\n";
        f << "  \"best_path\": [";
        for (int i = 0; i < (int)best_path.size(); i++)
            f << best_path[i] << (i + 1 < (int)best_path.size() ? "," : "");
        f << "],\n";
        f << "  \"convergence\": [";
        for (int i = 0; i < (int)best_cost_history.size(); i++)
            f << fixed << setprecision(4) << best_cost_history[i]
              << (i + 1 < (int)best_cost_history.size() ? "," : "");
        f << "]\n";
        f << "}\n";
        cout << "  Results saved to " << filename << "\n";
    }
};

// ─── Utility: print matrix ────────────────────────────────────────────
void print_matrix(const vector<vector<double>>& m) {
    int n = m.size();
    cout << "  Fuel Matrix (" << n << " cities):\n";
    for (int i = 0; i < n; i++) {
        cout << "  ";
        for (int j = 0; j < n; j++)
            cout << setw(6) << fixed << setprecision(1) << m[i][j];
        cout << "\n";
    }
}

// ─── Main ─────────────────────────────────────────────────────────────
int main() {
    cout << "\n";
    cout << "╔══════════════════════════════════════════╗\n";
    cout << "║       🍃  BioPath Optimizer  🍃          ║\n";
    cout << "║   Ant Colony Optimization — C++ Engine   ║\n";
    cout << "╚══════════════════════════════════════════╝\n\n";

    // ── Test Case 1: 5-city example ─────────────────────────────────
    cout << "▶ Test Case 1: 5-City Network\n";
    cout << "  Biomimicry: Simulating " << NUM_ANTS << " ants over "
         << ITERATIONS << " generations...\n\n";

    vector<vector<double>> fuel_5 = {
        { 0, 10, 15, 20, 25},
        {10,  0, 35, 25, 30},
        {15, 35,  0, 30,  5},
        {20, 25, 30,  0, 15},
        {25, 30,  5, 15,  0}
    };

    print_matrix(fuel_5);
    cout << "\n";

    BioPathOptimizer engine5(5, fuel_5);
    auto [path5, cost5] = engine5.run(true);

    cout << "\n  ✅ Best Route: ";
    for (int c : path5) cout << c << " → ";
    cout << path5[0] << "\n";
    cout << "  ✅ Total Fuel Cost: " << fixed << setprecision(2) << cost5 << "\n\n";
    engine5.export_json("results_5city.json", path5, cost5);

    // ── Test Case 2: 10-city random ──────────────────────────────────
    cout << "\n▶ Test Case 2: 10-City Random Network\n";
    int N = 10;
    mt19937 gen(99);
    uniform_real_distribution<double> dist(5.0, 50.0);

    vector<vector<double>> fuel_10(N, vector<double>(N, 0.0));
    for (int i = 0; i < N; i++)
        for (int j = i + 1; j < N; j++) {
            double d = dist(gen);
            fuel_10[i][j] = d;
            fuel_10[j][i] = d;
        }

    cout << "  Running ACO on 10 cities...\n\n";
    BioPathOptimizer engine10(N, fuel_10);
    auto [path10, cost10] = engine10.run(true);

    cout << "\n  ✅ Best Route: ";
    for (int c : path10) cout << c << " → ";
    cout << path10[0] << "\n";
    cout << "  ✅ Total Fuel Cost: " << fixed << setprecision(2) << cost10 << "\n\n";
    engine10.export_json("results_10city.json", path10, cost10);

    cout << "╔══════════════════════════════════════════╗\n";
    cout << "║  Open index.html to visualize results!   ║\n";
    cout << "╚══════════════════════════════════════════╝\n\n";

    return 0;
}

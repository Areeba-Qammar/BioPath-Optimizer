#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <numeric>
#include <limits>
using namespace std;

const int NUM_ANTS = 20;
const int ITERATIONS = 100;
const double ALPHA = 1.0;
const double BETA = 2.0;
const double EVAPORATION = 0.5;
const double Q = 100.0;

struct Ant {
    vector<int> path;
    double total_fuel_cost = 0.0;
};

class BioPathOptimizer {
private:
    int num_nodes;
    vector<vector<double>> fuel_matrix;
    vector<vector<double>> pheromones;
    mt19937 rng;

public:
    BioPathOptimizer(int n, vector<vector<double>> matrix)
        : num_nodes(n), fuel_matrix(matrix), rng(42) {
        pheromones.assign(n, vector<double>(n, 0.1));
    }

    // FIXED: Roulette Wheel Selection
    int select_next_node(int current_node, vector<bool>& visited) {
        vector<double> probabilities(num_nodes, 0.0);
        double total = 0.0;

        for (int j = 0; j < num_nodes; j++) {
            if (!visited[j] && fuel_matrix[current_node][j] > 0) {
                double pheromone = pow(pheromones[current_node][j], ALPHA);
                double heuristic = pow(1.0 / fuel_matrix[current_node][j], BETA);
                probabilities[j] = pheromone * heuristic;
                total += probabilities[j];
            }
        }

        if (total == 0.0) {
            // fallback: pick any unvisited
            for (int j = 0; j < num_nodes; j++)
                if (!visited[j]) return j;
            return -1;
        }

        // Roulette wheel spin
        uniform_real_distribution<double> dist(0.0, total);
        double spin = dist(rng);
        double cumulative = 0.0;
        for (int j = 0; j < num_nodes; j++) {
            cumulative += probabilities[j];
            if (spin <= cumulative) return j;
        }
        // Fallback: return last unvisited
        for (int j = num_nodes - 1; j >= 0; j--)
            if (!visited[j]) return j;
        return -1;
    }

    void run() {
        double global_best_fuel = numeric_limits<double>::max();
        vector<int> global_best_path;

        for (int t = 0; t < ITERATIONS; t++) {
            vector<Ant> colony(NUM_ANTS);

            // FIXED: Simulate ant travel
            for (auto& ant : colony) {
                vector<bool> visited(num_nodes, false);
                int start = 0;
                ant.path.push_back(start);
                visited[start] = true;

                while ((int)ant.path.size() < num_nodes) {
                    int current = ant.path.back();
                    int next = select_next_node(current, visited);
                    if (next == -1) break;
                    ant.path.push_back(next);
                    visited[next] = true;
                    ant.total_fuel_cost += fuel_matrix[current][next];
                }
                // Return to start
                if (!ant.path.empty())
                    ant.total_fuel_cost += fuel_matrix[ant.path.back()][ant.path[0]];

                if (ant.total_fuel_cost < global_best_fuel) {
                    global_best_fuel = ant.total_fuel_cost;
                    global_best_path = ant.path;
                }
            }

            update_pheromones(colony);

            if (t % 10 == 0)
                cout << "Iteration " << t << " | Best Fuel Cost: " << global_best_fuel << endl;
        }

        cout << "\n=== FINAL RESULT ===" << endl;
        cout << "Best Fuel Cost: " << global_best_fuel << endl;
        cout << "Best Path: ";
        for (int city : global_best_path) cout << city << " -> ";
        cout << global_best_path[0] << endl;
    }

    // FIXED: Pheromone update
    void update_pheromones(vector<Ant>& colony) {
        // Evaporation
        for (int i = 0; i < num_nodes; i++)
            for (int j = 0; j < num_nodes; j++)
                pheromones[i][j] *= (1.0 - EVAPORATION);

        // Reinforcement: better paths get more pheromone
        for (auto& ant : colony) {
            if (ant.total_fuel_cost == 0) continue;
            double deposit = Q / ant.total_fuel_cost;
            for (int k = 0; k < (int)ant.path.size() - 1; k++) {
                int i = ant.path[k];
                int j = ant.path[k + 1];
                pheromones[i][j] += deposit;
                pheromones[j][i] += deposit; // symmetric
            }
        }
    }
};

int main() {
    vector<vector<double>> mock_fuel = {
        {0, 10, 15, 20, 25},
        {10, 0, 35, 25, 30},
        {15, 35, 0, 30, 5},
        {20, 25, 30, 0, 15},
        {25, 30, 5, 15, 0}
    };

    BioPathOptimizer engine(5, mock_fuel);
    engine.run();
    return 0;
}

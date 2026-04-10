import numpy as np

class BioPathOptimizerFast:
    def __init__(self, fuel_matrix, num_ants=20, iterations=100, alpha=1.0, beta=2.0, evaporation=0.5):
        self.fuel_matrix = fuel_matrix
        self.num_cities = len(fuel_matrix)
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = alpha  # Importance of pheromones
        self.beta = beta    # Importance of fuel efficiency
        self.evaporation = evaporation
        self.pheromones = np.ones((self.num_cities, self.num_cities))

    def optimize(self, callback=None):
        best_path = None
        best_cost = float('inf')

        for i in range(self.iterations):
            paths = self._gen_all_paths()
            self._update_pheromones(paths)
            
            # Find the best path in this iteration
            for path, cost in paths:
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
            
            if callback:
                callback(i, best_cost)

        return best_path, best_cost

    def _gen_all_paths(self):
        all_paths = []
        for _ in range(self.num_ants):
            path = self._gen_path(0) # Start at city 0
            cost = self._calc_cost(path)
            all_paths.append((path, cost))
        return all_paths

    def _gen_path(self, start):
        path = [start]
        visited = set([start])
        while len(visited) < self.num_cities:
            curr = path[-1]
            probs = self._calc_transition_probs(curr, visited)
            next_city = np.random.choice(range(self.num_cities), p=probs)
            path.append(next_city)
            visited.add(next_city)
        return path

    def _calc_transition_probs(self, curr, visited):
        row = (self.pheromones[curr] ** self.alpha) * \
              ((1.0 / (self.fuel_matrix[curr] + 1e-10)) ** self.beta)
        
        # Don't revisit cities
        mask = np.ones(self.num_cities)
        for v in visited:
            mask[v] = 0
        
        row *= mask
        return row / row.sum()

    def _calc_cost(self, path):
        return sum(self.fuel_matrix[path[i], path[i+1]] for i in range(len(path)-1)) + \
               self.fuel_matrix[path[-1], path[0]]

    def _update_pheromones(self, paths):
        self.pheromones *= (1 - self.evaporation)
        for path, cost in paths:
            for i in range(len(path)-1):
                self.pheromones[path[i], path[i+1]] += 1.0 / cost

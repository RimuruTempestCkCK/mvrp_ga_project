class Solution:
    def __init__(self, route, muatan):
        self.route = route  # List of port IDs
        self.muatan = muatan  # List of delivered volumes
        self.fitness = None

    def evaluate(self, ports, ship, distance_matrix, time_windows, service_time, speed):
        from ga.genetic_algorithm import hitung_fitness
        self.fitness = hitung_fitness(self, ports, distance_matrix, ship, time_windows, service_time, speed)
        id_to_index = {port.id: idx for idx, port in enumerate(ports.values())}
        total_cost = 0
        for i in range(1, len(self.route)):
            from_port = self.route[i - 1]
            to_port = self.route[i]

            # Gunakan mapping ID ke index
            idx_from = id_to_index[from_port]
            idx_to = id_to_index[to_port]

            # Debug bantu jika masih error
            print(f"from_port: {from_port}, to_port: {to_port}, idx_from: {idx_from}, idx_to: {idx_to}")
            print(f"Matrix size: {len(distance_matrix)}x{len(distance_matrix[0])}")

            distance = distance_matrix[idx_from][idx_to]
            total_cost += distance * 100  # biaya per mil laut
            total_cost += ports[idx_to].biaya_sandar
        self.fitness = total_cost
        return self.fitness



    def __repr__(self):
        return f"Solution(Route: {self.route}, Fitness: {self.fitness})"


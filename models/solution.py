class Solution:
    def __init__(self, route, muatan):
        self.route = route  # List of port IDs
        self.muatan = muatan  # List of delivered volumes
        self.fitness = None

    def evaluate(self, ports, ship, distance_matrix, time_windows, service_time, speed):
        id_to_index = {port.id: i for i, port in ports.items()}
        total_cost = 0

        for i in range(len(self.route) - 1):
            from_port = self.route[i]
            to_port = self.route[i+1]
            idx_from = id_to_index[from_port]
            idx_to = id_to_index[to_port]

            jarak = distance_matrix[idx_from][idx_to]
            biaya_per_mil = 50000
            biaya = jarak * biaya_per_mil
            total_cost += biaya

            if to_port != 0:  # Bukan depot
                total_cost += ports[to_port].biaya_sandar

        self.fitness = total_cost


    def get_deliveries(self):
        return {
            pid: vol for pid, vol in zip(self.route, self.muatan)
            if pid != 0  # Asumsikan 0 adalah ID depot
        }

    def __repr__(self):
        return f"Solution(Route: {self.route}, Fitness: {self.fitness})"

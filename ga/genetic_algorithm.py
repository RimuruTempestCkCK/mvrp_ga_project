import random
from models.solution import Solution

# Membuat populasi awal untuk algoritma genetika
# Setiap individu merupakan rute pengiriman dari depot ke semua pelabuhan dan kembali ke depot
def create_initial_population(ports, size):
    population = []
    # Ambil semua ID pelabuhan kecuali depot (diasumsikan ID=0)
    port_ids = [port.id for port in ports.values() if port.id != 0]
    for _ in range(size):
        # Susun rute dengan urutan acak (random) dan awali serta akhiri dengan depot
        route = [0] + random.sample(port_ids, len(port_ids)) + [0]
        # Ambil muatan sesuai demand dari setiap pelabuhan dalam rute
        muatan = [ports[i].demand_kl for i in route]
        population.append(Solution(route, muatan))
    return population

# Mengevaluasi setiap individu dalam populasi berdasarkan fitness
def evaluate_population(population, ports, ship, distance_matrix, time_windows, service_time, speed):
    for solution in population:
        # Evaluasi dilakukan melalui method di kelas Solution
        solution.evaluate(ports, ship, distance_matrix, time_windows, service_time, speed)

# Seleksi individu terbaik dari sejumlah kandidat acak (tournament selection)
def selection(population, k=3):
    selected = random.sample(population, k)
    return min(selected, key=lambda s: s.fitness)

# Operasi crossover (persilangan) antar dua parent untuk menghasilkan child baru
def crossover(parent1, parent2):
    # Jika rute terlalu pendek, salin parent langsung
    if len(parent1.route) < 5:
        return Solution(parent1.route[:], parent1.muatan[:])  # Salin langsung

    # Pilih segmen acak dari parent1
    start = random.randint(1, len(parent1.route) - 3)
    end = random.randint(start + 1, len(parent1.route) - 2)

    # Ambil bagian tengah rute dari parent1
    middle = parent1.route[start:end]

    # Bangun child dengan mempertahankan bagian dari parent1 dan sisanya dari parent2
    remaining = [gene for gene in parent2.route if gene not in middle]
    child_route = remaining[:start] + middle + remaining[start:]

    # Muatan sementara tetap disalin dari parent1 (bisa dikembangkan lebih akurat)
    child_muatan = parent1.muatan[:]

    return Solution(child_route, child_muatan)

# Mutasi rute dengan cara menukar posisi dua pelabuhan secara acak
def mutate(solution, mutation_rate=0.1):
    route = solution.route[1:-1]  # Ambil bagian tengah (tanpa depot)
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]  # Tukar dua posisi
    solution.route = [0] + route + [0]  # Tambahkan depot di awal dan akhir

# Fungsi utama untuk menjalankan algoritma genetika
def run_ga(ports, ship, distance_matrix, time_windows, service_time, speed, pop_size=10, generations=50):
    # 1. Inisialisasi populasi
    population = create_initial_population(ports, pop_size)
    evaluate_population(population, ports, ship, distance_matrix, time_windows, service_time, speed)

    for gen in range(generations):
        new_population = []
        for _ in range(pop_size):
            # 2. Seleksi dua parent terbaik
            p1 = selection(population)
            p2 = selection(population)
            # 3. Crossover untuk membentuk child
            child = crossover(p1, p2)
            # 4. Mutasi child
            mutate(child)
            # 5. Evaluasi child
            child.evaluate(ports, ship, distance_matrix, time_windows, service_time, speed)
            new_population.append(child)
        # 6. Seleksi elitisme: ambil individu terbaik dari gabungan populasi lama + baru
        population = sorted(new_population + population, key=lambda s: s.fitness)[:pop_size]

    # Kembalikan solusi terbaik dari populasi terakhir
    return min(population, key=lambda s: s.fitness)

# Fungsi untuk menghitung nilai fitness (biaya total) dari sebuah solusi/rute
def hitung_fitness(solution, ports, distance_matrix, ship, time_windows, service_time, speed):
    route = solution.route
    total_biaya = 0
    total_waktu = 0
    penalty_waktu = 0
    penalti_per_jam_terlambat = 10000  # Penalti jika waktu kedatangan melebihi batas

    for i in range(len(route) - 1):
        current_port = route[i]
        next_port = route[i+1]
        jarak = distance_matrix[current_port][next_port]
        waktu_tempuh = jarak / speed  # Hitung waktu tempuh

        total_waktu += waktu_tempuh

        # Periksa apakah waktu kedatangan sesuai dengan time window
        earliest, latest = time_windows.get(next_port, (0, float('inf')))
        if total_waktu < earliest:
            total_waktu = earliest  # Menunggu hingga pelabuhan buka
        elif total_waktu > latest:
            penalty_waktu += penalti_per_jam_terlambat * (total_waktu - latest)  # Tambah penalti

        total_waktu += service_time.get(next_port, 0)  # Tambah waktu pelayanan
        tarif_per_mil = 50000
        total_biaya += jarak * tarif_per_mil  # Biaya perjalanan

    total_biaya += penalty_waktu  # Tambah penalti ke biaya total
    return total_biaya

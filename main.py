from models.ship import Ship
from utils import load_ports, generate_distance_matrix
from ga.genetic_algorithm import run_ga
import csv
import matplotlib.pyplot as plt

def simpan_solusi(solution, ports, path="hasil_solusi.csv"):
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["No", "Nama Pelabuhan", "ID", "Muatan (KL)"])
        for i, pid in enumerate(solution.route):
            nama = ports[pid].nama
            muat = solution.muatan[i] if i < len(solution.muatan) else "-"
            writer.writerow([i+1, nama, pid, muat])
        writer.writerow([])
        writer.writerow(["Total Biaya", solution.fitness])

def plot_rute(ports, solution, ship=None):
    latitudes = [ports[pid].latitude for pid in solution.route]
    longitudes = [ports[pid].longitude for pid in solution.route]
    names = [ports[pid].nama for pid in solution.route]

    plt.figure(figsize=(12, 6))
    plt.plot(longitudes, latitudes, marker='o', linestyle='-', color='blue')

    # Beri label nama pelabuhan dengan nomor urut
    for i, name in enumerate(names):
        plt.text(longitudes[i], latitudes[i], f"{i+1}. {name}", fontsize=8)

    plt.title("Rute Pengangkutan BBM (Optimasi MVRP)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    # Tambahkan keterangan info di bawah plot (atau bisa di atas, sesuai selera)
    keterangan = f"Total Biaya: Rp {solution.fitness:,.2f}"
    if ship is not None:
        keterangan += f" | Kapasitas Kapal: {ship.kapasitas_kl} KL"
    # Tempatkan text keterangan di bawah plot
    plt.figtext(0.1, 0.02, keterangan, fontsize=10, ha="left", va="bottom")

    plt.tight_layout(rect=[0, 0.03, 1, 1])  # beri ruang bawah untuk figtext
    plt.show()


def main():
    ports = load_ports("data/pelabuhan.csv")
    distance_matrix = generate_distance_matrix("data/jarak.csv") 
    ship = Ship("Kapal A", "General Purpose", kapasitas_kl=30000)

    # Buat dictionary time_windows dan service_time dari data pelabuhan
    time_windows = {}
    service_time = {}
    for pid, port in ports.items():
        earliest = 0
        latest = port.batas_waktu_hari * 24  # hari ke jam
        time_windows[pid] = (earliest, latest)
        service_time[pid] = port.waktu_layanan_jam

    # Tambahkan parameter baru pada run_ga: time_windows, service_time, speed
    best_solution = run_ga(
        ports, ship, distance_matrix, 
        time_windows=time_windows, 
        service_time=service_time, 
        speed=12
    )

    print("\n=== HASIL OPTIMAL ===")
    print(f"Rute terbaik (ID): {best_solution.route}")
    print("Rute terbaik (Nama Pelabuhan):")
    for pid in best_solution.route:
        print(f"- {ports[pid].nama}")

    print(f"\nFitness (Total Biaya): Rp {best_solution.fitness:,.2f}")
    print(f"Muatan: {best_solution.muatan}")

    simpan_solusi(best_solution, ports)
    plot_rute(ports, best_solution, ship)  # tambahkan ship agar keterangan kapasitas muncul
    print("\n✅ Hasil disimpan ke: hasil_solusi.csv")



if __name__ == "__main__":
    main()

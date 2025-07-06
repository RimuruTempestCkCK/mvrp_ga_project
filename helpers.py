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

    for i, name in enumerate(names):
        plt.text(longitudes[i], latitudes[i], f"{i+1}. {name}", fontsize=8)

    plt.title("Rute Pengangkutan BBM (Optimasi MVRP)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    keterangan = f"Total Biaya: Rp {solution.fitness:,.2f}"
    if ship:
        keterangan += f" | Kapasitas Kapal: {ship.kapasitas_kl} KL"
    plt.figtext(0.1, 0.02, keterangan, fontsize=10, ha="left", va="bottom")
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.show()

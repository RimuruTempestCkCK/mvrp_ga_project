from models.ship import Ship
from utils import load_ports, generate_distance_matrix
from models.inventory import InventoryManager
from ga.scheduler import run_ga_for_day
from ga.genetic_algorithm import run_ga
from helpers import simpan_solusi, plot_rute  # (bisa kamu pisah nanti)
import csv
import matplotlib.pyplot as plt
from utils import simpan_stok_harian_csv

def simulasi_harian():
    ports_dict = load_ports("data/pelabuhan.csv")
    pelabuhan_list = list(ports_dict.values())
    ship = Ship("Kapal A", "General Purpose", kapasitas_kl=30000)
    inventory_mgr = InventoryManager(pelabuhan_list, total_hari=30)

    log_jadwal = []

    for hari in range(1, 31):
        print(f"\n=== Hari ke-{hari} ===")
        solusi = run_ga_for_day(hari, pelabuhan_list, ship, inventory_mgr)

        if solusi:
            deliveries = solusi.get_deliveries()
            inventory_mgr.update(hari, deliveries)

            print(f"Kapal mengirim ke: {list(deliveries.keys())}")
            log_jadwal.append({
                'hari': hari,
                'rute': ' -> '.join(str(r) for r in solusi.route),
                'muatan': ', '.join(map(str, solusi.muatan)),
                'fitness': solusi.fitness
            })
        else:
            inventory_mgr.update(hari, {})
            print("Tidak ada pengiriman")

    # Simpan CSV
    with open("jadwal_pengiriman.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["hari", "rute", "muatan", "fitness"])
        writer.writeheader()
        writer.writerows(log_jadwal)

    print("\n✅ Simulasi selesai. Jadwal tersimpan di jadwal_pengiriman.csv")
    plot_stok_history(inventory_mgr)

    # Simpan stok harian ke CSV
    simpan_stok_harian_csv(inventory_mgr, "stok_harian.csv")
    return inventory_mgr

    


def plot_stok_history(inventory_mgr):
    for pid, history in inventory_mgr.history.items():
        if len(history) > 1:
            hari = list(range(len(history)))
            plt.plot(hari, history, label=f'Pelabuhan {pid}')

    # Tambahkan garis batas stok minimum (dead_stock) dan maksimum (maks_stok)
    for port in inventory_mgr.pelabuhan_map.values():
        plt.axhline(port.dead_stock, linestyle='--', color='red', linewidth=0.5, alpha=0.5)
        plt.axhline(port.maks_stok, linestyle='--', color='green', linewidth=0.5, alpha=0.5)

    plt.xlabel('Hari ke-')
    plt.ylabel('Stok (KL)')
    plt.title('Perubahan Stok Harian Setiap Pelabuhan')
    plt.legend(loc='upper right', fontsize='small', bbox_to_anchor=(1.1, 1.0))
    plt.tight_layout()
    plt.grid(True)
    plt.show()



def run_sekali():
    ports = load_ports("data/pelabuhan.csv")
    distance_matrix = generate_distance_matrix("data/jarak.csv")
    ship = Ship("Kapal A", "General Purpose", kapasitas_kl=30000)

    # Time window & service time
    time_windows = {}
    service_time = {}
    for pid, port in ports.items():
        time_windows[pid] = (0, port.batas_waktu_hari * 24)
        service_time[pid] = port.waktu_layanan_jam

    best_solution = run_ga(
        ports, ship, distance_matrix,
        time_windows=time_windows,
        service_time=service_time,
        speed=12
    )

    print("\n=== HASIL OPTIMAL ===")
    print(f"Rute terbaik (ID): {best_solution.route}")
    print(f"Muatan: {best_solution.muatan}")
    print(f"Fitness (Rp): {best_solution.fitness:,.2f}")

    simpan_solusi(best_solution, ports)
    plot_rute(ports, best_solution, ship)


if __name__ == "__main__":
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Simulasi Harian (30 Hari)")
        print("2. Satu Kali Optimasi")
        print("3. Keluar")
        pilihan = input("Pilih mode [1/2/3]: ").strip()

        if pilihan == "1":
            inventory_mgr = simulasi_harian()
            # plot_stok_history(inventory_mgr) ← sudah dipanggil di dalam simulasi_harian()

        elif pilihan == "2":
            run_sekali()

        elif pilihan == "3":
            konfirmasi = input("Yakin ingin keluar? [y/n]: ").strip().lower()
            if konfirmasi == "y":
                print("👋 Program selesai. Sampai jumpa!")
                break
            else:
                continue

        else:
            print("⚠️ Pilihan tidak valid. Silakan coba lagi.")

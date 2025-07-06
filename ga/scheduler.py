from ga.genetic_algorithm import optimize
from utils import generate_distance_matrix

def run_ga_for_day(hari, semua_pelabuhan, kapal, inventory_mgr):
    distance_matrix = generate_distance_matrix("data/jarak.csv")

    # Gunakan pelabuhan yang butuh pengisian (berdasarkan stok)
    pelabuhan_kritis = [
        p for p in semua_pelabuhan
        if inventory_mgr.get_stok(p.id, hari) < p.dead_stock + 5000  # ambang batas
    ]

    # Jika tidak ada yang kritis, ambil semua
    if not pelabuhan_kritis:
        pelabuhan_kritis = semua_pelabuhan[1:]  # skip depot

    return optimize(pelabuhan_kritis, kapal, distance_matrix, inventory_mgr, hari)

import csv
import math
from models.port import Port

def load_ports(filepath):
    ports = {}
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pid = int(row['id'])
            ports[pid] = Port(
                id=pid,
                nama=row['nama'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                demand_kl=float(row['demand_kl']),
                waktu_layanan_jam=float(row['waktu_layanan_jam']),
                batas_waktu_hari=float(row['batas_waktu_hari']),
                biaya_sandar=int(row['biaya_sandar']),
                charter_rate=int(row['charter_rate']),
                stok_awal=float(row.get('stok_awal', 0)),
                maks_stok=float(row.get('maks_stok', 100000)),  # default jika tidak ada
                dead_stock=float(row.get('dead_stock', 5000))   # default jika tidak ada
            )
    return ports



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius bumi dalam km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c * 0.539957  # km to nautical miles


def generate_distance_matrix(filename):
    matrix = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matrix.append([float(x.replace(",", ".")) for x in row])
    return matrix

def get_kebutuhan_pengiriman(port, stok_sekarang):
    """
    Hitung kebutuhan isi ulang pelabuhan berdasarkan stok sekarang.
    """
    kebutuhan = port.maks_stok - stok_sekarang
    return max(0, kebutuhan)

def simpan_stok_harian_csv(inventory_mgr, filename="stok_harian.csv"):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        pelabuhan_ids = list(inventory_mgr.history.keys())
        header = ["Hari"] + [inventory_mgr.pelabuhan_map[pid].nama for pid in pelabuhan_ids]
        writer.writerow(header)

        for h in range(inventory_mgr.total_hari + 1):
            row = [h]
            for pid in pelabuhan_ids:
                row.append(inventory_mgr.get_stok(pid, h))
            writer.writerow(row)

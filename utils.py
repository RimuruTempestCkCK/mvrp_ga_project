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
                charter_rate=int(row['charter_rate'])
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



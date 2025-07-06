# models/port.py

class Port:
    def __init__(self, id, nama, latitude, longitude, demand_kl, waktu_layanan_jam, batas_waktu_hari,
                 biaya_sandar, charter_rate, stok_awal, maks_stok, dead_stock):
        self.id = id
        self.nama = nama
        self.latitude = latitude
        self.longitude = longitude
        self.demand_kl = demand_kl
        self.demand_harian = demand_kl / 30  # anggap 30 hari
        self.waktu_layanan_jam = waktu_layanan_jam
        self.batas_waktu_hari = batas_waktu_hari
        self.biaya_sandar = biaya_sandar
        self.charter_rate = charter_rate

        # Untuk manajemen inventory
        self.stok_awal = stok_awal
        self.maks_stok = maks_stok
        self.dead_stock = dead_stock

    def __repr__(self):
        return f"Port({self.id}, {self.nama}, Demand: {self.demand_harian:.2f} KL/hari)"

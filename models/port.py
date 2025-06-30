# Kelas Port merepresentasikan informasi dari sebuah pelabuhan
class Port:
    def __init__(self, id, nama, latitude, longitude, demand_kl, waktu_layanan_jam, batas_waktu_hari, biaya_sandar, charter_rate):
        self.id = id
        self.nama = nama
        self.latitude = latitude
        self.longitude = longitude
        self.demand_kl = demand_kl
        self.waktu_layanan_jam = waktu_layanan_jam
        self.batas_waktu_hari = batas_waktu_hari
        self.biaya_sandar = biaya_sandar
        self.charter_rate = charter_rate

    # Fungsi representasi objek saat dicetak/log untuk debug
    def __repr__(self):
        return f"Port({self.id}, {self.nama}, Demand: {self.demand_kl} KL)"

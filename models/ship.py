# Kelas Ship merepresentasikan kapal yang digunakan dalam proses distribusi BBM
class Ship:
    def __init__(self, id, tipe, kapasitas_kl, kecepatan_knot=12):
        self.id = id
        self.tipe = tipe
        self.kapasitas_kl = kapasitas_kl
        self.kecepatan_knot = kecepatan_knot
        self.route = []
        self.muatan = []

    # Fungsi representasi teks dari objek Ship, berguna saat debugging
    def __repr__(self):
        return f"Ship({self.id}, {self.tipe}, Kapasitas: {self.kapasitas_kl} KL)"

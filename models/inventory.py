# models/inventory.py

class InventoryManager:
    def __init__(self, pelabuhan_list, total_hari=30):
        self.pelabuhan_map = {p.id: p for p in pelabuhan_list}
        self.total_hari = total_hari
        self.history = {p.id: [p.stok_awal] for p in pelabuhan_list if p.id != 0}

    def update(self, hari, deliveries):
        for pid, pelabuhan in self.pelabuhan_map.items():
            if pid == 0:  # Skip depot
                continue

            stok_kemarin = self.history[pid][-1]
            stok_baru = stok_kemarin - pelabuhan.demand_harian

            if pid in deliveries:
                stok_baru += deliveries[pid]

            # Clamp stok
            stok_baru = max(0, min(stok_baru, pelabuhan.maks_stok))
            self.history[pid].append(stok_baru)

    def get_stok(self, pid, hari):
        history = self.history.get(pid, [])
        if hari < len(history):
            return history[hari]
        elif history:
            return history[-1]  # kembalikan stok terakhir yang tersedia
        else:
            return 0


    def get_pelabuhan_kritis(self, threshold_hari=2):
        kritis = []
        for pid, stok_list in self.history.items():
            pelabuhan = self.pelabuhan_map[pid]
            prediksi_stok = stok_list[-1] - pelabuhan.demand_harian * threshold_hari
            if prediksi_stok <= pelabuhan.dead_stock:
                kritis.append(pelabuhan)
        return kritis

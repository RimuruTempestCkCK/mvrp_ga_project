# ⛴️ Maritime Vehicle Routing Problem (MVRP) Optimization using Genetic Algorithm & Inventory Management

Proyek ini menyelesaikan permasalahan **Maritime Vehicle Routing Problem (MVRP)** dalam pendistribusian **bahan bakar minyak (BBM)** ke sejumlah pelabuhan menggunakan pendekatan **Algoritma Genetika (GA)**. Sistem juga mempertimbangkan **stok BBM harian (inventory)** untuk menentukan **jadwal pengiriman** selama periode waktu tertentu.

---

## 🎯 Tujuan

Mengoptimalkan rute dan waktu pengiriman BBM dengan mempertimbangkan:

- Kapasitas kapal
- Demand harian pelabuhan
- Waktu layanan & batas waktu layanan
- Stok awal, stok maksimal, dan stok minimum (dead stock)
- Biaya operasional (biaya sandar + charter rate kapal)

---

## 🔁 Konsep & Pemisahan Proses

### 1. **Genetic Algorithm (GA)**  
Digunakan untuk mengoptimalkan rute pengiriman **pada hari tertentu saja**. GA tidak bertanggung jawab terhadap penjadwalan jangka panjang.

### 2. **Inventory Manager**  
Mengelola stok BBM setiap pelabuhan. Untuk setiap hari, stok dihitung berdasarkan:

- Konsumsi harian (`demand_harian`)
- Tambahan stok dari pengiriman
- Batasan stok (`maks_stok` dan `dead_stock`)

### 3. **Penjadwalan**
GA hanya akan dijalankan jika ada pelabuhan yang memasuki **kondisi kritis** (stok < `dead_stock + buffer`). Penjadwalan ini dilakukan di luar proses GA sebagai **variabel keputusan**.

---

## 🧬 Representasi Kromosom

Kromosom dalam GA merepresentasikan **urutan pelabuhan yang dikunjungi kapal**. Contoh:

[1, 3, 5, 7]

Artinya: Kapal akan mengunjungi pelabuhan 1 → 3 → 5 → 7.  
Evaluasi kromosom mempertimbangkan:

- Total jarak tempuh
- Batas waktu layanan
- Durasi layanan
- Biaya sandar dan charter rate
- Kapasitas kapal

---

## 🛠️ Fitur

- ✅ Simulasi pengiriman selama **30 hari**
- ✅ Penjadwalan berdasarkan kondisi stok harian
- ✅ Penggunaan Algoritma Genetika untuk rute optimal
- ✅ Output ke file `.csv`
- ✅ Visualisasi stok BBM per pelabuhan

---

## 🧩 Struktur Folder
<pre> ```
mvrp_ga_project/
│
├── data/
│ ├── pelabuhan.csv # Data pelabuhan: lokasi, demand, biaya, stok
│ └── jarak.csv # Matriks jarak antar pelabuhan
│
├── models/
│ ├── port.py # Kelas pelabuhan
│ ├── ship.py # Kelas kapal
│ ├── inventory.py # Perhitungan stok harian
│ └── solution.py # Representasi solusi GA
│
├── ga/
│ ├── genetic_algorithm.py # Implementasi Algoritma Genetika
│ └── scheduler.py # Menjalankan GA per hari jika perlu
│
├── utils.py # Fungsi bantu: load data, jarak, simpan
├── helpers.py # Fungsi visualisasi dan penyimpanan hasil
├── main.py # Entry point program (menu interaktif)
│
├── jadwal_pengiriman.csv # Output rute harian dari simulasi
├── stok_harian.csv # Output stok BBM seluruh pelabuhan
``` </pre>


---

## ▶️ Cara Menjalankan Program

### 1. Clone repositori

git clone https://github.com/RimuruTempestCkCK/mvrp_ga_project.git
cd mvrp_ga_project

### 2. Install library Python

pip install matplotlib

### 3. Jalankan program

python main.py

### 4. 🖥️ Menu Program

=== MENU UTAMA ===
1. Simulasi Harian (30 Hari)
2. Satu Kali Optimasi
3. Keluar

Pilih 1 → sistem akan menjalankan simulasi selama 30 hari dan mencatat jadwal pengiriman serta stok harian.

Pilih 2 → menjalankan satu kali optimasi GA untuk rute terbaik saat ini (tanpa memperhitungkan stok).

Pilih 3 → keluar dari program.

📈 Output
📄 File CSV:
jadwal_pengiriman.csv: Jadwal dan rute pengiriman tiap hari

stok_harian.csv: Stok BBM semua pelabuhan per hari

📊 Grafik:
Grafik stok BBM harian setiap pelabuhan

Garis merah → batas stok minimum (dead stock)

Garis hijau → batas stok maksimum


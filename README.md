# 🛒 E-Commerce Public Dataset Dashboard

Dashboard interaktif hasil analisis **E-Commerce Public Dataset** periode **Januari 2017 – Agustus 2018**. Proyek ini dibuat untuk memenuhi submission kelas **Belajar Analisis Data dengan Python** di Dicoding Indonesia.

---

## 🔗 Live Dashboard

Dashboard dapat diakses secara online di:

**https://ariani-ecommerce-dashboard.streamlit.app/**

---

## 📊 Fitur Dashboard

Dashboard menampilkan tiga analisis utama:

1. **📦 Kategori Produk** — Top 10 kategori berdasarkan total revenue, dengan persentase kontribusi terhadap total pendapatan.
2. **🚚 Waktu Pengiriman** — Rata-rata waktu pengiriman per negara bagian (27 state), dengan penanda rata-rata nasional.
3. **👥 Segmentasi RFM** — Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary menggunakan kuantil dan aturan bisnis.

Dashboard dilengkapi **filter interaktif** di sidebar:
- Filter negara bagian (`customer_state`) — multi-select.
- Filter kategori produk (`product_category_name_english`) — multi-select.

---

## 🚀 Menjalankan Secara Lokal

### Prasyarat

- Python 3.9 atau lebih baru
- pip

### Langkah-langkah

1. **Clone repository ini:**

   ```bash
   git clone https://github.com/arianisepti/ecommerce-dashboard-dicoding.git
   cd ecommerce-dashboard-dicoding

2. **(Opsional) Buat virtual environment:**

    python -m venv venv

    # Windows
    venv\Scripts\activate

    # Mac/Linux
    source venv/bin/activate

3. **Install dependensi:**

    pip install -r requirements.txt
    Jalankan dashboard:

    
    streamlit run dashboard/dashboard.py
    Buka browser di http://localhost:8501.


📁 Struktur Proyek

```text
submission/
├── dashboard/
│   ├── main_data.csv       # Dataset bersih hasil cleaning
│   └── dashboard.py        # Aplikasi Streamlit
├── data/                   # Dataset mentah (9 CSV)
├── notebook.ipynb          # Notebook analisis lengkap
├── README.md               # Dokumentasi proyek (file ini)
├── requirements.txt        # Dependensi Python
└── url.txt                 # Tautan dashboard live
```


### 🔍 Metodologi Analisis
Analisis dilakukan di `notebook.ipynb` melalui tahapan berikut:

1. **Gathering Data** — Memuat 9 dataset CSV ke DataFrame.
2. **Assessing Data** — Mengidentifikasi *missing value*, *duplicate*, kesalahan tipe data, nilai tidak valid, dan *outlier*.
3. **Cleaning Data** — Menangani permasalahan data, lalu menggabungkan dataset menjadi `main_data.csv`.
4. **Exploratory Data Analysis (EDA)** — Menjawab 3 pertanyaan bisnis (SMART).
5. **Visualization & Explanatory Analysis** — Visualisasi untuk setiap pertanyaan bisnis.
6. **Conclusion & Recommendation** — Kesimpulan dan 3 *action item*.

**Analisis Lanjutan: RFM Analysis**
Segmentasi pelanggan menggunakan RFM Analysis dengan pendekatan:
* Skoring kuantil (1–5) untuk *Recency*, *Frequency*, dan *Monetary*.
* *Manual grouping* berbasis aturan bisnis untuk menentukan segmen: **Champions**, **Loyal Customers**, **New Customers**, **Potential Loyalist**, **At Risk**, dan **Hibernating**.
* Tanpa algoritma *machine learning*, sesuai panduan proyek.


---

## 📝 Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan *revenue* tertinggi dan terendah selama Januari 2017 – Agustus 2018, dan bagaimana kontribusinya terhadap total *revenue*?
2. Berapa rata-rata waktu pengiriman per negara bagian, dan *state* mana yang memiliki rata-rata waktu pengiriman terlama?
3. Bagaimana segmentasi pelanggan berdasarkan RFM, dan segmen mana yang perlu diprioritaskan untuk retensi?


## 💡 Kesimpulan Singkat
* **Kategori Produk:** *Revenue* sangat terkonsentrasi — hanya 16 dari 71 kategori menyumbang ~79% *revenue*. Tiga teratas: `health_beauty`, `watches_gifts`, `bed_bath_table`.
* **Waktu Pengiriman:** Rata-rata nasional 12,46 hari. *State* dengan pengiriman terlama: **RR, AP, AM** (>26 hari). **RJ** menjadi prioritas perbaikan (volume besar + pengiriman lambat).
* **Segmentasi RFM:** **Potential Loyalist** (31,20% pelanggan) dan **At Risk** (23,86% pelanggan) adalah segmen terbesar. **Champions** (6,96% pelanggan) menyumbang 14,65% *revenue* dengan rata-rata *monetary* tertinggi.


## 🛠️ Teknologi yang Digunakan
* **Python 3** — Bahasa pemrograman utama
* **pandas** — Pengolahan dan analisis data
* **matplotlib & seaborn** — Visualisasi data
* **Streamlit** — Framework *dashboard* interaktif
* **Jupyter Notebook** — Analisis eksploratif


## 👤 Author
**Ariani Dwi Septi**  
Dicoding Indonesia — Belajar Analisis Data dengan Python


## 📄 Lisensi
Proyek ini dibuat untuk keperluan *submission* Dicoding Indonesia. Dataset bersumber dari *E-Commerce Public Dataset* oleh Olist.

# 📺 Trafix YouTube View Bot via CroxyProxy

Skrip otomatisasi Python untuk meningkatkan tampilan video YouTube dengan menggunakan **Playwright** dan proxy dari **CroxyProxy**. Proses dijalankan dalam mode multi-threading dan menampilkan status real-time setiap thread di terminal dengan bantuan library **Rich**.

---

## 🧩 Fitur

- 🔄 Multi-threading: Menjalankan beberapa instance secara paralel.
- 🌍 Menggunakan proxy CroxyProxy secara dinamis.
- 🎥 Memutar video YouTube secara otomatis.
- 🕒 Durasi menonton bisa dikustomisasi (dalam menit).
- 📊 Tampilan terminal real-time yang rapi dengan status setiap thread.

---

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/trafix-croxyproxy-bot.git
cd trafix-croxyproxy-bot
```

### 2. Buat Virtual Environment (opsional tapi direkomendasikan)

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Install Semua Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Browser untuk Playwright

```bash
playwright install
```

---

## 🚀 Cara Menjalankan

```bash
python views.py <youtube_url> --durasi=<menit> --threads=<jumlah_thread>
```

### ✅ Contoh:

```bash
python views.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --durasi=2 --threads=5
```

> Artinya: Menjalankan 5 thread yang masing-masing akan menonton video selama 2 menit melalui CroxyProxy.

---

## 🔧 Argumen

| Argumen         | Tipe   | Default | Deskripsi                                       |
|-----------------|--------|---------|-------------------------------------------------|
| `<youtube_url>` | str    | wajib   | URL video YouTube yang ingin ditonton           |
| `--durasi`      | int    | 0       | Durasi menonton video dalam **menit**           |
| `--threads`     | int    | 0       | Jumlah thread (session paralel) yang dijalankan |

Jika `--durasi` dan `--threads` tidak diisi, maka akan menggunakan default: 30 detik dan 5 thread.

---

## 📋 Output Terminal

Setiap thread akan menampilkan:

- Status saat ini: inisialisasi, mengisi CroxyProxy, mendapatkan IP, memutar video, dll.
- Proxy yang digunakan: apakah menggunakan IP publik atau domain proxy Croxy.
- Hitung mundur durasi menonton per thread, ditampilkan secara real-time.

Contoh tampilan:
```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Thread   ┃ Status                     ┃ Proxy            ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Thread 1 │ [Play] 59s                 │ 159.223.45.12    │
│ Thread 2 │ [Wait] IP publik...        │ ⏳ Mendeteksi...  │
│ Thread 3 │ [Form] CroxyProxy          │ ⏳ Mendeteksi...  │
│ Thread 4 │ [Done] Selesai nonton      │ 146.190.123.87   │
│ Thread 5 │ [Play] 58s                 │ 146.190.123.87   │
└──────────┴────────────────────────────┴──────────────────┘
```

---

## 🛠 Tips Tambahan

- 💡 Gunakan proxy eksternal atau VPN tambahan untuk meningkatkan variasi IP.
- ⌛ Durasi terlalu pendek bisa tidak terhitung sebagai view oleh YouTube.
- 🚫 Jangan gunakan akun Google login di Playwright, skrip ini berjalan anonim.

---

## 📥 Requirements

Daftar dependensi ada di `requirements.txt`, terdiri dari:

```txt
playwright>=1.44.0
rich>=13.7.0
```

---

## ⚠️ Disclaimer

> Script ini hanya ditujukan untuk **tujuan edukasi dan eksperimen**.  
> Segala bentuk penyalahgunaan menjadi tanggung jawab masing-masing pengguna.  
> Menyalahgunakan trafik bot bisa melanggar ketentuan layanan YouTube.

---

## 🤝 Kontribusi

Pull request dan saran sangat diterima!  
Silakan fork, perbaiki, dan ajukan PR.

---

## ❤️ Donasi

https://saweria.co/RizkiAlamR

# 📊 Stats Lapas Lubuk Pakam

Aplikasi web statis untuk memantau data **Jumlah Narapidana Menurut Jenis Kelamin** di Lembaga Pemasyarakatan (Lapas) Lubuk Pakam secara berkala.

## 🚀 Fitur Utama
- **Automated Data Fetching**: Menggunakan GitHub Actions untuk mengambil data terbaru dari Web API BPS Deli Serdang tanpa mengekspos API Key.
- **Interactive Visualization**: Grafik tren tahun ke tahun menggunakan Chart.js.
- **Lightweight & Fast**: Dibangun dengan HTML5, Tailwind CSS, dan Vanilla JS (tanpa framework berat).
- **Secure**: Implementasi rahasia API menggunakan GitHub Secrets.

## 🛠️ Teknologi yang Digunakan
- **Frontend**: Tailwind CSS & Chart.js
- **Automation**: Python (Data Scraping) & GitHub Actions
- **Data Source**: Web API BPS (Badan Pusat Statistik)
- **Deployment**: GitHub Pages

## 🛡️ Keamanan (Security)
Projek ini menggunakan metode *Server-side Fetching* melalui GitHub Actions. API Key BPS disimpan dengan aman di **GitHub Secrets**, sehingga tidak terlihat oleh publik di kode frontend. Data dikonversi menjadi file `data.json` secara otomatis setiap hari.

---
*Dibuat untuk tujuan transparansi data publik dan pengembangan portofolio sistem informasi.*
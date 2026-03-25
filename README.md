# Zerg App BOT

> Bot otomatis untuk menjalankan daily spin dan mengelola banyak akun

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Deskripsi

Zerg App BOT adalah tools otomatis yang digunakan untuk menjalankan fitur daily spin pada banyak akun secara bersamaan. Bot ini juga dilengkapi dengan dukungan proxy yang fleksibel untuk meningkatkan keamanan dan kestabilan penggunaan.

**🔗 Mulai di sini:** [Daftar Zerg App](https://welcome.zerg.app/referral/F9LWA40W3B)

> **Catatan:** Gunakan wallet Solana baru saat registrasi dan hubungkan akun sosial Anda.

## ✨ Fitur

- 🔄 **Manajemen Akun Otomatis** – Mengambil dan mengelola akun secara otomatis  
- 🌐 **Dukungan Proxy** – Bisa dijalankan dengan atau tanpa proxy  
- 🔀 **Rotasi Proxy Otomatis** – Mengganti proxy yang tidak valid  
- 🎡 **Daily Spin Otomatis** – Menjalankan spin harian secara otomatis  
- 👥 **Multi-Akun** – Mendukung banyak akun sekaligus  

## 📋 Persyaratan

- **Python:** 3.9 atau lebih baru  
- **pip:** Disarankan versi terbaru  

## 🛠 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/DropsterMind/Zerg-BOT.git
cd Zerg-BOT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
# atau
pip3 install -r requirements.txt
```

### 3. Manajemen Versi Library

> ⚠️ Pastikan versi library sesuai dengan `requirements.txt`

Cek versi:
```bash
pip show nama_library
```

Hapus library:
```bash
pip uninstall nama_library
```

Install versi tertentu:
```bash
pip install nama_library==versi
```

## ⚙️ Konfigurasi

### Setup Akun

Edit atau buat file `accounts.txt`:

```
private_key_solana_1
private_key_solana_2
private_key_solana_3
```

### Proxy (Opsional)

Edit atau buat file `proxy.txt`:

```
# Format default (HTTP)
192.168.1.1:8080

# Dengan protokol
http://192.168.1.1:8080
https://192.168.1.1:8080

# Dengan autentikasi
http://username:password@192.168.1.1:8080
```

## 🚀 Menjalankan Bot

```bash
python bot.py
# atau
python3 bot.py
```

### Opsi Saat Menjalankan

- **Mode Proxy:**
  - `1` → Gunakan proxy  
  - `2` → Tanpa proxy  

- **Rotasi Proxy:**
  - `y` → Aktif  
  - `n` → Nonaktif  

## 🤝 Kontribusi

Kontribusi sangat terbuka:

- ⭐ Beri star pada repo ini  
- 👥 Follow untuk update  
- 🐛 Laporkan bug di Issues  
- 💡 Ajukan fitur baru  
- 🔧 Kirim pull request  

## 📞 Kontak

- **Developer:** DropsterMind  

---

<div align="center">

**Dibuat dengan ❤️ oleh DropsterMind**

*Terima kasih sudah menggunakan Zerg App BOT! Jangan lupa ⭐ repository ini.*

</div>

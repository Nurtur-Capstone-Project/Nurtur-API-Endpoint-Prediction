Deskripsi Singkat
-----------------
API Flask sederhana untuk melakukan prediksi emosi dari sebuah gambar menggunakan model Keras yang sudah dilatih (ResNet50V2). Aplikasi ini memuat model saat startup sehingga setiap request hanya melakukan preprocessing dan inferensi.

Setup & Instalasi
-----------------
1. Buat virtual environment dan aktifkan:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instal dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Tempatkan file model `ResNet50V2_Model.h5` di root proyek ini. Jika ingin meletakkannya di lokasi lain, set environment variable `MODEL_PATH` sebelum menjalankan server, contohnya:

```bash
export MODEL_PATH=/path/to/ResNet50V2_Model.h5
```

Cara Menjalankan Server
-----------------------
Jalankan aplikasi Flask:

```bash
python app.py
```

Server akan berjalan di `http://0.0.0.0:5000` secara default.

Dokumentasi Endpoint
--------------------
Endpoint utama:

- Endpoint: `/predict`
- Method: `POST`
- Body: `multipart/form-data` dengan key `file` (juga menerima key `image` untuk kompatibilitas)

Preprocessing yang dilakukan server:

- Ubah gambar menjadi RGB
- Resize ke 224x224 piksel
- Normalisasi dengan membagi nilai piksel dengan 255.0
- Tambahkan dimensi batch sebelum dikirim ke model

Respons sukses (JSON):

```json
{
	"emotion": "Happy",
	"confidence": 0.9821
}
```

Penanganan Error:

- 400 Bad Request: jika tidak ada file yang diunggah atau file bukan gambar valid.
- 500 Internal Server Error: jika terjadi kegagalan saat prediksi.

Contoh Penggunaan (curl)
------------------------
Contoh curl untuk mengirim gambar:

```bash
curl -X POST \
	-F "file=@/path/to/image.jpg" \
	http://localhost:5000/predict
```

Jika server berjalan di mesin lain atau port berbeda, sesuaikan URL.

Informasi Tambahan
------------------
- Default path model: `ResNet50V2_Model.h5` di root proyek atau gunakan env `MODEL_PATH`.
- Untuk deployment production, jalankan dengan WSGI server (mis. gunicorn):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

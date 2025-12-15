# Nurtur API Endpoint Prediction

## Deskripsi
Proyek ini adalah API sederhana berbasis Flask untuk melakukan prediksi emosi dari gambar menggunakan model Keras yang telah dilatih (ResNet50V2). Model dimuat saat startup untuk efisiensi, sehingga setiap permintaan prediksi hanya memproses gambar tanpa memuat ulang model.

Model dapat mendeteksi 7 emosi: Angry, Disgust, Fear, Happy, Neutral, Sad, dan Surprise.

## Instalasi
1. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Untuk Linux/Mac
   .venv\Scripts\activate     # Untuk Windows
   ```

2. Instal dependensi:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Letakkan file model `ResNet50V2_Model.h5` di root direktori proyek. Jika ingin di lokasi lain, atur variabel lingkungan `MODEL_PATH`:
   ```bash
   export MODEL_PATH=/path/to/ResNet50V2_Model.h5  # Linux/Mac
   set MODEL_PATH=C:\path\to\ResNet50V2_Model.h5    # Windows
   ```

## Menjalankan Server
Jalankan aplikasi Flask:
```bash
python app.py
```

Server akan berjalan di `http://0.0.0.0:5000` secara default.

Untuk produksi, gunakan WSGI server seperti Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Dokumentasi API
### Endpoint Prediksi
- **URL**: `/predict`
- **Method**: `POST`
- **Body**: `multipart/form-data` dengan kunci `file` atau `image` (berisi file gambar).

### Preprocessing Gambar
- Konversi ke RGB.
- Resize ke 224x224 piksel.
- Normalisasi piksel dengan membagi 255.0.
- Tambahkan dimensi batch.

### Response Sukses (JSON)
```json
{
  "emotion": "Happy",
  "confidence": 0.9821
}
```

### Error Handling
- **400 Bad Request**: Jika tidak ada file atau file bukan gambar valid.
- **500 Internal Server Error**: Jika prediksi gagal.

### Endpoint Health Check (Opsional)
- **URL**: `/health`
- **Method**: `GET`
- **Response**: Informasi status model dan kelas emosi.

## Contoh Penggunaan
Kirim gambar menggunakan curl:
```bash
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/predict
```

## Catatan Tambahan
- Pastikan TensorFlow dan dependensi lainnya terinstal.
- Model default: `ResNet50V2_Model.h5` di root atau sesuai `MODEL_PATH`.
- Untuk kompatibilitas, endpoint menerima kunci `file` atau `image`.

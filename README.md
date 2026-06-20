# FertilityPro - Backend Flask Application

Aplikasi backend Flask untuk sistem skrining keberhasilan kehamilan berbasis Machine Learning.

## ✨ Fitur Utama

### Backend
- ✅ **Model Machine Learning**: XGBoost dengan hyperparameter tuning
- ✅ **Standard Scaler**: Normalisasi fitur numerik
- ✅ **Label Encoder**: Encoding fitur kategori
- ✅ **Prediksi Real-time**: Proses cepat dengan probabilitas akurat
- ✅ **Validasi Input**: Pengecekan data komprehensif
- ✅ **REST API**: Endpoint JSON untuk integrasi
- ✅ **Error Handling**: Manajemen error yang robust

### Frontend
- ✅ **UI Responsif**: Bootstrap 5 untuk semua device
- ✅ **Desain Modern**: Warna #67C090 dengan tema healthcare
- ✅ **Form Dinamis**: Input terstruktur dengan placeholder dan dropdown
- ✅ **Result Visualization**: Probabilitas dengan progress bar
- ✅ **UX Intuitif**: Pengalaman pengguna yang smooth
- ✅ **Validasi Klien**: Real-time form validation
- ✅ **Loading State**: Visual feedback saat processing

## 💻 Persyaratan Sistem

### Minimum Requirements
- Python 3.8+
- 512 MB RAM
- 200 MB Storage
- Browser modern (Chrome, Firefox, Safari, Edge)

### Recommended
- Python 3.10+
- 1 GB RAM
- 500 MB Storage
- Linux/macOS atau Windows 10+

## 📦 Instalasi

### 1. Clone atau Download Project
```bash
cd /home/user/Downloads/archive/ML-Fertic_Predict/app
```

### 2. Buat Virtual Environment
```bash
# Gunakan venv (recommended)
python3 -m venv venv

# Atau gunakan conda
conda create -n fertility-pro python=3.10
```

### 3. Aktivasi Virtual Environment
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Conda
conda activate fertility-pro
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 💡 Tips Efisiensi: Menggunakan Library Sebelumnya & Instalasi Parsial
Jika Anda sudah pernah membuat virtual environment atau menginstal library ML di project sebelumnya, Anda dapat memanfaatkannya kembali tanpa mendownload ulang seluruh library:

* **Mendeteksi Library Terinstal Otomatis**: 
  Saat Anda menjalankan `pip install -r requirements.txt` di environment yang sudah memiliki sebagian library, pip akan mendeteksi kecocokan versi (*Requirement already satisfied*) dan **hanya akan menginstal library yang belum terinstal**.
* **Menginstal 1 Library yang Kurang Secara Spesifik**:
  Jika Anda hanya kekurangan satu pustaka tertentu (misalnya `xgboost` yang sebelumnya hilang), Anda tidak perlu menginstal ulang semua isi requirements. Cukup jalankan perintah instalasi khusus untuk pustaka tersebut:
  ```bash
  # Contoh menginstal 1 library spesifik (xgboost)
  pip install xgboost
  
  # Atau menginstal versi spesifik agar cocok dengan model pelatihan
  pip install xgboost==3.3.0
  ```

### 5. Verifikasi Model Files
Pastikan folder `app/model/` berisi:
- `best_model.pkl` - Model terbaik (XGBoost Pipeline)
- `preprocessor.pkl` - StandardScaler dan OneHotEncoder (unfitted template)
- `label_encoder.pkl` - Label encoder untuk target
- `feature_names.pkl` - Nama-nama fitur

## 🚀 Menjalankan Aplikasi

### Method 1: Langsung dengan Python
```bash
python run.py
```

### Method 2: Dengan Flask CLI
```bash
export FLASK_APP=app.py  # Linux/macOS
set FLASK_APP=app.py     # Windows

flask run
```

### Method 3: Dengan Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Method 4: Dengan Docker & Docker Compose (Containerized)
Untuk kemudahan deploy dan isolasi penuh, Anda dapat menjalankan aplikasi di dalam container Docker. Docker Compose akan mengaktifkan container backend (Gunicorn) bersama dengan Nginx reverse proxy.

1. Masuk ke direktori docker:
   ```bash
   cd app/docker
   ```
2. Jalankan perintah build dan up:
   ```bash
   docker-compose up -d --build
   ```
3. Periksa status container:
   ```bash
   docker-compose ps
   ```
4. Untuk menghentikan container:
   ```bash
   docker-compose down
   ```

### Akses Aplikasi
- **URL (Direct/Docker Backend)**: http://localhost:5000
- **URL (Nginx Reverse Proxy)**: http://localhost (Port 80/443)
- **API Health Check**: http://localhost:5000/health


## 📂 Struktur Folder

```
app/
├── __init__.py              # Flask app factory
├── app.py                   # Routes utama (LEGACY - gunakan __init__.py)
├── config.py                # Konfigurasi aplikasi
├── run.py                   # Entry point aplikasi
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.example            # Template .env
├── README.md               # Dokumentasi ini
├── templates/
│   └── index.html          # Template HTML (Bootstrap 5)
├── static/
│   ├── css/               # CSS files (optional)
│   ├── js/                # JavaScript files (optional)
│   └── images/            # Image assets (optional)
└── logs/                  # Log files (created at runtime)
```

## 🔌 API Endpoints

### 1. Home Page
```
GET /
```
Menampilkan halaman utama dengan form prediksi.

**Response**: HTML page

---

### 2. Predict Endpoint
```
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "Female_Age": 30,
  "Male_Age": 35,
  "BMI": 24.5,
  "Menstrual_Regularity": "Regular",
  "PCOS": "No",
  "Stress_Level": "Low",
  "Smoking": "No",
  "Alcohol_Intake": "None",
  "Sperm_Count_Million_per_ml": 75.5,
  "Motility_%": 72.3,
  "Trying_Duration_Months": 12,
  "Treatment_Type": "None"
}
```

**Response (Success):**
```json
{
  "success": true,
  "prediction": "Success",
  "prediction_label": "Berhasil",
  "prediction_color": "success",
  "prediction_icon": "✓",
  "probability": 85.42,
  "confidence": "Tinggi",
  "timestamp": "2026-06-20T10:30:45.123456"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Usia wanita harus antara 18-55 tahun"
}
```

---

### 3. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running",
  "model_loaded": true,
  "timestamp": "2026-06-20T10:30:45.123456"
}
```

---

### 4. Get Categories
```
GET /api/categories
```

**Response:**
```json
{
  "Menstrual_Regularity": {
    "Regular": "Teratur",
    "Irregular": "Tidak Teratur"
  },
  "PCOS": {
    "Yes": "Ya",
    "No": "Tidak"
  },
  ...
}
```

## 📚 Dokumentasi Teknis

### Model Architecture
- **Algorithm**: XGBoost Classification
- **Input Features**: 12 (8 kategori + 4 numerik)
- **Output**: Binary classification (Success/Failure) + Probability
- **Performance**: F1-Score optimized dengan ROC-AUC consideration

### Data Preprocessing
1. **Numeric Features**: StandardScaler normalization
2. **Categorical Features**: OneHotEncoder
3. **Target Encoding**: LabelEncoder

### Fitur Input Detail

#### Data Wanita
| Field | Type | Range | Unit |
|-------|------|-------|------|
| Female_Age | Integer | 18-55 | tahun |
| BMI | Float | 15-50 | kg/m² |
| Menstrual_Regularity | Kategori | Regular/Irregular | - |
| PCOS | Kategori | Yes/No | - |
| Stress_Level | Kategori | High/Low | - |
| Smoking | Kategori | Yes/No | - |
| Alcohol_Intake | Kategori | None/Moderate/High | - |

#### Data Pria
| Field | Type | Range | Unit |
|-------|------|-------|------|
| Male_Age | Integer | 18-70 | tahun |
| Sperm_Count_Million_per_ml | Float | 0-300 | juta/ml |
| Motility_% | Float | 0-100 | % |
| Trying_Duration_Months | Integer | 0-120 | bulan |

#### Riwayat Pengobatan
| Field | Type | Options |
|-------|------|---------|
| Treatment_Type | Kategori | None/IVF/IUI/Medication/Surgery |

### Validasi Input
- Range checking untuk numeric fields
- Category validation untuk categorical fields
- Required field validation
- Type conversion dan error handling

### Response Interpretation
- **Probability > 80%**: Tingkat Keyakinan "Sangat Tinggi"
- **Probability 60-80%**: Tingkat Keyakinan "Tinggi"
- **Probability 40-60%**: Tingkat Keyakinan "Sedang"
- **Probability < 40%**: Tingkat Keyakinan "Rendah"

## ⚙️ Environment Variables

Konfigurasi di file `.env`:

```env
# Development
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Security (change in production!)
SECRET_KEY=your-secret-key-here

# Model paths
MODEL_PATH=../model/best_model.pkl
```

## 🔒 Security Notes

### Development
⚠️ **JANGAN GUNAKAN DI PRODUCTION** konfigurasi berikut:
- `FLASK_DEBUG=True`
- `SECRET_KEY` default
- `CORS_ORIGINS=*`

### Production Checklist
- [ ] Ubah `FLASK_ENV` ke `production`
- [ ] Gunakan unique `SECRET_KEY`
- [ ] Restrict `CORS_ORIGINS`
- [ ] Gunakan HTTPS
- [ ] Setup database properly
- [ ] Configure logging
- [ ] Gunakan production WSGI server (Gunicorn)
- [ ] Setup reverse proxy (Nginx)

## 🐛 Troubleshooting

### Error: "Model tidak ditemukan"
```
Solusi: Pastikan folder model/ berisi semua file .pkl
```

### Error: "ModuleNotFoundError: No module named 'flask'"
```
Solusi: Jalankan: pip install -r requirements.txt
```

### Error: "Port 5000 sudah digunakan"
```
Solusi: 
- Ubah PORT di .env: FLASK_PORT=5001
- Atau kill process: lsof -ti:5000 | xargs kill -9
```

### Slow Response
```
Solusi:
- Tingkatkan RAM
- Gunakan Gunicorn dengan multiple workers: gunicorn -w 4 app:app
- Enable caching
```

## 📊 Monitoring

### Check Health
```bash
curl http://localhost:5000/health
```

### View Logs
```bash
tail -f logs/app.log
```

### Load Testing
```bash
pip install locust
locust -f locustfile.py --host=http://localhost:5000
```

## 🔄 Update Model

Untuk mengupdate model dengan training baru:

1. Jalankan training di `code/Fertality_Predict.py`
2. Replace files di folder `model/`
3. Restart Flask server

---

**Last Updated**: Juni 2026
**Version**: 1.0.0
**Status**: Production Ready ✅

"""
FertilityPro Flask Application
Main application factory and routes
"""
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Konfigurasi path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# Load model, preprocessor, dan label encoder
try:
    model = joblib.load(os.path.join(MODEL_DIR, 'best_model.pkl'))
    preprocessor = joblib.load(os.path.join(MODEL_DIR, 'preprocessor.pkl'))
    label_encoder = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
    feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))
    print("✓ Model, preprocessor, dan label encoder berhasil dimuat")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None
    preprocessor = None
    label_encoder = None
    feature_names = None

# Mapping kategori untuk display
category_mappings = {
    'Menstrual_Regularity': {
        'Regular': 'Teratur',
        'Irregular': 'Tidak Teratur'
    },
    'PCOS': {
        'Yes': 'Ya',
        'No': 'Tidak'
    },
    'Stress_Level': {
        'High': 'Tinggi',
        'Low': 'Rendah'
    },
    'Smoking': {
        'Yes': 'Ya',
        'No': 'Tidak'
    },
    'Alcohol_Intake': {
        'None': 'Tidak Ada',
        'Moderate': 'Sedang',
        'High': 'Tinggi'
    },
    'Treatment_Type': {
        'None': 'Tidak Ada',
        'IVF': 'IVF',
        'IUI': 'IUI',
        'Medication': 'Obat',
        'Surgery': 'Operasi'
    }
}

# Reverse mapping untuk processing input
reverse_mappings = {key: {v: k for k, v in val.items()} 
                    for key, val in category_mappings.items()}

@app.route('/')
def home():
    """Render halaman utama aplikasi"""
    return render_template('index.html', categories=category_mappings)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint untuk prediksi kesuburan kehamilan"""
    try:
        if model is None:
            return jsonify({'success': False, 'error': 'Model belum dimuat'}), 500
        
        data = request.get_json()
        
        # Konversi string input menjadi tipe data yang tepat
        input_data = {
            'Female_Age': int(data.get('Female_Age', 0)),
            'Male_Age': int(data.get('Male_Age', 0)),
            'BMI': float(data.get('BMI', 0)),
            'Menstrual_Regularity': data.get('Menstrual_Regularity', ''),
            'PCOS': data.get('PCOS', ''),
            'Stress_Level': data.get('Stress_Level', ''),
            'Smoking': data.get('Smoking', ''),
            'Alcohol_Intake': data.get('Alcohol_Intake', ''),
            'Sperm_Count_Million_per_ml': float(data.get('Sperm_Count_Million_per_ml', 0)),
            'Motility_%': float(data.get('Motility_%', 0)),
            'Trying_Duration_Months': int(data.get('Trying_Duration_Months', 0)),
            'Treatment_Type': data.get('Treatment_Type', '')
        }
        
        # Validasi input
        validation = validate_input(input_data)
        if not validation['valid']:
            return jsonify({'success': False, 'error': validation['error']}), 400
        
        # Buat DataFrame dari input
        df_input = pd.DataFrame([input_data])
        
        # Prediksi langsung menggunakan pipeline (tidak melakukan double preprocessing)
        prediction = model.predict(df_input)[0]
        probability = model.predict_proba(df_input)[0]
        
        # Decode prediction
        predicted_label = label_encoder.inverse_transform([prediction])[0]
        success_probability = float(probability[1]) if len(probability) > 1 else float(probability[0])
        
        # Mapping untuk hasil
        result_mapping = {
            'Success': {'label': 'Berhasil', 'color': 'success', 'icon': '✓'},
            'Failure': {'label': 'Tidak Berhasil', 'color': 'danger', 'icon': '✗'}
        }
        
        result_info = result_mapping.get(predicted_label, 
                                        {'label': predicted_label, 'color': 'info', 'icon': '?'})
        
        # Tentukan confidence level
        if success_probability >= 0.8:
            confidence = 'Sangat Tinggi'
        elif success_probability >= 0.6:
            confidence = 'Tinggi'
        elif success_probability >= 0.4:
            confidence = 'Sedang'
        else:
            confidence = 'Rendah'
        
        return jsonify({
            'success': True,
            'prediction': predicted_label,
            'prediction_label': result_info['label'],
            'prediction_color': result_info['color'],
            'prediction_icon': result_info['icon'],
            'probability': round(success_probability * 100, 2),
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error dalam prediksi: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Terjadi kesalahan: {str(e)}'}), 500

def validate_input(data):
    """Validasi input data dari form"""
    try:
        # Validasi range umur
        if not (18 <= data['Female_Age'] <= 55):
            return {'valid': False, 'error': 'Usia wanita harus antara 18-55 tahun'}
        
        if not (18 <= data['Male_Age'] <= 70):
            return {'valid': False, 'error': 'Usia pria harus antara 18-70 tahun'}
        
        # Validasi range BMI
        if not (15 <= data['BMI'] <= 50):
            return {'valid': False, 'error': 'BMI harus antara 15-50'}
        
        # Validasi range Sperm Count
        if not (0 <= data['Sperm_Count_Million_per_ml'] <= 300):
            return {'valid': False, 'error': 'Jumlah Sperma harus antara 0-300 juta/ml'}
        
        # Validasi range Motility
        if not (0 <= data['Motility_%'] <= 100):
            return {'valid': False, 'error': 'Motilitas harus antara 0-100%'}
        
        # Validasi range durasi mencoba
        if not (0 <= data['Trying_Duration_Months'] <= 120):
            return {'valid': False, 'error': 'Durasi mencoba harus antara 0-120 bulan'}
        
        # Validasi kategori
        valid_categories = {
            'Menstrual_Regularity': ['Regular', 'Irregular'],
            'PCOS': ['Yes', 'No'],
            'Stress_Level': ['High', 'Low'],
            'Smoking': ['Yes', 'No'],
            'Alcohol_Intake': ['None', 'Moderate', 'High'],
            'Treatment_Type': ['None', 'IVF', 'IUI', 'Medication', 'Surgery']
        }
        
        for field, valid_values in valid_categories.items():
            if data[field] not in valid_values:
                return {'valid': False, 'error': f'Nilai {field} tidak valid'}
        
        return {'valid': True}
    
    except ValueError as e:
        return {'valid': False, 'error': f'Format input tidak valid: {str(e)}'}
    except Exception as e:
        return {'valid': False, 'error': f'Error validasi: {str(e)}'}

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok', 
        'message': 'Server is running',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/categories')
def get_categories():
    """Get kategori mapping untuk frontend"""
    return jsonify(category_mappings)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Halaman tidak ditemukan'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Terjadi kesalahan internal server'}), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Permintaan tidak valid'}), 400

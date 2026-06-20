"""
Utility functions untuk model prediction
"""
import joblib
import os
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any

class ModelLoader:
    """Class untuk load model dan preprocessor"""
    
    _instance = None
    _model = None
    _preprocessor = None
    _label_encoder = None
    _feature_names = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance
    
    @classmethod
    def _load_models(cls):
        """Load semua model dan preprocessor"""
        try:
            model_dir = os.path.join(os.path.dirname(__file__), 'model')
            
            cls._model = joblib.load(os.path.join(model_dir, 'best_model.pkl'))
            cls._preprocessor = joblib.load(os.path.join(model_dir, 'preprocessor.pkl'))
            cls._label_encoder = joblib.load(os.path.join(model_dir, 'label_encoder.pkl'))
            cls._feature_names = joblib.load(os.path.join(model_dir, 'feature_names.pkl'))
            
            print("✓ All models loaded successfully")
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            raise
    
    @classmethod
    def get_model(cls):
        """Get trained model"""
        instance = cls()
        return cls._model
    
    @classmethod
    def get_preprocessor(cls):
        """Get preprocessor"""
        instance = cls()
        return cls._preprocessor
    
    @classmethod
    def get_label_encoder(cls):
        """Get label encoder"""
        instance = cls()
        return cls._label_encoder
    
    @classmethod
    def get_feature_names(cls):
        """Get feature names"""
        instance = cls()
        return cls._feature_names


def predict_pregnancy_success(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prediksi keberhasilan kehamilan berdasarkan input data
    
    Args:
        input_data: Dictionary berisi fitur-fitur input
    
    Returns:
        Dictionary berisi hasil prediksi dan probability
    """
    loader = ModelLoader()
    model = loader.get_model()
    preprocessor = loader.get_preprocessor()
    label_encoder = loader.get_label_encoder()
    
    # Buat DataFrame dari input
    df_input = pd.DataFrame([input_data])
    
    # Prediksi langsung menggunakan pipeline (tidak melakukan double preprocessing)
    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0]
    
    # Decode label
    predicted_label = label_encoder.inverse_transform([prediction])[0]
    success_probability = float(probability[1]) if len(probability) > 1 else float(probability[0])
    
    return {
        'prediction': predicted_label,
        'probability': success_probability,
        'probability_percentage': round(success_probability * 100, 2),
        'confidence_level': get_confidence_level(success_probability)
    }


def get_confidence_level(probability: float) -> str:
    """
    Tentukan tingkat kepercayaan berdasarkan probability
    
    Args:
        probability: Nilai probabilitas (0-1)
    
    Returns:
        String yang menggambarkan tingkat kepercayaan
    """
    if probability >= 0.8:
        return 'Sangat Tinggi'
    elif probability >= 0.6:
        return 'Tinggi'
    elif probability >= 0.4:
        return 'Sedang'
    else:
        return 'Rendah'


def map_categorical_value(field: str, value: str, reverse: bool = False) -> str:
    """
    Map nilai kategori antara display dan internal format
    
    Args:
        field: Nama field
        value: Nilai yang akan di-map
        reverse: Jika True, map dari display ke internal
    
    Returns:
        Nilai yang sudah di-map
    """
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
    
    if reverse:
        reverse_map = {v: k for k, v in category_mappings.get(field, {}).items()}
        return reverse_map.get(value, value)
    else:
        return category_mappings.get(field, {}).get(value, value)

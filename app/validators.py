"""
Data Validation & Sanitization Utilities
"""
from typing import Dict, Any, Tuple, List

class DataValidator:
    """Class untuk validasi dan sanitasi data input"""
    
    # Definisi range untuk numeric fields
    NUMERIC_RANGES = {
        'Female_Age': {'min': 18, 'max': 55, 'unit': 'tahun'},
        'Male_Age': {'min': 18, 'max': 70, 'unit': 'tahun'},
        'BMI': {'min': 15, 'max': 50, 'unit': 'kg/m²'},
        'Sperm_Count_Million_per_ml': {'min': 0, 'max': 300, 'unit': 'juta/ml'},
        'Motility_%': {'min': 0, 'max': 100, 'unit': '%'},
        'Trying_Duration_Months': {'min': 0, 'max': 120, 'unit': 'bulan'}
    }
    
    # Definisi kategori yang valid
    VALID_CATEGORIES = {
        'Menstrual_Regularity': ['Regular', 'Irregular'],
        'PCOS': ['Yes', 'No'],
        'Stress_Level': ['High', 'Low'],
        'Smoking': ['Yes', 'No'],
        'Alcohol_Intake': ['None', 'Moderate', 'High'],
        'Treatment_Type': ['None', 'IVF', 'IUI', 'Medication', 'Surgery']
    }
    
    @classmethod
    def validate_numeric_field(cls, field_name: str, value: Any) -> Tuple[bool, str]:
        """
        Validasi numeric field
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            numeric_value = float(value)
            
            if field_name not in cls.NUMERIC_RANGES:
                return False, f"Field {field_name} tidak dikenal"
            
            range_config = cls.NUMERIC_RANGES[field_name]
            min_val = range_config['min']
            max_val = range_config['max']
            unit = range_config['unit']
            
            if numeric_value < min_val or numeric_value > max_val:
                return False, f"{field_name} harus antara {min_val}-{max_val} {unit}"
            
            return True, ""
        
        except (ValueError, TypeError):
            return False, f"{field_name} harus berupa angka"
    
    @classmethod
    def validate_category_field(cls, field_name: str, value: str) -> Tuple[bool, str]:
        """
        Validasi category field
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if field_name not in cls.VALID_CATEGORIES:
            return False, f"Field {field_name} tidak dikenal"
        
        valid_values = cls.VALID_CATEGORIES[field_name]
        
        if value not in valid_values:
            return False, f"{field_name} harus salah satu dari: {', '.join(valid_values)}"
        
        return True, ""
    
    @classmethod
    def validate_all_fields(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validasi semua field
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validasi numeric fields
        for field in cls.NUMERIC_RANGES.keys():
            if field not in data:
                errors.append(f"Field {field} wajib diisi")
                continue
            
            is_valid, error_msg = cls.validate_numeric_field(field, data[field])
            if not is_valid:
                errors.append(error_msg)
        
        # Validasi category fields
        for field in cls.VALID_CATEGORIES.keys():
            if field not in data:
                errors.append(f"Field {field} wajib diisi")
                continue
            
            is_valid, error_msg = cls.validate_category_field(field, data[field])
            if not is_valid:
                errors.append(error_msg)
        
        return len(errors) == 0, errors
    
    @classmethod
    def sanitize_numeric(cls, value: Any) -> float:
        """Sanitasi numeric value"""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Tidak bisa mengkonversi {value} ke float")
    
    @classmethod
    def sanitize_string(cls, value: str) -> str:
        """Sanitasi string value"""
        if not isinstance(value, str):
            return str(value)
        
        # Remove whitespace
        value = value.strip()
        
        # Limit length
        if len(value) > 255:
            value = value[:255]
        
        return value
    
    @classmethod
    def sanitize_all(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitasi semua field"""
        sanitized = {}
        
        for key, value in data.items():
            if key in cls.NUMERIC_RANGES:
                sanitized[key] = cls.sanitize_numeric(value)
            else:
                sanitized[key] = cls.sanitize_string(value)
        
        return sanitized


class DataStatistics:
    """Class untuk menghitung statistik dari data"""
    
    @staticmethod
    def calculate_age_group(age: int) -> str:
        """Kategorikan umur ke dalam group"""
        if age < 25:
            return "Muda"
        elif age < 35:
            return "Dewasa Awal"
        elif age < 45:
            return "Dewasa Tengah"
        else:
            return "Dewasa Akhir"
    
    @staticmethod
    def calculate_bmi_category(bmi: float) -> str:
        """Kategorikan BMI"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @staticmethod
    def calculate_fertility_risk_factors(data: Dict[str, Any]) -> Dict[str, bool]:
        """Identifikasi risk factors"""
        return {
            'high_female_age': data.get('Female_Age', 0) > 35,
            'high_male_age': data.get('Male_Age', 0) > 40,
            'high_bmi': data.get('BMI', 0) > 29,
            'low_bmi': data.get('BMI', 0) < 18.5,
            'irregular_menstruation': data.get('Menstrual_Regularity') == 'Irregular',
            'has_pcos': data.get('PCOS') == 'Yes',
            'high_stress': data.get('Stress_Level') == 'High',
            'smoking': data.get('Smoking') == 'Yes',
            'high_alcohol': data.get('Alcohol_Intake') == 'High',
            'low_sperm_count': data.get('Sperm_Count_Million_per_ml', 0) < 40,
            'low_motility': data.get('Motility_%', 0) < 40,
            'long_trying_duration': data.get('Trying_Duration_Months', 0) > 24
        }

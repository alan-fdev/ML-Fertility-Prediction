#!/usr/bin/env python3
"""
API Testing Script
Script untuk testing endpoint API FertilityPro
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_URL = "http://localhost:5000"
ENDPOINT_PREDICT = f"{API_URL}/predict"
ENDPOINT_HEALTH = f"{API_URL}/health"

# Test cases
TEST_CASES = {
    "success_case": {
        "name": "Kasus Sukses (Probabilitas Tinggi)",
        "data": {
            "Female_Age": 28,
            "Male_Age": 32,
            "BMI": 22.5,
            "Menstrual_Regularity": "Regular",
            "PCOS": "No",
            "Stress_Level": "Low",
            "Smoking": "No",
            "Alcohol_Intake": "None",
            "Sperm_Count_Million_per_ml": 80.0,
            "Motility_%": 75.0,
            "Trying_Duration_Months": 12,
            "Treatment_Type": "None"
        }
    },
    "moderate_case": {
        "name": "Kasus Moderat (Probabilitas Sedang)",
        "data": {
            "Female_Age": 35,
            "Male_Age": 38,
            "BMI": 26.0,
            "Menstrual_Regularity": "Irregular",
            "PCOS": "Yes",
            "Stress_Level": "High",
            "Smoking": "No",
            "Alcohol_Intake": "Moderate",
            "Sperm_Count_Million_per_ml": 50.0,
            "Motility_%": 50.0,
            "Trying_Duration_Months": 36,
            "Treatment_Type": "IVF"
        }
    },
    "challenging_case": {
        "name": "Kasus Menantang (Probabilitas Rendah)",
        "data": {
            "Female_Age": 42,
            "Male_Age": 45,
            "BMI": 29.0,
            "Menstrual_Regularity": "Irregular",
            "PCOS": "Yes",
            "Stress_Level": "High",
            "Smoking": "Yes",
            "Alcohol_Intake": "High",
            "Sperm_Count_Million_per_ml": 20.0,
            "Motility_%": 30.0,
            "Trying_Duration_Months": 60,
            "Treatment_Type": "IUI"
        }
    }
}

class APITester:
    """Class untuk testing API"""
    
    def __init__(self, base_url=API_URL):
        self.base_url = base_url
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'FertilityPro-Tester/1.0'
        })
    
    def print_header(self, text):
        """Print header"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70)
    
    def print_section(self, text):
        """Print section"""
        print(f"\n{'─'*70}")
        print(f"  {text}")
        print(f"{'─'*70}")
    
    def test_health(self):
        """Test health endpoint"""
        self.print_section("Testing Health Endpoint")
        
        try:
            response = self.session.get(ENDPOINT_HEALTH, timeout=5)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                print("\n✅ Health Check PASSED")
                return True
            else:
                print(f"\n❌ Health Check FAILED - Status {response.status_code}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Health Check FAILED - {str(e)}")
            return False
    
    def test_predict(self, case_name, case_data):
        """Test predict endpoint"""
        self.print_section(f"Testing: {case_data['name']}")
        
        print(f"\nInput Data:")
        print(json.dumps(case_data['data'], indent=2))
        
        try:
            start_time = time.time()
            response = self.session.post(
                ENDPOINT_PREDICT,
                json=case_data['data'],
                timeout=10
            )
            elapsed_time = time.time() - start_time
            
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response Time: {elapsed_time:.3f}s")
            print(f"\nResponse:")
            
            result = response.json()
            print(json.dumps(result, indent=2))
            
            # Store result
            self.results.append({
                'case': case_name,
                'name': case_data['name'],
                'status_code': response.status_code,
                'time': elapsed_time,
                'result': result,
                'success': response.status_code == 200 and result.get('success', False)
            })
            
            if response.status_code == 200 and result.get('success'):
                print(f"\n✅ Prediction PASSED")
                print(f"   Prediction: {result.get('prediction_label')}")
                print(f"   Probability: {result.get('probability')}%")
                print(f"   Confidence: {result.get('confidence')}")
                return True
            else:
                print(f"\n❌ Prediction FAILED")
                if not result.get('success'):
                    print(f"   Error: {result.get('error')}")
                return False
        
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Prediction FAILED - {str(e)}")
            self.results.append({
                'case': case_name,
                'name': case_data['name'],
                'status_code': 0,
                'time': 0,
                'result': None,
                'success': False,
                'error': str(e)
            })
            return False
    
    def test_invalid_input(self):
        """Test invalid input handling"""
        self.print_section("Testing Invalid Input Handling")
        
        invalid_cases = [
            {
                "name": "Usia terlalu muda",
                "data": {
                    **TEST_CASES['success_case']['data'],
                    'Female_Age': 15
                }
            },
            {
                "name": "BMI di luar range",
                "data": {
                    **TEST_CASES['success_case']['data'],
                    'BMI': 60
                }
            },
            {
                "name": "Kategori tidak valid",
                "data": {
                    **TEST_CASES['success_case']['data'],
                    'Stress_Level': 'Invalid'
                }
            }
        ]
        
        passed = 0
        for case in invalid_cases:
            print(f"\nTesting: {case['name']}")
            
            try:
                response = self.session.post(
                    ENDPOINT_PREDICT,
                    json=case['data'],
                    timeout=5
                )
                
                result = response.json()
                
                if response.status_code != 200 or not result.get('success'):
                    print(f"✅ Correctly rejected - {result.get('error')}")
                    passed += 1
                else:
                    print(f"❌ Should have been rejected")
            
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        return passed == len(invalid_cases)
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        if not self.results:
            print("Tidak ada hasil untuk ditampilkan")
            return
        
        print(f"\nTotal Tests: {len(self.results)}")
        
        passed = sum(1 for r in self.results if r['success'])
        failed = len(self.results) - passed
        
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/len(self.results)*100):.1f}%")
        
        print(f"\nResponse Time Statistics:")
        times = [r['time'] for r in self.results if r['time'] > 0]
        if times:
            print(f"  Min: {min(times):.3f}s")
            print(f"  Max: {max(times):.3f}s")
            print(f"  Avg: {sum(times)/len(times):.3f}s")
        
        print(f"\nDetailed Results:")
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['name']}: {result['time']:.3f}s")
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("FertilityPro API Test Suite")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API URL: {self.base_url}")
        
        # Test health
        health_ok = self.test_health()
        
        if not health_ok:
            print("\n⚠️  Server tidak merespons. Test dihentikan.")
            return False
        
        # Test predict cases
        for case_name, case_data in TEST_CASES.items():
            self.test_predict(case_name, case_data)
            time.sleep(0.5)  # Delay antara request
        
        # Test invalid input
        self.test_invalid_input()
        
        # Print summary
        self.print_summary()
        
        print(f"\nEnded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

def main():
    """Main function"""
    import sys
    
    # Check API server
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
    except:
        print(f"❌ Tidak bisa terhubung ke {API_URL}")
        print("Pastikan Flask server sudah berjalan: python run.py")
        sys.exit(1)
    
    # Run tests
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Verify FertilityPro Installation
Script untuk verifikasi instalasi lengkap
"""

import sys
import subprocess
import os
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def check_python():
    """Check Python version"""
    print_header("Checking Python")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    print(f"Executable: {sys.executable}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8+ required")
        return False
    
    print_success(f"Python {version.major}.{version.minor} OK")
    return True

def check_packages():
    """Check installed packages"""
    print_header("Checking Installed Packages")
    
    required_packages = {
        'flask': 'Flask',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'joblib': 'Joblib'
    }
    
    all_ok = True
    for pkg_import, pkg_name in required_packages.items():
        try:
            __import__(pkg_import)
            print_success(f"{pkg_name} installed")
        except ImportError:
            print_error(f"{pkg_name} NOT installed")
            all_ok = False
    
    return all_ok

def check_model_files():
    """Check model files"""
    print_header("Checking Model Files")
    
    model_dir = Path(__file__).parent.parent / 'model'
    required_files = [
        'best_model.pkl',
        'preprocessor.pkl',
        'label_encoder.pkl',
        'feature_names.pkl'
    ]
    
    if not model_dir.exists():
        print_error(f"Model directory not found: {model_dir}")
        return False
    
    all_ok = True
    for filename in required_files:
        filepath = model_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print_success(f"{filename} ({size_mb:.2f} MB)")
        else:
            print_error(f"{filename} NOT found")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check required directories"""
    print_header("Checking Directories")
    
    app_dir = Path(__file__).parent
    required_dirs = {
        'templates': app_dir / 'templates',
        'logs': app_dir / 'logs',
        'static': app_dir / 'static'
    }
    
    for name, path in required_dirs.items():
        if path.exists():
            print_success(f"{name}/ directory exists")
        else:
            print_warning(f"{name}/ directory missing - creating...")
            path.mkdir(exist_ok=True)
            print_success(f"Created {name}/ directory")
    
    return True

def check_flask_app():
    """Check Flask app loads"""
    print_header("Checking Flask Application")
    
    try:
        from app import app
        print_success("Flask app imported successfully")
        
        # Check routes
        routes = [
            ('/', 'home'),
            ('/predict', 'predict'),
            ('/health', 'health'),
            ('/api/categories', 'get_categories')
        ]
        
        for route, expected in routes:
            found = False
            for rule in app.url_map.iter_rules():
                if rule.rule == route:
                    found = True
                    print_success(f"Route {route} registered")
                    break
            
            if not found:
                print_warning(f"Route {route} might be missing")
        
        return True
    
    except Exception as e:
        print_error(f"Failed to import Flask app: {e}")
        return False

def check_environment():
    """Check environment variables"""
    print_header("Checking Environment")
    
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        print_success(".env file exists")
        
        with open(env_file) as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    if key:
                        print_success(f"  {key} configured")
    else:
        print_warning(".env file not found - using defaults")
        print_warning("Copy .env.example to .env for production setup")
    
    return True

def test_api():
    """Test API endpoint"""
    print_header("Testing API")
    
    try:
        import requests
        
        # Test health check
        try:
            response = requests.get('http://localhost:5000/health', timeout=2)
            if response.status_code == 200:
                print_success("Health check endpoint responding")
                return True
        except:
            pass
        
        print_warning("API server not running (This is OK - just testing structure)")
        print_warning("Start server with: python run.py")
        return True
    
    except ImportError:
        print_warning("requests library not installed")
        return True

def main():
    """Run all checks"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════╗")
    print("║   FertilityPro Installation Verify     ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    checks = [
        ("Python Version", check_python),
        ("Packages", check_packages),
        ("Model Files", check_model_files),
        ("Directories", check_directories),
        ("Flask App", check_flask_app),
        ("Environment", check_environment),
        ("API", test_api)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error checking {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = Colors.GREEN + "PASS" + Colors.RESET if result else Colors.RED + "FAIL" + Colors.RESET
        print(f"  {name}: {status}")
    
    print(f"\nResult: {passed}/{total} checks passed\n")
    
    if passed == total:
        print_success("✓ All checks passed! Installation is complete.")
        print(f"\nNext steps:")
        print(f"  1. Activate virtual environment: source venv/bin/activate")
        print(f"  2. Run the application: python run.py")
        print(f"  3. Open browser: http://localhost:5000")
        return 0
    else:
        print_error("✗ Some checks failed. Please review the errors above.")
        print(f"\nFor help, see: INSTALL.md or QUICK_START.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())

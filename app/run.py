"""
Run Flask Application
"""
import os
import sys
from app import app
from config import get_config

if __name__ == '__main__':
    # Set environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Load config
    app.config.from_object(get_config(env))
    
    # Run app
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = env == 'development'
    
    print(f"\n{'='*60}")
    print(f"FertilityPro - Backend Application")
    print(f"{'='*60}")
    print(f"Environment: {env}")
    print(f"Debug Mode: {debug}")
    print(f"Server: http://{host}:{port}")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)

"""
🚀 Run Backend Server
NASA Space Apps 2024

Simple script to run the Flask backend server with proper configuration.
"""

import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

if __name__ == '__main__':
    from app import app
    
    print("🌍☄️ NASA Space Apps - Asteroid Impact Modeling API")
    print("=" * 60)
    print("🚀 Starting Flask backend server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🌐 CORS enabled for React frontend")
    print("📚 API documentation: http://localhost:5000/api/info")
    print("💡 Health check: http://localhost:5000/api/health")
    print("=" * 60)
    
    # Development server configuration
    app.run(
        host='0.0.0.0',        # Listen on all interfaces
        port=5000,             # Port 5000
        debug=True,            # Enable debug mode
        threaded=True,         # Enable threading
        use_reloader=True      # Auto-reload on code changes
    )
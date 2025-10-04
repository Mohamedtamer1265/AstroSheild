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
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Check if we're in production (Railway sets this)
    is_production = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    print("🌍☄️ NASA Space Apps - Asteroid Impact Modeling API")
    print("=" * 60)
    print("🚀 Starting Flask backend server...")
    
    if is_production:
        print(f"📡 Production API available on port: {port}")
        print("🌐 CORS enabled for production frontend")
        print("🔒 Running in production mode")
    else:
        print(f"📡 Development API available at: http://localhost:{port}")
        print("🌐 CORS enabled for React frontend")
        print("🔧 Running in development mode")
    
    print(f"📚 API documentation: /api/info")
    print(f"💡 Health check: /api/health")
    print("=" * 60)
    
    # Server configuration based on environment
    app.run(
        host='0.0.0.0',                    # Listen on all interfaces
        port=port,                         # Use environment port or default
        debug=not is_production,           # Disable debug in production
        threaded=True,                     # Enable threading
        use_reloader=not is_production     # Disable reloader in production
    )
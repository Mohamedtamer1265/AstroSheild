"""
WSGI entry point for Railway deployment
"""
import sys
import os

# Add the server directory to Python path
server_path = os.path.join(os.path.dirname(__file__), 'server')
sys.path.insert(0, server_path)

try:
    # Try to import the full Flask app first
    from app import app
    
    # This is what gunicorn looks for
    application = app
    
    print("✅ Full Flask app loaded successfully")
    
except ImportError as import_error:
    print(f"⚠️ Full app import failed: {str(import_error)}")
    print("🔄 Trying minimal app...")
    
    try:
        # Fallback to minimal app
        from app_minimal import app as minimal_app
        application = minimal_app
        print("✅ Minimal Flask app loaded successfully")
    except ImportError as minimal_error:
        print(f"❌ Minimal app also failed: {str(minimal_error)}")
        raise import_error
    
except ImportError as e:
    print(f"❌ Failed to import Flask app: {str(e)}")
    print(f"Python path: {sys.path}")
    print(f"Server path: {server_path}")
    print(f"Server path exists: {os.path.exists(server_path)}")
    
    # Create a minimal Flask app as fallback
    from flask import Flask, jsonify
    fallback_app = Flask(__name__)
    
    @fallback_app.route('/')
    def health():
        return jsonify({
            'status': 'error',
            'message': 'Main app failed to load',
            'error': str(e)
        })
    
    application = fallback_app
    
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
    
    # Create a minimal Flask app as fallback
    from flask import Flask, jsonify
    fallback_app = Flask(__name__)
    
    @fallback_app.route('/')
    def error():
        return jsonify({
            'status': 'error',
            'message': 'Unexpected error during app initialization',
            'error': str(e)
        })
    
    application = fallback_app

if __name__ == "__main__":
    application.run()
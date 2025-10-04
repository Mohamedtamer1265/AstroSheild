"""
WSGI entry point for Railway deployment
"""
import sys
import os
import logging

# Set up logging immediately
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting WSGI application...")
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")

# Add the server directory to Python path
server_path = os.path.join(os.path.dirname(__file__), 'server')
sys.path.insert(0, server_path)

logger.info(f"Server path: {server_path}")
logger.info(f"Server path exists: {os.path.exists(server_path)}")
logger.info(f"Python path: {sys.path}")

# Initialize application variable
application = None

try:
    logger.info("🔄 Attempting to load minimal Flask app...")
    
    # Try minimal app first (more likely to work)
    from app_minimal import app as minimal_app
    application = minimal_app
    logger.info("✅ Minimal Flask app loaded successfully")
    
except ImportError as minimal_error:
    logger.warning(f"⚠️ Minimal app import failed: {str(minimal_error)}")
    logger.info("🔄 Trying full app...")
    
    try:
        # Fallback to full app
        from app import app
        application = app
        logger.info("✅ Full Flask app loaded successfully")
        
    except ImportError as full_error:
        logger.error(f"❌ Full app also failed: {str(full_error)}")
        logger.error("🆘 Creating emergency fallback app...")
        
        # Create emergency fallback
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        fallback_app = Flask(__name__)
        CORS(fallback_app)
        
        @fallback_app.route('/')
        def emergency_root():
            return jsonify({
                'status': 'emergency_mode',
                'message': 'AstroShield API - Emergency Mode',
                'minimal_error': str(minimal_error),
                'full_error': str(full_error),
                'timestamp': '2024-10-04'
            })
        
        @fallback_app.route('/api/health')
        def emergency_health():
            return jsonify({
                'success': False,
                'status': 'emergency_mode',
                'message': 'Both main apps failed to load',
                'errors': {
                    'minimal': str(minimal_error),
                    'full': str(full_error)
                }
            })
        
        application = fallback_app
        logger.info("🆘 Emergency fallback app created")

except Exception as unexpected_error:
    logger.error(f"💥 Unexpected error during app initialization: {str(unexpected_error)}")
    logger.error(f"Error type: {type(unexpected_error)}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Last resort fallback
    from flask import Flask, jsonify
    emergency_app = Flask(__name__)
    
    @emergency_app.route('/')
    def last_resort():
        return f"AstroShield API - Last Resort Mode. Error: {str(unexpected_error)}"
    
    application = emergency_app
    logger.info("🚨 Last resort app created")

# Verify application was created
if application is None:
    logger.error("💀 No application was created!")
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def no_app():
        return "No application could be created"

logger.info("✅ WSGI setup complete")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🌍 Running on port {port}")
    application.run(host='0.0.0.0', port=port)
"""
Minimal Flask app for Railway deployment
Only includes essential endpoints that don't require heavy dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_minimal_app():
    """Create a minimal Flask application for Railway deployment."""
    app = Flask(__name__)
    
    # Enable CORS for all origins in production (Railway deployment)
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
        # In production, allow all origins for now
        CORS(app, origins="*")
        logger.info("🌐 CORS enabled for all origins (production mode)")
    else:
        # Development mode - specific origins
        allowed_origins = [
            "http://localhost:3000", 
            "http://localhost:5173",
            "http://localhost:3001"
        ]
        CORS(app, origins=allowed_origins)
        logger.info(f"🌐 CORS enabled for specific origins: {allowed_origins}")
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nasa-space-apps-2024')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error.description)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle uncaught exceptions."""
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'debug': str(e) if app.debug else None
        }), 500
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'success': True,
            'message': 'AstroShield API is running (minimal mode)',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0-minimal',
            'environment': 'railway-deployment'
        })
    
    # API Information endpoint
    @app.route('/api/info', methods=['GET'])
    def api_info():
        """Get API information and available endpoints."""
        return jsonify({
            'success': True,
            'data': {
                'name': 'AstroShield API - Minimal Mode',
                'version': '1.0.0-minimal',
                'description': 'NASA Space Apps 2024 - Asteroid Impact Analysis System (Railway Deployment)',
                'status': 'Basic endpoints active. Full functionality loading...',
                'endpoints': {
                    'health': '/api/health',
                    'info': '/api/info',
                    'status': '/api/status'
                },
                'note': 'This is a minimal version for Railway deployment testing'
            }
        })
    
    # Status endpoint
    @app.route('/api/status', methods=['GET'])
    def status():
        """Get system status."""
        return jsonify({
            'success': True,
            'status': 'running',
            'mode': 'minimal',
            'deployment': 'railway',
            'python_version': os.environ.get('PYTHON_VERSION', 'unknown'),
            'environment_vars': {
                'PORT': os.environ.get('PORT', 'not set'),
                'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT', 'not set')
            }
        })
    
    # Root route
    @app.route('/')
    def root():
        """Root endpoint."""
        return jsonify({
            'message': 'AstroShield API - Minimal Mode',
            'status': 'running',
            'version': '1.0.0-minimal',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'health': '/api/health',
                'info': '/api/info',
                'status': '/api/status'
            }
        })
    
    # Test route to verify everything works
    @app.route('/test')
    def test():
        """Simple test endpoint."""
        return "AstroShield API is working!"
    
    return app

# Create the application instance
app = create_minimal_app()

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting AstroShield API (Minimal Mode)...")
    print(f"🌍 Serving on port {port}")
    print("📡 Basic API endpoints available")
    print("💡 Visit /api/info for API documentation")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )
#!/usr/bin/env python3
"""
Direct Flask app runner for Railway deployment debugging
This bypasses gunicorn to test if Flask itself works
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_direct():
    """Run Flask app directly"""
    logger.info("🚀 Starting direct Flask app runner...")
    
    # Add server path
    server_path = os.path.join(os.path.dirname(__file__), 'server')
    sys.path.insert(0, server_path)
    
    # Get port
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Using port: {port}")
    
    try:
        # Try minimal app first
        logger.info("Loading minimal app...")
        from server.app_minimal import app
        logger.info("✅ Minimal app loaded")
        
        logger.info(f"🌍 Starting Flask development server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Failed to start app: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Create emergency app
        from flask import Flask, jsonify
        emergency_app = Flask(__name__)
        
        @emergency_app.route('/')
        def emergency():
            return jsonify({
                'status': 'emergency',
                'error': str(e),
                'message': 'Direct Flask runner failed'
            })
        
        logger.info("🆘 Starting emergency app...")
        emergency_app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    run_direct()
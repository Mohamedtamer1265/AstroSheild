#!/usr/bin/env python3
"""
Railway deployment entry point for AstroShield
Imports and runs the Flask application from the server directory
"""

import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Disable debug mode in production
    )
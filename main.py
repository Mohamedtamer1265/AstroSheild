#!/usr/bin/env python3
"""
Railway deployment entry point for AstroShield
Imports the Flask application from the server directory
"""

import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

# Import the Flask app (this is what gunicorn will use)
from app import app

# For gunicorn, we just need to expose the app object
# gunicorn will handle the server startup

if __name__ == '__main__':
    # Fallback for direct execution (development only)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
"""
WSGI entry point for Railway deployment
"""
import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

# Import the Flask app
from app import app

# This is what gunicorn looks for
application = app

if __name__ == "__main__":
    app.run()
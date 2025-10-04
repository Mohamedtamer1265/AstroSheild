"""
Health Check API - Vercel Serverless Function
"""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'AstroShield API is running on Vercel',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

def handler(request):
    """Vercel handler"""
    with app.test_request_context(request.path, method=request.method):
        return app.full_dispatch_request()

# For local testing
if __name__ == "__main__":
    app.run(debug=True)
"""
AstroShield API - Vercel Serverless Function
Simplified version with minimal dependencies for Vercel deployment
"""

from flask import Flask, jsonify, request
import requests
import math
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Handle OPTIONS requests
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'AstroShield API is running on Vercel',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'platform': 'Vercel Serverless'
    })

# API Info endpoint
@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information and available endpoints."""
    return jsonify({
        'success': True,
        'data': {
            'name': 'AstroShield API',
            'version': '1.0.0',
            'description': 'NASA Space Apps 2024 - Asteroid Impact Analysis System',
            'platform': 'Vercel Serverless',
            'endpoints': {
                'health': '/api/health',
                'info': '/api/info',
                'get_asteroid_data': '/api/asteroids/<asteroid_id>',
                'search_asteroids': '/api/asteroids/search'
            },
            'capabilities': [
                'NASA JPL Small-Body Database integration',
                'Asteroid data fetching',
                'Basic impact assessment'
            ]
        }
    })

# Simplified asteroid data fetcher
class SimpleAsteroidFetcher:
    def __init__(self):
        self.jpl_url = "https://ssd-api.jpl.nasa.gov/sbdb.api"
        
    def fetch_asteroid_data(self, asteroid_id: str):
        """Fetch real asteroid data from JPL database"""
        try:
            params = {
                'sstr': asteroid_id,
                'full-prec': 'true',
                'phys-par': 'true'
            }
            
            logger.info(f"Fetching asteroid data for ID: {asteroid_id}")
            response = requests.get(self.jpl_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if 'object' not in data:
                return {'success': False, 'error': 'Asteroid not found'}
            
            # Parse basic data
            result = {
                'success': True,
                'id': asteroid_id,
                'name': data['object'].get('fullname', asteroid_id),
                'neo': data['object'].get('neo', False),
                'pha': data['object'].get('pha', False),
                'source': 'JPL Small-Body Database'
            }
            
            # Parse physical properties
            if 'phys_par' in data:
                physical_properties = {}
                for phys in data['phys_par']:
                    name = phys.get('name', '')
                    try:
                        value = float(phys.get('value', 0))
                        if name == 'diameter':
                            physical_properties['diameter_km'] = value
                        elif name == 'H':
                            physical_properties['absolute_magnitude'] = value
                        elif name == 'albedo':
                            physical_properties['albedo'] = value
                    except:
                        pass
                result['physical_properties'] = physical_properties
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching asteroid data: {str(e)}")
            return {'success': False, 'error': f'Failed to fetch data: {str(e)}'}

    def search_asteroids(self, query: str, limit: int = 10):
        """Search for asteroids by name"""
        try:
            search_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
            params = {
                'fields': 'spkid,full_name,neo,pha,H,diameter',
                'sb-kind': 'a',
                'full-name': f'*{query}*',
                'limit': limit
            }
            
            response = requests.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data:
                return {'success': False, 'error': 'No search results found'}
            
            results = []
            for row in data['data']:
                if len(row) >= 6:
                    results.append({
                        'id': str(row[0]),
                        'name': row[1],
                        'neo': row[2] == '1' if row[2] else False,
                        'pha': row[3] == '1' if row[3] else False,
                        'absolute_magnitude': float(row[4]) if row[4] else None,
                        'diameter_km': float(row[5]) if row[5] else None
                    })
            
            return {
                'success': True,
                'query': query,
                'count': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error searching asteroids: {str(e)}")
            return {'success': False, 'error': f'Search failed: {str(e)}'}

# Initialize fetcher
fetcher = SimpleAsteroidFetcher()

# Asteroid data endpoints
@app.route('/api/asteroids/<asteroid_id>', methods=['GET'])
def get_asteroid_data(asteroid_id):
    """Get detailed asteroid data from JPL database"""
    try:
        result = fetcher.fetch_asteroid_data(asteroid_id)
        if not result.get('success'):
            return jsonify(result), 404
        return jsonify(result)
    except Exception as e:
        logger.error(f"Asteroid data fetch failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Asteroid data fetch failed: {str(e)}'
        }), 500

@app.route('/api/asteroids/search', methods=['GET'])
def search_asteroids():
    """Search for asteroids by name or designation"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter "q" is required'
            }), 400
        
        result = fetcher.search_asteroids(query, limit)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Asteroid search failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Asteroid search failed: {str(e)}'
        }), 500

# Basic impact simulation endpoint
@app.route('/api/impact/simulate', methods=['POST'])
def simulate_impact():
    """Simulate basic asteroid impact"""
    try:
        data = request.get_json()
        latitude = data.get('latitude', 0)
        longitude = data.get('longitude', 0)
        asteroid_diameter_m = data.get('asteroid_diameter_m', 100)
        
        # Simple impact calculation
        velocity_km_s = 20  # Typical impact velocity
        mass_kg = (4/3) * math.pi * (asteroid_diameter_m/2)**3 * 2500  # Assume rocky density
        energy_joules = 0.5 * mass_kg * (velocity_km_s * 1000)**2
        energy_megatons = energy_joules / 4.184e15
        
        # Simple crater calculation
        crater_diameter_m = 1.8 * asteroid_diameter_m * (velocity_km_s * 1000 / 1000)**(2/3)
        
        return jsonify({
            'success': True,
            'impact_location': {
                'latitude': latitude,
                'longitude': longitude
            },
            'asteroid_properties': {
                'diameter_m': asteroid_diameter_m,
                'estimated_mass_kg': mass_kg,
                'impact_velocity_km_s': velocity_km_s
            },
            'impact_effects': {
                'energy_megatons': round(energy_megatons, 3),
                'crater_diameter_m': round(crater_diameter_m, 0),
                'damage_radius_km': round((energy_megatons)**0.5, 1)
            }
        })
        
    except Exception as e:
        logger.error(f"Impact simulation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Impact simulation failed: {str(e)}'
        }), 500

# Export the Flask app
def handler(request):
    return app
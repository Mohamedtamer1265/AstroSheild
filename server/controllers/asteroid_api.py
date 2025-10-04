"""
Asteroid API Controller - Single asteroid data fetching
"""
from flask import Blueprint, jsonify, request
import logging
import sys
import os
import requests
import random
import math
from datetime import datetime, timedelta
from typing import Dict

# Add the parent directory to path to access utils
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.asteroid_fetcher import PracticalAsteroidFetcher

logger = logging.getLogger(__name__)

# Create blueprint for asteroid APIs
asteroid_bp = Blueprint('asteroid', __name__)

# Initialize the asteroid fetcher
asteroid_fetcher = PracticalAsteroidFetcher()

class NASANeoWsAPI:
    """NASA NeoWs API for getting multiple asteroids"""
    
    def __init__(self):
        self.base_url = "https://api.nasa.gov/neo/rest/v1"
        self.api_key = "Sjdyck7V9bl6zInxWYhkZvPditLcGVtP9jlVDbxe"  # You can get a free key from NASA
        
    def get_asteroids_feed(self, start_date: str = None, end_date: str = None) -> Dict:
        """Get asteroid feed from NASA NeoWs"""
        try:
            if not start_date:
                start_date = datetime.now().strftime('%Y-%m-%d')
            if not end_date:
                end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                
            params = {
                'start_date': start_date,
                'end_date': end_date,
                'api_key': self.api_key
            }
            
            logger.info(f"Fetching asteroid feed from {start_date} to {end_date}")
            response = requests.get(f"{self.base_url}/feed", params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Extract asteroid data
            asteroids = []
            for date, date_asteroids in data.get('near_earth_objects', {}).items():
                for asteroid in date_asteroids:
                    asteroids.append({
                        'id': asteroid.get('id'),
                        'name': asteroid.get('name'),
                        'neo_reference_id': asteroid.get('neo_reference_id'),
                        'nasa_jpl_url': asteroid.get('nasa_jpl_url'),
                        'absolute_magnitude_h': asteroid.get('absolute_magnitude_h'),
                        'estimated_diameter_km_min': asteroid.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_min'),
                        'estimated_diameter_km_max': asteroid.get('estimated_diameter', {}).get('kilometers', {}).get('estimated_diameter_max'),
                        'is_potentially_hazardous': asteroid.get('is_potentially_hazardous_asteroid'),
                        'close_approach_date': asteroid.get('close_approach_data', [{}])[0].get('close_approach_date') if asteroid.get('close_approach_data') else None,
                        'miss_distance_km': asteroid.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('kilometers') if asteroid.get('close_approach_data') else None,
                        'relative_velocity_km_s': asteroid.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_second') if asteroid.get('close_approach_data') else None
                    })
            
            return {
                'success': True,
                'element_count': data.get('element_count', 0),
                'asteroids': asteroids
            }
            
        except Exception as e:
            logger.error(f"Error fetching NASA NeoWs data: {str(e)}")
            return {'success': False, 'error': str(e)}

# Initialize NASA NeoWs API
nasa_neows = NASANeoWsAPI()

class SimpleImpactPredictor:
    """Simple impact prediction with lat/long/velocity generation"""
    
    def __init__(self):
        self.random = random.Random()
        self.random.seed(42)  # Reproducible results for testing
        
    def generate_impact_prediction(self, asteroid_data: Dict) -> Dict:
        """Generate impact prediction with coordinates and velocity"""
        try:
            # Generate realistic impact coordinates
            latitude = self.random.uniform(-60, 60)  # Avoid extreme poles
            longitude = self.random.uniform(-180, 180)
            
            # Generate realistic impact velocity (11-30 km/s typical for asteroids)
            velocity_km_s = self.random.uniform(11, 30)
            
            # Generate approach direction
            directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
            direction = self.random.choice(directions)
            bearing_degrees = self.random.uniform(0, 360)
            
            # Calculate impact energy based on asteroid size
            diameter_km = asteroid_data.get('physical_properties', {}).get('diameter_km', 1.0)
            mass_kg = self._estimate_mass(diameter_km)
            energy_joules = 0.5 * mass_kg * (velocity_km_s * 1000)**2
            energy_megatons = energy_joules / 4.184e15
            
            # Generate impact date (within next 2 years)
            days_ahead = self.random.randint(30, 730)
            impact_date = (datetime.now() + timedelta(days=days_ahead)).isoformat()
            
            return {
                'success': True,
                'impact_coordinates': {
                    'latitude': round(latitude, 6),
                    'longitude': round(longitude, 6)
                },
                'impact_velocity': {
                    'velocity_km_s': round(velocity_km_s, 2),
                    'direction': direction,
                    'bearing_degrees': round(bearing_degrees, 1)
                },
                'impact_details': {
                    'estimated_impact_date': impact_date,
                    'energy_megatons': round(energy_megatons, 3),
                    'asteroid_diameter_km': diameter_km,
                    'estimated_mass_kg': mass_kg
                },
                'note': 'Simulated impact prediction for testing purposes'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _estimate_mass(self, diameter_km: float) -> float:
        """Estimate asteroid mass from diameter"""
        density = 2500  # kg/m³ typical asteroid density
        radius_m = diameter_km * 500  # Convert to radius in meters
        volume_m3 = (4/3) * math.pi * radius_m**3
        return volume_m3 * density

# Initialize impact predictor
impact_predictor = SimpleImpactPredictor()

@asteroid_bp.route('/asteroids/all', methods=['GET'])
def get_all_asteroids():
    """
    Get all asteroid data using NASA NeoWs
    
    Example URL: /api/asteroids/all
    Optional parameters: ?start_date=2024-10-01&end_date=2024-10-07
    Returns: List of asteroids from NASA Near Earth Object Web Service
    """
    try:
        # Get optional query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        logger.info(f"Fetching all asteroids from NASA NeoWs (start: {start_date}, end: {end_date})")
        
        # Fetch asteroids from NASA NeoWs
        asteroids_data = nasa_neows.get_asteroids_feed(start_date, end_date)
        
        if not asteroids_data.get('success'):
            return jsonify({
                'success': False,
                'error': 'Failed to fetch asteroids from NASA NeoWs',
                'details': asteroids_data.get('error', 'Unknown error')
            }), 500
        
        return jsonify({
            'success': True,
            'total_count': asteroids_data.get('element_count', 0),
            'asteroids': asteroids_data.get('asteroids', []),
            'data_source': 'NASA NeoWs API',
            'date_range': {
                'start_date': start_date or datetime.now().strftime('%Y-%m-%d'),
                'end_date': end_date or (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_all_asteroids: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@asteroid_bp.route('/asteroid/<asteroid_id>', methods=['GET'])
def get_asteroid_details(asteroid_id):
    """
    Get complete asteroid data by ID from JPL database
    
    Example URL: /api/asteroid/433
    Returns: Complete JPL asteroid data in JSON format
    """
    try:
        logger.info(f"Fetching asteroid data for ID: {asteroid_id}")
        
        # Use your existing fetcher to get data from JPL
        asteroid_data = asteroid_fetcher.fetch_asteroid_data(asteroid_id)
        
        # Check if data was successfully fetched
        if not asteroid_data.get('success'):
            return jsonify({
                'success': False,
                'error': f'Asteroid not found or JPL API error',
                'asteroid_id': asteroid_id,
                'details': asteroid_data.get('error', 'Unknown error')
            }), 404
        
        # Return successful response with all data
        return jsonify({
            'success': True,
            'asteroid_id': asteroid_id,
            'data': asteroid_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_asteroid_details: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'asteroid_id': asteroid_id,
            'details': str(e)
        }), 500

@asteroid_bp.route('/predict/impact', methods=['POST'])
def predict_impact():
    """
    Predict impact coordinates and details for an asteroid
    
    Example URL: POST /api/predict/impact
    Body: {"asteroid_id": "433"}
    Returns: latitude, longitude, velocity, direction for asteroid impact
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body reuired with asteroid_id'
            }), 400
        
        asteroid_id = data.get('asteroid_id')
        if not asteroid_id:
            return jsonify({
                'success': False,
                'error': 'asteroid_id parameter required'
            }), 400
        
        logger.info(f"Generating impact prediction for asteroid ID: {asteroid_id}")
        
        # First, get asteroid data
        asteroid_data = asteroid_fetcher.fetch_asteroid_data(asteroid_id)
        
        if not asteroid_data.get('success'):
            return jsonify({
                'success': False,
                'error': f'Failed to fetch asteroid data for ID: {asteroid_id}',
                'details': asteroid_data.get('error', 'Unknown error')
            }), 404
        
        # Generate impact prediction
        impact_prediction = impact_predictor.generate_impact_prediction(asteroid_data)
        
        if not impact_prediction.get('success'):
            return jsonify({
                'success': False,
                'error': 'Failed to generate impact prediction',
                'details': impact_prediction.get('error', 'Unknown error')
            }), 500
        
        # Combine asteroid data with prediction
        response = {
            'success': True,
            'asteroid_info': {
                'id': asteroid_data.get('id'),
                'name': asteroid_data.get('name'),
                'diameter_km': asteroid_data.get('physical_properties', {}).get('diameter_km'),
                'neo': asteroid_data.get('neo'),
                'pha': asteroid_data.get('pha')
            },
            'impact_prediction': impact_prediction,
            'prediction_method': 'Simulated impact scenario for testing'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in predict_impact: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

# Health check endpoint
@asteroid_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check for asteroid API"""
    return jsonify({
        'success': True,
        'message': 'Asteroid API is running',
        'endpoints': [
            'GET /asteroid/<id> - Get asteroid details by ID',
            'GET /asteroids/all - Get all asteroids from NASA NeoWs',
            'POST /predict/impact - Predict impact coordinates and velocity (Body: {"asteroid_id": "433"})'
        ]
    }), 200
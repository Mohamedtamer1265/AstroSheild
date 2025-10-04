"""
🌍☄️ Asteroid Impact Modeling API
NASA Space Apps 2024 - Flask Backend

Main Flask application providing REST API endpoints for asteroid impact modeling.
Integrates with React frontend for comprehensive impact analysis and visualization.
"""
# Add this import at the top with other imports
from controllers.asteroid_api import asteroid_bp
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import traceback
import os
import json
from datetime import datetime

# Import our custom modules
from models.asteroid_impact import AsteroidImpact
from models.scenarios import ImpactScenarios
from utils.visualization import VisualizationManager
from utils.nasa_apis import NASAAPIManager
from controllers.impact_controller import ImpactController
from controllers.scenario_controller import ScenarioController
from controllers.tsunami_controller import tsunami_bp
from controllers.prediction_controller import PredictionController

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for React frontend
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:3002"])
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nasa-space-apps-2024')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    

    # Initialize managers
    nasa_api_manager = NASAAPIManager()
    viz_manager = VisualizationManager(nasa_api_manager)
    
    # Initialize controllers
    impact_controller = ImpactController(nasa_api_manager, viz_manager)
    scenario_controller = ScenarioController(nasa_api_manager, viz_manager)
    prediction_controller = PredictionController()
    
    # Register blueprints
    app.register_blueprint(tsunami_bp)
    app.register_blueprint(asteroid_bp, url_prefix='/api')
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
            'message': 'Asteroid Impact API is running',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    # API Information endpoint
    @app.route('/api/info', methods=['GET'])
    def api_info():
        """Get API information and available endpoints."""
        return jsonify({
            'success': True,
            'data': {
                'name': 'Asteroid Impact Modeling API',
                'version': '1.0.0',
                'description': 'NASA Space Apps 2024 - Asteroid Impact Analysis System',
                'endpoints': {
                    'health': '/api/health',
                    'info': '/api/info',
                    'analyze_impact': '/api/impact/analyze',
                    'custom_impact': '/api/impact/custom',
                    'scenarios': '/api/scenarios',
                    'scenario_details': '/api/scenarios/<scenario_name>',
                    'run_scenario': '/api/scenarios/<scenario_name>/run',
                    'compare_scenarios': '/api/scenarios/compare',
                    'parameter_study': '/api/impact/parameter-study',
                    'shake_map': '/api/visualization/shake-map',
                    'impact_chart': '/api/visualization/impact-chart',
                    'tsunami_assess': '/api/tsunami/assess',
                    'tsunami_quick_check': '/api/tsunami/quick-check',
                    'tsunami_risk_levels': '/api/tsunami/risk-levels',
                    'predict_impact': '/api/predict/impact',
                    'predict_position': '/api/predict/position/<asteroid_id>',
                    'predict_trajectory': '/api/predict/trajectory/<asteroid_id>',
                    'predict_multi_asteroid': '/api/predict/multi-asteroid',
                    'assess_impact_risk': '/api/predict/risk/<asteroid_id>',
                    'search_asteroids': '/api/asteroids/search',
                    'get_asteroid_data': '/api/asteroids/<asteroid_id>',
                    'notable_asteroids': '/api/asteroids/list/notable',
                    'search_all_asteroids': '/api/asteroids/list/search-all'
                },
                'capabilities': [
                    'Asteroid impact physics modeling',
                    'Seismic activity calculation with USGS earthquake data',
                    'Energy release analysis',
                    'Casualty estimation',
                    'Crater formation modeling',
                    'Interactive shake maps',
                    'Pre-defined scenarios',
                    'Parameter sensitivity analysis',
                    'Tsunami risk assessment and coastal impact analysis',
                    'Real Keplerian orbital mechanics for asteroid prediction',
                    'NASA JPL Small-Body Database integration',
                    'Advanced impact scenario generation',
                    'Multi-asteroid risk assessment',
                    'Comprehensive trajectory prediction',
                    'Close approach analysis and impact probability'
                ],
                'external_apis': [
                    'Open-Elevation API for elevation data',
                    'USGS Earthquake API for seismic comparisons',
                    'Population density estimation algorithms',
                    'NASA JPL Small-Body Database API',
                    'NASA JPL Small-Body Database Query API'
                ]
            }
        })
    
    # Impact Analysis Routes
    @app.route('/api/impact/analyze', methods=['POST'])
    def analyze_impact():
        """Analyze a custom asteroid impact."""
        return impact_controller.analyze_impact(request)
    
    @app.route('/api/impact/custom', methods=['POST'])
    def create_custom_impact():
        """Create and analyze a custom impact scenario."""
        return impact_controller.create_custom_impact(request)
    
    @app.route('/api/impact/parameter-study', methods=['POST'])
    def parameter_study():
        """Perform parameter sensitivity study."""
        return impact_controller.parameter_study(request)
    
    # Scenario Management Routes
    @app.route('/api/scenarios', methods=['GET'])
    def get_scenarios():
        """Get all available impact scenarios."""
        return scenario_controller.get_scenarios()
    
    @app.route('/api/scenarios/<scenario_name>', methods=['GET'])
    def get_scenario_details(scenario_name):
        """Get details of a specific scenario."""
        return scenario_controller.get_scenario_details(scenario_name)
    
    @app.route('/api/scenarios/<scenario_name>/run', methods=['POST'])
    def run_scenario(scenario_name):
        """Run a pre-defined impact scenario."""
        return scenario_controller.run_scenario(scenario_name, request)
    
    @app.route('/api/scenarios/compare', methods=['POST'])
    def compare_scenarios():
        """Compare multiple impact scenarios."""
        return scenario_controller.compare_scenarios(request)
    
    # Visualization Routes
    @app.route('/api/visualization/shake-map', methods=['POST'])
    def generate_shake_map():
        """Generate interactive shake map data."""
        return impact_controller.generate_shake_map(request)
    
    @app.route('/api/visualization/impact-chart', methods=['POST'])
    def generate_impact_chart():
        """Generate impact analysis chart data."""
        return impact_controller.generate_impact_chart(request)
    
    # Advanced Prediction Routes
    @app.route('/api/predict/impact', methods=['POST'])
    def comprehensive_impact_prediction():
        """
        Comprehensive impact prediction using real Keplerian physics
        Expects JSON: {"asteroid_id": "asteroid_name", "search_days": 60}
        Returns: lat, long, velocity, direction, and complete impact analysis
        """
        try:
            data = request.get_json()
            asteroid_id = data.get('asteroid_id')
            search_days = data.get('search_days', 60)
            
            if not asteroid_id:
                return jsonify({
                    'success': False,
                    'error': 'asteroid_id parameter required'
                }), 400
            
            result = prediction_controller.comprehensive_impact_prediction(asteroid_id, search_days)
            
            if not result.get('success'):
                return jsonify(result), 500 if 'error' in result else 200
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Comprehensive impact prediction failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Comprehensive impact prediction failed: {str(e)}'
            }), 500
    
    @app.route('/api/predict/position/<asteroid_id>', methods=['GET'])
    def predict_asteroid_position(asteroid_id):
        """
        Predict asteroid position at specific date using real Keplerian mechanics
        Query parameter: ?date=YYYY-MM-DD
        Returns: position, velocity, distance from Earth
        """
        try:
            target_date = request.args.get('date')
            result = prediction_controller.predict_asteroid_position(asteroid_id, target_date)
            
            if not result.get('success'):
                return jsonify(result), 404 if 'not found' in result.get('error', '').lower() else 500
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Position prediction failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Position prediction failed: {str(e)}'
            }), 500
    
    @app.route('/api/predict/trajectory/<asteroid_id>', methods=['GET'])
    def predict_trajectory(asteroid_id):
        """
        Generate multi-point trajectory prediction
        Query parameters: ?days=365&points=12
        Returns: Array of positions over time with lat/long/velocity/direction data
        """
        try:
            days = int(request.args.get('days', 365))
            points = int(request.args.get('points', 12))
            
            # Fetch asteroid data first
            asteroid_data = prediction_controller.fetcher.fetch_asteroid_data(asteroid_id)
            
            if not asteroid_data.get('success'):
                return jsonify({
                    'success': False,
                    'error': f'Failed to fetch asteroid data for ID: {asteroid_id}'
                }), 404
            
            # Generate trajectory
            trajectory_result = prediction_controller.orbital_mechanics.predict_trajectory(
                asteroid_data['orbital_elements'], days, points
            )
            
            if not trajectory_result.get('success'):
                return jsonify(trajectory_result), 500
            
            # Add asteroid info to response
            trajectory_result['asteroid_info'] = {
                'id': asteroid_data['id'],
                'name': asteroid_data['name'],
                'source': asteroid_data['source']
            }
            
            return jsonify(trajectory_result)
            
        except Exception as e:
            logger.error(f"Trajectory prediction failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Trajectory prediction failed: {str(e)}'
            }), 500
    
    @app.route('/api/predict/multi-asteroid', methods=['POST'])
    def predict_multiple_asteroids():
        """
        Predict impact scenarios for multiple asteroids
        Expects JSON: {"asteroid_ids": ["id1", "id2", ...], "search_days": 60}
        Returns: Array of predictions with lat/long/velocity/direction for each
        """
        try:
            data = request.get_json()
            asteroid_ids = data.get('asteroid_ids', [])
            search_days = data.get('search_days', 60)
            
            if not asteroid_ids:
                return jsonify({
                    'success': False,
                    'error': 'asteroid_ids array required'
                }), 400
            
            result = prediction_controller.predict_multiple_asteroids(asteroid_ids, search_days)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Multi-asteroid prediction failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Multi-asteroid prediction failed: {str(e)}'
            }), 500
    
    @app.route('/api/predict/risk/<asteroid_id>', methods=['GET'])
    def assess_impact_risk(asteroid_id):
        """
        Assess impact risk and consequences for an asteroid
        Returns: Risk assessment including damage estimates
        """
        try:
            asteroid_data = prediction_controller.fetcher.fetch_asteroid_data(asteroid_id)
            
            if not asteroid_data.get('success'):
                return jsonify({
                    'success': False,
                    'error': f'Failed to fetch asteroid data for ID: {asteroid_id}'
                }), 404
            
            # Assess impact risk
            risk_assessment = prediction_controller.orbital_mechanics.assess_impact_risk(
                asteroid_data['orbital_elements'],
                asteroid_data['physical_properties']
            )
            
            if not risk_assessment.get('success'):
                return jsonify(risk_assessment), 500
            
            # Add asteroid info to assessment
            risk_assessment['asteroid_info'] = {
                'id': asteroid_data['id'],
                'name': asteroid_data['name'],
                'neo': asteroid_data['neo'],
                'pha': asteroid_data['pha'],
                'source': asteroid_data['source']
            }
            
            return jsonify(risk_assessment)
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Risk assessment failed: {str(e)}'
            }), 500
    
    @app.route('/api/asteroids/search', methods=['GET'])
    def search_asteroids():
        """
        Search for asteroids by name or designation
        Query parameter: ?q=search_term&limit=10
        Returns: List of matching asteroids
        """
        try:
            query = request.args.get('q', '')
            limit = int(request.args.get('limit', 10))
            
            if not query:
                return jsonify({
                    'success': False,
                    'error': 'Query parameter "q" is required'
                }), 400
            
            result = prediction_controller.fetcher.search_asteroids(query, limit)
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Asteroid search failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Asteroid search failed: {str(e)}'
            }), 500
    
    @app.route('/api/asteroids/<asteroid_id>', methods=['GET'])
    def get_asteroid_data(asteroid_id):
        """
        Get detailed asteroid data from JPL database
        Returns: Complete asteroid orbital and physical data
        """
        try:
            result = prediction_controller.fetcher.fetch_asteroid_data(asteroid_id)
            
            if not result.get('success'):
                return jsonify(result), 404
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Asteroid data fetch failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Asteroid data fetch failed: {str(e)}'
            }), 500
    
    @app.route('/api/asteroids/list/notable', methods=['GET'])
    def get_notable_asteroids():
        """
        Get a list of notable asteroids including NEOs and PHAs
        Returns: List of well-known asteroids with basic info
        """
        try:
            # List of notable asteroids with their common names/IDs
            notable_asteroids = [
                {'id': '433', 'name': 'Eros', 'type': 'Near-Earth Object'},
                {'id': '1036', 'name': 'Ganymed', 'type': 'Near-Earth Object'},
                {'id': '1566', 'name': 'Icarus', 'type': 'Potentially Hazardous'},
                {'id': '1620', 'name': 'Geographos', 'type': 'Near-Earth Object'},
                {'id': '1862', 'name': 'Apollo', 'type': 'Near-Earth Object'},
                {'id': '1863', 'name': 'Antinous', 'type': 'Apollo Group'},
                {'id': '1864', 'name': 'Daedalus', 'type': 'Apollo Group'},
                {'id': '1865', 'name': 'Cerberus', 'type': 'Apollo Group'},
                {'id': '1866', 'name': 'Sisyphus', 'type': 'Apollo Group'},
                {'id': '1980', 'name': 'Tezcatlipoca', 'type': 'Apollo Group'},
                {'id': '2060', 'name': 'Chiron', 'type': 'Centaur'},
                {'id': '2062', 'name': 'Aten', 'type': 'Aten Group'},
                {'id': '2100', 'name': 'Ra-Shalom', 'type': 'Aten Group'},
                {'id': '2101', 'name': 'Adonis', 'type': 'Apollo Group'},
                {'id': '2102', 'name': 'Tantalus', 'type': 'Apollo Group'},
                {'id': '2135', 'name': 'Aristaeus', 'type': 'Apollo Group'},
                {'id': '2201', 'name': 'Oljato', 'type': 'Apollo Group'},
                {'id': '2212', 'name': 'Hephaistos', 'type': 'Apollo Group'},
                {'id': '3122', 'name': 'Florence', 'type': 'Potentially Hazardous'},
                {'id': '3200', 'name': 'Phaethon', 'type': 'Apollo Group'},
                {'id': '3554', 'name': 'Amun', 'type': 'Aten Group'},
                {'id': '4015', 'name': 'Wilson-Harrington', 'type': 'Apollo Group'},
                {'id': '4179', 'name': 'Toutatis', 'type': 'Apollo Group'},
                {'id': '4183', 'name': 'Cuno', 'type': 'Apollo Group'},
                {'id': '4450', 'name': 'Pan', 'type': 'Apollo Group'},
                {'id': '4660', 'name': 'Nereus', 'type': 'Apollo Group'},
                {'id': '4769', 'name': 'Castalia', 'type': 'Apollo Group'},
                {'id': '5143', 'name': 'Itokawa', 'type': 'Apollo Group'},
                {'id': '6489', 'name': 'Golevka', 'type': 'Apollo Group'},
                {'id': '25143', 'name': 'Itokawa', 'type': 'Apollo Group'},
                {'id': '99942', 'name': 'Apophis', 'type': 'Potentially Hazardous'},
                {'id': '101955', 'name': 'Bennu', 'type': 'Apollo Group'},
                {'id': '162173', 'name': 'Ryugu', 'type': 'Apollo Group'}
            ]
            
            return jsonify({
                'success': True,
                'count': len(notable_asteroids),
                'asteroids': notable_asteroids,
                'note': 'This list includes notable Near-Earth Objects, Potentially Hazardous Asteroids, and mission targets'
            })
            
        except Exception as e:
            logger.error(f"Notable asteroids list failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Notable asteroids list failed: {str(e)}'
            }), 500
    
    @app.route('/api/asteroids/list/search-all', methods=['GET'])
    def search_all_asteroids():
        """
        Search for asteroids without specific query (gets recent discoveries/notable ones)
        Query parameters: ?limit=50&neo_only=true&pha_only=false
        Returns: List of asteroids based on filters
        """
        try:
            limit = int(request.args.get('limit', 50))
            neo_only = request.args.get('neo_only', 'false').lower() == 'true'
            pha_only = request.args.get('pha_only', 'false').lower() == 'true'
            
            # Use JPL's query API to get a broader list
            search_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
            params = {
                'fields': 'spkid,full_name,neo,pha,H,diameter,class',
                'sb-kind': 'a',  # asteroids only
                'limit': limit
            }
            
            # Add filters based on parameters
            if neo_only:
                params['neo'] = '1'
            if pha_only:
                params['pha'] = '1'
            
            logger.info(f"Fetching asteroid list with limit: {limit}, NEO only: {neo_only}, PHA only: {pha_only}")
            
            import requests
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No asteroid data available'
                }), 404
            
            results = []
            for row in data['data']:
                if len(row) >= 7:  # Ensure we have all expected fields
                    results.append({
                        'id': str(row[0]),
                        'name': row[1],
                        'neo': row[2] == '1' if row[2] else False,
                        'pha': row[3] == '1' if row[3] else False,
                        'absolute_magnitude': float(row[4]) if row[4] else None,
                        'diameter_km': float(row[5]) if row[5] else None,
                        'class': row[6] if len(row) > 6 else None
                    })
            
            return jsonify({
                'success': True,
                'count': len(results),
                'filters': {
                    'limit': limit,
                    'neo_only': neo_only,
                    'pha_only': pha_only
                },
                'asteroids': results
            })
            
        except Exception as e:
            logger.error(f"Asteroid list search failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Asteroid list search failed: {str(e)}'
            }), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    print("🚀 Starting Asteroid Impact Modeling API...")
    print("🌍 Serving on http://localhost:5000")
    print("📡 API endpoints available at /api/")
    print("💡 Visit /api/info for full API documentation")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
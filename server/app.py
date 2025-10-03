"""
🌍☄️ Asteroid Impact Modeling API
NASA Space Apps 2024 - Flask Backend

Main Flask application providing REST API endpoints for asteroid impact modeling.
Integrates with React frontend for comprehensive impact analysis and visualization.
"""

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for React frontend
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nasa-space-apps-2024')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize managers
    nasa_api_manager = NASAAPIManager()
    viz_manager = VisualizationManager(nasa_api_manager)
    
    # Initialize controllers
    impact_controller = ImpactController(nasa_api_manager, viz_manager)
    scenario_controller = ScenarioController(nasa_api_manager, viz_manager)
    
    # Register blueprints
    app.register_blueprint(tsunami_bp)
    
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
                    'tsunami_risk_levels': '/api/tsunami/risk-levels'
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
                    'Tsunami risk assessment and coastal impact analysis'
                ],
                'external_apis': [
                    'Open-Elevation API for elevation data',
                    'USGS Earthquake API for seismic comparisons',
                    'Population density estimation algorithms'
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
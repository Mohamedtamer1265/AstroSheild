"""
🎯 Impact Analysis Controller
NASA Space Apps 2024

Controller for handling asteroid impact analysis requests from React frontend.
Provides endpoints for custom impact scenarios, parameter studies, and visualizations.
"""

from flask import request, jsonify
import logging
from typing import Dict, Any, List, Optional
import traceback

from models.asteroid_impact import AsteroidImpact
from utils.nasa_apis import NASAAPIManager
from utils.visualization import VisualizationManager

logger = logging.getLogger(__name__)


class ImpactController:
    """Controller for asteroid impact analysis endpoints."""
    
    def __init__(self, nasa_api_manager: NASAAPIManager, viz_manager: VisualizationManager):
        """Initialize controller with API and visualization managers."""
        self.nasa_api = nasa_api_manager
        self.viz_manager = viz_manager
    
    def analyze_impact(self, request) -> Dict[str, Any]:
        """
        Analyze a custom asteroid impact with comprehensive results.
        
        Expected request JSON:
        {
            "diameter_m": float,
            "velocity_km_s": float,
            "density_kg_m3": float (optional, default: 2600),
            "angle_degrees": float (optional, default: 45),
            "impact_lat": float,
            "impact_lon": float,
            "location_name": string (optional)
        }
        """
        try:
            # Validate request
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            # Required parameters
            required_params = ['diameter_m', 'velocity_km_s', 'impact_lat', 'impact_lon']
            missing_params = [param for param in required_params if param not in data]
            
            if missing_params:
                return jsonify({
                    'success': False,
                    'error': f'Missing required parameters: {", ".join(missing_params)}'
                }), 400
            
            # Validate coordinates
            coord_validation = self.nasa_api.validate_coordinates(
                data['impact_lat'], data['impact_lon']
            )
            
            if not coord_validation['valid']:
                return jsonify({
                    'success': False,
                    'error': 'Invalid coordinates',
                    'details': coord_validation['errors']
                }), 400
            
            # Create asteroid impact object
            asteroid = AsteroidImpact(
                diameter_m=float(data['diameter_m']),
                velocity_km_s=float(data['velocity_km_s']),
                density_kg_m3=float(data.get('density_kg_m3', 2600)),
                angle_degrees=float(data.get('angle_degrees', 45))
            )
            
            # Get comprehensive analysis
            analysis = asteroid.get_comprehensive_analysis()
            
            # Get regional impact data
            regional_data = self.nasa_api.get_regional_impact_data(
                data['impact_lat'], data['impact_lon']
            )
            
            # Calculate casualties if population data available
            casualties = {}
            if regional_data['regional_population']['status'] in ['success', 'fallback']:
                pop_data = regional_data['regional_population']
                casualties = asteroid.estimate_casualties(
                    pop_data['population_density_per_km2'],
                    pop_data['population_estimate']
                )
            
            # Create visualization data
            shake_map_data = self.viz_manager.create_shake_map_data(
                data['impact_lat'], data['impact_lon'], asteroid,
                title=data.get('location_name', 'Custom Impact')
            )
            
            chart_data = self.viz_manager.create_impact_chart_data(asteroid)
            
            # Prepare response
            response_data = {
                'success': True,
                'data': {
                    'asteroid_properties': analysis['asteroid_properties'],
                    'impact_location': {
                        'latitude': data['impact_lat'],
                        'longitude': data['impact_lon'],
                        'name': data.get('location_name', f"({data['impact_lat']:.3f}, {data['impact_lon']:.3f})"),
                        'elevation_m': regional_data['impact_location']['elevation_m']
                    },
                    'analysis': {
                        'energy': analysis['energy'],
                        'seismic': analysis['seismic'],
                        'crater': analysis['crater'],
                        'air_blast_ranges': analysis['air_blast_ranges']
                    },
                    'casualties': casualties,
                    'regional_data': regional_data,
                    'visualizations': {
                        'shake_map': shake_map_data,
                        'charts': chart_data
                    },
                    'summary': {
                        'energy_megatons': analysis['energy']['energy_tnt_megatons'],
                        'seismic_magnitude': analysis['seismic']['moment_magnitude'],
                        'crater_diameter_km': analysis['crater']['diameter_km'],
                        'max_damage_range_km': max(analysis['air_blast_ranges'].values()) if analysis['air_blast_ranges'] else 0,
                        'total_fatalities': casualties.get('totals', {}).get('fatalities', 0),
                        'total_injuries': casualties.get('totals', {}).get('injuries', 0)
                    }
                }
            }
            
            return jsonify(response_data)
            
        except ValueError as e:
            logger.error(f"Value error in analyze_impact: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid parameter values',
                'details': str(e)
            }), 400
            
        except Exception as e:
            logger.error(f"Error in analyze_impact: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'details': str(e)
            }), 500
    
    def create_custom_impact(self, request) -> Dict[str, Any]:
        """
        Create and analyze a custom impact scenario with simplified response.
        
        Expected request JSON: Same as analyze_impact
        """
        try:
            # Reuse the comprehensive analysis but provide simplified response
            full_response = self.analyze_impact(request)
            
            if isinstance(full_response, tuple):
                return full_response  # Error response
            
            # Extract key data for simplified response
            full_data = full_response.get_json()
            
            if not full_data.get('success'):
                return full_response
            
            data = full_data['data']
            
            simplified_response = {
                'success': True,
                'data': {
                    'impact_info': {
                        'location': data['impact_location'],
                        'asteroid': data['asteroid_properties']
                    },
                    'results': {
                        'energy_megatons': data['summary']['energy_megatons'],
                        'seismic_magnitude': data['summary']['seismic_magnitude'],
                        'crater_diameter_km': data['summary']['crater_diameter_km'],
                        'max_damage_range_km': data['summary']['max_damage_range_km']
                    },
                    'casualties': {
                        'fatalities': data['summary']['total_fatalities'],
                        'injuries': data['summary']['total_injuries']
                    },
                    'visualization_data': data['visualizations']
                }
            }
            
            return jsonify(simplified_response)
            
        except Exception as e:
            logger.error(f"Error in create_custom_impact: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to create custom impact',
                'details': str(e)
            }), 500
    
    def parameter_study(self, request) -> Dict[str, Any]:
        """
        Perform parameter sensitivity study.
        
        Expected request JSON:
        {
            "base_diameter_m": float,
            "impact_lat": float,
            "impact_lon": float,
            "parameter": string ("diameter", "velocity", "angle"),
            "values": [float, ...] (optional),
            "location_name": string (optional)
        }
        """
        try:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            # Required parameters
            required_params = ['base_diameter_m', 'impact_lat', 'impact_lon', 'parameter']
            missing_params = [param for param in required_params if param not in data]
            
            if missing_params:
                return jsonify({
                    'success': False,
                    'error': f'Missing required parameters: {", ".join(missing_params)}'
                }), 400
            
            parameter = data['parameter']
            
            # Validate parameter
            if parameter not in ['diameter', 'velocity', 'angle']:
                return jsonify({
                    'success': False,
                    'error': 'Parameter must be one of: diameter, velocity, angle'
                }), 400
            
            # Validate coordinates
            coord_validation = self.nasa_api.validate_coordinates(
                data['impact_lat'], data['impact_lon']
            )
            
            if not coord_validation['valid']:
                return jsonify({
                    'success': False,
                    'error': 'Invalid coordinates',
                    'details': coord_validation['errors']
                }), 400
            
            # Set default values for parameter study
            if 'values' not in data:
                if parameter == 'diameter':
                    values = [50, 100, 200, 500, 1000]  # meters
                elif parameter == 'velocity':
                    values = [10, 15, 20, 25, 30]  # km/s
                elif parameter == 'angle':
                    values = [15, 30, 45, 60, 90]  # degrees
            else:
                values = data['values']
            
            # Perform parameter study
            results = []
            base_diameter = float(data['base_diameter_m'])
            
            for value in values:
                if parameter == 'diameter':
                    asteroid = AsteroidImpact(value, 20, 2600, 45)
                elif parameter == 'velocity':
                    asteroid = AsteroidImpact(base_diameter, value, 2600, 45)
                elif parameter == 'angle':
                    asteroid = AsteroidImpact(base_diameter, 20, 2600, value)
                
                analysis = asteroid.get_comprehensive_analysis()
                blast = analysis['air_blast_ranges']
                
                result = {
                    'parameter_value': value,
                    'energy_mt': analysis['energy']['energy_tnt_megatons'],
                    'seismic_magnitude': analysis['seismic']['moment_magnitude'],
                    'crater_diameter_km': analysis['crater']['diameter_km'],
                    'crater_depth_m': analysis['crater']['depth_m'],
                    'severe_damage_km': blast.get('20_psi_km', 0),
                    'light_damage_km': blast.get('1_psi_km', 0),
                    'analysis': analysis
                }
                
                results.append(result)
            
            # Create chart data
            chart_data = self.viz_manager.create_parameter_study_chart(
                parameter, values, [r['analysis'] for r in results]
            )
            
            # Prepare response
            response_data = {
                'success': True,
                'data': {
                    'study_info': {
                        'parameter': parameter,
                        'base_diameter_m': base_diameter,
                        'location': {
                            'latitude': data['impact_lat'],
                            'longitude': data['impact_lon'],
                            'name': data.get('location_name', f"({data['impact_lat']:.3f}, {data['impact_lon']:.3f})")
                        },
                        'values_tested': values,
                        'total_scenarios': len(values)
                    },
                    'results': [
                        {
                            'parameter_value': r['parameter_value'],
                            'energy_mt': round(r['energy_mt'], 3),
                            'seismic_magnitude': round(r['seismic_magnitude'], 2),
                            'crater_diameter_km': round(r['crater_diameter_km'], 3),
                            'crater_depth_m': round(r['crater_depth_m'], 1),
                            'severe_damage_km': round(r['severe_damage_km'], 2),
                            'light_damage_km': round(r['light_damage_km'], 2)
                        }
                        for r in results
                    ],
                    'visualization': chart_data,
                    'summary': {
                        'parameter_range': {
                            'min': min(values),
                            'max': max(values)
                        },
                        'energy_range_mt': {
                            'min': round(min([r['energy_mt'] for r in results]), 3),
                            'max': round(max([r['energy_mt'] for r in results]), 3)
                        },
                        'damage_range_km': {
                            'min': round(min([r['severe_damage_km'] for r in results]), 2),
                            'max': round(max([r['severe_damage_km'] for r in results]), 2)
                        }
                    }
                }
            }
            
            return jsonify(response_data)
            
        except ValueError as e:
            logger.error(f"Value error in parameter_study: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Invalid parameter values',
                'details': str(e)
            }), 400
            
        except Exception as e:
            logger.error(f"Error in parameter_study: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'details': str(e)
            }), 500
    
    def generate_shake_map(self, request) -> Dict[str, Any]:
        """
        Generate shake map data for visualization.
        
        Expected request JSON:
        {
            "asteroid": {
                "diameter_m": float,
                "velocity_km_s": float,
                "density_kg_m3": float (optional),
                "angle_degrees": float (optional)
            },
            "impact_lat": float,
            "impact_lon": float,
            "title": string (optional)
        }
        """
        try:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            # Validate required parameters
            if 'asteroid' not in data or 'impact_lat' not in data or 'impact_lon' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameters: asteroid, impact_lat, impact_lon'
                }), 400
            
            asteroid_data = data['asteroid']
            required_asteroid_params = ['diameter_m', 'velocity_km_s']
            missing_params = [param for param in required_asteroid_params if param not in asteroid_data]
            
            if missing_params:
                return jsonify({
                    'success': False,
                    'error': f'Missing asteroid parameters: {", ".join(missing_params)}'
                }), 400
            
            # Create asteroid object
            asteroid = AsteroidImpact(
                diameter_m=float(asteroid_data['diameter_m']),
                velocity_km_s=float(asteroid_data['velocity_km_s']),
                density_kg_m3=float(asteroid_data.get('density_kg_m3', 2600)),
                angle_degrees=float(asteroid_data.get('angle_degrees', 45))
            )
            
            # Generate shake map data
            shake_map_data = self.viz_manager.create_shake_map_data(
                data['impact_lat'],
                data['impact_lon'],
                asteroid,
                data.get('title', 'Asteroid Impact Shake Map')
            )
            
            return jsonify({
                'success': True,
                'data': shake_map_data
            })
            
        except Exception as e:
            logger.error(f"Error in generate_shake_map: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to generate shake map',
                'details': str(e)
            }), 500
    
    def generate_impact_chart(self, request) -> Dict[str, Any]:
        """
        Generate impact analysis chart data.
        
        Expected request JSON: Same as generate_shake_map
        """
        try:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            # Validate required parameters
            if 'asteroid' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameter: asteroid'
                }), 400
            
            asteroid_data = data['asteroid']
            required_asteroid_params = ['diameter_m', 'velocity_km_s']
            missing_params = [param for param in required_asteroid_params if param not in asteroid_data]
            
            if missing_params:
                return jsonify({
                    'success': False,
                    'error': f'Missing asteroid parameters: {", ".join(missing_params)}'
                }), 400
            
            # Create asteroid object
            asteroid = AsteroidImpact(
                diameter_m=float(asteroid_data['diameter_m']),
                velocity_km_s=float(asteroid_data['velocity_km_s']),
                density_kg_m3=float(asteroid_data.get('density_kg_m3', 2600)),
                angle_degrees=float(asteroid_data.get('angle_degrees', 45))
            )
            
            # Generate chart data
            chart_data = self.viz_manager.create_impact_chart_data(asteroid)
            
            return jsonify({
                'success': True,
                'data': chart_data
            })
            
        except Exception as e:
            logger.error(f"Error in generate_impact_chart: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to generate impact chart',
                'details': str(e)
            }), 500
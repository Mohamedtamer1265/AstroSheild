"""
🎯 Scenario Management Controller
NASA Space Apps 2024

Controller for handling pre-defined asteroid impact scenarios.
Provides endpoints for scenario listing, execution, and comparison.
"""

from flask import request, jsonify
import logging
from typing import Dict, Any, List, Optional
import traceback

from models.scenarios import ImpactScenarios
from utils.nasa_apis import NASAAPIManager
from utils.visualization import VisualizationManager

logger = logging.getLogger(__name__)


class ScenarioController:
    """Controller for scenario management endpoints."""
    
    def __init__(self, nasa_api_manager: NASAAPIManager, viz_manager: VisualizationManager):
        """Initialize controller with API and visualization managers."""
        self.nasa_api = nasa_api_manager
        self.viz_manager = viz_manager
        self.scenarios = ImpactScenarios()
    
    def get_scenarios(self) -> Dict[str, Any]:
        """
        Get all available impact scenarios.
        
        Returns:
            JSON response with scenario information
        """
        try:
            scenarios = self.scenarios.get_scenarios()
            categories = self.scenarios.get_scenario_categories()
            
            # Organize scenarios for frontend
            scenario_list = []
            for name, scenario in scenarios.items():
                scenario_list.append({
                    'id': name,
                    'name': scenario['name'],
                    'description': scenario['description'],
                    'category': scenario.get('category', 'unknown'),
                    'historical': scenario.get('historical', False),
                    'location': scenario['location'],
                    'parameters': {
                        'diameter_m': scenario['diameter_m'],
                        'velocity_km_s': scenario['velocity_km_s'],
                        'density_kg_m3': scenario['density_kg_m3'],
                        'angle_degrees': scenario['angle_degrees']
                    }
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'scenarios': scenario_list,
                    'categories': categories,
                    'total_scenarios': len(scenario_list),
                    'historical_count': len([s for s in scenario_list if s['historical']]),
                    'category_counts': {cat: len(scenarios) for cat, scenarios in categories.items()}
                }
            })
            
        except Exception as e:
            logger.error(f"Error in get_scenarios: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve scenarios',
                'details': str(e)
            }), 500
    
    def get_scenario_details(self, scenario_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific scenario.
        
        Args:
            scenario_name (str): Name of the scenario
            
        Returns:
            JSON response with scenario details
        """
        try:
            scenario = self.scenarios.get_scenario_by_name(scenario_name)
            
            if not scenario:
                return jsonify({
                    'success': False,
                    'error': f'Scenario "{scenario_name}" not found'
                }), 404
            
            # Create asteroid for analysis preview
            asteroid = self.scenarios.create_asteroid_from_scenario(scenario_name)
            if not asteroid:
                return jsonify({
                    'success': False,
                    'error': 'Failed to create asteroid from scenario'
                }), 500
            
            # Get basic analysis
            analysis = asteroid.get_comprehensive_analysis()
            
            response_data = {
                'success': True,
                'data': {
                    'scenario_info': {
                        'id': scenario_name,
                        'name': scenario['name'],
                        'description': scenario['description'],
                        'category': scenario.get('category', 'unknown'),
                        'historical': scenario.get('historical', False),
                        'location': scenario['location']
                    },
                    'asteroid_parameters': {
                        'diameter_m': scenario['diameter_m'],
                        'velocity_km_s': scenario['velocity_km_s'],
                        'density_kg_m3': scenario['density_kg_m3'],
                        'angle_degrees': scenario['angle_degrees']
                    },
                    'preview_analysis': {
                        'energy_megatons': round(analysis['energy']['energy_tnt_megatons'], 3),
                        'seismic_magnitude': round(analysis['seismic']['moment_magnitude'], 2),
                        'crater_diameter_km': round(analysis['crater']['diameter_km'], 3),
                        'crater_depth_m': round(analysis['crater']['depth_m'], 1),
                        'max_damage_range_km': round(max(analysis['air_blast_ranges'].values()) if analysis['air_blast_ranges'] else 0, 2)
                    },
                    'damage_zones': {
                        'severe_destruction_km': analysis['air_blast_ranges'].get('20_psi_km', 0),
                        'heavy_damage_km': analysis['air_blast_ranges'].get('5_psi_km', 0),
                        'light_damage_km': analysis['air_blast_ranges'].get('1_psi_km', 0),
                        'thermal_burns_km': analysis['air_blast_ranges'].get('thermal_3rd_degree_km', 0)
                    }
                }
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Error in get_scenario_details: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve scenario details',
                'details': str(e)
            }), 500
    
    def run_scenario(self, scenario_name: str, request) -> Dict[str, Any]:
        """
        Run a pre-defined impact scenario with comprehensive analysis.
        
        Args:
            scenario_name (str): Name of the scenario to run
            request: Flask request object
            
        Expected request JSON (optional):
        {
            "custom_location": {
                "lat": float,
                "lon": float,
                "name": string (optional)
            }
        }
        """
        try:
            # Get scenario
            scenario = self.scenarios.get_scenario_by_name(scenario_name)
            
            if not scenario:
                return jsonify({
                    'success': False,
                    'error': f'Scenario "{scenario_name}" not found'
                }), 404
            
            # Check for custom location
            custom_location = None
            if request.is_json:
                data = request.get_json()
                if data and 'custom_location' in data:
                    custom_location = data['custom_location']
                    
                    # Validate custom location coordinates
                    if 'lat' in custom_location and 'lon' in custom_location:
                        coord_validation = self.nasa_api.validate_coordinates(
                            custom_location['lat'], custom_location['lon']
                        )
                        
                        if not coord_validation['valid']:
                            return jsonify({
                                'success': False,
                                'error': 'Invalid custom location coordinates',
                                'details': coord_validation['errors']
                            }), 400
            
            # Run scenario analysis
            scenario_results = self.scenarios.run_scenario_analysis(scenario_name, custom_location)
            
            if not scenario_results:
                return jsonify({
                    'success': False,
                    'error': 'Failed to analyze scenario'
                }), 500
            
            # Get regional impact data
            location = scenario_results['impact_location']
            regional_data = self.nasa_api.get_regional_impact_data(
                location['latitude'], location['longitude']
            )
            
            # Create asteroid object for casualty calculation
            asteroid = self.scenarios.create_asteroid_from_scenario(scenario_name)
            
            # Calculate casualties if population data available
            casualties = {}
            if regional_data['regional_population']['status'] in ['success', 'fallback']:
                pop_data = regional_data['regional_population']
                casualties = asteroid.estimate_casualties(
                    pop_data['population_density_per_km2'],
                    pop_data['population_estimate']
                )
            
            # Create visualizations
            shake_map_data = self.viz_manager.create_shake_map_data(
                location['latitude'], location['longitude'], asteroid,
                title=f"{scenario['name']} - {location['name']}"
            )
            
            chart_data = self.viz_manager.create_impact_chart_data(asteroid)
            
            # Prepare comprehensive response
            response_data = {
                'success': True,
                'data': {
                    'scenario_info': scenario_results['scenario_info'],
                    'impact_location': scenario_results['impact_location'],
                    'asteroid_data': scenario_results['asteroid_data'],
                    'analysis': scenario_results['analysis'],
                    'casualties': casualties,
                    'regional_data': regional_data,
                    'visualizations': {
                        'shake_map': shake_map_data,
                        'charts': chart_data
                    },
                    'summary': {
                        **scenario_results['summary'],
                        'total_fatalities': casualties.get('totals', {}).get('fatalities', 0),
                        'total_injuries': casualties.get('totals', {}).get('injuries', 0),
                        'affected_population': casualties.get('totals', {}).get('affected_population', 0)
                    },
                    'execution_info': {
                        'scenario_name': scenario_name,
                        'used_custom_location': custom_location is not None,
                        'location_source': 'custom' if custom_location else 'scenario_default'
                    }
                }
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Error in run_scenario: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Failed to run scenario',
                'details': str(e)
            }), 500
    
    def compare_scenarios(self, request) -> Dict[str, Any]:
        """
        Compare multiple impact scenarios.
        
        Expected request JSON:
        {
            "scenario_names": [string, ...],
            "comparison_metrics": [string, ...] (optional)
        }
        """
        try:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            if 'scenario_names' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameter: scenario_names'
                }), 400
            
            scenario_names = data['scenario_names']
            
            if not isinstance(scenario_names, list) or len(scenario_names) < 2:
                return jsonify({
                    'success': False,
                    'error': 'scenario_names must be a list with at least 2 scenarios'
                }), 400
            
            # Validate scenario names
            available_scenarios = self.scenarios.get_scenarios()
            invalid_scenarios = [name for name in scenario_names if name not in available_scenarios]
            
            if invalid_scenarios:
                return jsonify({
                    'success': False,
                    'error': f'Invalid scenario names: {", ".join(invalid_scenarios)}',
                    'available_scenarios': list(available_scenarios.keys())
                }), 400
            
            # Perform comparison
            comparison_results = self.scenarios.compare_scenarios(scenario_names)
            
            # Add additional analysis
            comparison_data = comparison_results['comparison_data']
            
            # Calculate relative scales
            if comparison_data:
                energy_values = [item['energy_mt'] for item in comparison_data]
                max_energy = max(energy_values)
                min_energy = min(energy_values)
                
                for item in comparison_data:
                    item['energy_scale_factor'] = item['energy_mt'] / min_energy if min_energy > 0 else 1
                    item['energy_percentage'] = (item['energy_mt'] / max_energy * 100) if max_energy > 0 else 0
            
            # Prepare response
            response_data = {
                'success': True,
                'data': {
                    'comparison_info': {
                        'scenarios_compared': scenario_names,
                        'total_scenarios': comparison_results['total_scenarios'],
                        'categories_included': comparison_results['categories'],
                        'comparison_metrics': [
                            'energy_mt', 'seismic_magnitude', 'crater_diameter_km',
                            'crater_depth_m', 'severe_damage_range_km', 'light_damage_range_km'
                        ]
                    },
                    'comparison_results': comparison_data,
                    'summary_statistics': {
                        'energy_range': comparison_results['energy_range'],
                        'size_range': comparison_results['size_range'],
                        'most_powerful': max(comparison_data, key=lambda x: x['energy_mt']) if comparison_data else None,
                        'least_powerful': min(comparison_data, key=lambda x: x['energy_mt']) if comparison_data else None,
                        'largest_crater': max(comparison_data, key=lambda x: x['crater_diameter_km']) if comparison_data else None,
                        'widest_damage': max(comparison_data, key=lambda x: x['light_damage_range_km']) if comparison_data else None
                    },
                    'visualization_data': {
                        'energy_comparison': [
                            {'scenario': item['display_name'], 'energy_mt': item['energy_mt']}
                            for item in comparison_data
                        ],
                        'damage_comparison': [
                            {
                                'scenario': item['display_name'],
                                'severe_km': item['severe_damage_range_km'],
                                'light_km': item['light_damage_range_km']
                            }
                            for item in comparison_data
                        ],
                        'size_comparison': [
                            {
                                'scenario': item['display_name'],
                                'diameter_m': item['diameter_m'],
                                'crater_km': item['crater_diameter_km']
                            }
                            for item in comparison_data
                        ]
                    }
                }
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Error in compare_scenarios: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': 'Failed to compare scenarios',
                'details': str(e)
            }), 500
    
    def search_scenarios(self, request) -> Dict[str, Any]:
        """
        Search scenarios by keyword.
        
        Expected request JSON:
        {
            "query": string
        }
        """
        try:
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            if 'query' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameter: query'
                }), 400
            
            query = data['query'].strip()
            
            if not query:
                return jsonify({
                    'success': False,
                    'error': 'Query cannot be empty'
                }), 400
            
            # Perform search
            search_results = self.scenarios.search_scenarios(query)
            
            # Format results
            formatted_results = []
            for result in search_results:
                scenario_name = result['scenario_name']
                scenario_data = result['scenario_data']
                
                formatted_results.append({
                    'scenario_id': scenario_name,
                    'name': scenario_data['name'],
                    'description': scenario_data['description'],
                    'category': scenario_data.get('category', 'unknown'),
                    'historical': scenario_data.get('historical', False),
                    'location': scenario_data['location'],
                    'parameters': {
                        'diameter_m': scenario_data['diameter_m'],
                        'velocity_km_s': scenario_data['velocity_km_s']
                    }
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'query': query,
                    'results': formatted_results,
                    'total_results': len(formatted_results)
                }
            })
            
        except Exception as e:
            logger.error(f"Error in search_scenarios: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to search scenarios',
                'details': str(e)
            }), 500
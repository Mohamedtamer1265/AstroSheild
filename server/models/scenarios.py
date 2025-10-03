"""
🎯 Impact Scenarios Management
NASA Space Apps 2024

Pre-defined asteroid impact scenarios based on historical events and potential threats.
Includes comparison and analysis tools for different impact scales.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from .asteroid_impact import AsteroidImpact


class ImpactScenarios:
    """Pre-defined impact scenarios for testing and comparison."""
    
    @staticmethod
    def get_scenarios() -> Dict[str, Dict[str, Any]]:
        """Return dictionary of pre-defined asteroid scenarios."""
        return {
            'chelyabinsk_2013': {
                'name': '2013 Chelyabinsk Event (Actual)',
                'diameter_m': 20,
                'velocity_km_s': 19.16,
                'density_kg_m3': 3300,
                'angle_degrees': 18,
                'description': 'Actual airburst over Russia in 2013. Injured ~1500 people.',
                'location': {'lat': 55.1544, 'lon': 61.4294, 'name': 'Chelyabinsk, Russia'},
                'historical': True,
                'category': 'small_event'
            },
            'tunguska_1908': {
                'name': '1908 Tunguska Event (Estimated)',
                'diameter_m': 60,
                'velocity_km_s': 27,
                'density_kg_m3': 2000,
                'angle_degrees': 30,
                'description': 'Massive airburst over Siberia. Flattened 2,000 km² of forest.',
                'location': {'lat': 60.8858, 'lon': 101.8942, 'name': 'Tunguska, Siberia'},
                'historical': True,
                'category': 'medium_event'
            },
            'apophis_potential': {
                'name': 'Apophis 2029 Close Approach',
                'diameter_m': 340,
                'velocity_km_s': 12.87,
                'density_kg_m3': 2600,
                'angle_degrees': 45,
                'description': 'Potentially hazardous asteroid - modeled impact scenario.',
                'location': {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York City, USA'},
                'historical': False,
                'category': 'city_killer'
            },
            'chicxulub_scale': {
                'name': 'Chicxulub-Scale Event (K-Pg Extinction)',
                'diameter_m': 10000,
                'velocity_km_s': 20,
                'density_kg_m3': 2600,
                'angle_degrees': 60,
                'description': 'Dinosaur extinction event scale impact (66 million years ago).',
                'location': {'lat': 21.4, 'lon': -89.5, 'name': 'Yucatan Peninsula, Mexico'},
                'historical': True,
                'category': 'extinction_event'
            },
            'city_killer': {
                'name': 'City Killer Scenario',
                'diameter_m': 140,
                'velocity_km_s': 18,
                'density_kg_m3': 2600,
                'angle_degrees': 45,
                'description': 'NASA threshold for city-destroying asteroid.',
                'location': {'lat': 35.6762, 'lon': 139.6503, 'name': 'Tokyo, Japan'},
                'historical': False,
                'category': 'city_killer'
            },
            'regional_disaster': {
                'name': 'Regional Disaster Scenario',
                'diameter_m': 500,
                'velocity_km_s': 25,
                'density_kg_m3': 2800,
                'angle_degrees': 30,
                'description': 'Regional-scale impact causing widespread damage.',
                'location': {'lat': 51.5074, 'lon': -0.1278, 'name': 'London, UK'},
                'historical': False,
                'category': 'regional_disaster'
            },
            'small_meteor': {
                'name': 'Small Meteor Event',
                'diameter_m': 5,
                'velocity_km_s': 15,
                'density_kg_m3': 3000,
                'angle_degrees': 45,
                'description': 'Typical small meteor event - usually burns up in atmosphere.',
                'location': {'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles, USA'},
                'historical': False,
                'category': 'small_event'
            },
            'planetary_defense_test': {
                'name': 'Planetary Defense Test Case',
                'diameter_m': 250,
                'velocity_km_s': 22,
                'density_kg_m3': 2400,
                'angle_degrees': 35,
                'description': 'Test case for planetary defense systems and impact mitigation.',
                'location': {'lat': 48.8566, 'lon': 2.3522, 'name': 'Paris, France'},
                'historical': False,
                'category': 'city_killer'
            }
        }
    
    @staticmethod
    def get_scenario_by_name(scenario_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific scenario by name."""
        scenarios = ImpactScenarios.get_scenarios()
        return scenarios.get(scenario_name)
    
    @staticmethod
    def get_scenarios_by_category(category: str) -> Dict[str, Dict[str, Any]]:
        """Get all scenarios in a specific category."""
        scenarios = ImpactScenarios.get_scenarios()
        return {k: v for k, v in scenarios.items() if v.get('category') == category}
    
    @staticmethod
    def get_historical_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get all historical scenarios."""
        scenarios = ImpactScenarios.get_scenarios()
        return {k: v for k, v in scenarios.items() if v.get('historical', False)}
    
    @staticmethod
    def create_asteroid_from_scenario(scenario_name: str) -> Optional[AsteroidImpact]:
        """Create an AsteroidImpact object from a scenario."""
        scenario = ImpactScenarios.get_scenario_by_name(scenario_name)
        if not scenario:
            return None
        
        return AsteroidImpact(
            diameter_m=scenario['diameter_m'],
            velocity_km_s=scenario['velocity_km_s'],
            density_kg_m3=scenario['density_kg_m3'],
            angle_degrees=scenario['angle_degrees']
        )
    
    @staticmethod
    def run_scenario_analysis(scenario_name: str, custom_location: Optional[Dict[str, float]] = None) -> Optional[Dict[str, Any]]:
        """
        Run comprehensive analysis for a scenario.
        
        Args:
            scenario_name (str): Name of the scenario
            custom_location (dict): Optional custom location {'lat': float, 'lon': float}
            
        Returns:
            dict: Complete scenario analysis
        """
        scenario = ImpactScenarios.get_scenario_by_name(scenario_name)
        if not scenario:
            return None
        
        # Create asteroid object
        asteroid = ImpactScenarios.create_asteroid_from_scenario(scenario_name)
        if not asteroid:
            return None
        
        # Determine impact location
        if custom_location:
            impact_lat = custom_location['lat']
            impact_lon = custom_location['lon']
            location_name = custom_location.get('name', f"({impact_lat:.3f}, {impact_lon:.3f})")
        else:
            impact_lat = scenario['location']['lat']
            impact_lon = scenario['location']['lon']
            location_name = scenario['location']['name']
        
        # Get comprehensive analysis
        analysis = asteroid.get_comprehensive_analysis()
        
        return {
            'scenario_info': scenario,
            'asteroid_data': asteroid.to_dict(),
            'impact_location': {
                'latitude': impact_lat,
                'longitude': impact_lon,
                'name': location_name
            },
            'analysis': analysis,
            'summary': {
                'energy_megatons': analysis['energy']['energy_tnt_megatons'],
                'seismic_magnitude': analysis['seismic']['moment_magnitude'],
                'crater_diameter_km': analysis['crater']['diameter_km'],
                'crater_depth_m': analysis['crater']['depth_m'],
                'severe_damage_radius_km': analysis['air_blast_ranges'].get('20_psi_km', 0),
                'light_damage_radius_km': analysis['air_blast_ranges'].get('1_psi_km', 0)
            }
        }
    
    @staticmethod
    def compare_scenarios(scenario_names: List[str]) -> Dict[str, Any]:
        """
        Compare multiple impact scenarios.
        
        Args:
            scenario_names (list): List of scenario names to compare
            
        Returns:
            dict: Comparison data including DataFrame-compatible structure
        """
        scenarios = ImpactScenarios.get_scenarios()
        results = []
        valid_scenarios = []
        
        for name in scenario_names:
            if name not in scenarios:
                continue
                
            scenario = scenarios[name]
            asteroid = AsteroidImpact(
                diameter_m=scenario['diameter_m'],
                velocity_km_s=scenario['velocity_km_s'],
                density_kg_m3=scenario['density_kg_m3'],
                angle_degrees=scenario['angle_degrees']
            )
            
            analysis = asteroid.get_comprehensive_analysis()
            
            result = {
                'scenario_name': name,
                'display_name': scenario['name'],
                'category': scenario.get('category', 'unknown'),
                'historical': scenario.get('historical', False),
                'diameter_m': scenario['diameter_m'],
                'velocity_km_s': scenario['velocity_km_s'],
                'energy_mt': round(analysis['energy']['energy_tnt_megatons'], 3),
                'seismic_magnitude': round(analysis['seismic']['moment_magnitude'], 2),
                'crater_diameter_km': round(analysis['crater']['diameter_km'], 3),
                'crater_depth_m': round(analysis['crater']['depth_m'], 1),
                'severe_damage_range_km': round(analysis['air_blast_ranges'].get('20_psi_km', 0), 2),
                'light_damage_range_km': round(analysis['air_blast_ranges'].get('1_psi_km', 0), 2),
                'thermal_range_km': round(analysis['air_blast_ranges'].get('thermal_3rd_degree_km', 0), 2)
            }
            
            results.append(result)
            valid_scenarios.append(name)
        
        # Sort by energy for better comparison
        results.sort(key=lambda x: x['energy_mt'])
        
        return {
            'comparison_data': results,
            'valid_scenarios': valid_scenarios,
            'total_scenarios': len(results),
            'categories': list(set([r['category'] for r in results])),
            'energy_range': {
                'min_mt': min([r['energy_mt'] for r in results]) if results else 0,
                'max_mt': max([r['energy_mt'] for r in results]) if results else 0
            },
            'size_range': {
                'min_diameter_m': min([r['diameter_m'] for r in results]) if results else 0,
                'max_diameter_m': max([r['diameter_m'] for r in results]) if results else 0
            }
        }
    
    @staticmethod
    def get_scenario_categories() -> Dict[str, List[str]]:
        """Get scenarios organized by category."""
        scenarios = ImpactScenarios.get_scenarios()
        categories = {}
        
        for name, scenario in scenarios.items():
            category = scenario.get('category', 'unknown')
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        
        return categories
    
    @staticmethod
    def search_scenarios(query: str) -> List[Dict[str, Any]]:
        """
        Search scenarios by name or description.
        
        Args:
            query (str): Search query
            
        Returns:
            list: Matching scenarios
        """
        scenarios = ImpactScenarios.get_scenarios()
        results = []
        query_lower = query.lower()
        
        for name, scenario in scenarios.items():
            if (query_lower in name.lower() or 
                query_lower in scenario['name'].lower() or 
                query_lower in scenario['description'].lower()):
                
                results.append({
                    'scenario_name': name,
                    'scenario_data': scenario
                })
        
        return results
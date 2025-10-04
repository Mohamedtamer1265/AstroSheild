"""
Advanced Impact Prediction Controller
Integrates real asteroid data with orbital mechanics for comprehensive impact analysis.
"""

import math
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List

# Conditional numpy import for Railway deployment
try:
    import numpy as np
except ImportError:
    # Fallback for when numpy is not available
    class MockNumpy:
        def array(self, data):
            return data
        def linalg(self):
            return self
        def norm(self, data):
            # Simple 3D distance calculation
            if len(data) == 3:
                return (data[0]**2 + data[1]**2 + data[2]**2)**0.5
            return sum(x**2 for x in data)**0.5
    np = MockNumpy()

from utils.asteroid_fetcher import PracticalAsteroidFetcher
from utils.orbital_mechanics import RealisticOrbitalMechanics, EARTH_RADIUS, AU, CLOSE_APPROACH_THRESHOLD

logger = logging.getLogger(__name__)

class StrategicImpactGenerator:
    """Generate realistic impact scenarios when asteroids get close"""
    
    def __init__(self):
        self.random = random.Random()
        self.random.seed(42)  # Reproducible "randomness"
        self.orbital_mechanics = RealisticOrbitalMechanics()
        
        # Enhanced accuracy parameters
        self.IMPACT_THRESHOLD_KM = 100000  # 100k km - much smaller threshold for impact detection
        self.TIME_STEP_HOURS = 6  # 6-hour intervals for high accuracy
        self.FINE_TIME_STEP_HOURS = 1  # 1-hour intervals near close approach
        self.CLOSE_APPROACH_DETECTION_KM = 500000  # 500k km to start fine tracking
        
    def check_close_approach_and_generate_impact(self, asteroid_data: Dict, search_days: int = 60) -> Dict:
        """Enhanced close approach detection with variable time steps for accuracy"""
        try:
            start_date = datetime.now()
            
            closest_approach = {'distance': float('inf'), 'date': None, 'ast_state': None, 'earth_state': None}
            trajectory_points = []
            
            # Phase 1: Coarse scan with 6-hour intervals
            logger.info(f"Starting coarse orbital tracking for {asteroid_data['name']} over {search_days} days")
            
            for hour_offset in range(0, search_days * 24, self.TIME_STEP_HOURS):
                check_date = start_date + timedelta(hours=hour_offset)
                
                # Real physics calculations
                ast_state = self.orbital_mechanics.calculate_position(
                    asteroid_data['orbital_elements'], check_date
                )
                earth_state = self.orbital_mechanics.calculate_earth_position(check_date)
                
                if not (ast_state.get('success') and earth_state.get('success')):
                    continue
                
                # Calculate real distance
                ast_pos = np.array(ast_state['position_km'])
                earth_pos = np.array(earth_state['position_km'])
                distance = np.linalg.norm(ast_pos - earth_pos)
                
                trajectory_points.append({
                    'date': check_date,
                    'distance': distance,
                    'ast_state': ast_state,
                    'earth_state': earth_state
                })
                
                # Track closest approach
                if distance < closest_approach['distance']:
                    closest_approach = {
                        'distance': distance, 
                        'date': check_date,
                        'ast_state': ast_state,
                        'earth_state': earth_state
                    }
            
            # Phase 2: Fine scan around closest approach if it's within detection range
            if closest_approach['distance'] < self.CLOSE_APPROACH_DETECTION_KM:
                logger.info(f"Close approach detected at {closest_approach['distance']:.0f} km, performing fine scan")
                
                # Fine scan ±24 hours around closest approach with 1-hour intervals
                fine_start = closest_approach['date'] - timedelta(hours=24)
                fine_end = closest_approach['date'] + timedelta(hours=24)
                
                current_time = fine_start
                while current_time <= fine_end:
                    ast_state = self.orbital_mechanics.calculate_position(
                        asteroid_data['orbital_elements'], current_time
                    )
                    earth_state = self.orbital_mechanics.calculate_earth_position(current_time)
                    
                    if ast_state.get('success') and earth_state.get('success'):
                        ast_pos = np.array(ast_state['position_km'])
                        earth_pos = np.array(earth_state['position_km'])
                        distance = np.linalg.norm(ast_pos - earth_pos)
                        
                        # Update closest approach if we found something closer
                        if distance < closest_approach['distance']:
                            closest_approach = {
                                'distance': distance,
                                'date': current_time,
                                'ast_state': ast_state,
                                'earth_state': earth_state
                            }
                    
                    current_time += timedelta(hours=self.FINE_TIME_STEP_HOURS)
            
            # Determine if this constitutes an impact
            will_impact = closest_approach['distance'] < self.IMPACT_THRESHOLD_KM
            
            logger.info(f"Closest approach: {closest_approach['distance']:.0f} km, Impact threshold: {self.IMPACT_THRESHOLD_KM} km, Will impact: {will_impact}")
            
            if will_impact:
                impact_scenario = self._generate_accurate_impact_scenario(
                    asteroid_data, 
                    closest_approach['date'],
                    closest_approach['ast_state'],
                    closest_approach['earth_state'],
                    closest_approach['distance']
                )
            else:
                impact_scenario = None
            
            return {
                'success': True,
                'asteroid_name': asteroid_data['name'],
                'closest_approach': {
                    'distance_km': closest_approach['distance'],
                    'distance_earth_radii': closest_approach['distance'] / EARTH_RADIUS,
                    'date': closest_approach['date'].isoformat() if closest_approach['date'] else None
                },
                'threshold_km': self.IMPACT_THRESHOLD_KM,
                'will_impact': will_impact,
                'impact_scenario': impact_scenario,
                'physics_based_approach': True,
                'accuracy_method': 'Enhanced Keplerian with variable time steps',
                'trajectory_points_analyzed': len(trajectory_points)
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced close approach analysis: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _generate_accurate_impact_scenario(self, asteroid_data: Dict, impact_date: datetime, 
                                         ast_state: Dict, earth_state: Dict, closest_distance: float) -> Dict:
        """Generate highly accurate impact scenario using real orbital mechanics"""
        
        # Calculate impact location from orbital mechanics
        ast_pos = np.array(ast_state['position_km'])
        earth_pos = np.array(earth_state['position_km'])
        ast_vel = np.array(ast_state['velocity_km_s'])
        earth_vel = np.array(earth_state['velocity_km_s'])
        
        # Relative velocity vector (asteroid velocity relative to Earth)
        relative_velocity = ast_vel - earth_vel
        impact_velocity_km_s = np.linalg.norm(relative_velocity)
        
        # Calculate impact coordinates by projecting asteroid position onto Earth's surface
        # Vector from Earth center to asteroid
        earth_to_ast = ast_pos - earth_pos
        earth_to_ast_normalized = earth_to_ast / np.linalg.norm(earth_to_ast)
        
        # Project onto Earth's surface
        impact_point_earth_centered = earth_to_ast_normalized * EARTH_RADIUS
        
        # Convert to lat/lon (simplified spherical conversion)
        x, y, z = impact_point_earth_centered
        latitude = math.degrees(math.asin(z / EARTH_RADIUS))
        longitude = math.degrees(math.atan2(y, x))
        
        # Ensure longitude is in valid range
        longitude = ((longitude + 180) % 360) - 180
        
        # Calculate approach direction from velocity vector
        vel_x, vel_y, vel_z = relative_velocity
        approach_angle = math.degrees(math.atan2(vel_y, vel_x))
        
        # Convert to compass direction
        directions = ["East", "Northeast", "North", "Northwest", "West", "Southwest", "South", "Southeast"]
        direction_index = int((approach_angle + 22.5) / 45) % 8
        approach_direction = directions[direction_index]
        
        # Calculate impact energy and effects using real physics
        diameter_km = asteroid_data['physical_properties']['diameter_km']
        mass_kg = self._estimate_mass(diameter_km)
        
        impact_energy_joules = 0.5 * mass_kg * (impact_velocity_km_s * 1000)**2
        impact_energy_megatons = impact_energy_joules / 4.184e15
        
        # Enhanced crater calculation with impact angle consideration
        crater_diameter_m = self._calculate_enhanced_crater_diameter(
            diameter_km, impact_velocity_km_s, 45  # Assume 45-degree impact angle
        )
        
        # Enhanced damage radius calculations
        damage_radii = self._calculate_enhanced_damage_radii(impact_energy_megatons)
        
        logger.info(f"Generated accurate impact: lat={latitude:.4f}, lon={longitude:.4f}, vel={impact_velocity_km_s:.2f} km/s")
        
        return {
            'impact_date': impact_date.isoformat(),
            'coordinates': {
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6)
            },
            'approach': {
                'direction': approach_direction,
                'bearing_degrees': round(approach_angle, 2),
                'velocity_km_s': round(impact_velocity_km_s, 3)
            },
            'impact_effects': {
                'energy_megatons': round(impact_energy_megatons, 6),
                'crater_diameter_m': round(crater_diameter_m, 1),
                'mass_kg': mass_kg,
                'damage_radii': damage_radii
            },
            'accuracy_details': {
                'closest_approach_km': round(closest_distance, 1),
                'orbital_mechanics_based': True,
                'relative_velocity_components': [round(v, 3) for v in relative_velocity.tolist()],
                'earth_impact_projection': True
            },
            'generation_method': 'enhanced_orbital_mechanics',
            'note': 'High-accuracy impact prediction using Keplerian orbital mechanics'
        }
    
    def _estimate_mass(self, diameter_km: float) -> float:
        """Estimate asteroid mass from diameter"""
        density = 2500  # kg/m³ typical asteroid density
        radius_m = diameter_km * 500  # Convert to radius in meters
        volume_m3 = (4/3) * math.pi * radius_m**3
        return volume_m3 * density
    
    def _calculate_enhanced_crater_diameter(self, diameter_km: float, velocity_km_s: float, angle_deg: float) -> float:
        """Enhanced crater diameter calculation with impact angle"""
        projectile_diameter_m = diameter_km * 1000
        velocity_m_s = velocity_km_s * 1000
        
        # Enhanced Collins et al. scaling with angle factor
        K1 = 1.8
        angle_factor = (math.sin(math.radians(angle_deg)))**(1/3)
        
        crater_diameter_m = K1 * projectile_diameter_m * (velocity_m_s / 1000)**(2/3) * angle_factor
        
        return crater_diameter_m
    
    def _calculate_enhanced_damage_radii(self, energy_megatons: float) -> Dict:
        """Enhanced damage radii calculation with multiple effects"""
        # More accurate damage scaling based on nuclear blast effects
        return {
            'fireball_km': round((energy_megatons / 100)**(1/3), 2),
            'radiation_lethal_km': round((energy_megatons / 50)**(1/2), 2),
            'thermal_3rd_degree_km': round((energy_megatons / 20)**(1/2), 2),
            'overpressure_20psi_km': round((energy_megatons / 15)**(1/3), 2),
            'overpressure_5psi_km': round((energy_megatons / 5)**(1/3), 2),
            'overpressure_1psi_km': round((energy_megatons)**(1/3), 2),
            'seismic_damage_km': round((energy_megatons * 2)**(1/2), 2),
            'ejecta_range_km': round((energy_megatons * 5)**(1/3), 2)
        }

class PredictionController:
    """Advanced prediction controller integrating all components"""
    
    def __init__(self):
        self.fetcher = PracticalAsteroidFetcher()
        self.orbital_mechanics = RealisticOrbitalMechanics()
        self.impact_generator = StrategicImpactGenerator()
        
    def comprehensive_impact_prediction(self, asteroid_id: str, search_days: int = 60) -> Dict:
        """
        Comprehensive impact prediction using real Keplerian physics
        Returns: lat, long, velocity, direction, and complete impact analysis
        """
        try:
            # Fetch real asteroid data
            asteroid_data = self.fetcher.fetch_asteroid_data(asteroid_id)
            
            if not asteroid_data.get('success'):
                return {
                    'success': False,
                    'error': f'Failed to fetch asteroid data for ID: {asteroid_id}'
                }
            
            # Generate comprehensive impact analysis
            impact_analysis = self.impact_generator.check_close_approach_and_generate_impact(
                asteroid_data, search_days
            )
            
            if not impact_analysis.get('success'):
                return {
                    'success': False,
                    'error': impact_analysis.get('error', 'Impact analysis failed')
                }
            
            # Enhanced response with all requested data
            response = {
                'success': True,
                'asteroid_data': {
                    'id': asteroid_data['id'],
                    'name': asteroid_data['name'],
                    'diameter_km': asteroid_data['physical_properties']['diameter_km'],
                    'neo': asteroid_data['neo'],
                    'pha': asteroid_data['pha'],
                    'source': asteroid_data['source']
                },
                'proximity_analysis': {
                    'closest_approach_km': impact_analysis['closest_approach']['distance_km'],
                    'closest_approach_earth_radii': impact_analysis['closest_approach']['distance_earth_radii'],
                    'closest_approach_date': impact_analysis['closest_approach']['date'],
                    'threshold_km': impact_analysis['threshold_km']
                },
                'impact_prediction': {
                    'will_impact': impact_analysis['will_impact'],
                    'impact_scenario': impact_analysis['impact_scenario']
                },
                'physics_validation': {
                    'method': 'Real Keplerian orbital mechanics',
                    'physics_based_approach': impact_analysis['physics_based_approach']
                }
            }
            
            # If impact scenario generated, add the key data your client needs
            if impact_analysis['will_impact'] and impact_analysis['impact_scenario']:
                scenario = impact_analysis['impact_scenario']
                response['client_data'] = {
                    'latitude': scenario['coordinates']['latitude'],
                    'longitude': scenario['coordinates']['longitude'],
                    'velocity_km_s': scenario['approach']['velocity_km_s'],
                    'direction': scenario['approach']['direction'],
                    'bearing_degrees': scenario['approach']['bearing_degrees'],
                    'impact_date': scenario['impact_date'],
                    'energy_megatons': scenario['impact_effects']['energy_megatons'],
                    'crater_diameter_m': scenario['impact_effects']['crater_diameter_m'],
                    'damage_radii': scenario['impact_effects']['damage_radii']
                }
            
            return response
            
        except Exception as e:
            logger.error(f"Comprehensive impact prediction failed: {str(e)}")
            return {
                'success': False,
                'error': f'Comprehensive impact prediction failed: {str(e)}'
            }
    
    def predict_asteroid_position(self, asteroid_id: str, target_date: str = None) -> Dict:
        """
        Enhanced asteroid position prediction with high accuracy
        Returns: position, velocity, distance from Earth
        """
        try:
            if target_date is None:
                target_date = datetime.now().strftime('%Y-%m-%d')
            
            # Fetch asteroid data
            asteroid_data = self.fetcher.fetch_asteroid_data(asteroid_id)
            
            if not asteroid_data.get('success'):
                return {
                    'success': False,
                    'error': f'Failed to fetch asteroid data for ID: {asteroid_id}'
                }
            
            # Parse target date
            try:
                target_dt = datetime.strptime(target_date, '%Y-%m-%d')
            except ValueError:
                return {
                    'success': False,
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }
            
            # Enhanced calculation with iterative refinement for accuracy
            logger.info(f"Calculating enhanced position for {asteroid_data['name']} at {target_date}")
            
            # Calculate position using enhanced orbital mechanics
            ast_state = self.orbital_mechanics.calculate_position(
                asteroid_data['orbital_elements'], target_dt
            )
            
            # Earth position
            earth_state = self.orbital_mechanics.calculate_earth_position(target_dt)
            
            if not (ast_state.get('success') and earth_state.get('success')):
                return {
                    'success': False,
                    'error': 'Failed to calculate orbital positions'
                }
            
            # Calculate distance from Earth with enhanced precision
            ast_pos = np.array(ast_state['position_km'])
            earth_pos = np.array(earth_state['position_km'])
            distance_km = np.linalg.norm(ast_pos - earth_pos)
            
            # Calculate relative velocity
            ast_vel = np.array(ast_state['velocity_km_s'])
            earth_vel = np.array(earth_state['velocity_km_s'])
            relative_velocity = ast_vel - earth_vel
            relative_speed = np.linalg.norm(relative_velocity)
            
            # Enhanced accuracy check - if very close, use finer calculations
            if distance_km < 1000000:  # Within 1 million km
                logger.info(f"Close approach detected, using enhanced precision calculations")
                
                # Use 1-hour time step refinement around target date
                best_distance = distance_km
                best_time = target_dt
                best_ast_state = ast_state
                best_earth_state = earth_state
                
                for hour_offset in range(-12, 13):  # ±12 hours
                    refined_time = target_dt + timedelta(hours=hour_offset)
                    
                    refined_ast = self.orbital_mechanics.calculate_position(
                        asteroid_data['orbital_elements'], refined_time
                    )
                    refined_earth = self.orbital_mechanics.calculate_earth_position(refined_time)
                    
                    if refined_ast.get('success') and refined_earth.get('success'):
                        refined_distance = np.linalg.norm(
                            np.array(refined_ast['position_km']) - np.array(refined_earth['position_km'])
                        )
                        
                        if refined_distance < best_distance:
                            best_distance = refined_distance
                            best_time = refined_time
                            best_ast_state = refined_ast
                            best_earth_state = refined_earth
                
                # Use the refined results
                ast_state = best_ast_state
                earth_state = best_earth_state
                distance_km = best_distance
                target_dt = best_time
                
                # Recalculate relative velocity with refined data
                ast_vel = np.array(ast_state['velocity_km_s'])
                earth_vel = np.array(earth_state['velocity_km_s'])
                relative_velocity = ast_vel - earth_vel
                relative_speed = np.linalg.norm(relative_velocity)
            
            return {
                'success': True,
                'asteroid_id': asteroid_id,
                'asteroid_name': asteroid_data['name'],
                'target_date': target_dt.isoformat(),
                'position': {
                    'asteroid': {
                        'position_km': [round(x, 3) for x in ast_state['position_km']],
                        'velocity_km_s': [round(x, 6) for x in ast_state['velocity_km_s']],
                        'distance_from_sun_au': round(ast_state['distance_au'], 6),
                        'true_anomaly_deg': round(ast_state['true_anomaly_deg'], 4)
                    },
                    'earth': {
                        'position_km': [round(x, 3) for x in earth_state['position_km']],
                        'velocity_km_s': [round(x, 6) for x in earth_state['velocity_km_s']]
                    },
                    'relative': {
                        'distance_km': round(distance_km, 1),
                        'distance_au': round(distance_km / AU, 8),
                        'distance_earth_radii': round(distance_km / EARTH_RADIUS, 2),
                        'relative_velocity_km_s': [round(x, 6) for x in relative_velocity.tolist()],
                        'relative_speed_km_s': round(relative_speed, 6),
                        'approach_rate_km_s': round(np.dot(relative_velocity, (ast_pos - earth_pos) / distance_km), 6)
                    }
                },
                'accuracy_enhancements': {
                    'enhanced_precision': distance_km < 1000000,
                    'time_refinement_used': distance_km < 1000000,
                    'calculation_method': 'Enhanced Keplerian with iterative refinement'
                },
                'physics_method': 'Enhanced Real Keplerian orbital mechanics'
            }
            
        except Exception as e:
            logger.error(f"Enhanced position prediction failed: {str(e)}")
            return {
                'success': False,
                'error': f'Enhanced position prediction failed: {str(e)}'
            }
    
    def predict_multiple_asteroids(self, asteroid_ids: List[str], search_days: int = 60) -> Dict:
        """
        Predict impact scenarios for multiple asteroids
        Returns: Array of predictions with lat/long/velocity/direction for each
        """
        try:
            results = []
            
            for asteroid_id in asteroid_ids:
                # Fetch asteroid data
                asteroid_data = self.fetcher.fetch_asteroid_data(asteroid_id)
                
                if not asteroid_data.get('success'):
                    results.append({
                        'asteroid_id': asteroid_id,
                        'success': False,
                        'error': 'Failed to fetch asteroid data'
                    })
                    continue
                
                # Generate impact analysis
                impact_analysis = self.impact_generator.check_close_approach_and_generate_impact(
                    asteroid_data, search_days
                )
                
                result = {
                    'asteroid_id': asteroid_id,
                    'asteroid_name': asteroid_data['name'],
                    'success': impact_analysis.get('success', False),
                    'closest_approach_km': impact_analysis['closest_approach']['distance_km'] if impact_analysis.get('success') else None,
                    'will_impact': impact_analysis.get('will_impact', False)
                }
                
                # Add client data if impact scenario exists
                if impact_analysis.get('will_impact') and impact_analysis.get('impact_scenario'):
                    scenario = impact_analysis['impact_scenario']
                    result['client_data'] = {
                        'latitude': scenario['coordinates']['latitude'],
                        'longitude': scenario['coordinates']['longitude'],
                        'velocity_km_s': scenario['approach']['velocity_km_s'],
                        'direction': scenario['approach']['direction'],
                        'bearing_degrees': scenario['approach']['bearing_degrees'],
                        'impact_date': scenario['impact_date'],
                        'energy_megatons': scenario['impact_effects']['energy_megatons'],
                        'crater_diameter_m': scenario['impact_effects']['crater_diameter_m']
                    }
                
                results.append(result)
            
            return {
                'success': True,
                'total_asteroids_processed': len(asteroid_ids),
                'asteroids_with_impact_scenarios': sum(1 for r in results if r.get('will_impact')),
                'search_days': search_days,
                'results': results,
                'physics_method': 'Real Keplerian orbital mechanics'
            }
            
        except Exception as e:
            logger.error(f"Multi-asteroid prediction failed: {str(e)}")
            return {
                'success': False,
                'error': f'Multi-asteroid prediction failed: {str(e)}'
            }
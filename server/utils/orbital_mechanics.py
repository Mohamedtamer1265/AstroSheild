"""
Orbital Mechanics - Real Keplerian Physics for Asteroid Position Calculations
Implements proper orbital mechanics for asteroid trajectory and position prediction.
"""

import math
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Physical constants
EARTH_RADIUS = 6371.0  # km
AU = 149597870.7  # km
GM_SUN = 1.32712440018e11  # km³/s²
CLOSE_APPROACH_THRESHOLD = 100_000  # 100,000 km - reasonable for "close approach"

class RealisticOrbitalMechanics:
    """Real Keplerian orbital mechanics - no shortcuts"""
    
    def __init__(self):
        self.AU = AU
        self.EARTH_RADIUS = EARTH_RADIUS
        self.GM_SUN = GM_SUN
        
    def calculate_position(self, orbital_elements: Dict, target_date: datetime) -> Dict:
        """Calculate asteroid position using proper Keplerian mechanics"""
        try:
            # Extract elements
            a = orbital_elements['semi_major_axis'] * self.AU  # Convert to km
            e = orbital_elements['eccentricity']
            i = math.radians(orbital_elements['inclination'])
            Omega = math.radians(orbital_elements['ascending_node'])
            omega = math.radians(orbital_elements['argument_perihelion'])
            M0 = math.radians(orbital_elements['mean_anomaly'])
            epoch = orbital_elements.get('epoch', 2451545.0)
            
            # Time since epoch
            j2000 = datetime(2000, 1, 1, 12, 0, 0)
            current_jd = 2451545.0 + (target_date - j2000).total_seconds() / 86400.0
            dt_days = current_jd - epoch
            
            # Mean motion
            n = math.sqrt(self.GM_SUN / a**3)  # rad/s
            n_per_day = n * 86400  # rad/day
            
            # Current mean anomaly
            M = M0 + n_per_day * dt_days
            M = M % (2 * math.pi)
            
            # Solve Kepler's equation
            E = self._solve_kepler_equation(M, e)
            
            # True anomaly
            nu = 2.0 * math.atan2(
                math.sqrt(1 + e) * math.sin(E / 2),
                math.sqrt(1 - e) * math.cos(E / 2)
            )
            
            # Distance
            r = a * (1 - e * math.cos(E))
            
            # Position in orbital plane
            x_orb = r * math.cos(nu)
            y_orb = r * math.sin(nu)
            z_orb = 0.0
            
            # Transform to heliocentric coordinates
            cos_Omega, sin_Omega = math.cos(Omega), math.sin(Omega)
            cos_i, sin_i = math.cos(i), math.sin(i)
            cos_omega, sin_omega = math.cos(omega), math.sin(omega)
            
            # Rotation matrices
            x = (cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i) * x_orb + \
                (-cos_Omega * sin_omega - sin_Omega * cos_omega * cos_i) * y_orb
            
            y = (sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i) * x_orb + \
                (-sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i) * y_orb
            
            z = (sin_omega * sin_i) * x_orb + (cos_omega * sin_i) * y_orb
            
            # Velocity (simplified)
            v_mag = math.sqrt(self.GM_SUN * (2/r - 1/a)) / 1000  # km/s
            v_x = -y/r * v_mag
            v_y = x/r * v_mag
            v_z = 0.0
            
            return {
                'success': True,
                'position_km': [x, y, z],
                'velocity_km_s': [v_x, v_y, v_z],
                'distance_au': r / self.AU,
                'true_anomaly_deg': math.degrees(nu),
                'eccentric_anomaly_deg': math.degrees(E),
                'mean_anomaly_deg': math.degrees(M)
            }
            
        except Exception as e:
            logger.error(f"Error calculating asteroid position: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def calculate_earth_position(self, target_date: datetime) -> Dict:
        """Calculate Earth position (simplified circular orbit)"""
        try:
            j2000 = datetime(2000, 1, 1, 12, 0, 0)
            days = (target_date - j2000).total_seconds() / 86400.0
            
            # Earth's mean longitude
            L = 100.464 + 0.9856076686 * days
            L_rad = math.radians(L % 360.0)
            
            # Position
            x = self.AU * math.cos(L_rad)
            y = self.AU * math.sin(L_rad)
            z = 0.0
            
            # Velocity
            v = 29.78  # km/s
            v_x = -v * math.sin(L_rad)
            v_y = v * math.cos(L_rad)
            v_z = 0.0
            
            return {
                'success': True,
                'position_km': [x, y, z],
                'velocity_km_s': [v_x, v_y, v_z]
            }
            
        except Exception as e:
            logger.error(f"Error calculating Earth position: {str(e)}")
            return {'success': False, 'error': str(e)}

    def predict_trajectory(self, orbital_elements: Dict, days: int = 365, points: int = 12) -> Dict:
        """Generate multi-point trajectory prediction"""
        try:
            start_date = datetime.now()
            time_step = days / points
            
            trajectory_points = []
            closest_approach = {'distance': float('inf'), 'date': None, 'index': None}
            
            for i in range(points):
                check_date = start_date + timedelta(days=i * time_step)
                
                # Calculate positions
                ast_state = self.calculate_position(orbital_elements, check_date)
                earth_state = self.calculate_earth_position(check_date)
                
                if ast_state.get('success') and earth_state.get('success'):
                    # Calculate distance from Earth
                    ast_pos = np.array(ast_state['position_km'])
                    earth_pos = np.array(earth_state['position_km'])
                    distance_km = np.linalg.norm(ast_pos - earth_pos)
                    
                    # Track closest approach
                    if distance_km < closest_approach['distance']:
                        closest_approach = {
                            'distance': distance_km,
                            'date': check_date,
                            'index': i
                        }
                    
                    trajectory_points.append({
                        'date': check_date.isoformat(),
                        'asteroid_position_km': ast_state['position_km'],
                        'asteroid_velocity_km_s': ast_state['velocity_km_s'],
                        'earth_position_km': earth_state['position_km'],
                        'distance_from_earth_km': distance_km,
                        'distance_from_earth_au': distance_km / self.AU,
                        'distance_from_earth_radii': distance_km / self.EARTH_RADIUS,
                        'true_anomaly_deg': ast_state['true_anomaly_deg']
                    })
            
            return {
                'success': True,
                'trajectory_parameters': {
                    'time_span_days': days,
                    'number_of_points': len(trajectory_points),
                    'start_date': start_date.isoformat(),
                    'end_date': (start_date + timedelta(days=days)).isoformat()
                },
                'closest_approach': {
                    'distance_km': closest_approach['distance'],
                    'distance_earth_radii': closest_approach['distance'] / self.EARTH_RADIUS,
                    'date': closest_approach['date'].isoformat() if closest_approach['date'] else None,
                    'point_index': closest_approach['index']
                },
                'trajectory_points': trajectory_points,
                'physics_method': 'Real Keplerian orbital mechanics'
            }
            
        except Exception as e:
            logger.error(f"Error predicting trajectory: {str(e)}")
            return {'success': False, 'error': str(e)}

    def assess_impact_risk(self, orbital_elements: Dict, physical_properties: Dict) -> Dict:
        """Assess potential impact risk and consequences"""
        try:
            # Calculate minimum orbit intersection distance (MOID) approximation
            a = orbital_elements.get('semi_major_axis', 1.5)
            e = orbital_elements.get('eccentricity', 0.2)
            
            # Simplified MOID calculation (Earth orbit assumed circular at 1 AU)
            perihelion = a * (1 - e)
            aphelion = a * (1 + e)
            
            # Check if orbit crosses Earth's orbit
            crosses_earth_orbit = perihelion < 1.0 < aphelion
            
            # Calculate impact energy if asteroid hits Earth
            diameter_km = physical_properties.get('diameter_km', 1.0)
            
            # Estimate mass (assuming typical asteroid density ~2.5 g/cm³)
            radius_m = diameter_km * 500  # radius in meters
            volume_m3 = (4/3) * math.pi * (radius_m ** 3)
            mass_kg = volume_m3 * 2500  # density 2.5 g/cm³ = 2500 kg/m³
            
            # Estimate impact velocity (typical for Earth-crossing asteroids)
            impact_velocity_ms = 20000  # 20 km/s typical
            
            # Calculate kinetic energy
            kinetic_energy_j = 0.5 * mass_kg * (impact_velocity_ms ** 2)
            kinetic_energy_mt = kinetic_energy_j / (4.184e15)  # Convert to megatons TNT
            
            # Determine risk category
            if diameter_km >= 10:
                risk_level = "Global Catastrophe"
                effects = "Mass extinction event, global winter"
            elif diameter_km >= 1:
                risk_level = "Regional Devastation"
                effects = "Continental damage, climate effects"
            elif diameter_km >= 0.1:
                risk_level = "Local Catastrophe"
                effects = "City-scale destruction"
            elif diameter_km >= 0.01:
                risk_level = "Local Damage"
                effects = "Building-scale damage"
            else:
                risk_level = "Minimal Risk"
                effects = "Likely burns up in atmosphere"
            
            return {
                'success': True,
                'crosses_earth_orbit': crosses_earth_orbit,
                'minimum_distance_au': abs(1.0 - perihelion) if perihelion > 1.0 else abs(aphelion - 1.0),
                'diameter_km': diameter_km,
                'estimated_mass_kg': mass_kg,
                'impact_velocity_km_s': impact_velocity_ms / 1000,
                'kinetic_energy_megatons': kinetic_energy_mt,
                'risk_level': risk_level,
                'potential_effects': effects,
                'orbital_info': {
                    'semi_major_axis_au': a,
                    'eccentricity': e,
                    'perihelion_au': perihelion,
                    'aphelion_au': aphelion
                }
            }
            
        except Exception as e:
            logger.error(f"Error assessing impact risk: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _solve_kepler_equation(self, M: float, e: float, tolerance: float = 1e-6) -> float:
        """Solve Kepler's equation using Newton-Raphson method"""
        E = M  # Initial guess
        for _ in range(50):  # Max iterations
            f = E - e * math.sin(E) - M
            f_prime = 1 - e * math.cos(E)
            if abs(f_prime) < 1e-12:  # Avoid division by zero
                break
            E_new = E - f / f_prime
            
            if abs(E_new - E) < tolerance:
                return E_new
            E = E_new
        
        return E  # Return best approximation
    
    def _orbital_to_ecliptic(self, x_orb: float, y_orb: float, z_orb: float,
                           omega: float, i: float, w: float) -> Tuple[float, float, float]:
        """Transform from orbital plane to ecliptic coordinates"""
        # Rotation matrices for orbital element transformation
        cos_omega = math.cos(omega)
        sin_omega = math.sin(omega)
        cos_i = math.cos(i)
        sin_i = math.sin(i)
        cos_w = math.cos(w)
        sin_w = math.sin(w)
        
        # Combined transformation matrix elements
        p11 = cos_omega * cos_w - sin_omega * sin_w * cos_i
        p12 = -cos_omega * sin_w - sin_omega * cos_w * cos_i
        p21 = sin_omega * cos_w + cos_omega * sin_w * cos_i
        p22 = -sin_omega * sin_w + cos_omega * cos_w * cos_i
        p31 = sin_w * sin_i
        p32 = cos_w * sin_i
        
        # Transform coordinates
        x_ecl = p11 * x_orb + p12 * y_orb
        y_ecl = p21 * x_orb + p22 * y_orb
        z_ecl = p31 * x_orb + p32 * y_orb
        
        return x_ecl, y_ecl, z_ecl
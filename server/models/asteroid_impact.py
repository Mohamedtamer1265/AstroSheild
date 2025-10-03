"""
🔬 Asteroid Impact Physics Models
NASA Space Apps 2024

Core physics calculations for asteroid impact modeling including:
- Kinetic energy calculations
- Crater formation using Schmidt-Housen scaling laws
- Seismic magnitude estimation using Kanamori relationships
- Air blast effects and overpressure zones
- Casualty estimation based on damage zones
"""

import math
import numpy as np
from typing import Dict, Optional, Tuple, Any


class AsteroidImpact:
    """
    Comprehensive asteroid impact modeling class.
    
    Calculates impact energy, seismic effects, crater size, and damage assessment
    based on established scientific scaling laws and impact physics.
    """
    
    def __init__(self, diameter_m: float, velocity_km_s: float, 
                 density_kg_m3: float = 2600, angle_degrees: float = 45):
        """
        Initialize asteroid parameters.
        
        Args:
            diameter_m (float): Asteroid diameter in meters
            velocity_km_s (float): Impact velocity in km/s
            density_kg_m3 (float): Asteroid density in kg/m³ (default: 2600 for stony)
            angle_degrees (float): Impact angle in degrees (default: 45°)
        """
        self.diameter = diameter_m
        self.velocity = velocity_km_s * 1000  # Convert to m/s
        self.density = density_kg_m3
        self.angle = math.radians(angle_degrees)
        
        # Calculate basic properties
        self.radius = diameter_m / 2
        self.volume = (4/3) * math.pi * (self.radius ** 3)
        self.mass = self.volume * density_kg_m3
        
        # Constants
        self.g = 9.81  # Gravity (m/s²)
        self.target_density = 2670  # Average crustal density (kg/m³)
        
    def calculate_kinetic_energy(self) -> Dict[str, float]:
        """Calculate kinetic energy of impact in Joules and TNT equivalent."""
        ke_joules = 0.5 * self.mass * (self.velocity ** 2)
        
        # Convert to TNT equivalent (1 kiloton TNT = 4.184e12 J)
        tnt_kilotons = ke_joules / (4.184e12)
        tnt_megatons = tnt_kilotons / 1000
        
        return {
            'energy_joules': ke_joules,
            'energy_tnt_kilotons': tnt_kilotons,
            'energy_tnt_megatons': tnt_megatons
        }
    
    def calculate_crater_size(self) -> Dict[str, float]:
        """
        Calculate crater diameter and depth using scaling laws.
        
        Uses the Schmidt-Housen crater scaling law for complex craters.
        """
        # Effective kinetic energy accounting for impact angle
        ke = self.calculate_kinetic_energy()['energy_joules']
        eff_energy = ke * (math.sin(self.angle) ** 2)
        
        # Schmidt-Housen scaling (for gravity-dominated craters)
        # D = K * (E/ρt*g)^0.22 * ρi^0.11 / ρt^0.11
        K = 1.88  # Scaling constant for complex craters
        
        crater_diameter = K * ((eff_energy / (self.target_density * self.g)) ** 0.22) * \
                         ((self.density ** 0.11) / (self.target_density ** 0.11))
        
        # Crater depth (empirical relationship: depth ≈ 0.2 * diameter for complex craters)
        crater_depth = crater_diameter * 0.2
        
        # Rim height (typically 5-10% of diameter)
        rim_height = crater_diameter * 0.07
        
        return {
            'diameter_m': crater_diameter,
            'diameter_km': crater_diameter / 1000,
            'depth_m': crater_depth,
            'rim_height_m': rim_height,
            'volume_m3': math.pi * (crater_diameter/2)**2 * crater_depth / 3
        }
    
    def calculate_seismic_magnitude(self) -> Dict[str, float]:
        """
        Calculate equivalent earthquake magnitude using energy-magnitude relationship.
        
        Uses the relationship: log10(E) = 11.8 + 1.5*M (Kanamori, 1977)
        where E is energy in ergs and M is moment magnitude.
        """
        ke = self.calculate_kinetic_energy()['energy_joules']
        
        # Convert Joules to ergs (1 J = 10^7 ergs)
        energy_ergs = ke * 1e7
        
        # Calculate moment magnitude
        if energy_ergs > 0:
            magnitude = (math.log10(energy_ergs) - 11.8) / 1.5
        else:
            magnitude = 0
        
        # Richter scale approximation (for comparison)
        richter_approx = magnitude - 0.2  # Rough conversion
        
        return {
            'moment_magnitude': max(0, magnitude),
            'richter_approximate': max(0, richter_approx),
            'energy_ergs': energy_ergs
        }
    
    def calculate_air_blast(self) -> Dict[str, float]:
        """Calculate air blast effects and overpressure zones."""
        ke = self.calculate_kinetic_energy()['energy_tnt_kilotons']
        
        # Air blast ranges (empirical formulas for kiloton yield)
        # Overpressure distances in km
        ranges = {}
        
        if ke > 0:
            # 1 psi overpressure (window breaking) - R = 2.2 * Y^0.33
            ranges['1_psi_km'] = 2.2 * (ke ** 0.33)
            
            # 5 psi overpressure (building damage) - R = 0.8 * Y^0.33  
            ranges['5_psi_km'] = 0.8 * (ke ** 0.33)
            
            # 20 psi overpressure (severe destruction) - R = 0.3 * Y^0.33
            ranges['20_psi_km'] = 0.3 * (ke ** 0.33)
            
            # Thermal radiation (3rd degree burns) - R = 1.9 * Y^0.41
            ranges['thermal_3rd_degree_km'] = 1.9 * (ke ** 0.41)
        
        return ranges
    
    def estimate_casualties(self, population_density_per_km2: float, 
                          total_population: int) -> Dict[str, Any]:
        """
        Estimate casualties based on blast effects and population density.
        
        Args:
            population_density_per_km2 (float): People per square kilometer
            total_population (int): Total population in affected area
            
        Returns:
            dict: Casualty estimates by damage zone
        """
        blast_ranges = self.calculate_air_blast()
        
        casualties = {}
        
        if blast_ranges:
            # Calculate affected areas (π * r²)
            area_20_psi = math.pi * (blast_ranges.get('20_psi_km', 0) ** 2)
            area_5_psi = math.pi * (blast_ranges.get('5_psi_km', 0) ** 2) - area_20_psi
            area_1_psi = math.pi * (blast_ranges.get('1_psi_km', 0) ** 2) - area_5_psi - area_20_psi
            
            # Estimate population in each zone
            pop_20_psi = min(area_20_psi * population_density_per_km2, total_population)
            pop_5_psi = min(area_5_psi * population_density_per_km2, total_population - pop_20_psi)
            pop_1_psi = min(area_1_psi * population_density_per_km2, total_population - pop_20_psi - pop_5_psi)
            
            # Casualty rates by zone (based on nuclear weapons effects studies)
            fatality_rate_20_psi = 0.90  # 90% fatality rate in severe destruction zone
            injury_rate_20_psi = 0.10   # 10% injury rate (survivors)
            
            fatality_rate_5_psi = 0.50   # 50% fatality rate in heavy damage zone
            injury_rate_5_psi = 0.40     # 40% injury rate
            
            fatality_rate_1_psi = 0.05   # 5% fatality rate in light damage zone
            injury_rate_1_psi = 0.30     # 30% injury rate
            
            casualties = {
                'severe_zone': {
                    'population': int(pop_20_psi),
                    'fatalities': int(pop_20_psi * fatality_rate_20_psi),
                    'injuries': int(pop_20_psi * injury_rate_20_psi),
                    'radius_km': blast_ranges.get('20_psi_km', 0)
                },
                'heavy_damage_zone': {
                    'population': int(pop_5_psi),
                    'fatalities': int(pop_5_psi * fatality_rate_5_psi),
                    'injuries': int(pop_5_psi * injury_rate_5_psi),
                    'radius_km': blast_ranges.get('5_psi_km', 0)
                },
                'light_damage_zone': {
                    'population': int(pop_1_psi),
                    'fatalities': int(pop_1_psi * fatality_rate_1_psi),
                    'injuries': int(pop_1_psi * injury_rate_1_psi),
                    'radius_km': blast_ranges.get('1_psi_km', 0)
                }
            }
            
            # Calculate totals
            total_fatalities = sum([zone['fatalities'] for zone in casualties.values()])
            total_injuries = sum([zone['injuries'] for zone in casualties.values()])
            total_affected = sum([zone['population'] for zone in casualties.values()])
            
            casualties['totals'] = {
                'fatalities': total_fatalities,
                'injuries': total_injuries,
                'affected_population': total_affected
            }
        
        return casualties
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Get complete impact analysis."""
        energy = self.calculate_kinetic_energy()
        crater = self.calculate_crater_size()
        seismic = self.calculate_seismic_magnitude()
        blast = self.calculate_air_blast()
        
        return {
            'asteroid_properties': {
                'diameter_m': self.diameter,
                'velocity_km_s': self.velocity / 1000,
                'mass_kg': self.mass,
                'density_kg_m3': self.density,
                'impact_angle_degrees': math.degrees(self.angle)
            },
            'energy': energy,
            'crater': crater,
            'seismic': seismic,
            'air_blast_ranges': blast
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert asteroid object to dictionary for JSON serialization."""
        return {
            'diameter_m': self.diameter,
            'velocity_km_s': self.velocity / 1000,
            'density_kg_m3': self.density,
            'angle_degrees': math.degrees(self.angle),
            'mass_kg': self.mass,
            'volume_m3': self.volume
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AsteroidImpact':
        """Create asteroid object from dictionary."""
        return cls(
            diameter_m=data['diameter_m'],
            velocity_km_s=data['velocity_km_s'],
            density_kg_m3=data.get('density_kg_m3', 2600),
            angle_degrees=data.get('angle_degrees', 45)
        )
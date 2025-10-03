"""
🗺️ Visualization Utilities
NASA Space Apps 2024

Utilities for creating visualizations, maps, and charts for asteroid impact analysis.
Includes shake map generation, impact zone visualization, and chart data preparation.
"""

import json
import base64
import io
import math
from typing import Dict, List, Any, Optional, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from models.asteroid_impact import AsteroidImpact


class VisualizationManager:
    """Manager for creating visualizations and maps for asteroid impacts."""
    
    def __init__(self, nasa_api_manager=None):
        """Initialize visualization settings."""
        # Set matplotlib style
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
        # Define colors for different zones
        self.zone_colors = {
            'crater': '#8B0000',           # Dark red for crater
            'severe': '#FF0000',           # Red for severe damage (20 psi)
            'heavy': '#FF8C00',            # Orange for heavy damage (5 psi)  
            'light': '#FFD700',            # Gold for light damage (1 psi)
            'thermal': '#FF69B4'           # Pink for thermal effects
        }
        
        # Store reference to NASA API manager for earthquake data
        self.nasa_api_manager = nasa_api_manager
    
    def create_shake_map_data(self, impact_lat: float, impact_lon: float, 
                             asteroid_impact: AsteroidImpact, title: str = "Asteroid Impact") -> Dict[str, Any]:
        """
        Create shake map data structure for frontend rendering.
        
        Args:
            impact_lat (float): Impact latitude
            impact_lon (float): Impact longitude  
            asteroid_impact (AsteroidImpact): Impact analysis object
            title (str): Map title
            
        Returns:
            dict: Map data structure with impact zones and markers
        """
        # Get impact analysis
        blast_ranges = asteroid_impact.calculate_air_blast()
        crater = asteroid_impact.calculate_crater_size()
        energy = asteroid_impact.calculate_kinetic_energy()
        seismic = asteroid_impact.calculate_seismic_magnitude()
        
        # Create base map configuration
        map_data = {
            'center': {
                'lat': impact_lat,
                'lng': impact_lon
            },
            'zoom': 10,
            'title': title,
            'impact_point': {
                'lat': impact_lat,
                'lng': impact_lon,
                'info': {
                    'energy_mt': round(energy['energy_tnt_megatons'], 2),
                    'seismic_magnitude': round(seismic['moment_magnitude'], 1),
                    'crater_diameter_km': round(crater['diameter_km'], 2),
                    'crater_depth_m': round(crater['depth_m'], 0),
                    'asteroid_diameter_m': asteroid_impact.diameter,
                    'impact_velocity_km_s': round(asteroid_impact.velocity / 1000, 1)
                }
            },
            'zones': [],
            'legend': {
                'title': title,
                'energy_mt': round(energy['energy_tnt_megatons'], 1),
                'magnitude': round(seismic['moment_magnitude'], 1)
            }
        }
        
        # Add crater zone
        crater_radius_km = crater['diameter_km'] / 2
        if crater_radius_km > 0:
            map_data['zones'].append({
                'type': 'crater',
                'center': {'lat': impact_lat, 'lng': impact_lon},
                'radius_m': crater_radius_km * 1000,
                'color': self.zone_colors['crater'],
                'fillOpacity': 0.7,
                'weight': 3,
                'popup': f"🕳️ Crater<br>Diameter: {crater['diameter_km']:.2f} km<br>Depth: {crater['depth_m']:.0f} m"
            })
        
        # Add blast effect zones
        if blast_ranges:
            # Severe damage zone (20 psi)
            if '20_psi_km' in blast_ranges and blast_ranges['20_psi_km'] > 0:
                map_data['zones'].append({
                    'type': 'severe_damage',
                    'center': {'lat': impact_lat, 'lng': impact_lon},
                    'radius_m': blast_ranges['20_psi_km'] * 1000,
                    'color': self.zone_colors['severe'],
                    'fillOpacity': 0.3,
                    'weight': 2,
                    'popup': f"💥 Severe Destruction Zone<br>20 psi overpressure<br>Radius: {blast_ranges['20_psi_km']:.1f} km"
                })
            
            # Heavy damage zone (5 psi)
            if '5_psi_km' in blast_ranges and blast_ranges['5_psi_km'] > 0:
                map_data['zones'].append({
                    'type': 'heavy_damage',
                    'center': {'lat': impact_lat, 'lng': impact_lon},
                    'radius_m': blast_ranges['5_psi_km'] * 1000,
                    'color': self.zone_colors['heavy'],
                    'fillOpacity': 0.2,
                    'weight': 2,
                    'popup': f"🏢 Heavy Damage Zone<br>5 psi overpressure<br>Radius: {blast_ranges['5_psi_km']:.1f} km"
                })
            
            # Light damage zone (1 psi)
            if '1_psi_km' in blast_ranges and blast_ranges['1_psi_km'] > 0:
                map_data['zones'].append({
                    'type': 'light_damage',
                    'center': {'lat': impact_lat, 'lng': impact_lon},
                    'radius_m': blast_ranges['1_psi_km'] * 1000,
                    'color': self.zone_colors['light'],
                    'fillOpacity': 0.1,
                    'weight': 2,
                    'popup': f"🪟 Light Damage Zone<br>1 psi overpressure<br>Radius: {blast_ranges['1_psi_km']:.1f} km"
                })
            
            # Thermal radiation zone
            if 'thermal_3rd_degree_km' in blast_ranges and blast_ranges['thermal_3rd_degree_km'] > 0:
                map_data['zones'].append({
                    'type': 'thermal',
                    'center': {'lat': impact_lat, 'lng': impact_lon},
                    'radius_m': blast_ranges['thermal_3rd_degree_km'] * 1000,
                    'color': self.zone_colors['thermal'],
                    'fillOpacity': 0.1,
                    'weight': 1,
                    'popup': f"🔥 Thermal Radiation Zone<br>3rd degree burns<br>Radius: {blast_ranges['thermal_3rd_degree_km']:.1f} km"
                })
        
        return map_data
    
    def create_impact_chart_data(self, asteroid_impact: AsteroidImpact) -> Dict[str, Any]:
        """
        Create chart data for impact analysis visualization.
        
        Args:
            asteroid_impact (AsteroidImpact): Impact analysis object
            
        Returns:
            dict: Chart data structure for frontend rendering
        """
        analysis = asteroid_impact.get_comprehensive_analysis()
        
        # Energy comparison data
        energy_data = analysis['energy']
        
        # Seismic comparison with earthquakes from API
        seismic_data = analysis['seismic']
        
        # Get earthquake data from API or fallback to static data
        if self.nasa_api_manager:
            historical_earthquakes = self.nasa_api_manager.get_historical_earthquakes()
        else:
            # Fallback if no API manager available
            historical_earthquakes = {
                '2011 Japan': 9.1,
                '2004 Sumatra': 9.1,
                '1906 San Francisco': 7.9,
                '2010 Haiti': 7.0,
                '1994 Northridge': 6.7
            }
        
        # Add the current impact to comparison
        famous_earthquakes = {'This Impact': seismic_data['moment_magnitude']}
        famous_earthquakes.update(historical_earthquakes)
        
        # Crater dimensions
        crater_data = analysis['crater']
        
        # Blast ranges
        blast_data = analysis['air_blast_ranges']
        
        chart_data = {
            'energy': {
                'title': 'Energy Release',
                'data': {
                    'joules': energy_data['energy_joules'],
                    'kilotons': energy_data['energy_tnt_kilotons'],
                    'megatons': energy_data['energy_tnt_megatons']
                },
                'display_value': f"{energy_data['energy_tnt_megatons']:.2f} Megatons TNT"
            },
            'seismic_comparison': {
                'title': 'Seismic Magnitude Comparison',
                'data': [
                    {'name': name, 'magnitude': mag, 'is_impact': name == 'This Impact'}
                    for name, mag in famous_earthquakes.items()
                ]
            },
            'crater_dimensions': {
                'title': 'Crater Dimensions',
                'data': {
                    'diameter_km': crater_data['diameter_km'],
                    'depth_m': crater_data['depth_m'],
                    'rim_height_m': crater_data['rim_height_m'],
                    'volume_m3': crater_data['volume_m3']
                }
            },
            'blast_ranges': {
                'title': 'Blast Effect Ranges (km)',
                'data': [
                    {'zone': 'Severe (20 psi)', 'range_km': blast_data.get('20_psi_km', 0), 'color': self.zone_colors['severe']},
                    {'zone': 'Heavy (5 psi)', 'range_km': blast_data.get('5_psi_km', 0), 'color': self.zone_colors['heavy']},
                    {'zone': 'Light (1 psi)', 'range_km': blast_data.get('1_psi_km', 0), 'color': self.zone_colors['light']},
                    {'zone': 'Thermal Burns', 'range_km': blast_data.get('thermal_3rd_degree_km', 0), 'color': self.zone_colors['thermal']}
                ]
            },
            'summary': {
                'asteroid_diameter_m': asteroid_impact.diameter,
                'impact_velocity_km_s': asteroid_impact.velocity / 1000,
                'energy_megatons': energy_data['energy_tnt_megatons'],
                'seismic_magnitude': seismic_data['moment_magnitude'],
                'crater_diameter_km': crater_data['diameter_km'],
                'max_damage_range_km': max(blast_data.values()) if blast_data else 0
            }
        }
        
        return chart_data
    
    def generate_matplotlib_chart(self, asteroid_impact: AsteroidImpact, 
                                 chart_type: str = 'comprehensive') -> str:
        """
        Generate matplotlib chart and return as base64 encoded string.
        
        Args:
            asteroid_impact (AsteroidImpact): Impact analysis object
            chart_type (str): Type of chart to generate
            
        Returns:
            str: Base64 encoded image
        """
        analysis = asteroid_impact.get_comprehensive_analysis()
        
        if chart_type == 'comprehensive':
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('🌍☄️ Asteroid Impact Analysis', fontsize=16, fontweight='bold')
            
            # 1. Energy visualization
            energy_data = analysis['energy']
            ax1.pie([1], labels=[f"{energy_data['energy_tnt_megatons']:.2f} Megatons TNT"], 
                    autopct='%1.1f%%', startangle=90, colors=['red'])
            ax1.set_title('💥 Energy Release')
            
            # 2. Crater dimensions
            crater_data = analysis['crater']
            crater_metrics = ['Diameter (km)', 'Depth (m)', 'Rim Height (m)']
            crater_values = [crater_data['diameter_km'], crater_data['depth_m']/1000, crater_data['rim_height_m']/1000]
            
            bars = ax2.bar(crater_metrics, crater_values, color=['brown', 'orange', 'yellow'])
            ax2.set_title('🕳️ Crater Dimensions')
            ax2.set_ylabel('Size (km)')
            for bar, value in zip(bars, crater_values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                        f'{value:.2f}', ha='center', va='bottom')
            
            # 3. Seismic comparison
            seismic_data = analysis['seismic']
            
            # Get earthquake data from API or fallback
            if self.nasa_api_manager:
                historical_earthquakes = self.nasa_api_manager.get_historical_earthquakes()
            else:
                historical_earthquakes = {
                    '2011 Japan': 9.1,
                    '2004 Sumatra': 9.1,
                    '1906 San Francisco': 7.9,
                    '2010 Haiti': 7.0
                }
            
            # Limit to 5 for chart readability
            limited_earthquakes = dict(list(historical_earthquakes.items())[:4])
            famous_earthquakes = {'This Impact': seismic_data['moment_magnitude']}
            famous_earthquakes.update(limited_earthquakes)
            
            names = list(famous_earthquakes.keys())
            magnitudes = list(famous_earthquakes.values())
            colors_eq = ['red' if name == 'This Impact' else 'blue' for name in names]
            
            bars = ax3.barh(names, magnitudes, color=colors_eq)
            ax3.set_title('📊 Seismic Magnitude Comparison')
            ax3.set_xlabel('Moment Magnitude')
            for bar, mag in zip(bars, magnitudes):
                ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        f'M{mag:.1f}', va='center')
            
            # 4. Blast ranges
            blast_data = analysis['air_blast_ranges']
            if blast_data:
                zones = ['Severe\\n(20 psi)', 'Heavy\\n(5 psi)', 'Light\\n(1 psi)', 'Thermal\\nBurns']
                distances = [blast_data.get('20_psi_km', 0), blast_data.get('5_psi_km', 0), 
                            blast_data.get('1_psi_km', 0), blast_data.get('thermal_3rd_degree_km', 0)]
                colors_blast = ['darkred', 'red', 'orange', 'pink']
                
                bars = ax4.bar(zones, distances, color=colors_blast)
                ax4.set_title('🌊 Blast Effect Ranges')
                ax4.set_ylabel('Distance (km)')
                for bar, dist in zip(bars, distances):
                    if dist > 0:
                        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                                f'{dist:.1f}', ha='center', va='bottom')
            else:
                ax4.text(0.5, 0.5, 'No blast data available', ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('🌊 Blast Effect Ranges')
            
            plt.tight_layout()
        
        # Convert plot to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return image_base64
    
    def create_parameter_study_chart(self, parameter: str, values: List[float], 
                                   results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create parameter study chart data.
        
        Args:
            parameter (str): Parameter being studied
            values (list): Parameter values
            results (list): Analysis results for each value
            
        Returns:
            dict: Chart data for parameter study
        """
        chart_data = {
            'parameter': parameter,
            'title': f'Parameter Study: {parameter.title()} Effects',
            'data': {
                'parameter_values': values,
                'energy_mt': [r['energy']['energy_tnt_megatons'] for r in results],
                'seismic_magnitude': [r['seismic']['moment_magnitude'] for r in results],
                'crater_diameter_km': [r['crater']['diameter_km'] for r in results],
                'severe_damage_km': [r['air_blast_ranges'].get('20_psi_km', 0) for r in results],
                'light_damage_km': [r['air_blast_ranges'].get('1_psi_km', 0) for r in results]
            },
            'charts': [
                {
                    'title': 'Energy Release vs ' + parameter.title(),
                    'x_label': parameter.title(),
                    'y_label': 'Energy (Megatons TNT)',
                    'data_key': 'energy_mt',
                    'color': 'red',
                    'scale': 'log' if max([r['energy']['energy_tnt_megatons'] for r in results]) / min([r['energy']['energy_tnt_megatons'] for r in results]) > 100 else 'linear'
                },
                {
                    'title': 'Seismic Magnitude vs ' + parameter.title(),
                    'x_label': parameter.title(),
                    'y_label': 'Seismic Magnitude',
                    'data_key': 'seismic_magnitude',
                    'color': 'blue',
                    'scale': 'linear'
                },
                {
                    'title': 'Crater Size vs ' + parameter.title(),
                    'x_label': parameter.title(),
                    'y_label': 'Crater Diameter (km)',
                    'data_key': 'crater_diameter_km',
                    'color': 'green',
                    'scale': 'linear'
                },
                {
                    'title': 'Damage Ranges vs ' + parameter.title(),
                    'x_label': parameter.title(),
                    'y_label': 'Damage Range (km)',
                    'data_keys': ['severe_damage_km', 'light_damage_km'],
                    'colors': ['red', 'orange'],
                    'labels': ['Severe (20 psi)', 'Light (1 psi)'],
                    'scale': 'linear'
                }
            ]
        }
        
        return chart_data
"""
📡 NASA APIs Integration
NASA Space Apps 2024

Utilities for integrating with NASA and other APIs for elevation, population,
and geographic data to enhance asteroid impact analysis.
"""

import requests
import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, List
import logging

logger = logging.getLogger(__name__)


class NASAAPIManager:
    """Manager for NASA and external API integrations."""
    
    def __init__(self):
        """Initialize API manager with configurations."""
        self.apis = {
            'elevation': {
                'base_url': 'https://api.open-elevation.com/api/v1/lookup',
                'timeout': 10
            },
            'nasa_dem': {
                'base_url': 'https://cloud.sdgsat.com/api/v1/dem',
                'timeout': 15
            }
        }
        
        # Fallback data for when APIs are unavailable
        self.fallback_elevation = 100  # meters
        self.fallback_population_density = 50  # people per km²
        
        # USGS Earthquake API configuration
        self.apis['earthquake'] = {
            'base_url': 'https://earthquake.usgs.gov/fdsnws/event/1/query',
            'timeout': 10
        }
    
    def get_elevation_single(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get elevation for a single coordinate using Open-Elevation API.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Elevation data with status
        """
        try:
            # Validate coordinates
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return {
                    'status': 'error',
                    'error': 'Invalid coordinates',
                    'elevation': self.fallback_elevation
                }
            
            # Make API request
            params = {
                'locations': f"{lat},{lon}"
            }
            
            response = requests.get(
                self.apis['elevation']['base_url'],
                params=params,
                timeout=self.apis['elevation']['timeout']
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    elevation = data['results'][0].get('elevation', self.fallback_elevation)
                    return {
                        'status': 'success',
                        'elevation': elevation,
                        'source': 'open-elevation'
                    }
            
            # If API call fails, return fallback
            logger.warning(f"Elevation API failed for {lat}, {lon}: {response.status_code}")
            return {
                'status': 'fallback',
                'elevation': self.fallback_elevation,
                'error': f"API returned status {response.status_code}"
            }
            
        except requests.exceptions.Timeout:
            logger.warning(f"Elevation API timeout for {lat}, {lon}")
            return {
                'status': 'fallback',
                'elevation': self.fallback_elevation,
                'error': 'API timeout'
            }
        except Exception as e:
            logger.error(f"Elevation API error for {lat}, {lon}: {str(e)}")
            return {
                'status': 'fallback',
                'elevation': self.fallback_elevation,
                'error': str(e)
            }
    
    def estimate_population_bbox(self, south: float, north: float, 
                               west: float, east: float) -> Dict[str, Any]:
        """
        Estimate population in a bounding box using geographic approximations.
        
        Args:
            south (float): Southern latitude
            north (float): Northern latitude
            west (float): Western longitude
            east (float): Eastern longitude
            
        Returns:
            dict: Population estimate data
        """
        try:
            # Validate bounding box
            if not (-90 <= south <= north <= 90) or not (-180 <= west <= east <= 180):
                return {
                    'status': 'error',
                    'error': 'Invalid bounding box coordinates'
                }
            
            # Calculate area in km²
            # This is an approximation - more accurate methods would account for Earth's curvature
            lat_diff = north - south
            lon_diff = east - west
            
            # Average latitude for more accurate longitude distance calculation
            avg_lat = (north + south) / 2
            
            # Convert degrees to km (approximately)
            lat_km = lat_diff * 111  # 1 degree latitude ≈ 111 km
            lon_km = lon_diff * 111 * math.cos(math.radians(avg_lat))  # Longitude varies with latitude
            
            area_km2 = lat_km * lon_km
            
            # Estimate population density based on location characteristics
            population_density = self._estimate_population_density(south, north, west, east)
            
            # Calculate population estimate
            population_estimate = int(area_km2 * population_density)
            
            return {
                'status': 'success',
                'population_estimate': population_estimate,
                'area_km2': round(area_km2, 2),
                'population_density_per_km2': population_density,
                'method': 'geographic_approximation',
                'bbox': {
                    'south': south,
                    'north': north,
                    'west': west,
                    'east': east
                }
            }
            
        except Exception as e:
            logger.error(f"Population estimation error: {str(e)}")
            # Fallback calculation
            area_km2 = ((north - south) * 111) * ((east - west) * 111 * math.cos(math.radians((north + south) / 2)))
            pop_estimate = int(area_km2 * self.fallback_population_density)
            
            return {
                'status': 'fallback',
                'population_estimate': pop_estimate,
                'area_km2': round(area_km2, 2),
                'population_density_per_km2': self.fallback_population_density,
                'error': str(e)
            }
    
    def _estimate_population_density(self, south: float, north: float, 
                                   west: float, east: float) -> float:
        """
        Estimate population density based on geographic location.
        
        This is a simplified model - real applications would use detailed datasets.
        """
        # Calculate center point
        center_lat = (north + south) / 2
        center_lon = (east + west) / 2
        
        # Very basic population density estimation based on known populated regions
        # This is highly simplified and should be replaced with real data in production
        
        # Major metropolitan areas (rough approximations)
        major_cities = [
            {'lat': 40.7128, 'lon': -74.0060, 'density': 10000, 'name': 'New York'},
            {'lat': 51.5074, 'lon': -0.1278, 'density': 5000, 'name': 'London'},
            {'lat': 35.6762, 'lon': 139.6503, 'density': 6000, 'name': 'Tokyo'},
            {'lat': 48.8566, 'lon': 2.3522, 'density': 8000, 'name': 'Paris'},
            {'lat': 34.0522, 'lon': -118.2437, 'density': 3000, 'name': 'Los Angeles'},
            {'lat': 30.0444, 'lon': 31.2357, 'density': 4000, 'name': 'Cairo'},
            {'lat': 55.7558, 'lon': 37.6176, 'density': 4500, 'name': 'Moscow'},
            {'lat': 28.6139, 'lon': 77.2090, 'density': 12000, 'name': 'Delhi'},
            {'lat': 31.2304, 'lon': 121.4737, 'density': 7000, 'name': 'Shanghai'},
            {'lat': -23.5505, 'lon': -46.6333, 'density': 7500, 'name': 'São Paulo'}
        ]
        
        # Find closest major city
        min_distance = float('inf')
        closest_density = self.fallback_population_density
        
        for city in major_cities:
            # Calculate approximate distance
            lat_diff = center_lat - city['lat']
            lon_diff = center_lon - city['lon']
            distance = math.sqrt(lat_diff**2 + lon_diff**2)  # Rough distance in degrees
            
            if distance < min_distance:
                min_distance = distance
                closest_density = city['density']
        
        # Adjust density based on distance from nearest major city
        if min_distance < 1:  # Very close to major city
            return closest_density
        elif min_distance < 5:  # Moderate distance
            return closest_density * 0.5
        elif min_distance < 10:  # Suburban/rural
            return closest_density * 0.1
        else:  # Very rural/remote
            return max(10, self.fallback_population_density * 0.2)
    
    def get_regional_impact_data(self, impact_lat: float, impact_lon: float, 
                               search_radius_km: float = 100) -> Dict[str, Any]:
        """
        Get comprehensive regional data for impact analysis.
        
        Args:
            impact_lat (float): Impact latitude
            impact_lon (float): Impact longitude
            search_radius_km (float): Search radius in kilometers
            
        Returns:
            dict: Regional impact data
        """
        # Calculate bounding box
        degree_offset = search_radius_km / 111  # Approximate conversion
        
        south = impact_lat - degree_offset
        north = impact_lat + degree_offset
        west = impact_lon - degree_offset
        east = impact_lon + degree_offset
        
        # Get elevation data
        elevation_data = self.get_elevation_single(impact_lat, impact_lon)
        
        # Get population data
        population_data = self.estimate_population_bbox(south, north, west, east)
        
        return {
            'impact_location': {
                'latitude': impact_lat,
                'longitude': impact_lon,
                'elevation_m': elevation_data.get('elevation', self.fallback_elevation),
                'elevation_status': elevation_data.get('status', 'unknown')
            },
            'regional_population': population_data,
            'search_radius_km': search_radius_km,
            'bounding_box': {
                'south': south,
                'north': north,
                'west': west,
                'east': east
            }
        }
    
    def assess_tsunami_risk(self, impact_lat: float, impact_lon: float, 
                           asteroid_diameter_m: float, search_radius_km: float = 200) -> Dict[str, Any]:
        """
        Assess tsunami risk based on impact location, elevation, and surrounding geography.
        
        Args:
            impact_lat (float): Impact latitude
            impact_lon (float): Impact longitude
            asteroid_diameter_m (float): Asteroid diameter in meters
            search_radius_km (float): Search radius for coastal analysis
            
        Returns:
            dict: Tsunami risk assessment
        """
        try:
            # Get impact point elevation
            impact_elevation = self.get_elevation_single(impact_lat, impact_lon)
            elevation_m = impact_elevation.get('elevation', self.fallback_elevation)
            
            # Initialize risk assessment
            risk_assessment = {
                'tsunami_likely': False,
                'risk_level': 'none',  # none, low, moderate, high, extreme
                'risk_factors': [],
                'warnings': [],
                'impact_location': {
                    'latitude': impact_lat,
                    'longitude': impact_lon,
                    'elevation_m': elevation_m,
                    'is_underwater': elevation_m <= 0
                },
                'coastal_analysis': {
                    'nearby_coastlines': [],
                    'affected_regions': [],
                    'max_wave_height_estimate_m': 0
                },
                'asteroid_size_factor': self._get_tsunami_size_factor(asteroid_diameter_m)
            }
            
            # Check if impact is in water (elevation <= 0)
            if elevation_m <= 0:
                risk_assessment['risk_factors'].append('Impact location is underwater/at sea level')
                risk_assessment['tsunami_likely'] = True
                
                # Analyze surrounding area for coastlines and populated areas
                coastal_analysis = self._analyze_coastal_impact(
                    impact_lat, impact_lon, asteroid_diameter_m, search_radius_km
                )
                risk_assessment['coastal_analysis'] = coastal_analysis
                
                # Calculate risk level based on multiple factors
                risk_level = self._calculate_tsunami_risk_level(
                    asteroid_diameter_m, elevation_m, coastal_analysis
                )
                risk_assessment['risk_level'] = risk_level
                
                # Generate warnings and recommendations
                warnings = self._generate_tsunami_warnings(
                    risk_level, asteroid_diameter_m, coastal_analysis
                )
                risk_assessment['warnings'] = warnings
                
            else:
                # Land impact - check if close to water bodies
                distance_to_water = self._estimate_distance_to_water(impact_lat, impact_lon)
                
                if distance_to_water < 50:  # Within 50km of water
                    risk_assessment['risk_factors'].append(f'Impact within ~{distance_to_water}km of water body')
                    
                    if asteroid_diameter_m > 500:  # Large asteroid
                        risk_assessment['tsunami_likely'] = True
                        risk_assessment['risk_level'] = 'low'
                        risk_assessment['warnings'].append('Large asteroid impact near water may cause local tsunamis')
                
                risk_assessment['distance_to_water_km'] = distance_to_water
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error in tsunami risk assessment: {str(e)}")
            return {
                'tsunami_likely': False,
                'risk_level': 'unknown',
                'error': str(e),
                'impact_location': {
                    'latitude': impact_lat,
                    'longitude': impact_lon,
                    'elevation_m': None,
                    'is_underwater': False
                }
            }
    
    def assess_tsunami_risk(self, impact_lat: float, impact_lon: float, 
                           asteroid_diameter_m: float, search_radius_km: float = 200) -> Dict[str, Any]:
        """
        Assess tsunami risk based on impact location, elevation, and surrounding geography.
        
        Args:
            impact_lat (float): Impact latitude
            impact_lon (float): Impact longitude
            asteroid_diameter_m (float): Asteroid diameter in meters
            search_radius_km (float): Search radius for coastal analysis
            
        Returns:
            dict: Tsunami risk assessment
        """
        try:
            # Get impact point elevation
            impact_elevation = self.get_elevation_single(impact_lat, impact_lon)
            elevation_m = impact_elevation.get('elevation', self.fallback_elevation)
            
            # Initialize risk assessment
            risk_assessment = {
                'tsunami_likely': False,
                'risk_level': 'none',  # none, low, moderate, high, extreme
                'risk_factors': [],
                'warnings': [],
                'impact_location': {
                    'latitude': impact_lat,
                    'longitude': impact_lon,
                    'elevation_m': elevation_m,
                    'is_underwater': elevation_m <= 0
                },
                'coastal_analysis': {
                    'nearby_coastlines': [],
                    'affected_regions': [],
                    'max_wave_height_estimate_m': 0
                },
                'asteroid_size_factor': self._get_tsunami_size_factor(asteroid_diameter_m)
            }
            
            # Check if impact is in water (elevation <= 0)
            if elevation_m <= 0:
                risk_assessment['risk_factors'].append('Impact location is underwater/at sea level')
                risk_assessment['tsunami_likely'] = True
                
                # Analyze surrounding area for coastlines and populated areas
                coastal_analysis = self._analyze_coastal_impact(
                    impact_lat, impact_lon, asteroid_diameter_m, search_radius_km
                )
                risk_assessment['coastal_analysis'] = coastal_analysis
                
                # Calculate risk level based on multiple factors
                risk_level = self._calculate_tsunami_risk_level(
                    asteroid_diameter_m, elevation_m, coastal_analysis
                )
                risk_assessment['risk_level'] = risk_level
                
                # Generate warnings and recommendations
                warnings = self._generate_tsunami_warnings(
                    risk_level, asteroid_diameter_m, coastal_analysis
                )
                risk_assessment['warnings'] = warnings
                
            else:
                # Land impact - check if close to water bodies
                distance_to_water = self._estimate_distance_to_water(impact_lat, impact_lon)
                
                if distance_to_water < 50:  # Within 50km of water
                    risk_assessment['risk_factors'].append(f'Impact within ~{distance_to_water}km of water body')
                    
                    if asteroid_diameter_m > 500:  # Large asteroid
                        risk_assessment['tsunami_likely'] = True
                        risk_assessment['risk_level'] = 'low'
                        risk_assessment['warnings'].append('Large asteroid impact near water may cause local tsunamis')
                
                risk_assessment['distance_to_water_km'] = distance_to_water
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error in tsunami risk assessment: {str(e)}")
            return {
                'tsunami_likely': False,
                'risk_level': 'unknown',
                'error': str(e),
                'impact_location': {
                    'latitude': impact_lat,
                    'longitude': impact_lon,
                    'elevation_m': None,
                    'is_underwater': False
                }
            }
    
    def _get_tsunami_size_factor(self, diameter_m: float) -> Dict[str, Any]:
        """Get tsunami generation potential based on asteroid size."""
        if diameter_m < 50:
            return {'category': 'negligible', 'description': 'Too small to generate significant tsunamis'}
        elif diameter_m < 200:
            return {'category': 'minor', 'description': 'May cause local wave disturbances'}
        elif diameter_m < 500:
            return {'category': 'moderate', 'description': 'Can generate regional tsunamis'}
        elif diameter_m < 1000:
            return {'category': 'major', 'description': 'Can generate large regional tsunamis'}
        else:
            return {'category': 'catastrophic', 'description': 'Can generate ocean-wide mega-tsunamis'}
    
    def _analyze_coastal_impact(self, impact_lat: float, impact_lon: float, 
                               diameter_m: float, search_radius_km: float) -> Dict[str, Any]:
        """Analyze potential coastal impact areas."""
        
        # Sample multiple points around the impact to find coastlines
        sample_points = self._generate_sample_points(impact_lat, impact_lon, search_radius_km)
        
        coastlines = []
        land_points = []
        water_points = []
        
        for point in sample_points:
            elevation_data = self.get_elevation_single(point['lat'], point['lon'])
            elevation = elevation_data.get('elevation', 0)
            
            if elevation <= 0:
                water_points.append({
                    'lat': point['lat'],
                    'lon': point['lon'],
                    'elevation': elevation,
                    'distance_km': point['distance_km']
                })
            else:
                land_points.append({
                    'lat': point['lat'],
                    'lon': point['lon'], 
                    'elevation': elevation,
                    'distance_km': point['distance_km']
                })
        
        # Estimate wave height based on asteroid size and water depth
        estimated_wave_height = self._estimate_tsunami_wave_height(diameter_m, abs(min([p['elevation'] for p in water_points] + [0])))
        
        # Identify potentially affected coastal regions
        affected_regions = self._identify_coastal_regions(impact_lat, impact_lon, search_radius_km)
        
        return {
            'total_sample_points': len(sample_points),
            'water_points': len(water_points),
            'land_points': len(land_points),
            'water_to_land_ratio': len(water_points) / len(sample_points) if sample_points else 0,
            'max_wave_height_estimate_m': estimated_wave_height,
            'affected_regions': affected_regions,
            'search_radius_km': search_radius_km
        }
    
    def _generate_sample_points(self, center_lat: float, center_lon: float, 
                               radius_km: float, num_points: int = 16) -> List[Dict[str, Any]]:
        """Generate sample points in a circle around the impact location."""
        import math
        
        points = []
        for i in range(num_points):
            # Generate points in a circle
            angle = (2 * math.pi * i) / num_points
            
            # Convert km to degrees (approximate)
            lat_offset = (radius_km / 111) * math.cos(angle)
            lon_offset = (radius_km / 111) * math.sin(angle) / math.cos(math.radians(center_lat))
            
            point_lat = center_lat + lat_offset
            point_lon = center_lon + lon_offset
            
            points.append({
                'lat': point_lat,
                'lon': point_lon,
                'angle': angle,
                'distance_km': radius_km
            })
        
        return points
    
    def _estimate_tsunami_wave_height(self, diameter_m: float, water_depth_m: float) -> float:
        """Estimate tsunami wave height based on asteroid size and water depth."""
        # Simplified tsunami wave height estimation
        # Real calculations would be much more complex
        
        # Base energy factor from asteroid size
        if diameter_m < 100:
            energy_factor = 1
        elif diameter_m < 500:
            energy_factor = 5
        elif diameter_m < 1000:
            energy_factor = 20
        else:
            energy_factor = 50
        
        # Water depth factor (shallower water = higher waves near shore)
        depth_factor = max(1, 100 / max(water_depth_m, 10))
        
        # Estimate wave height
        estimated_height = energy_factor * depth_factor * 0.1
        
        return min(estimated_height, 100)  # Cap at reasonable maximum
    
    def _identify_coastal_regions(self, impact_lat: float, impact_lon: float, 
                                 radius_km: float) -> List[str]:
        """Identify major coastal regions that could be affected."""
        # Simplified regional identification based on coordinates
        # Real implementation would use detailed geographic databases
        
        regions = []
        
        # Major ocean/sea identification
        if -180 <= impact_lon <= -30:  # Atlantic/Pacific Americas
            if impact_lat > 0:
                regions.extend(['North American Coast', 'European Coast'])
            else:
                regions.extend(['South American Coast', 'African Coast'])
        elif -30 <= impact_lon <= 60:  # Atlantic/Indian Ocean
            if impact_lat > 0:
                regions.extend(['European Coast', 'Middle Eastern Coast'])
            else:
                regions.extend(['African Coast', 'Indian Ocean Islands'])
        elif 60 <= impact_lon <= 180:  # Pacific/Indian Ocean
            if impact_lat > 0:
                regions.extend(['Asian Coast', 'Pacific Islands'])
            else:
                regions.extend(['Australian Coast', 'Pacific Islands'])
        
        # Add specific high-risk areas based on location
        if 20 <= impact_lat <= 50 and 120 <= impact_lon <= 150:
            regions.append('Japan Coast (High Risk)')
        elif -10 <= impact_lat <= 10 and 90 <= impact_lon <= 120:
            regions.append('Indonesia/Philippines (High Risk)')
        elif 30 <= impact_lat <= 45 and -130 <= impact_lon <= -115:
            regions.append('US West Coast (High Risk)')
        
        return regions[:5]  # Limit to top 5 regions
    
    def _calculate_tsunami_risk_level(self, diameter_m: float, elevation_m: float, 
                                    coastal_analysis: Dict[str, Any]) -> str:
        """Calculate overall tsunami risk level."""
        risk_score = 0
        
        # Size factor
        if diameter_m > 1000:
            risk_score += 5
        elif diameter_m > 500:
            risk_score += 4
        elif diameter_m > 200:
            risk_score += 3
        elif diameter_m > 100:
            risk_score += 2
        else:
            risk_score += 1
        
        # Location factor
        if elevation_m < -1000:  # Deep ocean
            risk_score += 3
        elif elevation_m < -100:  # Continental shelf
            risk_score += 4
        elif elevation_m <= 0:  # Shallow water/coastline
            risk_score += 5
        
        # Coastal proximity factor
        water_ratio = coastal_analysis.get('water_to_land_ratio', 0)
        if water_ratio > 0.8:
            risk_score += 2
        elif water_ratio > 0.5:
            risk_score += 1
        
        # Convert score to risk level
        if risk_score >= 9:
            return 'extreme'
        elif risk_score >= 7:
            return 'high'
        elif risk_score >= 5:
            return 'moderate'
        elif risk_score >= 3:
            return 'low'
        else:
            return 'minimal'
    
    def _generate_tsunami_warnings(self, risk_level: str, diameter_m: float, 
                                  coastal_analysis: Dict[str, Any]) -> List[str]:
        """Generate tsunami warnings and recommendations."""
        warnings = []
        
        if risk_level in ['extreme', 'high']:
            warnings.append('⚠️ EXTREME TSUNAMI RISK: Immediate evacuation of all coastal areas required')
            warnings.append(f'🌊 Estimated wave heights up to {coastal_analysis.get("max_wave_height_estimate_m", 0):.1f}m')
            warnings.append('📍 Evacuate areas within 10km of coastline to elevations above 30m')
            
        elif risk_level == 'moderate':
            warnings.append('⚠️ MODERATE TSUNAMI RISK: Coastal areas should prepare for evacuation')
            warnings.append(f'🌊 Estimated wave heights up to {coastal_analysis.get("max_wave_height_estimate_m", 0):.1f}m')
            warnings.append('📍 Evacuate low-lying coastal areas to higher ground')
            
        elif risk_level == 'low':
            warnings.append('⚠️ LOW TSUNAMI RISK: Monitor coastal areas for unusual wave activity')
            warnings.append('📍 Be prepared to move away from immediate shoreline')
        
        # Add region-specific warnings
        affected_regions = coastal_analysis.get('affected_regions', [])
        if affected_regions:
            warnings.append(f'🗺️ Potentially affected regions: {", ".join(affected_regions)}')
        
        return warnings
    
    def _estimate_distance_to_water(self, lat: float, lon: float) -> float:
        """Estimate approximate distance to nearest water body."""
        # Very simplified estimation based on known geographic features
        # Real implementation would use detailed coastline databases
        
        # Major continental interior regions (rough estimates)
        if (20 <= lat <= 50) and (-105 <= lon <= -95):  # Central US
            return 800
        elif (45 <= lat <= 65) and (30 <= lon <= 140):  # Central Asia
            return 1000
        elif (-30 <= lat <= 10) and (10 <= lon <= 30):  # Central Africa
            return 500
        elif (-40 <= lat <= -10) and (-70 <= lon <= -40):  # Central South America
            return 600
        else:
            # Default assumption - most places are within 200km of water
            return 100
    
    def validate_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Validate geographic coordinates.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Validation result
        """
        errors = []
        
        if not isinstance(lat, (int, float)):
            errors.append("Latitude must be a number")
        elif not (-90 <= lat <= 90):
            errors.append("Latitude must be between -90 and 90 degrees")
        
        if not isinstance(lon, (int, float)):
            errors.append("Longitude must be a number")
        elif not (-180 <= lon <= 180):
            errors.append("Longitude must be between -180 and 180 degrees")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'coordinates': {
                'latitude': lat,
                'longitude': lon
            }
        }
    
    def get_location_info(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get general location information for coordinates.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Location information
        """
        # Basic location characterization
        location_info = {
            'coordinates': {'lat': lat, 'lon': lon},
            'hemisphere': {
                'ns': 'Northern' if lat >= 0 else 'Southern',
                'ew': 'Eastern' if lon >= 0 else 'Western'
            },
            'general_region': self._get_general_region(lat, lon),
            'climate_zone': self._get_climate_zone(lat),
            'ocean_proximity': self._estimate_ocean_proximity(lat, lon)
        }
        
        return location_info
    
    def _get_general_region(self, lat: float, lon: float) -> str:
        """Get general geographic region."""
        if -90 <= lat <= -60:
            return "Antarctica"
        elif -60 <= lat <= -23.5:
            return "Southern Temperate"
        elif -23.5 <= lat <= 23.5:
            return "Tropical"
        elif 23.5 <= lat <= 60:
            return "Northern Temperate"
        elif 60 <= lat <= 90:
            return "Arctic"
        else:
            return "Unknown"
    
    def _get_climate_zone(self, lat: float) -> str:
        """Get basic climate zone."""
        abs_lat = abs(lat)
        if abs_lat <= 23.5:
            return "Tropical"
        elif abs_lat <= 35:
            return "Subtropical"
        elif abs_lat <= 60:
            return "Temperate"
        else:
            return "Polar"
    
    def _estimate_ocean_proximity(self, lat: float, lon: float) -> str:
        """Rough estimate of ocean proximity."""
        # This is very simplified - real implementation would use coastline data
        # Major continental areas (very rough approximation)
        if (20 <= lat <= 70) and (-10 <= lon <= 60):  # Europe/Asia
            return "Continental"
        elif (30 <= lat <= 50) and (-125 <= lon <= -65):  # North America
            return "Continental"
        else:
            return "Coastal/Island"
    
    def _get_tsunami_size_factor(self, diameter_m: float) -> Dict[str, Any]:
        """Get tsunami generation potential based on asteroid size."""
        if diameter_m < 50:
            return {'category': 'negligible', 'description': 'Too small to generate significant tsunamis'}
        elif diameter_m < 200:
            return {'category': 'minor', 'description': 'May cause local wave disturbances'}
        elif diameter_m < 500:
            return {'category': 'moderate', 'description': 'Can generate regional tsunamis'}
        elif diameter_m < 1000:
            return {'category': 'major', 'description': 'Can generate large regional tsunamis'}
        else:
            return {'category': 'catastrophic', 'description': 'Can generate ocean-wide mega-tsunamis'}
    
    def _analyze_coastal_impact(self, impact_lat: float, impact_lon: float, 
                               diameter_m: float, search_radius_km: float) -> Dict[str, Any]:
        """Analyze potential coastal impact areas."""
        
        # Sample multiple points around the impact to find coastlines
        sample_points = self._generate_sample_points(impact_lat, impact_lon, search_radius_km)
        
        coastlines = []
        land_points = []
        water_points = []
        
        for point in sample_points:
            elevation_data = self.get_elevation_single(point['lat'], point['lon'])
            elevation = elevation_data.get('elevation', 0)
            
            if elevation <= 0:
                water_points.append({
                    'lat': point['lat'],
                    'lon': point['lon'],
                    'elevation': elevation,
                    'distance_km': point['distance_km']
                })
            else:
                land_points.append({
                    'lat': point['lat'],
                    'lon': point['lon'], 
                    'elevation': elevation,
                    'distance_km': point['distance_km']
                })
        
        # Estimate wave height based on asteroid size and water depth
        estimated_wave_height = self._estimate_tsunami_wave_height(diameter_m, abs(min([p['elevation'] for p in water_points] + [0])))
        
        # Identify potentially affected coastal regions
        affected_regions = self._identify_coastal_regions(impact_lat, impact_lon, search_radius_km)
        
        return {
            'total_sample_points': len(sample_points),
            'water_points': len(water_points),
            'land_points': len(land_points),
            'water_to_land_ratio': len(water_points) / len(sample_points) if sample_points else 0,
            'max_wave_height_estimate_m': estimated_wave_height,
            'affected_regions': affected_regions,
            'search_radius_km': search_radius_km
        }
    
    def _generate_sample_points(self, center_lat: float, center_lon: float, 
                               radius_km: float, num_points: int = 16) -> List[Dict[str, Any]]:
        """Generate sample points in a circle around the impact location."""
        points = []
        for i in range(num_points):
            # Generate points in a circle
            angle = (2 * math.pi * i) / num_points
            
            # Convert km to degrees (approximate)
            lat_offset = (radius_km / 111) * math.cos(angle)
            lon_offset = (radius_km / 111) * math.sin(angle) / math.cos(math.radians(center_lat))
            
            point_lat = center_lat + lat_offset
            point_lon = center_lon + lon_offset
            
            points.append({
                'lat': point_lat,
                'lon': point_lon,
                'angle': angle,
                'distance_km': radius_km
            })
        
        return points
    
    def _estimate_tsunami_wave_height(self, diameter_m: float, water_depth_m: float) -> float:
        """Estimate tsunami wave height based on asteroid size and water depth."""
        # Simplified tsunami wave height estimation
        # Real calculations would be much more complex
        
        # Base energy factor from asteroid size
        if diameter_m < 100:
            energy_factor = 1
        elif diameter_m < 500:
            energy_factor = 5
        elif diameter_m < 1000:
            energy_factor = 20
        else:
            energy_factor = 50
        
        # Water depth factor (shallower water = higher waves near shore)
        depth_factor = max(1, 100 / max(water_depth_m, 10))
        
        # Estimate wave height
        estimated_height = energy_factor * depth_factor * 0.1
        
        return min(estimated_height, 100)  # Cap at reasonable maximum
    
    def _identify_coastal_regions(self, impact_lat: float, impact_lon: float, 
                                 radius_km: float) -> List[str]:
        """Identify major coastal regions that could be affected."""
        # Simplified regional identification based on coordinates
        # Real implementation would use detailed geographic databases
        
        regions = []
        
        # Major ocean/sea identification
        if -180 <= impact_lon <= -30:  # Atlantic/Pacific Americas
            if impact_lat > 0:
                regions.extend(['North American Coast', 'European Coast'])
            else:
                regions.extend(['South American Coast', 'African Coast'])
        elif -30 <= impact_lon <= 60:  # Atlantic/Indian Ocean
            if impact_lat > 0:
                regions.extend(['European Coast', 'Middle Eastern Coast'])
            else:
                regions.extend(['African Coast', 'Indian Ocean Islands'])
        elif 60 <= impact_lon <= 180:  # Pacific/Indian Ocean
            if impact_lat > 0:
                regions.extend(['Asian Coast', 'Pacific Islands'])
            else:
                regions.extend(['Australian Coast', 'Pacific Islands'])
        
        # Add specific high-risk areas based on location
        if 20 <= impact_lat <= 50 and 120 <= impact_lon <= 150:
            regions.append('Japan Coast (High Risk)')
        elif -10 <= impact_lat <= 10 and 90 <= impact_lon <= 120:
            regions.append('Indonesia/Philippines (High Risk)')
        elif 30 <= impact_lat <= 45 and -130 <= impact_lon <= -115:
            regions.append('US West Coast (High Risk)')
        
        return regions[:5]  # Limit to top 5 regions
    
    def _calculate_tsunami_risk_level(self, diameter_m: float, elevation_m: float, 
                                    coastal_analysis: Dict[str, Any]) -> str:
        """Calculate overall tsunami risk level."""
        risk_score = 0
        
        # Size factor
        if diameter_m > 1000:
            risk_score += 5
        elif diameter_m > 500:
            risk_score += 4
        elif diameter_m > 200:
            risk_score += 3
        elif diameter_m > 100:
            risk_score += 2
        else:
            risk_score += 1
        
        # Location factor
        if elevation_m < -1000:  # Deep ocean
            risk_score += 3
        elif elevation_m < -100:  # Continental shelf
            risk_score += 4
        elif elevation_m <= 0:  # Shallow water/coastline
            risk_score += 5
        
        # Coastal proximity factor
        water_ratio = coastal_analysis.get('water_to_land_ratio', 0)
        if water_ratio > 0.8:
            risk_score += 2
        elif water_ratio > 0.5:
            risk_score += 1
        
        # Convert score to risk level
        if risk_score >= 9:
            return 'extreme'
        elif risk_score >= 7:
            return 'high'
        elif risk_score >= 5:
            return 'moderate'
        elif risk_score >= 3:
            return 'low'
        else:
            return 'minimal'
    
    def _generate_tsunami_warnings(self, risk_level: str, diameter_m: float, 
                                  coastal_analysis: Dict[str, Any]) -> List[str]:
        """Generate tsunami warnings and recommendations."""
        warnings = []
        
        if risk_level in ['extreme', 'high']:
            warnings.append('⚠️ EXTREME TSUNAMI RISK: Immediate evacuation of all coastal areas required')
            warnings.append(f'🌊 Estimated wave heights up to {coastal_analysis.get("max_wave_height_estimate_m", 0):.1f}m')
            warnings.append('📍 Evacuate areas within 10km of coastline to elevations above 30m')
            
        elif risk_level == 'moderate':
            warnings.append('⚠️ MODERATE TSUNAMI RISK: Coastal areas should prepare for evacuation')
            warnings.append(f'🌊 Estimated wave heights up to {coastal_analysis.get("max_wave_height_estimate_m", 0):.1f}m')
            warnings.append('📍 Evacuate low-lying coastal areas to higher ground')
            
        elif risk_level == 'low':
            warnings.append('⚠️ LOW TSUNAMI RISK: Monitor coastal areas for unusual wave activity')
            warnings.append('📍 Be prepared to move away from immediate shoreline')
        
        # Add region-specific warnings
        affected_regions = coastal_analysis.get('affected_regions', [])
        if affected_regions:
            warnings.append(f'🗺️ Potentially affected regions: {", ".join(affected_regions)}')
        
        return warnings
    
    def _estimate_distance_to_water(self, lat: float, lon: float) -> float:
        """Estimate approximate distance to nearest water body."""
        # Very simplified estimation based on known geographic features
        # Real implementation would use detailed coastline databases
        
        # Major continental interior regions (rough estimates)
        if (20 <= lat <= 50) and (-105 <= lon <= -95):  # Central US
            return 800
        elif (45 <= lat <= 65) and (30 <= lon <= 140):  # Central Asia
            return 1000
        elif (-30 <= lat <= 10) and (10 <= lon <= 30):  # Central Africa
            return 500
        elif (-40 <= lat <= -10) and (-70 <= lon <= -40):  # Central South America
            return 600
        else:
            # Default assumption - most places are within 200km of water
            return 100
    
    def get_historical_earthquakes(self) -> Dict[str, float]:
        """
        Get historical earthquake data from USGS API with fallback to static data.
        
        Returns:
            dict: Historical earthquake magnitudes for comparison
        """
        try:
            # Try to fetch recent significant earthquakes from USGS
            end_time = datetime.utcnow()
            start_time = datetime(2000, 1, 1)  # From year 2000
            
            params = {
                'format': 'geojson',
                'starttime': start_time.strftime('%Y-%m-%d'),
                'endtime': end_time.strftime('%Y-%m-%d'),
                'minmagnitude': 7.0,
                'orderby': 'magnitude',
                'limit': 20
            }
            
            response = requests.get(
                self.apis['earthquake']['base_url'],
                params=params,
                timeout=self.apis['earthquake']['timeout']
            )
            
            if response.status_code == 200:
                data = response.json()
                earthquakes = {}
                
                # Process earthquake data
                for feature in data.get('features', []):
                    props = feature['properties']
                    magnitude = props.get('mag')
                    place = props.get('place', 'Unknown')
                    time_ms = props.get('time', 0)
                    
                    if magnitude and time_ms:
                        # Create a readable name
                        eq_time = datetime.fromtimestamp(time_ms / 1000)
                        year = eq_time.year
                        
                        # Clean up place name
                        if place and place != 'Unknown':
                            # Extract main location from USGS place format
                            if ' of ' in place:
                                location = place.split(' of ')[-1]
                            else:
                                location = place
                            
                            # Limit length and clean
                            location = location.split(',')[0][:20]
                            name = f"{year} {location}"
                        else:
                            name = f"{year} Earthquake"
                        
                        earthquakes[name] = magnitude
                
                # Add some well-known historical earthquakes if we have room
                well_known = {
                    '2011 Japan': 9.1,
                    '2004 Sumatra': 9.1,
                    '1960 Chile': 9.5,
                    '1964 Alaska': 9.2
                }
                
                # Merge with API data, preferring API data
                for name, mag in well_known.items():
                    if len(earthquakes) < 8:  # Keep reasonable number for comparison
                        earthquakes[name] = mag
                
                if earthquakes:
                    logger.info(f"Successfully fetched {len(earthquakes)} earthquakes from USGS API")
                    return earthquakes
            
            # If API fails, log and fall through to static data
            logger.warning(f"USGS Earthquake API failed with status {response.status_code}")
            
        except Exception as e:
            logger.warning(f"Failed to fetch earthquake data from USGS API: {str(e)}")
        
        # Fallback to static historical data
        logger.info("Using fallback static earthquake data")
        return {
            '2011 Japan': 9.1,
            '2004 Sumatra': 9.1,
            '1906 San Francisco': 7.9,
            '2010 Haiti': 7.0,
            '1994 Northridge': 6.7,
            '1960 Chile': 9.5
        }
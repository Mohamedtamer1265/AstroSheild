"""
🌍 Enhanced Earthquake Data Integration
NASA Space Apps 2024

Example of how to add live USGS earthquake data to the asteroid impact system.
This would replace the static earthquake comparison with dynamic API data.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EarthquakeAPIManager:
    """Manager for USGS earthquake data integration."""
    
    def __init__(self):
        """Initialize earthquake API manager."""
        self.usgs_base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.timeout = 10
        
        # Famous historical earthquakes as fallback
        self.historical_earthquakes = {
            '2011 Japan (Tōhoku)': 9.1,
            '2004 Sumatra': 9.1,
            '1960 Chile': 9.5,
            '1964 Alaska': 9.2,
            '2010 Haiti': 7.0,
            '1906 San Francisco': 7.9,
            '1994 Northridge': 6.7,
            '2023 Turkey-Syria': 7.8
        }
    
    def get_recent_earthquakes(self, min_magnitude: float = 6.0, 
                             days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch recent significant earthquakes from USGS.
        
        Args:
            min_magnitude (float): Minimum magnitude to include
            days_back (int): Number of days to look back
            
        Returns:
            list: Recent earthquake data
        """
        try:
            # Calculate date range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days_back)
            
            # USGS API parameters
            params = {
                'format': 'geojson',
                'starttime': start_time.strftime('%Y-%m-%d'),
                'endtime': end_time.strftime('%Y-%m-%d'),
                'minmagnitude': min_magnitude,
                'orderby': 'magnitude',
                'limit': 20
            }
            
            response = requests.get(self.usgs_base_url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                earthquakes = []
                
                for feature in data.get('features', []):
                    props = feature['properties']
                    coords = feature['geometry']['coordinates']
                    
                    earthquakes.append({
                        'magnitude': props.get('mag'),
                        'location': props.get('place', 'Unknown'),
                        'time': datetime.fromtimestamp(props.get('time', 0) / 1000),
                        'latitude': coords[1],
                        'longitude': coords[0],
                        'depth_km': coords[2] if len(coords) > 2 else 0,
                        'url': props.get('url', '')
                    })
                
                return sorted(earthquakes, key=lambda x: x['magnitude'], reverse=True)
            
            else:
                logger.warning(f"USGS API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching earthquake data: {str(e)}")
            return []
    
    def get_regional_earthquakes(self, lat: float, lon: float, 
                               radius_km: float = 1000, 
                               min_magnitude: float = 5.0,
                               years_back: int = 10) -> List[Dict[str, Any]]:
        """
        Get historical earthquakes in a region around the impact point.
        
        Args:
            lat (float): Center latitude
            lon (float): Center longitude
            radius_km (float): Search radius in kilometers
            min_magnitude (float): Minimum magnitude
            years_back (int): Years of history to search
            
        Returns:
            list: Regional earthquake history
        """
        try:
            # Calculate date range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=years_back * 365)
            
            # Convert radius to degrees (approximate)
            radius_deg = radius_km / 111.0  # 1 degree ≈ 111 km
            
            params = {
                'format': 'geojson',
                'starttime': start_time.strftime('%Y-%m-%d'),
                'endtime': end_time.strftime('%Y-%m-%d'),
                'latitude': lat,
                'longitude': lon,
                'maxradiuskm': radius_km,
                'minmagnitude': min_magnitude,
                'orderby': 'magnitude',
                'limit': 50
            }
            
            response = requests.get(self.usgs_base_url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                earthquakes = []
                
                for feature in data.get('features', []):
                    props = feature['properties']
                    coords = feature['geometry']['coordinates']
                    
                    earthquakes.append({
                        'magnitude': props.get('mag'),
                        'location': props.get('place', 'Unknown'),
                        'time': datetime.fromtimestamp(props.get('time', 0) / 1000),
                        'latitude': coords[1],
                        'longitude': coords[0],
                        'depth_km': coords[2] if len(coords) > 2 else 0,
                        'distance_km': self._calculate_distance(lat, lon, coords[1], coords[0])
                    })
                
                return sorted(earthquakes, key=lambda x: x['magnitude'], reverse=True)
            
            else:
                logger.warning(f"USGS API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching regional earthquake data: {str(e)}")
            return []
    
    def create_enhanced_seismic_comparison(self, impact_magnitude: float, 
                                         impact_lat: float = None, 
                                         impact_lon: float = None) -> Dict[str, Any]:
        """
        Create enhanced seismic comparison with live and historical data.
        
        Args:
            impact_magnitude (float): Calculated impact magnitude
            impact_lat (float): Impact latitude for regional context
            impact_lon (float): Impact longitude for regional context
            
        Returns:
            dict: Enhanced comparison data
        """
        comparison_data = {
            'impact_magnitude': impact_magnitude,
            'categories': {}
        }
        
        # Add the impact
        comparison_data['categories']['This Impact'] = [{
            'name': 'Asteroid Impact',
            'magnitude': impact_magnitude,
            'type': 'impact',
            'is_impact': True
        }]
        
        # Add historical reference earthquakes
        historical_list = []
        for name, magnitude in self.historical_earthquakes.items():
            historical_list.append({
                'name': name,
                'magnitude': magnitude,
                'type': 'historical',
                'is_impact': False
            })
        
        comparison_data['categories']['Historical Major'] = sorted(
            historical_list, key=lambda x: x['magnitude'], reverse=True
        )
        
        # Add recent earthquakes
        recent_earthquakes = self.get_recent_earthquakes(min_magnitude=6.0, days_back=365)
        if recent_earthquakes:
            recent_list = []
            for eq in recent_earthquakes[:10]:  # Top 10 recent
                recent_list.append({
                    'name': f"{eq['location']} ({eq['time'].year})",
                    'magnitude': eq['magnitude'],
                    'type': 'recent',
                    'is_impact': False,
                    'date': eq['time']
                })
            
            comparison_data['categories']['Recent (Last Year)'] = recent_list
        
        # Add regional context if coordinates provided
        if impact_lat is not None and impact_lon is not None:
            regional_earthquakes = self.get_regional_earthquakes(
                impact_lat, impact_lon, radius_km=500, min_magnitude=5.0, years_back=20
            )
            
            if regional_earthquakes:
                regional_list = []
                for eq in regional_earthquakes[:10]:  # Top 10 regional
                    regional_list.append({
                        'name': f"{eq['location']} ({eq['time'].year})",
                        'magnitude': eq['magnitude'], 
                        'type': 'regional',
                        'is_impact': False,
                        'distance_km': eq['distance_km'],
                        'date': eq['time']
                    })
                
                comparison_data['categories']['Regional (500km)'] = regional_list
        
        return comparison_data
    
    def _calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calculate approximate distance between two points in km."""
        import math
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in km
        r = 6371
        
        return r * c


# Example integration into the visualization manager
def enhanced_seismic_comparison_example():
    """Example of how to use enhanced earthquake data in visualizations."""
    
    # Initialize earthquake API manager
    eq_manager = EarthquakeAPIManager()
    
    # Example impact magnitude
    impact_magnitude = 6.8
    impact_lat = 40.7128  # New York
    impact_lon = -74.0060
    
    # Get enhanced comparison
    comparison = eq_manager.create_enhanced_seismic_comparison(
        impact_magnitude, impact_lat, impact_lon
    )
    
    # This would replace the static comparison in visualization.py
    return {
        'seismic_comparison': {
            'title': 'Enhanced Seismic Magnitude Comparison',
            'impact_magnitude': impact_magnitude,
            'categories': comparison['categories'],
            'data_sources': ['USGS Recent', 'USGS Historical', 'Regional Context'],
            'last_updated': datetime.utcnow().isoformat()
        }
    }


if __name__ == "__main__":
    # Test the earthquake API integration
    eq_manager = EarthquakeAPIManager()
    
    print("🌍 Testing USGS Earthquake API Integration...")
    
    # Test recent earthquakes
    recent = eq_manager.get_recent_earthquakes(min_magnitude=6.5, days_back=30)
    print(f"📊 Found {len(recent)} recent significant earthquakes")
    
    # Test regional earthquakes around Tokyo
    regional = eq_manager.get_regional_earthquakes(35.6762, 139.6503, radius_km=1000)
    print(f"🗾 Found {len(regional)} earthquakes near Tokyo in last 10 years")
    
    # Test enhanced comparison
    comparison = eq_manager.create_enhanced_seismic_comparison(7.2, 35.6762, 139.6503)
    print(f"📈 Created enhanced comparison with {len(comparison['categories'])} categories")
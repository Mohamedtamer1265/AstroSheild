"""
Asteroid Data Fetcher - NASA JPL Small-Body Database Integration
Fetches real asteroid data from JPL's Small-Body Database for impact predictions.
"""

import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class PracticalAsteroidFetcher:
    """Fetch real asteroid data from JPL for predictions"""
    
    def __init__(self):
        self.jpl_url = "https://ssd-api.jpl.nasa.gov/sbdb.api"
        
    def fetch_asteroid_data(self, asteroid_id: str) -> Dict:
        """Fetch real asteroid data from JPL database"""
        try:
            params = {
                'sstr': asteroid_id,
                'full-prec': 'true',
                'phys-par': 'true'
            }
            
            logger.info(f"Fetching asteroid data for ID: {asteroid_id}")
            response = requests.get(self.jpl_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if 'object' not in data:
                logger.warning(f"No object data found for asteroid ID: {asteroid_id}")
                return {'success': False, 'error': 'Asteroid not found'}
            
            # Parse orbital elements
            orbital_elements = self._parse_orbital_elements(data)
            physical_properties = self._parse_physical_properties(data)
            
            result = {
                'success': True,
                'id': asteroid_id,
                'name': data['object'].get('fullname', asteroid_id),
                'neo': data['object'].get('neo', False),
                'pha': data['object'].get('pha', False),
                'orbital_elements': orbital_elements,
                'physical_properties': physical_properties,
                'source': 'JPL Small-Body Database'
            }
            
            logger.info(f"Successfully fetched data for asteroid: {result['name']}")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching asteroid data: {str(e)}")
            return {'success': False, 'error': f'Network error: {str(e)}'}
        except Exception as e:
            logger.error(f"Error fetching asteroid data: {str(e)}")
            return {'success': False, 'error': f'Data parsing error: {str(e)}'}
    
    def _parse_orbital_elements(self, data: Dict) -> Dict:
        """Parse orbital elements from JPL response"""
        elements = {}
        
        if 'orbit' in data and 'elements' in data['orbit']:
            for elem in data['orbit']['elements']:
                name = elem.get('name', '')
                try:
                    value = float(elem.get('value', 0))
                    
                    # Map JPL names to our standard names
                    if name == 'a':
                        elements['semi_major_axis'] = value
                    elif name == 'e':
                        elements['eccentricity'] = value
                    elif name == 'i':
                        elements['inclination'] = value
                    elif name == 'om':
                        elements['ascending_node'] = value
                    elif name == 'w':
                        elements['argument_perihelion'] = value
                    elif name == 'ma':
                        elements['mean_anomaly'] = value
                    elif name == 'epoch':
                        elements['epoch'] = value
                    elif name == 'n':
                        elements['mean_motion_deg_day'] = value
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse orbital element {name}: {elem.get('value')}")
                    continue
        
        # Set defaults if missing
        defaults = {
            'semi_major_axis': 2.0,
            'eccentricity': 0.2,
            'inclination': 5.0,
            'ascending_node': 45.0,
            'argument_perihelion': 30.0,
            'mean_anomaly': 0.0,
            'epoch': 2451545.0,  # J2000
            'mean_motion_deg_day': 0.5
        }
        
        for key, default_value in defaults.items():
            if key not in elements:
                elements[key] = default_value
                logger.debug(f"Using default value for {key}: {default_value}")
        
        return elements
    
    def _parse_physical_properties(self, data: Dict) -> Dict:
        """Parse physical properties from JPL response"""
        properties = {
            'diameter_km': 1.0,
            'absolute_magnitude': 20.0,
            'albedo': 0.14
        }
        
        if 'phys_par' in data:
            for phys in data['phys_par']:
                name = phys.get('name', '')
                try:
                    value = float(phys.get('value', 0))
                    if name == 'diameter':
                        properties['diameter_km'] = value
                    elif name == 'H':
                        properties['absolute_magnitude'] = value
                    elif name == 'albedo':
                        properties['albedo'] = value
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse physical property {name}: {phys.get('value')}")
                    continue
        
        return properties

    def search_asteroids(self, query: str, limit: int = 10) -> Dict:
        """Search for asteroids by name or designation"""
        try:
            # Use a simpler endpoint for searches
            search_url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
            params = {
                'fields': 'spkid,full_name,neo,pha,H,diameter',
                'sb-kind': 'a',  # asteroids only
                'full-name': f'*{query}*',
                'limit': limit
            }
            
            logger.info(f"Searching for asteroids with query: {query}")
            response = requests.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data:
                return {'success': False, 'error': 'No search results found'}
            
            results = []
            for row in data['data']:
                if len(row) >= 6:  # Ensure we have all expected fields
                    results.append({
                        'id': str(row[0]),
                        'name': row[1],
                        'neo': row[2] == '1' if row[2] else False,
                        'pha': row[3] == '1' if row[3] else False,
                        'absolute_magnitude': float(row[4]) if row[4] else None,
                        'diameter_km': float(row[5]) if row[5] else None
                    })
            
            return {
                'success': True,
                'query': query,
                'count': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error searching asteroids: {str(e)}")
            return {'success': False, 'error': f'Search failed: {str(e)}'}
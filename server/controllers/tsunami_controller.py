"""
🌊 Tsunami Risk Assessment Controller
NASA Space Apps 2024

REST API endpoints for tsunami risk assessment based on asteroid impact scenarios.
Analyzes elevation data and coastal proximity to determine tsunami generation potential.
"""

from flask import Blueprint, request, jsonify
from utils.nasa_apis import NASAAPIManager
import logging

logger = logging.getLogger(__name__)

# Create blueprint for tsunami endpoints
tsunami_bp = Blueprint('tsunami', __name__, url_prefix='/api/tsunami')

# Initialize NASA API manager
nasa_manager = NASAAPIManager()

@tsunami_bp.route('/assess', methods=['POST'])
def assess_tsunami_risk():
    """
    🌊 Assess tsunami risk for asteroid impact scenario
    
    POST /api/tsunami/assess
    Body: {
        "latitude": float,
        "longitude": float, 
        "diameter_m": float,
        "search_radius_km": float (optional, default: 1000)
    }
    
    Returns: {
        "success": bool,
        "data": {
            "location": dict,
            "impact_details": dict,
            "tsunami_assessment": dict,
            "risk_level": str,
            "warnings": list,
            "coastal_analysis": dict
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        required_fields = ['latitude', 'longitude', 'diameter_m']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract parameters
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        diameter_m = float(data['diameter_m'])
        search_radius_km = float(data.get('search_radius_km', 1000))
        
        # Validate parameter ranges
        if not (-90 <= latitude <= 90):
            return jsonify({
                'success': False,
                'error': 'Latitude must be between -90 and 90 degrees'
            }), 400
        
        if not (-180 <= longitude <= 180):
            return jsonify({
                'success': False,
                'error': 'Longitude must be between -180 and 180 degrees'
            }), 400
        
        if diameter_m <= 0:
            return jsonify({
                'success': False,
                'error': 'Asteroid diameter must be positive'
            }), 400
        
        if search_radius_km <= 0 or search_radius_km > 5000:
            return jsonify({
                'success': False,
                'error': 'Search radius must be between 0 and 5000 km'
            }), 400
        
        # Perform tsunami risk assessment
        logger.info(f"Assessing tsunami risk for impact at ({latitude}, {longitude}) "
                   f"with diameter {diameter_m}m")
        
        assessment_result = nasa_manager.assess_tsunami_risk(
            impact_lat=latitude,
            impact_lon=longitude,
            diameter_m=diameter_m,
            search_radius_km=search_radius_km
        )
        
        # Return successful response
        return jsonify({
            'success': True,
            'data': assessment_result,
            'message': f'Tsunami risk assessment completed for {diameter_m}m asteroid impact'
        })
    
    except ValueError as e:
        logger.error(f"Invalid parameter values: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Invalid parameter values: {str(e)}'
        }), 400
    
    except Exception as e:
        logger.error(f"Error in tsunami risk assessment: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to assess tsunami risk: {str(e)}'
        }), 500


@tsunami_bp.route('/risk-levels', methods=['GET'])
def get_risk_levels():
    """
    📊 Get information about tsunami risk levels
    
    GET /api/tsunami/risk-levels
    
    Returns: {
        "success": bool,
        "data": {
            "risk_levels": dict,
            "size_categories": dict,
            "assessment_factors": list
        }
    }
    """
    try:
        risk_info = {
            'risk_levels': {
                'minimal': {
                    'description': 'Very low tsunami risk',
                    'characteristics': 'Small asteroid or land impact',
                    'recommended_action': 'Monitor for updates'
                },
                'low': {
                    'description': 'Low tsunami risk',
                    'characteristics': 'Limited wave generation potential',
                    'recommended_action': 'Stay informed, prepare coastal monitoring'
                },
                'moderate': {
                    'description': 'Moderate tsunami risk',
                    'characteristics': 'Regional tsunami possible',
                    'recommended_action': 'Prepare evacuation plans for coastal areas'
                },
                'high': {
                    'description': 'High tsunami risk',
                    'characteristics': 'Large regional tsunami likely',
                    'recommended_action': 'Evacuate coastal areas immediately'
                },
                'extreme': {
                    'description': 'Extreme tsunami risk',
                    'characteristics': 'Ocean-wide mega-tsunami possible',
                    'recommended_action': 'Mass evacuation of all coastal regions'
                }
            },
            'size_categories': {
                'negligible': 'Diameter < 50m - Too small for significant tsunamis',
                'minor': 'Diameter 50-200m - Local wave disturbances possible',
                'moderate': 'Diameter 200-500m - Regional tsunamis possible',
                'major': 'Diameter 500-1000m - Large regional tsunamis likely',
                'catastrophic': 'Diameter > 1000m - Ocean-wide mega-tsunamis possible'
            },
            'assessment_factors': [
                'Asteroid diameter and impact energy',
                'Impact location (ocean depth, coastal proximity)',
                'Local topography and bathymetry',  
                'Distance to populated coastal areas',
                'Regional geographic features',
                'Wave propagation patterns'
            ]
        }
        
        return jsonify({
            'success': True,
            'data': risk_info,
            'message': 'Tsunami risk level information retrieved successfully'
        })
    
    except Exception as e:
        logger.error(f"Error retrieving risk level info: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve risk level information: {str(e)}'
        }), 500


@tsunami_bp.route('/quick-check', methods=['GET'])
def quick_tsunami_check():
    """
    ⚡ Quick tsunami risk check based on location
    
    GET /api/tsunami/quick-check?lat=X&lon=Y&diameter=Z
    
    Returns: {
        "success": bool,
        "data": {
            "is_water_impact": bool,
            "elevation_m": float,
            "risk_category": str,
            "quick_assessment": str
        }
    }
    """
    try:
        # Get query parameters
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lon', type=float)
        diameter_m = request.args.get('diameter', type=float)
        
        if None in [latitude, longitude, diameter_m]:
            return jsonify({
                'success': False,
                'error': 'Required parameters: lat, lon, diameter'
            }), 400
        
        # Get elevation data
        elevation_data = nasa_manager.get_elevation_single(latitude, longitude)
        elevation = elevation_data.get('elevation', 0)
        
        # Quick assessment
        is_water_impact = elevation <= 0
        
        if not is_water_impact:
            risk_category = 'minimal'
            quick_assessment = 'Land impact - minimal tsunami risk'
        else:
            if diameter_m < 50:
                risk_category = 'minimal'
                quick_assessment = 'Small asteroid, water impact - low tsunami risk'
            elif diameter_m < 200:
                risk_category = 'low'
                quick_assessment = 'Moderate asteroid, water impact - possible local tsunamis'
            elif diameter_m < 500:
                risk_category = 'moderate'  
                quick_assessment = 'Large asteroid, water impact - regional tsunami risk'
            else:
                risk_category = 'high'
                quick_assessment = 'Very large asteroid, water impact - major tsunami risk'
        
        return jsonify({
            'success': True,
            'data': {
                'is_water_impact': is_water_impact,
                'elevation_m': elevation,
                'risk_category': risk_category,
                'quick_assessment': quick_assessment,
                'diameter_m': diameter_m,
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                }
            }
        })
    
    except Exception as e:
        logger.error(f"Error in quick tsunami check: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Quick check failed: {str(e)}'
        }), 500


# Error handlers for the blueprint
@tsunami_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 'Bad request - check your parameters'
    }), 400


@tsunami_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
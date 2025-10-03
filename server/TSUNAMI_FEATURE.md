# 🌊 Tsunami Risk Assessment Feature

## Overview
The tsunami risk assessment feature analyzes the potential for tsunami generation from asteroid impacts by examining elevation data and coastal proximity. This feature determines if an impact location has water (elevation ≤ 0) and assesses the surrounding geography to evaluate tsunami risk.

## Key Features

### 🎯 Core Capabilities
- **Elevation-based Water Detection**: Determines if impact occurs in water (elevation ≤ 0 meters)
- **Coastal Proximity Analysis**: Examines surrounding areas to identify land/water boundaries
- **Risk Level Assessment**: Calculates tsunami risk from minimal to extreme
- **Size-based Categorization**: Evaluates asteroid size impact on tsunami generation
- **Regional Impact Estimation**: Identifies potentially affected coastal regions
- **Warning System**: Generates appropriate warnings and evacuation recommendations

### 📊 Risk Levels
- **Minimal**: Very low tsunami risk (land impacts, small asteroids)
- **Low**: Limited wave generation potential
- **Moderate**: Regional tsunami possible
- **High**: Large regional tsunami likely
- **Extreme**: Ocean-wide mega-tsunami possible

### 📏 Size Categories
- **Negligible** (< 50m): Too small for significant tsunamis
- **Minor** (50-200m): Local wave disturbances possible
- **Moderate** (200-500m): Regional tsunamis possible
- **Major** (500-1000m): Large regional tsunamis likely
- **Catastrophic** (> 1000m): Ocean-wide mega-tsunamis possible

## API Endpoints

### 1. Comprehensive Tsunami Assessment
```http
POST /api/tsunami/assess
Content-Type: application/json

{
    "latitude": 21.4,
    "longitude": -89.5,
    "diameter_m": 10000,
    "search_radius_km": 1000
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "location": {
            "latitude": 21.4,
            "longitude": -89.5,
            "elevation_m": -15.2,
            "impact_type": "Ocean Impact"
        },
        "impact_details": {
            "diameter_m": 10000,
            "search_radius_km": 1000
        },
        "tsunami_assessment": {
            "size_factor": {
                "category": "catastrophic",
                "description": "Can generate ocean-wide mega-tsunamis"
            },
            "is_water_impact": true,
            "distance_to_water_km": 0
        },
        "coastal_analysis": {
            "total_sample_points": 16,
            "water_points": 14,
            "land_points": 2,
            "water_to_land_ratio": 0.875,
            "max_wave_height_estimate_m": 45.2,
            "affected_regions": [
                "North American Coast",
                "South American Coast",
                "European Coast"
            ],
            "search_radius_km": 1000
        },
        "risk_level": "extreme",
        "warnings": [
            "⚠️ EXTREME TSUNAMI RISK: Immediate evacuation of all coastal areas required",
            "🌊 Estimated wave heights up to 45.2m",
            "📍 Evacuate areas within 10km of coastline to elevations above 30m"
        ]
    }
}
```

### 2. Quick Tsunami Check
```http
GET /api/tsunami/quick-check?lat=21.4&lon=-89.5&diameter=500
```

**Response:**
```json
{
    "success": true,
    "data": {
        "is_water_impact": true,
        "elevation_m": -15.2,
        "risk_category": "moderate",
        "quick_assessment": "Large asteroid, water impact - regional tsunami risk",
        "diameter_m": 500,
        "location": {
            "latitude": 21.4,
            "longitude": -89.5
        }
    }
}
```

### 3. Risk Level Information
```http
GET /api/tsunami/risk-levels
```

**Response:**
```json
{
    "success": true,
    "data": {
        "risk_levels": {
            "minimal": {
                "description": "Very low tsunami risk",
                "characteristics": "Small asteroid or land impact",
                "recommended_action": "Monitor for updates"
            },
            "extreme": {
                "description": "Extreme tsunami risk",
                "characteristics": "Ocean-wide mega-tsunami possible",
                "recommended_action": "Mass evacuation of all coastal regions"
            }
        },
        "size_categories": {
            "negligible": "Diameter < 50m - Too small for significant tsunamis",
            "catastrophic": "Diameter > 1000m - Ocean-wide mega-tsunamis possible"
        },
        "assessment_factors": [
            "Asteroid diameter and impact energy",
            "Impact location (ocean depth, coastal proximity)",
            "Local topography and bathymetry",
            "Distance to populated coastal areas"
        ]
    }
}
```

## Assessment Algorithm

### 1. Water Detection
```python
is_water_impact = elevation <= 0  # Sea level or below indicates water
```

### 2. Coastal Analysis
- Samples 16 points in a circle around the impact location
- Analyzes elevation at each point to identify land/water boundaries
- Calculates water-to-land ratio for coastal proximity assessment

### 3. Risk Calculation
Risk is determined by combining:
- **Asteroid size factor** (1-5 points based on diameter)
- **Impact location factor** (based on elevation/water depth)
- **Coastal proximity factor** (based on surrounding geography)

### 4. Wave Height Estimation
Simplified wave height calculation:
```python
wave_height = energy_factor * depth_factor * 0.1
```
Where:
- `energy_factor` depends on asteroid diameter
- `depth_factor` accounts for water depth (shallower = higher waves)

## Technical Implementation

### Files Structure
```
backend/
├── controllers/tsunami_controller.py    # REST API endpoints
├── utils/nasa_apis.py                  # Core assessment logic
└── test_tsunami.py                     # Test script
```

### Key Classes and Methods

#### NASAAPIManager.assess_tsunami_risk()
Main assessment method that:
1. Gets elevation data for impact location
2. Analyzes surrounding coastal geography
3. Calculates risk level based on multiple factors
4. Generates appropriate warnings

#### Helper Methods
- `_get_tsunami_size_factor()`: Categorizes asteroid by size
- `_analyze_coastal_impact()`: Examines surrounding geography
- `_calculate_tsunami_risk_level()`: Determines overall risk
- `_generate_tsunami_warnings()`: Creates warning messages
- `_estimate_distance_to_water()`: Estimates distance to nearest water body

### External API Integration
- **Open-Elevation API**: Provides elevation data for impact location and surrounding points
- **Geographic Analysis**: Uses coordinate-based regional identification

## Testing

### Test Script
Run the included test script to see the tsunami assessment in action:

```bash
cd backend
python test_tsunami.py
```

This will test various scenarios:
- Chicxulub-like impact (large ocean impact)
- Tunguska-like impact (small land impact)
- Pacific Ocean impact (deep water)
- Mediterranean impact (shallow sea)

### Example Test Scenarios

1. **Extreme Risk**: 10km asteroid in Gulf of Mexico
   - Risk Level: Extreme
   - Warnings: Immediate mass evacuation
   - Estimated waves: 45+ meters

2. **Minimal Risk**: 60m airburst over Siberia
   - Risk Level: Minimal  
   - Warnings: Monitor for updates
   - Impact Type: Land impact

3. **Moderate Risk**: 500m asteroid in Pacific
   - Risk Level: High
   - Warnings: Regional evacuation
   - Estimated waves: 15-20 meters

## Usage Examples

### Frontend Integration
```javascript
// Assess tsunami risk for an impact
const assessTsunami = async (lat, lon, diameter) => {
    const response = await fetch('/api/tsunami/assess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            latitude: lat,
            longitude: lon,
            diameter_m: diameter,
            search_radius_km: 1000
        })
    });
    
    const result = await response.json();
    if (result.success) {
        console.log('Risk Level:', result.data.risk_level);
        console.log('Warnings:', result.data.warnings);
    }
};
```

### Python Integration
```python
from utils.nasa_apis import NASAAPIManager

nasa_manager = NASAAPIManager()

# Assess tsunami risk
result = nasa_manager.assess_tsunami_risk(
    impact_lat=21.4,
    impact_lon=-89.5,
    diameter_m=1000,
    search_radius_km=500
)

print(f"Risk Level: {result['risk_level']}")
print(f"Is Water Impact: {result['tsunami_assessment']['is_water_impact']}")
```

## Limitations and Considerations

### Current Limitations
1. **Simplified Physics**: Uses basic wave height estimation formulas
2. **Geographic Resolution**: Limited to Open-Elevation API resolution
3. **Regional Database**: Uses coordinate-based region identification rather than detailed geographic databases
4. **Real-time Data**: Does not account for current ocean conditions

### Future Enhancements
1. **Advanced Physics Models**: Integrate more sophisticated tsunami propagation models
2. **Bathymetry Data**: Include ocean floor topography data
3. **Population Integration**: Add coastal population density analysis
4. **Real-time Ocean Data**: Incorporate current sea conditions
5. **Detailed Coastline Data**: Use high-resolution geographic databases

## Error Handling

The API provides comprehensive error handling:
- Parameter validation (coordinates, diameter ranges)
- API connectivity error handling
- Graceful degradation when external APIs fail
- Detailed error messages for debugging

## Security and Rate Limiting

- Input validation prevents malicious coordinate data
- Reasonable search radius limits (max 5000km)
- Graceful handling of API rate limits
- No sensitive data exposure in error messages

---

*This tsunami risk assessment feature was developed for NASA Space Apps 2024 to provide comprehensive asteroid impact analysis including potential secondary effects like tsunamis.*
# 🎯 Backend Controllers Documentation
## NASA Space Apps 2024 - Asteroid Impact Analysis System

This document provides comprehensive documentation for all controllers in the Flask backend, detailing their purpose, methods, inputs, outputs, and usage examples.

---

## 📋 Table of Contents
1. [Impact Controller](#impact-controller)
2. [Scenario Controller](#scenario-controller) 
3. [Tsunami Controller](#tsunami-controller)
4. [Common Patterns](#common-patterns)
5. [Error Handling](#error-handling)

---

## 🎯 Impact Controller
**File:** `controllers/impact_controller.py`  
**Purpose:** Handles custom asteroid impact analysis, parameter studies, and visualization generation.

### Class: `ImpactController`

#### Constructor
```python
def __init__(self, nasa_api_manager: NASAAPIManager, viz_manager: VisualizationManager)
```
**Purpose:** Initialize controller with API and visualization managers.  
**Parameters:**
- `nasa_api_manager`: Manager for external API integrations
- `viz_manager`: Manager for visualization generation

---

### 🔬 Method: `analyze_impact(request)`
**Endpoint:** `POST /api/impact/analyze`  
**Purpose:** Perform comprehensive analysis of a custom asteroid impact scenario.

#### Input Parameters (JSON)
```json
{
    "diameter_m": 1000.0,           // Required: Asteroid diameter in meters
    "velocity_km_s": 20.0,          // Required: Impact velocity in km/s
    "density_kg_m3": 2600,          // Optional: Asteroid density (default: 2600)
    "angle_degrees": 45,            // Optional: Impact angle (default: 45)
    "impact_lat": 40.7128,          // Required: Impact latitude (-90 to 90)
    "impact_lon": -74.0060,         // Required: Impact longitude (-180 to 180)
    "location_name": "New York"     // Optional: Human-readable location name
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "impact_parameters": {
            "diameter_m": 1000.0,
            "velocity_km_s": 20.0,
            "density_kg_m3": 2600,
            "angle_degrees": 45,
            "kinetic_energy_mt": 1234.5
        },
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "elevation_m": 10.2,
            "location_name": "New York"
        },
        "impact_effects": {
            "crater_diameter_m": 15000,
            "crater_depth_m": 2500,
            "seismic_magnitude": 7.2,
            "seismic_radius_km": 500,
            "air_blast_radius_km": 200,
            "thermal_radius_km": 150
        },
        "casualties": {
            "estimated_deaths": 50000,
            "estimated_injuries": 200000,
            "population_affected": 8000000,
            "confidence_level": "medium"
        },
        "regional_data": {
            "elevation": {...},
            "population": {...},
            "earthquake_comparison": {...}
        }
    },
    "message": "Impact analysis completed successfully"
}
```

#### Error Responses
- **400 Bad Request:** Missing required parameters or invalid coordinates
- **500 Internal Server Error:** Analysis calculation failure

---

### 🛠️ Method: `create_custom_impact(request)`
**Endpoint:** `POST /api/impact/custom`  
**Purpose:** Create and analyze a completely custom impact scenario with additional metadata.

#### Input Parameters (JSON)
```json
{
    "diameter_m": 500.0,
    "velocity_km_s": 25.0,
    "density_kg_m3": 3000,
    "angle_degrees": 60,
    "impact_lat": 35.6762,
    "impact_lon": 139.6503,
    "location_name": "Tokyo",
    "scenario_name": "Tokyo Urban Impact",    // Optional: Custom scenario name
    "description": "Hypothetical impact...",  // Optional: Scenario description
    "save_scenario": true                     // Optional: Save for reuse
}
```

#### Output Response
Similar to `analyze_impact` with additional fields:
```json
{
    "success": true,
    "data": {
        // ... (same as analyze_impact)
        "scenario_info": {
            "scenario_name": "Tokyo Urban Impact",
            "description": "Hypothetical impact scenario",
            "created_timestamp": "2025-10-03T12:00:00Z",
            "saved": true
        }
    }
}
```

---

### 📊 Method: `parameter_study(request)`
**Endpoint:** `POST /api/impact/parameter-study`  
**Purpose:** Analyze how different asteroid parameters affect impact outcomes.

#### Input Parameters (JSON)
```json
{
    "base_impact": {
        "diameter_m": 500,
        "velocity_km_s": 20,
        "density_kg_m3": 2600,
        "angle_degrees": 45,
        "impact_lat": 40.0,
        "impact_lon": -74.0
    },
    "parameter_ranges": {
        "diameter_m": [100, 500, 1000, 2000],     // Test different diameters
        "velocity_km_s": [15, 20, 25, 30]         // Test different velocities
    },
    "metrics": ["crater_diameter_m", "seismic_magnitude", "casualties"]
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "base_scenario": {...},
        "parameter_variations": {
            "diameter_m": [
                {
                    "parameter_value": 100,
                    "results": {
                        "crater_diameter_m": 1500,
                        "seismic_magnitude": 5.2,
                        "estimated_deaths": 1000
                    }
                }
                // ... more variations
            ]
        },
        "sensitivity_analysis": {
            "most_sensitive_parameter": "diameter_m",
            "parameter_correlations": {...}
        }
    }
}
```

---

### 🗺️ Method: `generate_shake_map(request)`
**Endpoint:** `POST /api/visualization/shake-map`  
**Purpose:** Generate interactive shake map data for seismic visualization.

#### Input Parameters (JSON)
```json
{
    "impact_lat": 40.7128,
    "impact_lon": -74.0060,
    "seismic_magnitude": 7.2,
    "max_radius_km": 1000,
    "grid_resolution": 50        // Number of grid points per side
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "shake_map": {
            "center": [40.7128, -74.0060],
            "magnitude": 7.2,
            "max_radius_km": 1000,
            "grid_data": [
                {
                    "lat": 40.5,
                    "lon": -74.2,
                    "intensity": 8.5,
                    "distance_km": 25.3,
                    "color": "#FF0000"
                }
                // ... more grid points
            ]
        },
        "intensity_scale": {
            "scale_type": "Modified Mercalli",
            "levels": {...}
        }
    }
}
```

---

### 📈 Method: `generate_impact_chart(request)`
**Endpoint:** `POST /api/visualization/impact-chart`  
**Purpose:** Generate chart data for impact analysis visualization.

#### Input Parameters (JSON)
```json
{
    "chart_type": "energy_distribution",    // Options: energy, crater, casualties, seismic
    "impact_data": {
        "diameter_m": 1000,
        "velocity_km_s": 20,
        "kinetic_energy_mt": 1234.5,
        "crater_diameter_m": 15000
    },
    "comparison_data": [...]               // Optional: For comparison charts
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "chart_config": {
            "type": "energy_distribution",
            "title": "Energy Distribution Analysis",
            "data": [
                {"label": "Kinetic Energy", "value": 1234.5, "unit": "MT"},
                {"label": "Crater Formation", "value": 800.2, "unit": "MT"},
                {"label": "Seismic Energy", "value": 234.1, "unit": "MT"}
            ]
        },
        "visualization_options": {...}
    }
}
```

---

## 🎬 Scenario Controller
**File:** `controllers/scenario_controller.py`  
**Purpose:** Manages pre-defined impact scenarios, comparisons, and scenario searches.

### Class: `ScenarioController`

---

### 📚 Method: `get_scenarios()`
**Endpoint:** `GET /api/scenarios`  
**Purpose:** Retrieve all available pre-defined impact scenarios.

#### Input Parameters
None (GET request)

#### Output Response
```json
{
    "success": true,
    "data": {
        "scenarios": [
            {
                "id": "chicxulub",
                "name": "Chicxulub Impact",
                "description": "K-Pg extinction event impact",
                "category": "extinction",
                "historical": true,
                "location": {
                    "latitude": 21.4,
                    "longitude": -89.5,
                    "name": "Yucatan Peninsula"
                },
                "parameters": {
                    "diameter_m": 10000,
                    "velocity_km_s": 20,
                    "density_kg_m3": 2600,
                    "angle_degrees": 45
                }
            }
            // ... more scenarios
        ],
        "categories": {
            "extinction": ["chicxulub", "permian_triassic"],
            "historical": ["tunguska", "chelyabinsk"],
            "hypothetical": ["manhattan", "london"]
        },
        "total_scenarios": 15,
        "historical_count": 8,
        "category_counts": {
            "extinction": 2,
            "historical": 8,
            "hypothetical": 5
        }
    }
}
```

---

### 🔍 Method: `get_scenario_details(scenario_name)`
**Endpoint:** `GET /api/scenarios/<scenario_name>`  
**Purpose:** Get detailed information about a specific scenario.

#### Input Parameters
- **URL Parameter:** `scenario_name` (string) - ID of the scenario

#### Output Response
```json
{
    "success": true,
    "data": {
        "scenario": {
            "id": "chicxulub",
            "name": "Chicxulub Impact",
            "description": "The impact that caused the K-Pg extinction event...",
            "category": "extinction",
            "historical": true,
            "scientific_basis": "Geological and fossil evidence...",
            "estimated_date": "66 million years ago",
            "location": {
                "latitude": 21.4,
                "longitude": -89.5,
                "name": "Yucatan Peninsula",
                "country": "Mexico"
            },
            "parameters": {
                "diameter_m": 10000,
                "velocity_km_s": 20,
                "density_kg_m3": 2600,
                "angle_degrees": 45
            },
            "expected_effects": {
                "crater_diameter_km": 150,
                "global_effects": true,
                "extinction_level": "mass_extinction"
            }
        },
        "references": [
            "Alvarez et al. (1980)",
            "Schulte et al. (2010)"
        ]
    }
}
```

---

### ▶️ Method: `run_scenario(scenario_name, request)`
**Endpoint:** `POST /api/scenarios/<scenario_name>/run`  
**Purpose:** Execute analysis for a pre-defined scenario with optional parameter modifications.

#### Input Parameters (JSON - Optional)
```json
{
    "parameter_overrides": {
        "velocity_km_s": 25.0,          // Override default velocity
        "angle_degrees": 60             // Override default angle
    },
    "custom_location": {
        "latitude": 40.0,               // Override default location
        "longitude": -74.0
    },
    "analysis_options": {
        "include_casualties": true,
        "include_regional_data": true,
        "comparison_mode": false
    }
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "scenario_info": {
            "id": "chicxulub",
            "name": "Chicxulub Impact",
            "parameters_used": {
                "diameter_m": 10000,
                "velocity_km_s": 25.0,     // Modified from default
                "density_kg_m3": 2600,
                "angle_degrees": 60        // Modified from default
            }
        },
        "impact_analysis": {
            // ... (same structure as analyze_impact)
        },
        "scenario_comparison": {
            "original_vs_modified": {...}  // If parameters were overridden
        }
    }
}
```

---

### ⚖️ Method: `compare_scenarios(request)`
**Endpoint:** `POST /api/scenarios/compare`  
**Purpose:** Compare multiple scenarios or parameter variations side by side.

#### Input Parameters (JSON)
```json
{
    "scenarios": ["chicxulub", "tunguska", "chelyabinsk"],
    "comparison_metrics": [
        "crater_diameter_m",
        "seismic_magnitude", 
        "kinetic_energy_mt",
        "estimated_deaths"
    ],
    "normalization": "logarithmic"     // Options: linear, logarithmic, none
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "comparison_results": {
            "scenarios": [
                {
                    "id": "chicxulub",
                    "name": "Chicxulub Impact",
                    "metrics": {
                        "crater_diameter_m": 150000,
                        "seismic_magnitude": 10.5,
                        "kinetic_energy_mt": 100000000,
                        "estimated_deaths": 0
                    }
                }
                // ... more scenarios
            ],
            "relative_comparison": {
                "largest_crater": "chicxulub",
                "highest_casualties": "manhattan",
                "most_energetic": "chicxulub"
            },
            "normalized_data": [...]      // For charting
        },
        "visualization_config": {
            "chart_type": "radar",
            "normalization_applied": "logarithmic"
        }
    }
}
```

---

### 🔎 Method: `search_scenarios(request)`
**Endpoint:** `POST /api/scenarios/search`  
**Purpose:** Search scenarios based on criteria like size, location, or effects.

#### Input Parameters (JSON)
```json
{
    "filters": {
        "diameter_range": [100, 5000],          // Min and max diameter
        "category": ["historical", "extinction"],
        "location_region": ["North America", "Europe"],  
        "minimum_magnitude": 6.0
    },
    "sort_by": "diameter_m",                    // Sort field
    "sort_order": "desc",                       // asc or desc
    "limit": 10                                 // Max results
}
```

#### Output Response
```json
{
    "success": true,
    "data": {
        "search_results": [
            {
                "id": "chicxulub",
                "name": "Chicxulub Impact",
                "relevance_score": 0.95,
                "match_reasons": [
                    "Matches diameter range",
                    "Historical category match"
                ],
                "summary": {...}
            }
            // ... more results
        ],
        "search_metadata": {
            "total_matches": 5,
            "filters_applied": {...},
            "search_time_ms": 23
        }
    }
}
```

---

## 🌊 Tsunami Controller
**File:** `controllers/tsunami_controller.py`  
**Purpose:** Assesses tsunami risk from asteroid impacts using elevation data and coastal analysis.

### Blueprint: `tsunami_bp` (prefix: `/api/tsunami`)

---

### 🌊 Endpoint: `assess_tsunami_risk()`
**Route:** `POST /api/tsunami/assess`  
**Purpose:** Comprehensive tsunami risk assessment for asteroid impact scenarios.

#### Input Parameters (JSON)
```json
{
    "latitude": 21.4,               // Required: Impact latitude
    "longitude": -89.5,             // Required: Impact longitude  
    "diameter_m": 1000.0,           // Required: Asteroid diameter in meters
    "search_radius_km": 1000        // Optional: Analysis radius (default: 1000km)
}
```

#### Output Response
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
            "diameter_m": 1000,
            "search_radius_km": 1000
        },
        "tsunami_assessment": {
            "size_factor": {
                "category": "major",
                "description": "Can generate large regional tsunamis"
            },
            "is_water_impact": true,
            "distance_to_water_km": 0
        },
        "coastal_analysis": {
            "total_sample_points": 16,
            "water_points": 14,
            "land_points": 2,
            "water_to_land_ratio": 0.875,
            "max_wave_height_estimate_m": 25.4,
            "affected_regions": [
                "North American Coast",
                "European Coast",
                "Caribbean Islands"
            ],
            "search_radius_km": 1000
        },
        "risk_level": "high",
        "warnings": [
            "⚠️ HIGH TSUNAMI RISK: Coastal areas should prepare for evacuation",
            "🌊 Estimated wave heights up to 25.4m",
            "📍 Evacuate low-lying coastal areas to higher ground",
            "🗺️ Potentially affected regions: North American Coast, European Coast, Caribbean Islands"
        ]
    },
    "message": "Tsunami risk assessment completed for 1000m asteroid impact"
}
```

#### Risk Levels
- **minimal**: Very low tsunami risk
- **low**: Limited wave generation potential  
- **moderate**: Regional tsunami possible
- **high**: Large regional tsunami likely
- **extreme**: Ocean-wide mega-tsunami possible

---

### ⚡ Endpoint: `quick_tsunami_check()`
**Route:** `GET /api/tsunami/quick-check`  
**Purpose:** Fast tsunami risk evaluation based on basic parameters.

#### Input Parameters (Query String)
```
GET /api/tsunami/quick-check?lat=21.4&lon=-89.5&diameter=500
```

#### Output Response
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

---

### 📊 Endpoint: `get_risk_levels()`
**Route:** `GET /api/tsunami/risk-levels`  
**Purpose:** Get information about tsunami risk levels and assessment criteria.

#### Input Parameters
None (GET request)

#### Output Response
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
            // ... other levels
        },
        "size_categories": {
            "negligible": "Diameter < 50m - Too small for significant tsunamis",
            "catastrophic": "Diameter > 1000m - Ocean-wide mega-tsunamis possible"
            // ... other categories
        },
        "assessment_factors": [
            "Asteroid diameter and impact energy",
            "Impact location (ocean depth, coastal proximity)",
            "Local topography and bathymetry",
            "Distance to populated coastal areas",
            "Regional geographic features",
            "Wave propagation patterns"
        ]
    },
    "message": "Tsunami risk level information retrieved successfully"
}
```

---

## 🔄 Common Patterns

### Request Validation
All controllers follow consistent validation patterns:
```python
# JSON validation
if not request.is_json:
    return jsonify({'success': False, 'error': 'Request must be JSON'}), 400

# Parameter validation  
required_params = ['param1', 'param2']
missing_params = [p for p in required_params if p not in data]
if missing_params:
    return jsonify({
        'success': False, 
        'error': f'Missing parameters: {", ".join(missing_params)}'
    }), 400

# Coordinate validation
if not (-90 <= latitude <= 90):
    return jsonify({'success': False, 'error': 'Invalid latitude'}), 400
```

### Response Structure
All successful responses follow this structure:
```json
{
    "success": true,
    "data": {
        // Response data here
    },
    "message": "Operation completed successfully"
}
```

### Error Responses
All error responses follow this structure:
```json
{
    "success": false,
    "error": "Error category/type",
    "message": "Human-readable error description",
    "details": "Additional technical details (optional)"
}
```

---

## ⚠️ Error Handling

### HTTP Status Codes
- **200 OK**: Successful operation
- **400 Bad Request**: Invalid input parameters or malformed request
- **404 Not Found**: Requested resource/scenario not found
- **500 Internal Server Error**: Server-side processing error

### Common Error Types

#### Validation Errors (400)
```json
{
    "success": false,
    "error": "Validation Error",
    "message": "Missing required parameters: diameter_m, velocity_km_s",
    "details": {
        "required": ["diameter_m", "velocity_km_s"],
        "provided": ["impact_lat", "impact_lon"]
    }
}
```

#### Coordinate Errors (400)
```json
{
    "success": false,
    "error": "Invalid Coordinates",
    "message": "Latitude must be between -90 and 90 degrees",
    "details": {
        "provided_latitude": 95.0,
        "valid_range": [-90, 90]
    }
}
```

#### API Integration Errors (500)
```json
{
    "success": false,
    "error": "External API Error",
    "message": "Failed to retrieve elevation data",
    "details": {
        "api": "Open-Elevation",
        "status": "timeout",
        "fallback_used": true
    }
}
```

#### Scenario Not Found (404)
```json
{
    "success": false,
    "error": "Scenario Not Found",
    "message": "Scenario 'invalid_scenario' does not exist",
    "details": {
        "requested": "invalid_scenario",
        "available": ["chicxulub", "tunguska", "chelyabinsk"]
    }
}
```

---

## 🚀 Usage Examples

### Frontend Integration
```javascript
// Analyze custom impact
const analyzeImpact = async (impactData) => {
    const response = await fetch('/api/impact/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(impactData)
    });
    
    const result = await response.json();
    if (result.success) {
        console.log('Impact Analysis:', result.data);
    } else {
        console.error('Error:', result.error);
    }
};

// Run pre-defined scenario
const runScenario = async (scenarioId) => {
    const response = await fetch(`/api/scenarios/${scenarioId}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            analysis_options: {
                include_casualties: true,
                include_regional_data: true
            }
        })
    });
    
    return await response.json();
};

// Quick tsunami check
const checkTsunami = async (lat, lon, diameter) => {
    const response = await fetch(
        `/api/tsunami/quick-check?lat=${lat}&lon=${lon}&diameter=${diameter}`
    );
    return await response.json();
};
```

### Python Integration
```python
import requests

# Analyze impact using Python
def analyze_impact(impact_params):
    response = requests.post(
        'http://localhost:5000/api/impact/analyze',
        json=impact_params
    )
    return response.json()

# Compare scenarios  
def compare_scenarios(scenario_list):
    response = requests.post(
        'http://localhost:5000/api/scenarios/compare',
        json={'scenarios': scenario_list}
    )
    return response.json()
```

---

*This documentation was generated for NASA Space Apps 2024 - Asteroid Impact Analysis System. For additional technical details, refer to the individual controller source files.*
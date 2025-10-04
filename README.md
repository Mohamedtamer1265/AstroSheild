# 🌍☄️ Asteroid Impact Modeling API
# NASA Space Apps 2024

![NASA Space Apps](https://img.shields.io/badge/NASA-Space%20Apps%202024-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3+-red)

Flask backend API for asteroid impact modeling and analysis. Provides comprehensive physics-based calculations, visualization data, and scenario management for React frontend integration.

## 🚀 Quick Start

### Installation

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the Server**
```bash
python run.py
```

3. **Test the API**
```bash
curl http://localhost:5000/api/health
```

## 📡 API Endpoints

### Core Information
- `GET /api/health` - Health check
- `GET /api/info` - API documentation and capabilities

### Impact Analysis
- `POST /api/impact/analyze` - Comprehensive impact analysis
- `POST /api/impact/custom` - Create custom impact scenario
- `POST /api/impact/parameter-study` - Parameter sensitivity analysis

### Scenario Management
- `GET /api/scenarios` - List all available scenarios
- `GET /api/scenarios/<name>` - Get scenario details
- `POST /api/scenarios/<name>/run` - Run scenario analysis
- `POST /api/scenarios/compare` - Compare multiple scenarios

### Visualizations
- `POST /api/visualization/shake-map` - Generate shake map data
- `POST /api/visualization/impact-chart` - Generate chart data

## 📊 API Usage Examples

### Analyze Custom Impact
```json
POST /api/impact/analyze
{
    "diameter_m": 200,
    "velocity_km_s": 20,
    "impact_lat": 40.7128,
    "impact_lon": -74.0060,
    "location_name": "New York City"
}
```

### Run Pre-defined Scenario
```json
POST /api/scenarios/chelyabinsk_2013/run
{
    "custom_location": {
        "lat": 51.5074,
        "lon": -0.1278,
        "name": "London"
    }
}
```

### Compare Scenarios
```json
POST /api/scenarios/compare
{
    "scenario_names": ["chelyabinsk_2013", "city_killer", "regional_disaster"]
}
```

### Parameter Study
```json
POST /api/impact/parameter-study
{
    "base_diameter_m": 100,
    "impact_lat": 30.0444,
    "impact_lon": 31.2357,
    "parameter": "diameter",
    "values": [50, 100, 200, 500, 1000]
}
```

## 🔬 Physics Models

### Implemented Features
- **Energy Calculations**: Kinetic energy and TNT equivalents
- **Crater Formation**: Schmidt-Housen scaling laws
- **Seismic Analysis**: Kanamori energy-magnitude relationships with live USGS earthquake data
- **Air Blast Effects**: Overpressure zones and thermal radiation
- **Casualty Estimation**: Population impact assessment
- **Visualization Data**: Interactive maps and charts
- **Live API Integration**: USGS earthquake data, Open-Elevation API

### Available Scenarios
- `chelyabinsk_2013` - 2013 Chelyabinsk Event (Historical)
- `tunguska_1908` - 1908 Tunguska Event (Historical)
- `apophis_potential` - Apophis 2029 potential impact
- `city_killer` - NASA city-killer threshold
- `regional_disaster` - Regional-scale impact
- `chicxulub_scale` - Extinction-level event

## 🌐 React Frontend Integration

### CORS Configuration
- Enabled for `http://localhost:3000` (Create React App)
- Enabled for `http://localhost:5173` (Vite)
- JSON responses with proper error handling

### Response Format
```json
{
    "success": true,
    "data": {
        "analysis": { ... },
        "visualizations": { ... },
        "summary": { ... }
    }
}
```

### Error Responses
```json
{
    "success": false,
    "error": "Error type",
    "message": "Detailed error message",
    "details": "Additional information"
}
```

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── run.py                 # Development server runner
├── requirements.txt       # Python dependencies
├── models/
│   ├── asteroid_impact.py # Physics calculations
│   └── scenarios.py       # Pre-defined scenarios
├── controllers/
│   ├── impact_controller.py    # Impact analysis endpoints
│   └── scenario_controller.py  # Scenario management endpoints
└── utils/
    ├── visualization.py   # Chart and map data generation
    └── nasa_apis.py      # External API integrations
```

## 🛠️ Development

### Adding New Scenarios
1. Edit `models/scenarios.py`
2. Add scenario to `get_scenarios()` method
3. Include all required parameters

### Extending Physics Models
1. Modify `models/asteroid_impact.py`
2. Add new calculation methods
3. Update `get_comprehensive_analysis()`

### API Extensions
1. Add new endpoints to controllers
2. Register routes in `app.py`
3. Update API documentation

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY` - Flask secret key (default: auto-generated)
- `FLASK_ENV` - Environment mode (development/production)
- `PORT` - Server port (default: 5000)

### API Limits
- Max request size: 16MB
- Request timeout: 30 seconds
- CORS origins configurable in `app.py`

## 📚 Scientific References & Data Sources

- Schmidt & Housen crater scaling laws
- Kanamori seismic energy-magnitude relations
- Nuclear weapons effects for air blast modeling
- NASA planetary defense guidelines
- **USGS Earthquake API**: Live earthquake data for seismic comparisons
- **Open-Elevation API**: Terrain elevation data for impact locations

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 🔍 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Get scenarios
curl http://localhost:5000/api/scenarios

# Test impact analysis
curl -X POST http://localhost:5000/api/impact/analyze \
  -H "Content-Type: application/json" \
  -d '{"diameter_m":100,"velocity_km_s":20,"impact_lat":40.7,"impact_lon":-74.0}'
```

## 📞 Support

For issues and questions:
1. Check API documentation: `/api/info`
2. Review error responses for details
3. Ensure all required parameters are provided
4. Validate coordinate ranges (-90 to 90 lat, -180 to 180 lon)

---

**🌍☄️ Protecting Earth through science and technology - NASA Space Apps 2024**
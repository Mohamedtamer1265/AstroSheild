server/CONTROLLERS_DOCUMENTATION.md# 🌍☄️ Asteroid API Documentation
## NASA Space Apps 2024 - AstroShield Backend APIs

### 📡 Overview
Complete REST API system for asteroid data fetching and impact prediction. Integrates with NASA JPL Small-Body Database and NASA NeoWs for comprehensive asteroid analysis.

---

## 🚀 Base URL
```
http://localhost:5000/api
```

---

## 📋 API Endpoints

### 1. 🔍 Get Single Asteroid Details
Fetch comprehensive data for a specific asteroid from NASA JPL database.

**Endpoint:** `GET /asteroid/{asteroid_id}`

**Parameters:**
- `asteroid_id` (string, required) - Asteroid identifier (e.g., "433", "99942", "Apophis")

**Example Request:**
```http
GET /api/asteroid/433
```

**Example Response:**
```json
{
  "success": true,
  "asteroid_id": "433",
  "data": {
    "success": true,
    "id": "433",
    "name": "433 Eros (A898 PA)",
    "neo": true,
    "pha": false,
    "orbital_elements": {
      "semi_major_axis": 1.458,
      "eccentricity": 0.223,
      "inclination": 10.83,
      "ascending_node": 304.3,
      "argument_perihelion": 178.8,
      "mean_anomaly": 320.1,
      "epoch": 2460000.5,
      "mean_motion_deg_day": 0.5598
    },
    "physical_properties": {
      "diameter_km": 16.84,
      "absolute_magnitude": 11.16,
      "albedo": 0.25
    },
    "source": "JPL Small-Body Database"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Asteroid not found or JPL API error",
  "asteroid_id": "invalid_id",
  "details": "Asteroid not found"
}
```

---

### 2. 📊 Get All Asteroids (NASA NeoWs)
Retrieve multiple asteroids from NASA Near Earth Object Web Service.

**Endpoint:** `GET /asteroids/all`

**Query Parameters:**
- `start_date` (string, optional) - Start date in YYYY-MM-DD format (default: today)
- `end_date` (string, optional) - End date in YYYY-MM-DD format (default: today + 7 days)

**Example Requests:**
```http
GET /api/asteroids/all
GET /api/asteroids/all?start_date=2024-10-01&end_date=2024-10-07
```

**Example Response:**
```json
{
  "success": true,
  "total_count": 15,
  "asteroids": [
    {
      "id": "2154347",
      "name": "(2004 BL86)",
      "neo_reference_id": "2154347",
      "nasa_jpl_url": "http://ssd.jpl.nasa.gov/sbdb.cgi?sstr=2154347",
      "absolute_magnitude_h": 19.3,
      "estimated_diameter_km_min": 0.4248,
      "estimated_diameter_km_max": 0.9501,
      "is_potentially_hazardous": false,
      "close_approach_date": "2024-10-15",
      "miss_distance_km": "7162420.123456789"
    }
  ],
  "data_source": "NASA NeoWs API"
}
```

---

### 3. 🎯 Predict Asteroid Impact
Generate impact prediction with coordinates, velocity, and direction for a specific asteroid.

**Endpoint:** `POST /predict/impact`

**Request Body:**
```json
{
  "asteroid_id": "433"
}
```

**Example Request:**
```http
POST /api/predict/impact
Content-Type: application/json

{
  "asteroid_id": "433"
}
```

**Example Response:**
```json
{
  "success": true,
  "asteroid_info": {
    "id": "433",
    "name": "433 Eros (A898 PA)",
    "diameter_km": 16.84,
    "neo": true,
    "pha": false
  },
  "impact_prediction": {
    "success": true,
    "impact_coordinates": {
      "latitude": 25.374916,
      "longitude": -157.729843
    },
    "impact_velocity": {
      "velocity_km_s": 18.45,
      "direction": "Northeast",
      "bearing_degrees": 67.3
    },
    "impact_details": {
      "estimated_impact_date": "2025-08-12T15:30:45.123456",
      "energy_megatons": 1250.456,
      "asteroid_diameter_km": 16.84,
      "estimated_mass_kg": 6700000000000000
    },
    "note": "Simulated impact prediction for testing purposes"
  },
  "prediction_method": "Simulated impact scenario for testing"
}
```

---

### 4. ❤️ Health Check
Check API status and available endpoints.

**Endpoint:** `GET /health`

**Example Request:**
```http
GET /api/asteroid/health
```

**Example Response:**
```json
{
  "success": true,
  "message": "Asteroid API is running",
  "endpoints": [
    "GET /asteroid/<id> - Get asteroid details by ID",
    "GET /asteroids/all - Get all asteroids from NASA NeoWs",
    "POST /predict/impact - Predict impact coordinates and velocity"
  ]
}
```

---

## 💻 Code Examples

### JavaScript (Frontend Integration)

#### 1. Fetch Single Asteroid
```javascript
async function getAsteroidData(asteroidId) {
  try {
    const response = await fetch(`/api/asteroid/${asteroidId}`);
    const data = await response.json();
    
    if (data.success) {
      console.log('Asteroid:', data.data.name);
      console.log('Diameter:', data.data.physical_properties.diameter_km, 'km');
      return data.data;
    } else {
      throw new Error(data.error);
    }
  } catch (error) {
    console.error('Error fetching asteroid:', error);
    return null;
  }
}

// Usage
getAsteroidData('433').then(asteroid => {
  if (asteroid) {
    console.log('Successfully fetched:', asteroid.name);
  }
});
```

#### 2. Fetch All Asteroids
```javascript
async function getAllAsteroids(startDate = null, endDate = null) {
  try {
    let url = '/api/asteroids/all';
    const params = new URLSearchParams();
    
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    if (params.toString()) {
      url += '?' + params.toString();
    }
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.success) {
      console.log(`Found ${data.total_count} asteroids`);
      return data.asteroids;
    } else {
      throw new Error(data.error);
    }
  } catch (error) {
    console.error('Error fetching asteroids:', error);
    return [];
  }
}

// Usage
getAllAsteroids('2024-10-01', '2024-10-07').then(asteroids => {
  asteroids.forEach(asteroid => {
    console.log(`${asteroid.name} - ${asteroid.estimated_diameter_km_min}km`);
  });
});
```

#### 3. Predict Impact
```javascript
async function predictImpact(asteroidId) {
  try {
    const response = await fetch('/api/predict/impact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        asteroid_id: asteroidId
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      const prediction = data.impact_prediction;
      console.log('Impact Prediction:');
      console.log(`Location: ${prediction.impact_coordinates.latitude}, ${prediction.impact_coordinates.longitude}`);
      console.log(`Velocity: ${prediction.impact_velocity.velocity_km_s} km/s`);
      console.log(`Direction: ${prediction.impact_velocity.direction}`);
      console.log(`Energy: ${prediction.impact_details.energy_megatons} megatons`);
      return prediction;
    } else {
      throw new Error(data.error);
    }
  } catch (error) {
    console.error('Error predicting impact:', error);
    return null;
  }
}

// Usage
predictImpact('433').then(prediction => {
  if (prediction) {
    // Use prediction data for visualization
    const lat = prediction.impact_coordinates.latitude;
    const lng = prediction.impact_coordinates.longitude;
    // Add marker to map, etc.
  }
});
```

### Python Examples

#### 1. Fetch Single Asteroid
```python
import requests

def get_asteroid_data(asteroid_id):
    """Fetch single asteroid data"""
    try:
        response = requests.get(f'http://localhost:5000/api/asteroid/{asteroid_id}')
        response.raise_for_status()
        data = response.json()
        
        if data['success']:
            asteroid = data['data']
            print(f"Asteroid: {asteroid['name']}")
            print(f"Diameter: {asteroid['physical_properties']['diameter_km']} km")
            return asteroid
        else:
            print(f"Error: {data['error']}")
            return None
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Usage
asteroid = get_asteroid_data('433')
```

#### 2. Fetch All Asteroids
```python
def get_all_asteroids(start_date=None, end_date=None):
    """Fetch all asteroids from NASA NeoWs"""
    try:
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        response = requests.get(
            'http://localhost:5000/api/asteroids/all',
            params=params
        )
        response.raise_for_status()
        data = response.json()
        
        if data['success']:
            print(f"Found {data['total_count']} asteroids")
            return data['asteroids']
        else:
            print(f"Error: {data['error']}")
            return []
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

# Usage
asteroids = get_all_asteroids('2024-10-01', '2024-10-07')
for asteroid in asteroids:
    print(f"{asteroid['name']} - {asteroid['estimated_diameter_km_min']} km")
```

#### 3. Predict Impact
```python
def predict_impact(asteroid_id):
    """Predict asteroid impact"""
    try:
        data = {"asteroid_id": asteroid_id}
        response = requests.post(
            'http://localhost:5000/api/predict/impact',
            json=data
        )
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            prediction = result['impact_prediction']
            coords = prediction['impact_coordinates']
            velocity = prediction['impact_velocity']
            details = prediction['impact_details']
            
            print("Impact Prediction:")
            print(f"Location: {coords['latitude']}, {coords['longitude']}")
            print(f"Velocity: {velocity['velocity_km_s']} km/s")
            print(f"Direction: {velocity['direction']}")
            print(f"Energy: {details['energy_megatons']} megatons")
            
            return prediction
        else:
            print(f"Error: {result['error']}")
            return None
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Usage
prediction = predict_impact('433')
```

---

## 🧪 Testing the APIs

### Using Browser (GET requests only)
- Single asteroid: `http://localhost:5000/api/asteroid/433`
- All asteroids: `http://localhost:5000/api/asteroids/all`
- Health check: `http://localhost:5000/api/asteroid/health`

### Using curl
```bash
# Single asteroid
curl http://localhost:5000/api/asteroid/433

# All asteroids with date range
curl "http://localhost:5000/api/asteroids/all?start_date=2024-10-01&end_date=2024-10-07"

# Impact prediction
curl -X POST http://localhost:5000/api/predict/impact \
  -H "Content-Type: application/json" \
  -d '{"asteroid_id": "433"}'
```

### Popular Test Asteroid IDs
- `433` - Eros (famous near-Earth asteroid)
- `99942` - Apophis (potentially hazardous)
- `1` - Ceres (largest asteroid/dwarf planet)
- `2000 SG344` - Small near-Earth asteroid
- `Bennu` - OSIRIS-REx target asteroid

---

## 🔧 Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (missing parameters)
- `404` - Not Found (asteroid not found)
- `500` - Internal Server Error

### Error Response Format
```json
{
  "success": false,
  "error": "Error description",
  "details": "Additional error details"
}
```

---

## 📝 Notes

1. **Data Sources:**
   - Single asteroid data: NASA JPL Small-Body Database
   - Multiple asteroids: NASA NeoWs API
   - Impact predictions: Simulated for testing purposes

2. **Rate Limits:**
   - NASA APIs have rate limits
   - Use DEMO_KEY for testing (get free API key for production)

3. **Data Accuracy:**
   - Orbital elements and physical properties are real
   - Impact predictions are simulated for demonstration

4. **CORS:**
   - APIs support CORS for frontend integration
   - Configured for localhost:3000 and localhost:5173

---

## 🚀 Getting Started

1. **Start the server:**
   ```bash
   cd server
   python app.py
   ```

2. **Test the health endpoint:**
   ```bash
   curl http://localhost:5000/api/asteroid/health
   ```

3. **Try fetching an asteroid:**
   ```bash
   curl http://localhost:5000/api/asteroid/433
   ```

Your asteroid API system is ready for integration! 🌟
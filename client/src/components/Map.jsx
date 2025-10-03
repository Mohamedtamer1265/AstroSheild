import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMapEvents, Marker, Popup, Circle, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Custom marker icons for different impact effects
const impactIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Component to handle map clicks and asteroid impact simulation
const MapClickHandler = ({ onLocationSelect, impactData, setImpactData }) => {
  const map = useMap();

  useMapEvents({
    click: async (e) => {
      const { lat, lng } = e.latlng;
      console.log(`Clicked at: ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
      
      if (onLocationSelect) {
        onLocationSelect(lat, lng);
      }

      // Simulate asteroid impact at clicked location
      await simulateAsteroidImpact(lat, lng, setImpactData);
    },
  });

  // Add impact circles when impact data is available
  useEffect(() => {
    if (impactData && impactData.impact_effects) {
      // Zoom to impact location
      map.setView([impactData.location.latitude, impactData.location.longitude], 8);
    }
  }, [impactData, map]);

  return null;
};

// Simulate asteroid impact using the documented API
const simulateAsteroidImpact = async (lat, lng, setImpactData) => {
  try {
    setImpactData(null); // Clear previous data
    
    // Default asteroid parameters - can be customized
    const impactParams = {
      diameter_m: 1000.0,           // 1km asteroid
      velocity_km_s: 20.0,          // 20 km/s impact velocity
      density_kg_m3: 2600,          // Stone asteroid
      angle_degrees: 45,            // 45-degree impact angle
      impact_lat: lat,
      impact_lon: lng,
      location_name: `Impact Site (${lat.toFixed(2)}, ${lng.toFixed(2)})`
    };

    console.log('Simulating asteroid impact with params:', impactParams);

    // Call the Impact Controller API
    const response = await fetch('/api/impact/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(impactParams)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    
    if (result.success) {
      console.log('Impact analysis result:', result.data);
      setImpactData(result.data);
    } else {
      console.error('Impact analysis failed:', result.error);
      // Fallback with mock data for demonstration
      setImpactData(createMockImpactData(lat, lng, impactParams));
    }
  } catch (error) {
    console.error('Error simulating asteroid impact:', error);
    // Fallback with mock data for demonstration
    setImpactData(createMockImpactData(lat, lng, {
      diameter_m: 1000.0,
      velocity_km_s: 20.0,
      density_kg_m3: 2600,
      angle_degrees: 45,
      impact_lat: lat,
      impact_lon: lng
    }));
  }
};

// Create mock impact data for fallback/demo purposes
const createMockImpactData = (lat, lng, params) => {
  return {
    impact_parameters: params,
    location: {
      latitude: lat,
      longitude: lng,
      elevation_m: 0,
      location_name: `Impact Site (${lat.toFixed(2)}, ${lng.toFixed(2)})`
    },
    impact_effects: {
      crater_diameter_m: 15000,      // 15km crater
      crater_depth_m: 2500,          // 2.5km deep
      seismic_magnitude: 7.2,        // Magnitude 7.2 earthquake
      seismic_radius_km: 500,        // 500km seismic effects
      air_blast_radius_km: 200,      // 200km air blast
      thermal_radius_km: 150         // 150km thermal effects
    },
    casualties: {
      estimated_deaths: 50000,
      estimated_injuries: 200000,
      population_affected: 8000000,
      confidence_level: "medium"
    }
  };
};

// Main Map component
const Map = () => {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [impactData, setImpactData] = useState(null);
  const [asteroidParams, setAsteroidParams] = useState({
    diameter_m: 1000,
    velocity_km_s: 20,
    density_kg_m3: 2600,
    angle_degrees: 45
  });

  const handleLocationSelect = (lat, lng) => {
    setSelectedLocation({ lat, lng });
  };

  // Convert meters to approximate map radius (very rough approximation)
  const metersToMapRadius = (meters) => {
    return meters / 1000; // Convert to km for map display
  };

  return (
    <div className="w-full h-full relative overflow-hidden p-4" style={{
      background: 'url(../assets/img/introgame.jpg) no-repeat center center fixed',
//backgroundSize: '400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 100% 100%'
    }}>
      <div className="bg-white/5 backdrop-blur-sm text-white p-6 rounded-xl mb-6 border border-white/20 shadow-xl">
        <h2 className="text-3xl font-light mb-2 text-center tracking-wide">🌍 Asteroid Impact Simulator</h2>
        <p className="mb-2 text-center text-white/80 font-light">
          Click anywhere on the map to simulate an asteroid impact at that location.
        </p>
      </div>
      <div className="flex gap-4">
        {/* Map Container - Made smaller */}
        <div className="relative w-2/3" style={{ height: "400px" }}>
          <MapContainer
            center={[20, 0]} // Center on equator
            zoom={2}
            className="w-full h-full rounded-2xl border border-white/20 shadow-2xl overflow-hidden"
            style={{ height: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            
            <MapClickHandler 
              onLocationSelect={handleLocationSelect}
              impactData={impactData}
              setImpactData={setImpactData}
            />

            {/* Display impact marker and effects */}
            {impactData && (
              <>
                {/* Impact point marker */}
                <Marker 
                  position={[impactData.location.latitude, impactData.location.longitude]}
                  icon={impactIcon}
                >
                  <Popup>
                    <div className="p-2">
                      <h3 className="font-bold text-lg mb-2">🌠 Asteroid Impact</h3>
                      <p><strong>Location:</strong> {impactData.location.location_name}</p>
                      <p><strong>Coordinates:</strong> {impactData.location.latitude.toFixed(4)}°, {impactData.location.longitude.toFixed(4)}°</p>
                      <p><strong>Crater Diameter:</strong> {(impactData.impact_effects.crater_diameter_m / 1000).toFixed(1)} km</p>
                      <p><strong>Seismic Magnitude:</strong> {impactData.impact_effects.seismic_magnitude}</p>
                      <p><strong>Estimated Deaths:</strong> {impactData.casualties.estimated_deaths.toLocaleString()}</p>
                      <p><strong>Estimated Injuries:</strong> {impactData.casualties.estimated_injuries.toLocaleString()}</p>
                    </div>
                  </Popup>
                </Marker>

                {/* Crater circle */}
                <Circle
                  center={[impactData.location.latitude, impactData.location.longitude]}
                  radius={impactData.impact_effects.crater_diameter_m / 2}
                  pathOptions={{
                    color: 'red',
                    weight: 3,
                    opacity: 0.8,
                    fillColor: 'darkred',
                    fillOpacity: 0.3
                  }}
                />

                {/* Thermal effects circle */}
                <Circle
                  center={[impactData.location.latitude, impactData.location.longitude]}
                  radius={impactData.impact_effects.thermal_radius_km * 1000}
                  pathOptions={{
                    color: 'orange',
                    weight: 2,
                    opacity: 0.6,
                    fillColor: 'orange',
                    fillOpacity: 0.1
                  }}
                />

                {/* Air blast circle */}
                <Circle
                  center={[impactData.location.latitude, impactData.location.longitude]}
                  radius={impactData.impact_effects.air_blast_radius_km * 1000}
                  pathOptions={{
                    color: 'yellow',
                    weight: 2,
                    opacity: 0.5,
                    fillColor: 'yellow',
                    fillOpacity: 0.05
                  }}
                />

                {/* Seismic effects circle */}
                <Circle
                  center={[impactData.location.latitude, impactData.location.longitude]}
                  radius={impactData.impact_effects.seismic_radius_km * 1000}
                  pathOptions={{
                    color: 'purple',
                    weight: 1,
                    opacity: 0.4,
                    fillColor: 'purple',
                    fillOpacity: 0.02
                  }}
                />
              </>
            )}
          </MapContainer>
        </div>

        {/* Modern Legend Panel */}
        <div className="w-1/3">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-2xl">
            <h3 className="text-xl font-light mb-6 text-center text-white tracking-wide">Impact Effects</h3>
            <div className="space-y-4">
              <div className="flex items-center p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-300">
                <div className="w-3 h-3 rounded-full bg-red-500 mr-4 shadow-md"></div>
                <span className="text-white font-light">Impact Crater</span>
              </div>
              <div className="flex items-center p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-300">
                <div className="w-3 h-3 rounded-full bg-orange-500 mr-4 shadow-md"></div>
                <span className="text-white font-light">Thermal Effects</span>
              </div>
              <div className="flex items-center p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-300">
                <div className="w-3 h-3 rounded-full bg-yellow-500 mr-4 shadow-md"></div>
                <span className="text-white font-light">Air Blast Zone</span>
              </div>
              <div className="flex items-center p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-300">
                <div className="w-3 h-3 rounded-full bg-purple-500 mr-4 shadow-md"></div>
                <span className="text-white font-light">Seismic Effects</span>
              </div>
            </div>
            
            <div className="mt-6 p-4 bg-white/5 rounded-xl border border-white/10">
              <p className="text-sm text-white/70 text-center font-light">
                Simulation uses 1km asteroid parameters
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Modern Impact Analysis Results */}
      {impactData && (
        <div className="mt-8">
          <h3 className="text-2xl font-light mb-6 text-center text-white tracking-wide">
            Impact Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Asteroid Parameters Box */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 group">
              <div className="flex items-center mb-4">
                <div className="w-2 h-8 bg-gradient-to-b from-blue-400 to-blue-600 rounded-full mr-4"></div>
                <h4 className="font-light text-white text-lg">Asteroid Data</h4>
              </div>
              <div className="space-y-3 text-white/80">
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Diameter</span>
                  <span className="font-mono text-white">{impactData.impact_parameters.diameter_m}m</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Velocity</span>
                  <span className="font-mono text-white">{impactData.impact_parameters.velocity_km_s} km/s</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Density</span>
                  <span className="font-mono text-white">{impactData.impact_parameters.density_kg_m3} kg/m³</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Angle</span>
                  <span className="font-mono text-white">{impactData.impact_parameters.angle_degrees}°</span>
                </div>
              </div>
            </div>
            
            {/* Impact Effects Box */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 group">
              <div className="flex items-center mb-4">
                <div className="w-2 h-8 bg-gradient-to-b from-orange-400 to-red-600 rounded-full mr-4"></div>
                <h4 className="font-light text-white text-lg">Impact Effects</h4>
              </div>
              <div className="space-y-3 text-white/80">
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Crater</span>
                  <span className="font-mono text-white">{(impactData.impact_effects.crater_diameter_m / 1000).toFixed(1)} km</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Depth</span>
                  <span className="font-mono text-white">{(impactData.impact_effects.crater_depth_m / 1000).toFixed(1)} km</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Seismic</span>
                  <span className="font-mono text-white">M{impactData.impact_effects.seismic_magnitude}</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Thermal</span>
                  <span className="font-mono text-white">{impactData.impact_effects.thermal_radius_km} km</span>
                </div>
              </div>
            </div>
            
            {/* Casualties Box */}
            <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300 group">
              <div className="flex items-center mb-4">
                <div className="w-2 h-8 bg-gradient-to-b from-yellow-400 to-red-600 rounded-full mr-4"></div>
                <h4 className="font-light text-white text-lg">Human Impact</h4>
              </div>
              <div className="space-y-3 text-white/80">
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Deaths</span>
                  <span className="font-mono text-white">{impactData.casualties.estimated_deaths.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Injuries</span>
                  <span className="font-mono text-white">{impactData.casualties.estimated_injuries.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Affected</span>
                  <span className="font-mono text-white">{impactData.casualties.population_affected.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                  <span className="font-light">Confidence</span>
                  <span className="font-mono text-white capitalize">{impactData.casualties.confidence_level}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Map;

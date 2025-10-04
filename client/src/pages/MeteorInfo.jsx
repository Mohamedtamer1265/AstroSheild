
import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Map from "../components/Map";

const MeteorInfo = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get asteroid data from navigation state
  const asteroidData = location.state?.asteroidData;
  const fromPage = location.state?.fromPage;
  
  // State management
  const [viewMode, setViewMode] = useState("simple"); // simple or complex
  const [activeTab, setActiveTab] = useState("overview");
  const [impactData, setImpactData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detailedData, setDetailedData] = useState(null);

  // If no asteroid data, redirect back
  useEffect(() => {
    if (!asteroidData) {
      navigate('/meteor-page');
    } else {
      // Fetch detailed data from JPL if we have an ID
      fetchDetailedAsteroidData();
    }
  }, [asteroidData, navigate]);

  // Fetch detailed asteroid data from your single asteroid API
  const fetchDetailedAsteroidData = async () => {
    if (!asteroidData?.id) return;
    
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/asteroid/${asteroidData.id}`);
      const data = await response.json();
      
      if (data.success) {
        setDetailedData(data.data);
      }
    } catch (error) {
      console.error('Error fetching detailed data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch impact prediction
  const fetchImpactPrediction = async () => {
    if (!asteroidData?.id) return;
    
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/predict/impact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          asteroid_id: asteroidData.id
        })
      });
      
      const data = await response.json();
      if (data.success) {
        setImpactData(data.impact_prediction);
      }
    } catch (error) {
      console.error('Error fetching impact prediction:', error);
    } finally {
      setLoading(false);
    }
  };

  // Format functions
  const formatNumber = (num, decimals = 2) => {
    if (!num) return "Unknown";
    return parseFloat(num).toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  const formatDistance = (distance) => {
    if (!distance) return "Unknown";
    const distanceNum = parseFloat(distance);
    if (distanceNum > 1000000) {
      return `${formatNumber(distanceNum / 1000000)} million km`;
    } else if (distanceNum > 1000) {
      return `${formatNumber(distanceNum / 1000)} thousand km`;
    }
    return `${formatNumber(distanceNum)} km`;
  };

  const getRiskLevel = () => {
    if (!asteroidData) return { level: "Unknown", color: "gray" };
    
    if (asteroidData.is_potentially_hazardous) {
      return { level: "High Risk", color: "red" };
    } else {
      const distance = parseFloat(asteroidData.miss_distance_km || 0);
      if (distance < 1000000) {
        return { level: "Medium Risk", color: "yellow" };
      } else {
        return { level: "Low Risk", color: "green" };
      }
    }
  };

  if (!asteroidData) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🌌</div>
          <h2 className="text-2xl font-bold mb-2">No Asteroid Data</h2>
          <p className="text-gray-400 mb-4">Please select an asteroid from the main page</p>
          <button 
            onClick={() => navigate('/meteor-page')}
            className="px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-700"
          >
            Back to Asteroids
          </button>
        </div>
      </div>
    );
  }

  const riskLevel = getRiskLevel();

  return (
    <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover">
      {/* Header */}
      <div className="bg-black/80 backdrop-blur border-b border-blue-500">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => navigate(fromPage === 'meteor-page' ? '/meteor-page' : '/')}
                className="text-blue-400 hover:text-blue-300 transition-colors"
              >
                ← Back to {fromPage === 'meteor-page' ? 'Asteroids' : 'Home'}
              </button>
              <div>
                <h1 className="text-2xl font-bold">
                  {asteroidData.is_potentially_hazardous ? "⚠️" : "☄️"} {asteroidData.name}
                </h1>
                <p className="text-gray-400">ID: {asteroidData.id} • NASA JPL Database</p>
              </div>
            </div>
            
            {/* View Mode Toggle */}
            <div className="flex items-center space-x-4">
              <div className="bg-gray-800 rounded-lg p-1 flex">
                <button
                  onClick={() => setViewMode("simple")}
                  className={`px-4 py-2 rounded-md transition-all ${
                    viewMode === "simple" 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  👥 Simple View
                </button>
                <button
                  onClick={() => setViewMode("complex")}
                  className={`px-4 py-2 rounded-md transition-all ${
                    viewMode === "complex" 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  🔬 Scientific View
                </button>
              </div>
              
              <div className={`px-3 py-1 rounded-full text-sm font-bold ${
                riskLevel.color === "red" ? "bg-red-600" :
                riskLevel.color === "yellow" ? "bg-yellow-600" :
                "bg-green-600"
              }`}>
                {riskLevel.level}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex space-x-1 bg-gray-800 rounded-lg p-1 mb-8">
          {[
            { id: "overview", label: "📊 Overview", icon: "📊" },
            { id: "orbital", label: "🌌 Orbital Data", icon: "🌌" },
            { id: "physical", label: "🪨 Physical Props", icon: "🪨" },
            { id: "impact", label: "🎯 Impact Analysis", icon: "🎯" },
            { id: "visualization", label: "📍 Location", icon: "📍" }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 px-4 py-3 rounded-md transition-all font-medium ${
                activeTab === tab.id 
                  ? "bg-blue-600 text-white shadow-lg" 
                  : "text-gray-400 hover:text-white hover:bg-gray-700"
              }`}
            >
              <span className="hidden md:inline">{tab.label}</span>
              <span className="md:hidden text-xl">{tab.icon}</span>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Info Card */}
            <div className="lg:col-span-2 bg-black/60 border border-blue-500 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-6 flex items-center">
                📋 Basic Information
                {viewMode === "complex" && <span className="ml-2 text-sm text-gray-400">(Scientific)</span>}
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {viewMode === "simple" ? (
                  // Simple View
                  <>
                    <div className="space-y-4">
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-blue-400 mb-2">📏 Size</h3>
                        <p className="text-2xl font-bold">
                          {asteroidData.estimated_diameter_km_min ? 
                            `${formatNumber(asteroidData.estimated_diameter_km_min, 3)} - ${formatNumber(asteroidData.estimated_diameter_km_max, 3)} km` :
                            "Size unknown"
                          }
                        </p>
                        <p className="text-gray-400">Estimated diameter</p>
                      </div>
                      
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-green-400 mb-2">📅 Closest Approach</h3>
                        <p className="text-2xl font-bold">{asteroidData.close_approach_date || "Unknown"}</p>
                        <p className="text-gray-400">Date of closest approach to Earth</p>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-yellow-400 mb-2">📍 Distance</h3>
                        <p className="text-2xl font-bold">{formatDistance(asteroidData.miss_distance_km)}</p>
                        <p className="text-gray-400">Closest distance to Earth</p>
                      </div>
                      
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-purple-400 mb-2">🚀 Speed</h3>
                        <p className="text-2xl font-bold">
                          {asteroidData.relative_velocity_km_s ? 
                            `${formatNumber(asteroidData.relative_velocity_km_s)} km/s` :
                            "Unknown"
                          }
                        </p>
                        <p className="text-gray-400">Relative to Earth</p>
                      </div>
                    </div>
                  </>
                ) : (
                  // Complex View
                  <>
                    <div className="space-y-4">
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-blue-400 mb-2">📊 Diameter Estimation</h3>
                        <div className="space-y-2">
                          <p><span className="text-gray-400">Min:</span> {formatNumber(asteroidData.estimated_diameter_km_min, 6)} km</p>
                          <p><span className="text-gray-400">Max:</span> {formatNumber(asteroidData.estimated_diameter_km_max, 6)} km</p>
                          <p><span className="text-gray-400">Avg:</span> {
                            asteroidData.estimated_diameter_km_min && asteroidData.estimated_diameter_km_max ?
                            formatNumber((asteroidData.estimated_diameter_km_min + asteroidData.estimated_diameter_km_max) / 2, 6) :
                            "Unknown"
                          } km</p>
                          <p><span className="text-gray-400">Absolute Magnitude (H):</span> {asteroidData.absolute_magnitude_h || "Unknown"}</p>
                        </div>
                      </div>
                      
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-green-400 mb-2">🎯 Approach Geometry</h3>
                        <div className="space-y-2">
                          <p><span className="text-gray-400">Date:</span> {asteroidData.close_approach_date || "Unknown"}</p>
                          <p><span className="text-gray-400">Miss Distance:</span> {formatNumber(asteroidData.miss_distance_km)} km</p>
                          <p><span className="text-gray-400">Miss Distance (AU):</span> {
                            asteroidData.miss_distance_km ? 
                            formatNumber(parseFloat(asteroidData.miss_distance_km) / 149597870.7, 6) :
                            "Unknown"
                          }</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-purple-400 mb-2">⚡ Kinematics</h3>
                        <div className="space-y-2">
                          <p><span className="text-gray-400">Relative Velocity:</span> {formatNumber(asteroidData.relative_velocity_km_s)} km/s</p>
                          <p><span className="text-gray-400">Relative Velocity:</span> {
                            asteroidData.relative_velocity_km_s ?
                            formatNumber(parseFloat(asteroidData.relative_velocity_km_s) * 3600) :
                            "Unknown"
                          } km/h</p>
                        </div>
                      </div>
                      
                      <div className="bg-gray-800 p-4 rounded-lg">
                        <h3 className="text-lg font-semibold text-red-400 mb-2">⚠️ Hazard Assessment</h3>
                        <div className="space-y-2">
                          <p><span className="text-gray-400">PHA Status:</span> 
                            <span className={`ml-2 px-2 py-1 rounded text-sm ${
                              asteroidData.is_potentially_hazardous ? "bg-red-600" : "bg-green-600"
                            }`}>
                              {asteroidData.is_potentially_hazardous ? "POTENTIALLY HAZARDOUS" : "SAFE"}
                            </span>
                          </p>
                          <p><span className="text-gray-400">NEO Reference ID:</span> {asteroidData.neo_reference_id || "Unknown"}</p>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Quick Stats Sidebar */}
            <div className="space-y-6">
              <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
                <h3 className="text-xl font-bold mb-4">🎯 Quick Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Risk Level:</span>
                    <span className={`font-bold ${
                      riskLevel.color === "red" ? "text-red-400" :
                      riskLevel.color === "yellow" ? "text-yellow-400" :
                      "text-green-400"
                    }`}>
                      {riskLevel.level}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Type:</span>
                    <span className="font-bold text-blue-400">Near-Earth Object</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Database:</span>
                    <span className="font-bold text-purple-400">NASA JPL</span>
                  </div>
                </div>
              </div>

              <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
                <h3 className="text-xl font-bold mb-4">🔗 External Links</h3>
                <div className="space-y-3">
                  {asteroidData.nasa_jpl_url && (
                    <a 
                      href={asteroidData.nasa_jpl_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="block w-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-center transition-colors"
                    >
                      🚀 NASA JPL Database
                    </a>
                  )}
                  <button 
                    onClick={fetchImpactPrediction}
                    disabled={loading}
                    className="block w-full bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-center transition-colors disabled:opacity-50"
                  >
                    {loading ? "🔄 Loading..." : "🎯 Predict Impact"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "orbital" && (
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">🌌 Orbital Mechanics</h2>
            {detailedData ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {viewMode === "simple" ? (
                  // Simple orbital view
                  <>
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-400 mb-2">🛸 Orbit Shape</h3>
                      <p className="text-gray-400">How stretched the orbit is</p>
                      <p className="text-2xl font-bold">{
                        detailedData.orbital_elements?.eccentricity ? 
                        (detailedData.orbital_elements.eccentricity < 0.1 ? "Nearly Circular" :
                         detailedData.orbital_elements.eccentricity < 0.5 ? "Slightly Oval" : "Very Oval") :
                        "Unknown"
                      }</p>
                    </div>
                    
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-green-400 mb-2">📏 Orbit Size</h3>
                      <p className="text-gray-400">Average distance from Sun</p>
                      <p className="text-2xl font-bold">{
                        detailedData.orbital_elements?.semi_major_axis ?
                        `${formatNumber(detailedData.orbital_elements.semi_major_axis)} AU` :
                        "Unknown"
                      }</p>
                    </div>
                    
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-purple-400 mb-2">🔄 Orbit Period</h3>
                      <p className="text-gray-400">Time to complete one orbit</p>
                      <p className="text-2xl font-bold">{
                        detailedData.orbital_elements?.semi_major_axis ?
                        `${formatNumber(Math.pow(detailedData.orbital_elements.semi_major_axis, 1.5))} years` :
                        "Unknown"
                      }</p>
                    </div>
                  </>
                ) : (
                  // Complex orbital view
                  Object.entries(detailedData.orbital_elements || {}).map(([key, value]) => (
                    <div key={key} className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-400 mb-2 capitalize">
                        {key.replace(/_/g, ' ')}
                      </h3>
                      <p className="text-2xl font-bold">{formatNumber(value, 6)}</p>
                      <p className="text-gray-400 text-sm">
                        {key === 'semi_major_axis' && "AU"}
                        {key === 'eccentricity' && "dimensionless"}
                        {key.includes('angle') && "degrees"}
                        {key === 'epoch' && "Julian Day"}
                      </p>
                    </div>
                  ))
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔄</div>
                <p className="text-xl">Loading detailed orbital data...</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "physical" && (
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">🪨 Physical Properties</h2>
            {detailedData ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {viewMode === "simple" ? (
                  // Simple physical view
                  <>
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-400 mb-2">📏 Size</h3>
                      <p className="text-gray-400">How big the asteroid is</p>
                      <p className="text-2xl font-bold">{
                        detailedData.physical_properties?.diameter_km ?
                        `${formatNumber(detailedData.physical_properties.diameter_km)} km` :
                        "Unknown"
                      }</p>
                    </div>
                    
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-yellow-400 mb-2">💡 Brightness</h3>
                      <p className="text-gray-400">How bright it appears</p>
                      <p className="text-2xl font-bold">{
                        detailedData.physical_properties?.absolute_magnitude ?
                        `H = ${formatNumber(detailedData.physical_properties.absolute_magnitude)}` :
                        "Unknown"
                      }</p>
                    </div>
                    
                    <div className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-gray-400 mb-2">🌟 Reflectivity</h3>
                      <p className="text-gray-400">How much light it reflects</p>
                      <p className="text-2xl font-bold">{
                        detailedData.physical_properties?.albedo ?
                        `${formatNumber(detailedData.physical_properties.albedo * 100)}%` :
                        "Unknown"
                      }</p>
                    </div>
                  </>
                ) : (
                  // Complex physical view
                  Object.entries(detailedData.physical_properties || {}).map(([key, value]) => (
                    <div key={key} className="bg-gray-800 p-4 rounded-lg">
                      <h3 className="text-lg font-semibold text-blue-400 mb-2 capitalize">
                        {key.replace(/_/g, ' ')}
                      </h3>
                      <p className="text-2xl font-bold">{formatNumber(value, 6)}</p>
                      <p className="text-gray-400 text-sm">
                        {key === 'diameter_km' && "kilometers"}
                        {key === 'absolute_magnitude' && "magnitude (H)"}
                        {key === 'albedo' && "geometric albedo"}
                      </p>
                    </div>
                  ))
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔄</div>
                <p className="text-xl">Loading physical properties...</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "impact" && (
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">🎯 Impact Analysis</h2>
            {impactData ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold text-red-400 mb-4">📍 Impact Location</h3>
                    <div className="space-y-2">
                      <p><span className="text-gray-400">Latitude:</span> {formatNumber(impactData.impact_coordinates.latitude, 6)}°</p>
                      <p><span className="text-gray-400">Longitude:</span> {formatNumber(impactData.impact_coordinates.longitude, 6)}°</p>
                    </div>
                  </div>
                  
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold text-orange-400 mb-4">🚀 Impact Velocity</h3>
                    <div className="space-y-2">
                      <p><span className="text-gray-400">Speed:</span> {formatNumber(impactData.impact_velocity.velocity_km_s)} km/s</p>
                      <p><span className="text-gray-400">Direction:</span> {impactData.impact_velocity.direction}</p>
                      <p><span className="text-gray-400">Bearing:</span> {formatNumber(impactData.impact_velocity.bearing_degrees)}°</p>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-6">
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold text-purple-400 mb-4">💥 Impact Effects</h3>
                    <div className="space-y-2">
                      <p><span className="text-gray-400">Energy:</span> {formatNumber(impactData.impact_details.energy_megatons)} megatons TNT</p>
                      <p><span className="text-gray-400">Date:</span> {new Date(impactData.impact_details.estimated_impact_date).toLocaleDateString()}</p>
                      <p><span className="text-gray-400">Mass:</span> {formatNumber(impactData.impact_details.estimated_mass_kg / 1e12)} trillion kg</p>
                    </div>
                  </div>
                  
                  <div className="bg-yellow-900 border border-yellow-600 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold text-yellow-400 mb-2">⚠️ Important Note</h3>
                    <p className="text-sm text-yellow-200">{impactData.note}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🎯</div>
                <p className="text-xl mb-4">Impact prediction not generated yet</p>
                <button 
                  onClick={fetchImpactPrediction}
                  disabled={loading}
                  className="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? "🔄 Generating..." : "🎯 Generate Impact Prediction"}
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === "visualization" && (
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">📍 Location Visualization</h2>
            {impactData ? (
              <div className="space-y-6">
                <div className="text-center">
                  <p className="text-gray-400 mb-4">
                    Predicted impact location: {formatNumber(impactData.impact_coordinates.latitude, 4)}°N, 
                    {formatNumber(impactData.impact_coordinates.longitude, 4)}°E
                  </p>
                </div>
                <div className="h-96 bg-gray-800 rounded-lg flex items-center justify-center">
                  <Map 
                    impactLocation={{
                      lat: impactData.impact_coordinates.latitude,
                      lng: impactData.impact_coordinates.longitude
                    }}
                    asteroidData={asteroidData}
                  />
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🗺️</div>
                <p className="text-xl mb-4">Generate impact prediction to view location</p>
                <button 
                  onClick={fetchImpactPrediction}
                  disabled={loading}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? "🔄 Generating..." : "🎯 Generate Prediction"}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MeteorInfo;

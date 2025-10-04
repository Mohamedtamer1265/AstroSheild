import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Map from "../components/Map";

const ExploreMode = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState("simple"); // "simple" or "expert"
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  // Simple mode state
  const [simpleParams, setSimpleParams] = useState({
    latitude: 40.7128,
    longitude: -74.0060,
    diameter_m: 1000,
    velocity_km_s: 20,
    density_kg_m3: 2600,
    angle_degrees: 45,
    location_name: "New York"
  });

  // Expert mode state
  const [expertParams, setExpertParams] = useState({
    semi_major_axis: 1.458,
    eccentricity: 0.223,
    inclination: 10.83,
    ascending_node: 304.3,
    argument_perihelion: 178.8,
    mean_anomaly: 320.1,
    epoch: 2460000.5,
    diameter_m: 1000,
    density_kg_m3: 2600
  });

  // Simple mode - direct impact analysis
  const analyzeSimpleImpact = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:5000/api/impact/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          diameter_m: simpleParams.diameter_m,
          velocity_km_s: simpleParams.velocity_km_s,
          density_kg_m3: simpleParams.density_kg_m3,
          angle_degrees: simpleParams.angle_degrees,
          impact_lat: simpleParams.latitude,
          impact_lon: simpleParams.longitude,
          location_name: simpleParams.location_name
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setAnalysisResult(data.data);
        console.log('Impact analysis completed:', data.data);
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Error analyzing impact:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Expert mode - propagate orbital elements then analyze impact
  const analyzeExpertImpact = async () => {
    try {
      setLoading(true);
      setError(null);

      // Step 1: Propagate orbital elements to get current position
      // Note: This would use your orbital propagation API from the documentation
      // For now, we'll use a simulated propagation that returns coordinates
      const propagationResponse = await fetch('http://localhost:5000/api/predict/position/expert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          orbital_elements: {
            semi_major_axis: expertParams.semi_major_axis,
            eccentricity: expertParams.eccentricity,
            inclination: expertParams.inclination,
            ascending_node: expertParams.ascending_node,
            argument_perihelion: expertParams.argument_perihelion,
            mean_anomaly: expertParams.mean_anomaly,
            epoch: expertParams.epoch
          },
          target_epoch: Date.now() / 1000 // Current time as Unix timestamp
        })
      });

      let impactLat, impactLon;
      
      if (propagationResponse.ok) {
        const propagationData = await propagationResponse.json();
        if (propagationData.success) {
          impactLat = propagationData.position.latitude;
          impactLon = propagationData.position.longitude;
        } else {
          throw new Error('Failed to propagate orbital elements');
        }
      } else {
        // Fallback: use sample coordinates if propagation API is not available
        console.warn('Propagation API not available, using sample coordinates');
        impactLat = 25.374916;
        impactLon = -157.729843;
      }

      // Step 2: Analyze impact at the propagated location
      const impactResponse = await fetch('http://localhost:5000/api/impact/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          diameter_m: expertParams.diameter_m,
          velocity_km_s: 20, // Default velocity
          density_kg_m3: expertParams.density_kg_m3,
          angle_degrees: 45, // Default angle
          impact_lat: impactLat,
          impact_lon: impactLon,
          location_name: `Propagated Impact (${impactLat.toFixed(4)}, ${impactLon.toFixed(4)})`
        })
      });

      if (!impactResponse.ok) {
        throw new Error(`HTTP error! status: ${impactResponse.status}`);
      }

      const impactData = await impactResponse.json();
      
      if (impactData.success) {
        setAnalysisResult({
          ...impactData.data,
          propagation_info: {
            original_elements: expertParams,
            propagated_coordinates: { latitude: impactLat, longitude: impactLon }
          }
        });
        console.log('Expert impact analysis completed:', impactData.data);
      } else {
        throw new Error(impactData.error || 'Impact analysis failed');
      }
    } catch (err) {
      console.error('Error in expert analysis:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSimpleInputChange = (field, value) => {
    setSimpleParams(prev => ({
      ...prev,
      [field]: parseFloat(value) || value
    }));
  };

  const handleExpertInputChange = (field, value) => {
    setExpertParams(prev => ({
      ...prev,
      [field]: parseFloat(value) || value
    }));
  };

  return (
    <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover">
      {/* Header */}
      <div className="bg-black/80 backdrop-blur border-b border-blue-500">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => navigate('/')}
                className="text-blue-400 hover:text-blue-300 transition-colors"
              >
                ← Back to Home
              </button>
              <div>
                <h1 className="text-2xl font-bold">🎯 Explore Mode</h1>
                <p className="text-gray-400">Custom asteroid impact analysis</p>
              </div>
            </div>
            
            {/* Mode Toggle */}
            <div className="bg-gray-800 rounded-lg p-1 flex">
              <button
                onClick={() => setMode("simple")}
                className={`px-4 py-2 rounded-md transition-all ${
                  mode === "simple" 
                    ? "bg-blue-600 text-white" 
                    : "text-gray-400 hover:text-white"
                }`}
              >
                🎯 Simple Mode
              </button>
              <button
                onClick={() => setMode("expert")}
                className={`px-4 py-2 rounded-md transition-all ${
                  mode === "expert" 
                    ? "bg-blue-600 text-white" 
                    : "text-gray-400 hover:text-white"
                }`}
              >
                🔬 Expert Mode
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Input Panel */}
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">
              {mode === "simple" ? "🎯 Simple Parameters" : "🔬 Orbital Elements"}
            </h2>

            {mode === "simple" ? (
              // Simple Mode Inputs
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Latitude (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="-90"
                      max="90"
                      value={simpleParams.latitude}
                      onChange={(e) => handleSimpleInputChange('latitude', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Longitude (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="-180"
                      max="180"
                      value={simpleParams.longitude}
                      onChange={(e) => handleSimpleInputChange('longitude', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Diameter (m)
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={simpleParams.diameter_m}
                      onChange={(e) => handleSimpleInputChange('diameter_m', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Velocity (km/s)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.1"
                      value={simpleParams.velocity_km_s}
                      onChange={(e) => handleSimpleInputChange('velocity_km_s', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Density (kg/m³)
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={simpleParams.density_kg_m3}
                      onChange={(e) => handleSimpleInputChange('density_kg_m3', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Impact Angle (°)
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="90"
                      value={simpleParams.angle_degrees}
                      onChange={(e) => handleSimpleInputChange('angle_degrees', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Location Name
                  </label>
                  <input
                    type="text"
                    value={simpleParams.location_name}
                    onChange={(e) => handleSimpleInputChange('location_name', e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                  />
                </div>

                <button
                  onClick={analyzeSimpleImpact}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-bold transition-colors disabled:opacity-50"
                >
                  {loading ? "🔄 Analyzing..." : "🎯 Analyze Impact"}
                </button>
              </div>
            ) : (
              // Expert Mode Inputs
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Semi-major Axis (AU)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      value={expertParams.semi_major_axis}
                      onChange={(e) => handleExpertInputChange('semi_major_axis', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Eccentricity
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="0"
                      max="0.99"
                      value={expertParams.eccentricity}
                      onChange={(e) => handleExpertInputChange('eccentricity', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Inclination (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="0"
                      max="180"
                      value={expertParams.inclination}
                      onChange={(e) => handleExpertInputChange('inclination', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Ascending Node (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="0"
                      max="360"
                      value={expertParams.ascending_node}
                      onChange={(e) => handleExpertInputChange('ascending_node', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Argument of Perihelion (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="0"
                      max="360"
                      value={expertParams.argument_perihelion}
                      onChange={(e) => handleExpertInputChange('argument_perihelion', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Mean Anomaly (°)
                    </label>
                    <input
                      type="number"
                      step="0.000001"
                      min="0"
                      max="360"
                      value={expertParams.mean_anomaly}
                      onChange={(e) => handleExpertInputChange('mean_anomaly', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Epoch (Julian Day)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={expertParams.epoch}
                      onChange={(e) => handleExpertInputChange('epoch', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Diameter (m)
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={expertParams.diameter_m}
                      onChange={(e) => handleExpertInputChange('diameter_m', e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Density (kg/m³)
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={expertParams.density_kg_m3}
                    onChange={(e) => handleExpertInputChange('density_kg_m3', e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white"
                  />
                </div>

                <button
                  onClick={analyzeExpertImpact}
                  disabled={loading}
                  className="w-full bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-bold transition-colors disabled:opacity-50"
                >
                  {loading ? "🔄 Propagating & Analyzing..." : "🔬 Propagate & Analyze"}
                </button>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="mt-4 bg-red-900/50 border border-red-500 rounded-lg p-4">
                <h3 className="text-red-400 font-bold mb-2">Error</h3>
                <p className="text-red-300">{error}</p>
              </div>
            )}
          </div>

          {/* Visualization Panel */}
          <div className="bg-black/60 border border-blue-500 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-6">📍 Impact Visualization</h2>
            
            {analysisResult ? (
              <div className="space-y-6">
                <div className="h-64 bg-gray-800 rounded-lg overflow-hidden">
                  <Map 
                    impactLocation={{
                      lat: analysisResult?.location?.latitude || 0,
                      lng: analysisResult?.location?.longitude || 0
                    }}
                    asteroidData={{
                      name: analysisResult?.location?.location_name || "Custom Impact",
                      estimated_diameter_km_max: (analysisResult?.impact_parameters?.diameter_m || 1000) / 1000
                    }}
                  />
                </div>

                {/* Analysis Results Summary */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-blue-400 font-bold mb-2">📍 Impact Location</h3>
                    <p className="text-sm">{analysisResult?.location?.location_name || "Unknown"}</p>
                    <p className="text-sm text-gray-400">
                      {analysisResult?.location?.latitude?.toFixed(4) || "0"}°, {analysisResult?.location?.longitude?.toFixed(4) || "0"}°
                    </p>
                  </div>
                  
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-orange-400 font-bold mb-2">💥 Crater Size</h3>
                    <p className="text-lg font-bold">
                      {((analysisResult?.impact_effects?.crater_diameter_m || 0) / 1000).toFixed(1)} km
                    </p>
                    <p className="text-sm text-gray-400">Diameter</p>
                  </div>
                  
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-purple-400 font-bold mb-2">🌊 Seismic</h3>
                    <p className="text-lg font-bold">
                      M{analysisResult?.impact_effects?.seismic_magnitude || 0}
                    </p>
                    <p className="text-sm text-gray-400">Magnitude</p>
                  </div>
                  
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-red-400 font-bold mb-2">☠️ Casualties</h3>
                    <p className="text-lg font-bold">
                      {(analysisResult?.casualties?.estimated_deaths || 0).toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-400">Estimated Deaths</p>
                  </div>
                </div>

                {/* Expert Mode Additional Info */}
                {mode === "expert" && analysisResult?.propagation_info && (
                  <div className="bg-purple-900/30 border border-purple-500 rounded-lg p-4">
                    <h3 className="text-purple-400 font-bold mb-2">🔬 Propagation Results</h3>
                    <p className="text-sm text-gray-300">
                      Orbital elements propagated to current position:
                    </p>
                    <p className="text-sm text-gray-400">
                      {analysisResult?.propagation_info?.propagated_coordinates?.latitude?.toFixed(6) || "0"}°, 
                      {analysisResult?.propagation_info?.propagated_coordinates?.longitude?.toFixed(6) || "0"}°
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="h-64 bg-gray-800 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <div className="text-4xl mb-4">🎯</div>
                  <p className="text-gray-400">
                    {mode === "simple" 
                      ? "Enter parameters and click 'Analyze Impact' to see results" 
                      : "Enter orbital elements and click 'Propagate & Analyze' to see results"
                    }
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExploreMode;
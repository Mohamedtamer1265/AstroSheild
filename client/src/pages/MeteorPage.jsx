import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAccessibility } from "../contexts/AccessibilityContext";

export default function MeteorPage() {
  const [search, setSearch] = useState("");
  const [asteroids, setAsteroids] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    viewed: "all",
    hazardous: "all",
    dateRange: "current"
  });
  
  const navigate = useNavigate();
  const { getAccessibleColors } = useAccessibility();
  const colors = getAccessibleColors();

  // Fetch asteroids from your API
  useEffect(() => {
    fetchAsteroids();
  }, []);

  const fetchAsteroids = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch from your API
      const response = await fetch('http://localhost:5000/api/asteroids/all');
      const data = await response.json();
      console.log('Response data:', data); // Fixed: was print() which triggered browser print dialog
      
      if (data.success) {
        setAsteroids(data.asteroids);
        console.log(`Loaded ${data.total_count} asteroids from NASA NeoWs`);
      } else {
        throw new Error(data.error || 'Failed to fetch asteroids');
      }
    } catch (err) {
      console.error('Error fetching asteroids:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Filter asteroids based on search and filters
  const filteredAsteroids = asteroids.filter(asteroid => {
    const matchesSearch = asteroid.name.toLowerCase().includes(search.toLowerCase()) ||
                         asteroid.id.toString().includes(search);
    
    const matchesHazardous = filters.hazardous === "all" || 
                            (filters.hazardous === "hazardous" && asteroid.is_potentially_hazardous) ||
                            (filters.hazardous === "safe" && !asteroid.is_potentially_hazardous);
    
    return matchesSearch && matchesHazardous;
  });

  // Handle asteroid click - navigate to MeteorInfo with asteroid data
  const handleAsteroidClick = (asteroid) => {
    // Navigate to MeteorInfo page with asteroid data
    navigate('/meteor-info', { 
      state: { 
        asteroidData: asteroid,
        fromPage: 'meteor-page'
      } 
    });
  };

  // Format diameter for display
  const formatDiameter = (asteroid) => {
    if (asteroid.estimated_diameter_km_min && asteroid.estimated_diameter_km_max) {
      const min = asteroid.estimated_diameter_km_min.toFixed(3);
      const max = asteroid.estimated_diameter_km_max.toFixed(3);
      return `${min} - ${max} km`;
    }
    return "Unknown";
  };

  // Format distance for display
  const formatDistance = (distance) => {
    if (!distance) return "Unknown";
    const distanceNum = parseFloat(distance);
    if (distanceNum > 1000000) {
      return `${(distanceNum / 1000000).toFixed(2)}M km`;
    } else if (distanceNum > 1000) {
      return `${(distanceNum / 1000).toFixed(2)}K km`;
    }
    return `${distanceNum.toFixed(2)} km`;
  };

  // Generate placeholder image based on asteroid properties
  const getAsteroidImage = (asteroid) => {
    // You can replace this with actual asteroid images if available
    const imageIndex = parseInt(asteroid.id) % 5 + 1; // Cycle through 5 different placeholder images
    return `/src/assets/img/asteroid${imageIndex}.png`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-xl">Loading asteroids from NASA...</p>
          <p className="text-gray-400">Fetching real-time data</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover flex items-center justify-center">
        <div className="text-center">
          <div className={`text-6xl mb-4 ${colors.dangerText}`}>⚠️</div>
          <h2 className="text-2xl font-bold mb-2">Error Loading Asteroids</h2>
          <p className="text-gray-400 mb-4">{error}</p>
          <button 
            onClick={fetchAsteroids}
            className={`px-4 py-2 rounded-lg hover:opacity-80 transition-all ${colors.info}`}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover p-6">
      {/* Header Stats */}
      <div className="text-center mb-6">
        <h1 className="text-4xl font-bold mb-2">🌌 Near Earth Asteroids</h1>
        <p className="text-gray-300">
          Showing {filteredAsteroids.length} of {asteroids.length} asteroids from NASA NeoWs
        </p>
      </div>

      {/* Filters */}
      <div className="max-w-6xl mx-auto border border-blue-500 rounded-lg p-6 backdrop-blur bg-black/50 mb-8">
        <h2 className="text-xl font-bold mb-4 text-center">🔍 Asteroid Filters</h2>
        
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          {/* Search */}
          <div className="flex w-full md:w-1/3">
            <input
              type="text"
              placeholder="Search by name or ID..."
              className="w-full p-3 rounded-l bg-gray-900 border border-gray-600 focus:outline-none focus:border-blue-500"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button className="px-4 py-3 bg-blue-600 text-white rounded-r hover:bg-blue-700">
              🔍
            </button>
          </div>

          {/* Hazard Filter */}
          <select 
            className="p-3 rounded bg-gray-900 border border-gray-600 focus:outline-none focus:border-blue-500"
            value={filters.hazardous}
            onChange={(e) => setFilters({...filters, hazardous: e.target.value})}
          >
            <option value="all">All Asteroids</option>
            <option value="hazardous">⚠️ Potentially Hazardous</option>
            <option value="safe">✅ Safe</option>
          </select>

          {/* Date Range Filter */}
          <select 
            className="p-3 rounded bg-gray-900 border border-gray-600 focus:outline-none focus:border-blue-500"
            value={filters.dateRange}
            onChange={(e) => setFilters({...filters, dateRange: e.target.value})}
          >
            <option value="current">This Week</option>
            <option value="month">This Month</option>
            <option value="year">This Year</option>
          </select>

          {/* Refresh Button */}
          <button 
            onClick={fetchAsteroids}
            className={`px-4 py-3 rounded-lg hover:opacity-80 transition-colors ${colors.success}`}
            disabled={loading}
          >
            {loading ? "🔄" : "🔄 Refresh"}
          </button>
        </div>
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between max-w-6xl mx-auto mb-6">
        <h2 className="text-2xl font-bold">
          ☄️ Asteroids ({filteredAsteroids.length})
        </h2>
        <div className="flex gap-2">
          <span className={`px-3 py-1 rounded text-sm ${colors.warning}`}>
            ⚠️ {asteroids.filter(a => a.is_potentially_hazardous).length} Hazardous
          </span>
          <span className={`px-3 py-1 rounded text-sm ${colors.success}`}>
            ✅ {asteroids.filter(a => !a.is_potentially_hazardous).length} Safe
          </span>
        </div>
      </div>

      {/* Asteroid Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
        {filteredAsteroids.map((asteroid) => (
          <div
            key={asteroid.id}
            onClick={() => handleAsteroidClick(asteroid)}
            className="bg-black/60 border border-blue-500 rounded-lg text-center p-4 cursor-pointer hover:border-blue-400 hover:bg-black/70 transition-all duration-300 transform hover:scale-105"
          >
            {/* Asteroid Image/Icon */}
            <div className="w-full h-40 bg-gradient-to-b from-gray-800 to-gray-900 flex items-center justify-center rounded mb-4 relative">
              <div className="text-6xl">
                {asteroid.is_potentially_hazardous ? "⚠️☄️" : "☄️"}
              </div>
              {asteroid.is_potentially_hazardous && (
                <div className={`absolute top-2 right-2 text-xs px-2 py-1 rounded ${colors.danger}`}>
                  HAZARDOUS
                </div>
              )}
            </div>
            
            {/* Asteroid Info */}
            <div className="space-y-2">
              <h3 className="font-bold text-lg truncate" title={asteroid.name}>
                {asteroid.name}
              </h3>
              
              <div className="text-sm text-gray-300 space-y-1">
                <p>📏 <span className={colors.infoText}>{formatDiameter(asteroid)}</span></p>
                <p>📅 <span className={colors.successText}>{asteroid.close_approach_date}</span></p>
                <p>📍 <span className={colors.warningText}>{formatDistance(asteroid.miss_distance_km)}</span></p>
                <p>🚀 <span className={colors.dangerText}>{parseFloat(asteroid.relative_velocity_km_s || 0).toFixed(2)} km/s</span></p>
              </div>
              
              {/* Quick Stats */}
              <div className="flex justify-between text-xs mt-3 pt-2 border-t border-gray-600">
                <span className="text-gray-400">ID: {asteroid.id}</span>
                <span className={asteroid.is_potentially_hazardous ? colors.dangerText : colors.successText}>
                  {asteroid.is_potentially_hazardous ? "⚠️ PHA" : "✅ SAFE"}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* No Results */}
      {filteredAsteroids.length === 0 && !loading && (
        <div className="text-center mt-12">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-bold mb-2">No asteroids found</h3>
          <p className="text-gray-400">Try adjusting your search or filters</p>
        </div>
      )}

      {/* Footer Info */}
      <div className="max-w-6xl mx-auto mt-12 p-6 bg-black/50 rounded-lg border border-blue-500">
        <h3 className="text-lg font-bold mb-2">📊 Data Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
          <div>
            <p><strong>Data Source:</strong> NASA NeoWs API</p>
            <p><strong>Update Frequency:</strong> Real-time</p>
          </div>
          <div>
            <p><strong>Distance:</strong> Miss distance from Earth</p>
            <p><strong>Velocity:</strong> Relative to Earth</p>
          </div>
          <div>
            <p><strong>PHA:</strong> Potentially Hazardous Asteroid</p>
            <p><strong>Click:</strong> View detailed information</p>
          </div>
        </div>
      </div>
    </div>
  );
}

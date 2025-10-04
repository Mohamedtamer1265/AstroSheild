import React, { useEffect, useState } from "react";
import Map from "../components/Map";

const AsteroidDashboard = () => {
  const [asteroid, setAsteroid] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Dummy data
    const dummyData = {
      id: "2004MN4",
      name: "Apophis",
      discoveryDate: "2004-06-19",
      discoverer: "Roy A. Tucker / Kitt Peak Observatory",
      currentPosition: "Near-Earth Space",
      distanceFromEarth: "16.4 million km",
      orbitalSpeed: "30.73 km/s",
      orbitalPeriod: "323.6 days",
      orbitEccentricity: "0.191",
      diameter: "340 m",
      mass: "2.7×10¹⁰ kg",
      composition: "Stony",
      apparentMagnitude: "19.7",
      previousClose: "2029-04-13",
      facts: "Will pass closer than some satellites in 2029",
      nameMeaning: "Named after the Egyptian god of chaos",
      image: "../src/assets/img/asteroid.png",
    };

    setAsteroid(dummyData);
    setLoading(false);
  }, []);

  if (loading) return <p className="text-white text-center mt-20">Loading...</p>;
  if (!asteroid) return <p className="text-white text-center mt-20">No Data Found</p>;

  return (
    <div className="min-h-screen w-full relative overflow-hidden p-8" style={{
      background: `
        radial-gradient(2px 2px at 20px 30px, #fff, transparent),
        radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
        radial-gradient(1px 1px at 90px 40px, #fff, transparent),
        radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
        radial-gradient(2px 2px at 160px 30px, #fff, transparent),
        radial-gradient(1px 1px at 200px 90px, rgba(255,255,255,0.7), transparent),
        radial-gradient(2px 2px at 240px 50px, #fff, transparent),
        radial-gradient(1px 1px at 280px 10px, rgba(255,255,255,0.9), transparent),
        radial-gradient(1px 1px at 320px 70px, #fff, transparent),
        radial-gradient(2px 2px at 360px 20px, rgba(255,255,255,0.8), transparent),
        linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)
      `,
      backgroundSize: '400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px, 100% 100%'
    }}>

      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-light text-white tracking-wide">
            Asteroid ID: {asteroid.id}
          </h1>
          <button className="bg-white/15 backdrop-blur-md border border-white/20 rounded-2xl px-6 py-3 text-white font-light hover:bg-white/20 transition-all duration-300">
            + Get Started
          </button>
        </div>

        {/* Info Cards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Basic Info */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center mb-4">
              <div className="w-2 h-8 bg-gradient-to-b from-blue-400 to-blue-600 rounded-full mr-4"></div>
              <h3 className="text-xl font-light text-white">Basic Information</h3>
            </div>
            <div className="space-y-3 text-white/80">
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Name</span>
                <span className="font-mono text-white">{asteroid.name}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Discovery Date</span>
                <span className="font-mono text-white">{asteroid.discoveryDate}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Discoverer</span>
                <span className="font-mono text-white text-sm">{asteroid.discoverer}</span>
              </div>
            </div>
          </div>

          {/* Orbit & Position */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center mb-4">
              <div className="w-2 h-8 bg-gradient-to-b from-green-400 to-green-600 rounded-full mr-4"></div>
              <h3 className="text-xl font-light text-white">Orbit & Position</h3>
            </div>
            <div className="space-y-3 text-white/80">
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Current Position</span>
                <span className="font-mono text-white text-sm">{asteroid.currentPosition}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Distance From Earth</span>
                <span className="font-mono text-white">{asteroid.distanceFromEarth}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Orbital Speed</span>
                <span className="font-mono text-white">{asteroid.orbitalSpeed}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Orbital Period</span>
                <span className="font-mono text-white">{asteroid.orbitalPeriod}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Eccentricity</span>
                <span className="font-mono text-white">{asteroid.orbitEccentricity}</span>
              </div>
            </div>
          </div>

          {/* Physical Characteristics */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center mb-4">
              <div className="w-2 h-8 bg-gradient-to-b from-orange-400 to-red-600 rounded-full mr-4"></div>
              <h3 className="text-xl font-light text-white">Physical Characteristics</h3>
            </div>
            <div className="space-y-3 text-white/80">
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Diameter</span>
                <span className="font-mono text-white">{asteroid.diameter}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Mass</span>
                <span className="font-mono text-white">{asteroid.mass}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Composition</span>
                <span className="font-mono text-white">{asteroid.composition}</span>
              </div>
              <div className="flex justify-between items-center p-2 rounded-lg bg-white/5">
                <span className="font-light">Apparent Magnitude</span>
                <span className="font-mono text-white">{asteroid.apparentMagnitude}</span>
              </div>
            </div>
          </div>

          {/* Additional Info with Image */}
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 shadow-xl hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center mb-4">
              <div className="w-2 h-8 bg-gradient-to-b from-purple-400 to-purple-600 rounded-full mr-4"></div>
              <h3 className="text-xl font-light text-white">Additional Information</h3>
            </div>
            <div className="flex justify-between items-start">
              <div className="space-y-3 text-white/80 flex-1 mr-4">
                <div className="p-2 rounded-lg bg-white/5">
                  <span className="font-light block">Previous Close Approaches</span>
                  <span className="font-mono text-white text-sm">{asteroid.previousClose}</span>
                </div>
                <div className="p-2 rounded-lg bg-white/5">
                  <span className="font-light block">Interesting Facts</span>
                  <span className="font-mono text-white text-sm">{asteroid.facts}</span>
                </div>
                <div className="p-2 rounded-lg bg-white/5">
                  <span className="font-light block">Name Meaning</span>
                  <span className="font-mono text-white text-sm">{asteroid.nameMeaning}</span>
                </div>
              </div>
              <img 
                src={asteroid.image} 
                alt="asteroid" 
                className="w-32 h-32 object-cover rounded-xl border border-white/20"
              />
            </div>
          </div>
        </div>
      </div>
      <Map impactLocation={null} asteroidData={null} />
    </div>
  );
};

export default AsteroidDashboard;

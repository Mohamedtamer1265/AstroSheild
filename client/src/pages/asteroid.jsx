import React, { useEffect, useState } from "react";

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
    <div className="dashboard-page">
      <style>{`
        .dashboard-page {
          min-height: 100vh;
          width: 100%;
          background: url('../src/assets/img/gameintro.jpg') no-repeat center center fixed;
          background-size: cover;
          color: white;
          font-family: 'Open Sans', sans-serif;
          display: flex;
          justify-content: center;
          padding: 40px 20px;
        }

        .dashboard-container {
          max-width: 900px;
          width: 100%;
        }

        .dashboard-card {
          background: rgba(0,0,0,0.7);
          border: 1px solid #15EEFF;
          border-radius: 15px;
          padding: 25px;
          margin-bottom: 20px;
          box-shadow: 0 0 20px rgba(21, 238, 255, 0.4);
        }

        .dashboard-card h3 {
          font-size: 22px;
          margin-bottom: 10px;
          color: #F7F7F7;
        }

        .dashboard-card p {
          font-size: 18px;
          margin: 4px 0;
        }

        .asteroid-image {
          width: 150px;
          border-radius: 12px;
          margin-left: auto;
        }

        .top-section {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 30px;
        }

        .get-started-btn {
          background: #d84594;
          color: white;
          padding: 10px 20px;
          border-radius: 12px;
          font-weight: bold;
          cursor: pointer;
          text-decoration: none;
        }
      `}</style>

      <div className="dashboard-container">
        <div className="top-section">
          <h1>ID: {asteroid.id}</h1>
          <a href="#" className="get-started-btn">+ Get Started</a>
        </div>

        {/* Basic Info */}
        <div className="dashboard-card">
          <h3>Basic Information</h3>
          <p><strong>Name:</strong> {asteroid.name}</p>
          <p><strong>Discovery Date:</strong> {asteroid.discoveryDate}</p>
          <p><strong>Discoverer / Observatory:</strong> {asteroid.discoverer}</p>
        </div>

        {/* Orbit & Position */}
        <div className="dashboard-card">
          <h3>Orbit & Position</h3>
          <p><strong>Current Position:</strong> {asteroid.currentPosition}</p>
          <p><strong>Distance From Earth:</strong> {asteroid.distanceFromEarth}</p>
          <p><strong>Orbital Speed:</strong> {asteroid.orbitalSpeed}</p>
          <p><strong>Orbital Period:</strong> {asteroid.orbitalPeriod}</p>
          <p><strong>Orbit Shape (Eccentricity):</strong> {asteroid.orbitEccentricity}</p>
        </div>

        {/* Physical Characteristics */}
        <div className="dashboard-card">
          <h3>Physical Characteristics</h3>
          <p><strong>Estimated Diameter:</strong> {asteroid.diameter}</p>
          <p><strong>Mass:</strong> {asteroid.mass}</p>
          <p><strong>Composition:</strong> {asteroid.composition}</p>
          <p><strong>Apparent Magnitude:</strong> {asteroid.apparentMagnitude}</p>
        </div>

        {/* Image + Stats */}
        <div className="dashboard-card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h3>Additional Info</h3>
            <p><strong>Previous Close Approaches:</strong> {asteroid.previousClose}</p>
            <p><strong>Interesting Facts:</strong> {asteroid.facts}</p>
            <p><strong>Name Meaning:</strong> {asteroid.nameMeaning}</p>
          </div>
          <img src={asteroid.image} alt="asteroid" className="asteroid-image" />
        </div>
      </div>
    </div>
  );
};

export default AsteroidDashboard;

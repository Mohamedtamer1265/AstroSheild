// page/Home.jsx
import React from "react";
import bgImg from "../assets/img/intro.jpg";
import gameBgImg from "../assets/img/gameintro.jpg";
import wiiryvid from "../assets/vid/wiry.mp4";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const ASTRO_PINK = "#d84594";
  const navigate = useNavigate();
  
  return (
    <div>
      {/* ================= Home Section ================= */}
      <section
        id="home-section"
        className="h-screen w-full bg-cover bg-center flex flex-col items-center justify-center text-white"
        style={{ backgroundImage: `url(${bgImg})` }}
      >
        <div className="flex flex-col items-center z-10 p-4">
          <h1 className="text-astro-glow font-normal text-white mb-10 leading-none" style={{  fontFamily: '"Space Mono", monospace', fontSize: '64px'  }}>
            Astroshield
          </h1>

          {/* Explore Asteroids Button */}
          <button
            className="text-white px-8 py-4 rounded-lg font-bold text-xl mt-10 shadow-xl transition duration-300 hover:opacity-90"
            style={{ backgroundColor: ASTRO_PINK }}
            onClick={() => navigate("/MeteorPage")} // Navigate to MeteorPage
          >
            Explore Asteroids
          </button>

          {/* Play Now Button */}
          <button
            className="bg-transparent text-white border-2 px-8 py-4 rounded-lg font-bold text-xl mt-4 transition duration-300"
            style={{ borderColor: ASTRO_PINK, color: ASTRO_PINK }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.backgroundColor = `${ASTRO_PINK}20`)
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.backgroundColor = "transparent")
            }
            onClick={() => {
              const gameSection = document.getElementById("game-section"); // target section, not button
              if (gameSection) {
                gameSection.scrollIntoView({ behavior: "smooth" });
              }
            }}
          >
            Play Now
          </button>
        </div>
      </section>

      {/* -------------------- EXPLANATION SECTION -------------------- */}
      <section
        id="explanation-section"
        className="min-h-screen w-full bg-cover bg-center flex flex-col items-center justify-center text-white relative py-16"
        style={{ backgroundImage: `url(${gameBgImg})` }}
      >
        {/* Section Title */}
        <div className="relative z-10 text-center mb-12">
          <h1 className="text-5xl font-bold mb-4">🌍 About AstroShield</h1>
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Advanced asteroid impact simulation and planetary defense system
          </p>
        </div>

        {/* Info Blocks Grid */}
        <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto px-6">
          
          {/* Block 1: Impact Simulation */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-2xl font-bold text-white mb-4">Impact Simulation</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Interactive world map allowing you to simulate asteroid impacts anywhere on Earth. 
              Click on any location to see potential damage radius, affected population, and environmental effects.
            </p>
          </div>

          {/* Block 2: Real NASA Data */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">🛰️</div>
              <h3 className="text-2xl font-bold text-white mb-4">NASA Data Integration</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Powered by real NASA APIs and scientific models. Access up-to-date information about 
              near-Earth objects, their trajectories, and potential threat assessments.
            </p>
          </div>

          {/* Block 3: Disaster Modeling */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">🌊</div>
              <h3 className="text-2xl font-bold text-white mb-4">Disaster Modeling</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Advanced modeling of secondary effects including tsunami generation, seismic activity, 
              and atmospheric changes caused by asteroid impacts.
            </p>
          </div>

          {/* Block 4: Educational Purpose */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">📚</div>
              <h3 className="text-2xl font-bold text-white mb-4">Educational Tool</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Learn about planetary defense, asteroid characteristics, and the importance of 
              space surveillance programs in protecting our planet.
            </p>
          </div>

          {/* Block 5: Interactive Experience */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">🎮</div>
              <h3 className="text-2xl font-bold text-white mb-4">Interactive Gaming</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Engage with Wiiry, our planetary defense hero, in scenario-based challenges that 
              test your decision-making skills in asteroid threat situations.
            </p>
          </div>

          {/* Block 6: Research & Analysis */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-6">
              <div className="text-5xl mb-4">🔬</div>
              <h3 className="text-2xl font-bold text-white mb-4">Research Platform</h3>
            </div>
            <p className="text-gray-200 leading-relaxed">
              Comprehensive database of asteroid properties, impact scenarios, and risk assessment 
              tools for researchers and space enthusiasts.
            </p>
          </div>

        </div>

        {/* Call to Action */}
        <div className="relative z-10 text-center mt-12">
          <button
            className="bg-[#d84594] text-white px-12 py-4 rounded-full font-semibold text-xl shadow-lg transition duration-300 hover:opacity-90 hover:scale-105"
            onClick={() => navigate("/asteroid")}
          >
            🚀 Start Exploring
          </button>
        </div>
      </section>

      {/* ================= Game Section ================= */}
      <section
        id="game-section"
        className="min-h-screen w-full bg-cover bg-center text-white p-8 flex flex-col items-center justify-start relative"
        style={{ backgroundImage: `url(${gameBgImg})` }}
      >
        {/* Section Title */}
        <h1 className="text-4xl font-bold text-center mb-12">Who is Wiiry?</h1>

        {/* Character Card */}
        <div className="flex flex-col items-center space-y-6 mb-12 border-2 border-[#15EEFF] rounded-2xl p-6 shadow-lg">
          <div className="relative w-64 h-64 rounded-2xl overflow-hidden flex items-center justify-center border-2 border-[#15EEFF] shadow-lg">
            <video
              src={wiiryvid}
              autoPlay
              loop
              muted
              playsInline
              className="w-full h-full object-cover rounded-2xl"
            />
          </div>

          <h2
            className="text-3xl font-extrabold px-4 py-2"
            style={{ fontFamily: '"Pixelify Sans", sans-serif' }}
          >
            Wiiry Boy
          </h2>

          <button
            className="bg-[#d84594] text-white px-8 py-3 rounded-full font-semibold text-lg shadow-lg transition duration-300 hover:opacity-90"
            onClick={() => navigate("/Game")} // Navigate to /Game
          >
            Play Now
          </button>
        </div>

        {/* Story Sections Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto px-6">
          
          {/* The Hero's Mission */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">🦸</div>
              <h3 className="text-xl font-bold text-white mb-3">The Hero's Mission</h3>
            </div>
            <p className="text-gray-200 leading-relaxed text-sm">
              In a world constantly threatened by falling asteroids, Wiiry rises as the dedicated hero 
              protecting Earth and its people. He travels across diverse landscapes while danger 
              approaches from above.
            </p>
          </div>

          {/* Critical Decisions */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">⚡</div>
              <h3 className="text-xl font-bold text-white mb-3">Critical Decisions</h3>
            </div>
            <p className="text-gray-200 leading-relaxed text-sm">
              Each asteroid approach presents Wiiry with crucial choices. Make the right decision 
              to save lives and prevent disaster. Choose wrong, and consequences follow with 
              lives at stake.
            </p>
          </div>

          {/* The Challenge */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">🎯</div>
              <h3 className="text-xl font-bold text-white mb-3">The Challenge</h3>
            </div>
            <p className="text-gray-200 leading-relaxed text-sm">
              Wiiry has only three attempts. Every choice shapes our planet's fate. 
              Can you guide him through the critical moments and help save Earth from 
              asteroid devastation?
            </p>
          </div>

        </div>

        {/* Game Features */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto px-6">
          
          {/* Gameplay Mechanics */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">🎮</div>
              <h3 className="text-xl font-bold text-white mb-3">Interactive Gameplay</h3>
            </div>
            <p className="text-gray-200 leading-relaxed text-sm">
              Experience multiple-choice scenarios where your decisions determine the outcome. 
              Navigate through different environments and face unique challenges in each situation.
            </p>
          </div>

          {/* Educational Value */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300 shadow-2xl">
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">🧠</div>
              <h3 className="text-xl font-bold text-white mb-3">Learn & Explore</h3>
            </div>
            <p className="text-gray-200 leading-relaxed text-sm">
              Learn about asteroid impacts, disaster response, and planetary defense while 
              having fun. Each scenario teaches real-world concepts about space threats.
            </p>
          </div>

        </div>
      </section>
    </div>
  );
};

export default Home;
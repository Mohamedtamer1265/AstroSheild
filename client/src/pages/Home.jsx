// page/Home.jsx
import React from "react";
import bgImg from "../assets/img/intro.jpg";

function Home() {
  // Define the pink color as a constant for readability
  const ASTRO_PINK = "#d84594";

  return (
    <div
      className="h-screen w-full bg-cover bg-center flex flex-col items-center justify-center text-white"
      style={{ backgroundImage: `url(${bgImg})` }}
    >
      <div className="flex flex-col items-center z-10 p-4">
        {/* Title */}
        <h1 className="text-astro-glow font-normal text-white mb-10 leading-none">
          Astroshield
        </h1>

        {/* Explore Asteroids Button */}
        <button
          className="text-white px-8 py-4 rounded-lg font-bold text-xl mt-10 shadow-xl transition duration-300 hover:opacity-90"
          style={{ backgroundColor: ASTRO_PINK }}
        >
          Explore Asteroids
        </button>

        {/* Play Now Button */}
        <button
          className="bg-transparent text-white border-2 px-8 py-4 rounded-lg font-bold text-xl mt-4 transition duration-300"
          style={{
            borderColor: ASTRO_PINK,
            // Use rgba for hover effect
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = `${ASTRO_PINK}20`)}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
        >
          Play Now
        </button>
      </div>
    </div>
  );
}

export default Home;

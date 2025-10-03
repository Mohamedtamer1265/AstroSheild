// page/Home.jsx
import React from "react";
import bgImg from "../assets/img/intro.jpg";
import gameBgImg from "../assets/img/gameintro.jpg";
import wiiryvid from "../assets/vid/wiry.mp4";

const Home = () => {
  const ASTRO_PINK = "#d84594";

  return (
    <div>
      {/* ================= Home Section ================= */}
      <section
        id="home-section"
        className="h-screen w-full bg-cover bg-center flex flex-col items-center justify-center text-white"
        style={{ backgroundImage: `url(${bgImg})` }}
      >
        <div className="flex flex-col items-center z-10 p-4">
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
            style={{ borderColor: ASTRO_PINK }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.backgroundColor = `${ASTRO_PINK}20`)
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.backgroundColor = "transparent")
            }
          >
            Play Now
          </button>
        </div>
      </section>
      {/* -------------------- CREATE SECTION (Customize Asteroid) -------------------- */}
      <section
        id="create-asteroid-section"
        className="min-h-screen w-full bg-cover bg-center flex flex-col items-center justify-center text-white relative"
        style={{ backgroundImage: `url(${gameBgImg})` }}
      >
        {/* Content */}
        <div className="relative z-10 text-center space-y-8">
          <h1 className="text-4xl font-bold">🌑 Create Your Own Asteroid</h1>

          <button
            onClick={() => (window.location.href = "/create-asteroid")}
            className="bg-[#d84594] text-white px-10 py-4 rounded-full font-semibold text-xl shadow-lg transition duration-300 hover:opacity-90"
          >
            🚀 Create Asteroid
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

          <button className="bg-[#d84594] text-white px-8 py-3 rounded-full font-semibold text-lg shadow-lg transition duration-300 hover:opacity-90">
            Play Now
          </button>
        </div>

        {/* Description Box */}
        <div
          className="p-8 w-full max-w-6xl text-justify"
          style={{
            color: "#F7F7F7",
            fontFamily: '"Open Sans", sans-serif',
            fontSize: "18px",
            fontStyle: "normal",
            fontWeight: 400,
            lineHeight: "normal",
            borderRadius: "10px",
            border: "0.5px solid #15EEFF",
            background: "rgba(40, 77, 128, 0.30)",
            boxShadow: "0 4px 15px rgba(0, 0, 0, 0.2)",
          }}
        >
          <p className="mb-4">
            In a world constantly changing and threatened by falling asteroids,
            Wiiry rises as the hero who has dedicated his life to protecting
            Earth and its people. He walks through different places — sometimes
            by the shore, other times across the desert — while above him,
            danger draws closer with every moment.
          </p>
          <p className="mb-4">
            But Wiiry never gives up. Each time an asteroid approaches, he faces
            critical decisions. The game offers him multiple options — if he
            chooses the right one, he saves lives and prevents disaster. If he
            chooses wrong, people will be harmed, and he will lose one of his
            three chances.
          </p>
          <p>
            He has only three attempts. Every choice shapes the planet’s fate.
            Can you guide Wiiry to make the right decisions and save Earth?
          </p>
        </div>
      </section>
    </div>
  );
};

export default Home;

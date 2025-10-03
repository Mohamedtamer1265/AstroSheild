// src/pages/Game.jsx
import React from 'react';
import gameBgImg from '../assets/img/intro.jpg'; // Adjust path if needed
import wiiryImage from '../assets/img/intro.jpg'; // Assume you have Wiiry's image

const Game = () => {
    // Define the pink color for consistency
    const ASTRO_PINK = '#d84594';

    return (
        <div 
            className="min-h-screen w-full bg-cover bg-center text-white p-8 flex flex-col items-center justify-start relative"
            style={{ backgroundImage: `url(${gameBgImg})` }}
        >
            {/* Optional: Planet in top-left, shooting stars in top-right */}
            {/* These are typically part of the background image or absolute positioned SVGs/icons */}
            <div className="absolute top-8 left-8">
                {/* <img src="/path/to/planet.svg" alt="planet" className="w-24" /> */}
            </div>
            <div className="absolute top-8 right-8 flex flex-col space-y-2">
                {/* <img src="/path/to/star.svg" alt="star" className="w-8" /> */}
            </div>

            {/* Main content container */}
            <div className="max-w-4xl w-full flex flex-col items-center space-y-12">
                {/* Top Section: "Who is Wiiry ?" */}
                <h1 className="text-4xl font-bold mt-12 mb-8 text-center">
                    Who is Wiiry ?
                </h1>

                {/* Wiiry Character Card */}
                <div className="bg-blue-900 bg-opacity-30 border border-blue-600 rounded-2xl p-6 flex flex-col items-center max-w-sm mx-auto shadow-lg backdrop-blur-sm">
                    <div className="relative w-48 h-48 rounded-full border-4 border-blue-400 p-1 mb-4 flex items-center justify-center">
                        <img 
                            src={wiiryImage} 
                            alt="Wiiry Boy" 
                            className="w-full h-full object-cover rounded-full" 
                        />
                        {/* Optional: Add a subtle glow effect around the image */}
                        <div className="absolute inset-0 rounded-full animate-pulse-slow border-2 border-blue-300 opacity-0 transition-opacity duration-1000"></div>
                    </div>
                    
                    {/* Wiiry Boy Title - Using custom font/glow if configured, or direct classes */}
                    <h2 
                        className="text-4xl font-extrabold text-white mb-6"
                        // If you have 'Pixelify Sans' configured as 'font-pixel' in tailwind.config.js, use that
                        // className="font-pixel text-4xl font-extrabold text-white mb-6"
                        style={{ fontFamily: '"Pixelify Sans", sans-serif' }} // Fallback if not in Tailwind config
                    >
                        Wiiry Boy
                    </h2>

                    {/* Play Now Button */}
                    <button
                        className={`bg-[${ASTRO_PINK}] text-white px-10 py-3 rounded-lg font-semibold text-lg shadow-xl transition duration-300 hover:opacity-90`}
                    >
                        Play Now
                    </button>
                </div>

                {/* Game Description */}
                <div className="bg-gray-800 bg-opacity-50 rounded-lg p-8 mt-12 text-lg leading-relaxed shadow-lg backdrop-blur-sm text-justify">
                    <p className="mb-4">
                        In a world constantly changing and threatened by falling asteroids, Wiiry rises as the hero who has dedicated his life to protecting Earth and its people. He walks through different places — sometimes by the shore, other times across the desert — while above him, danger draws closer with every moment.
                    </p>
                    <p className="mb-4">
                        But Wiiry never gives up. Each time an asteroid approaches, he faces critical decisions. The game offers him multiple options — if he chooses the right one, he saves lives and prevents disaster. If he chooses wrong, people will be harmed, and he will lose one of his three chances.
                    </p>
                    <p className="mb-0">
                        He has only three attempts. Every choice shapes the planet's fate. Can you guide Wiiry to make the right decisions and save Earth?
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Game;
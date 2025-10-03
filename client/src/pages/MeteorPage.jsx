import React, { useState } from "react";

const asteroidData = [
  { id: 1, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 2, name: "Eros", img: null }, // missing image
  { id: 3, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 4, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 5, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 6, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 7, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 8, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 9, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 10, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 11, name: "Ceres", img: "/asteroids/ceres.png" },
  { id: 12, name: "Ceres", img: "/asteroids/ceres.png" },
];

export default function MeteorPage() {
  const [search, setSearch] = useState("");

  return (
    <div className="min-h-screen bg-black text-white bg-[url('/stars-bg.png')] bg-cover p-6">
      {/* Filters */}
      <h1 className="text-center text-2xl font-bold mb-4">Filters</h1>

      <div className="max-w-5xl mx-auto border border-blue-500 rounded-lg p-6 backdrop-blur bg-black/50">
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="flex w-full md:w-1/3">
            <input
              type="text"
              placeholder="Search for a tutor"
              className="w-full p-2 rounded-l bg-gray-900 border border-gray-600 focus:outline-none"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button className="px-4 py-2 bg-gray-300 text-black rounded-r">
              search
            </button>
          </div>

          <select className="p-2 rounded bg-gray-900 border border-gray-600">
            <option>Viewed</option>
            <option>All</option>
          </select>

          <select className="p-2 rounded bg-gray-900 border border-gray-600">
            <option>All Subject</option>
          </select>

          <select className="p-2 rounded bg-gray-900 border border-gray-600">
            <option>All availability time</option>
          </select>
        </div>
      </div>

      {/* Asteroid Section */}
      <div className="flex items-center justify-between max-w-6xl mx-auto mt-10 mb-6">
        <h2 className="text-xl font-bold">All Asteroids</h2>
        <button className="px-4 py-2 bg-pink-600 rounded-lg hover:bg-pink-700">
          + Asteroid Customizer
        </button>
      </div>

      {/* Asteroid Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
        {asteroidData.map((asteroid) => (
          <div
            key={asteroid.id}
            className="bg-black/60 border border-blue-500 rounded-lg text-center p-4"
          >
            {asteroid.img ? (
              <img
                src={asteroid.img}
                alt={asteroid.name}
                className="w-full h-40 object-cover rounded"
              />
            ) : (
              <div className="w-full h-40 bg-black flex items-center justify-center rounded">
                <span className="text-gray-400">missing.png</span>
              </div>
            )}
            <p className="mt-2 font-medium">{asteroid.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

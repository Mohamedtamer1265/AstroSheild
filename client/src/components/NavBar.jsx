import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex justify-center fixed top-4 w-full z-50">
      <ul className="flex space-x-12 bg-gradient-to-r from-[#0f172a] to-[#1e293b] 
                     px-10 py-3 rounded-full shadow-lg border border-white/20 
                     backdrop-blur-md">
        <li>
          <Link to="/" className="text-white font-semibold hover:text-gray-300">
            Home
          </Link>
        </li>
        <li>
          <Link to="/how-to-use" className="text-gray-300 hover:text-white">
            How to Use
          </Link>
        </li>
        <li>
          <Link to="/about" className="text-gray-300 hover:text-white">
            About Us
          </Link>
        </li>
        <li>
          <Link to="/game" className="text-gray-300 hover:text-white">
            Game
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

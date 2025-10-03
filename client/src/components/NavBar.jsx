import React, { useState } from "react";

const Navbar = () => {
  const [active, setActive] = useState("#home-section"); // default active link

  const links = [
    { href: "#home-section", label: "Home" },
    { href: "#create-asteroid-section", label: "Create" },
    { href: "#game-section", label: "Game" },
  ];

  return (
    <nav className="flex justify-center fixed top-10 w-full z-50">
      <ul
        className="flex space-x-12 bg-gradient-to-r from-[#0f172a] to-[#1e293b] 
                     px-10 py-3 rounded-full shadow-lg border border-white/20 
                     backdrop-blur-md"
      >
        {links.map((link) => (
          <li key={link.href}>
            <a
              href={link.href}
              onClick={() => setActive(link.href)}
              className={`${
                active === link.href
                  ? "text-white font-bold" // active link style
                  : "text-gray-300 font-normal" // normal link style
              } hover:text-white transition`}
            >
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;

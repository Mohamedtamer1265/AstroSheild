// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // Include all your component files here, e.g.,
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    // This is where you put global theme settings if you want to replace Tailwind's defaults
    extend: {
      // This is where you add new utility classes
      fontFamily: {
        // Now you can use the Tailwind class 'font-pixel'
        'pixel': ['"Pixelify Sans"', 'sans-serif'], 
      },
    },
  },
  plugins: [],
}
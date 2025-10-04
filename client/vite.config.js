// vite.config.js (Corrected)
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    // You've correctly used the Vite plugin for Tailwind here
    tailwindcss(), 
    react({
      // Keep your react plugins
      babel: {
        plugins: ['babel-plugin-react-compiler'],

      },
    }),
  ],
  base: '/', // Changed from '/AstroSheild' to '/' for local development
  server: {
    port: 3000,
  },
  // The 'extend' block has been removed from here!
})
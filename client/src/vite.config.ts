import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Needed for docker
    port: 3000,
    cors: true, // Enable CORS
    origin: 'http://localhost:3000',
  },
}) 
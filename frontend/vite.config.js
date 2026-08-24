import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Defaults to the bare-metal workflow; compose sets http://backend:8000.
const API_TARGET = process.env.VITE_API_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    ws: { clientPort: +(process.env.FORWARD_FE_PORT || 5173) },
    watch: { usePolling: true },
    proxy: {
      "/api": API_TARGET,
      "/admin": API_TARGET,
    },
  },
});

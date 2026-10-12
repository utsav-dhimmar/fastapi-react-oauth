import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import babel from "@rolldown/plugin-babel";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), babel({ presets: [reactCompilerPreset()] })],
  server: {
    proxy: {
      "/auth": {
        target: "http://localhost:8000", // Change 'localhost' to '127.0.0.1'
        changeOrigin: true,
        secure: false,
      },
    },
  },
});

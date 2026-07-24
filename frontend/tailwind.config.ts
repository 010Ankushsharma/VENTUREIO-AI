import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f0ff",
          100: "#e4e7ff",
          500: "#6764f6",
          600: "#5550d9",
          700: "#4440b8",
          900: "#2a2870",
        },
        accent: {
          500: "#FF000F",
          600: "#cc000c",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

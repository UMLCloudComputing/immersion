import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        "custom-cyan": "#59bcc8",
        "custom-purple": "#783192",
        "custom-mid": "#768bf3",
        "discord-purple": "#5865f2",
        "engage-green": "#3ab549"
      },
    },
  },
  plugins: [],
};
export default config;

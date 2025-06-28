import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cdn.discordapp.com"
      },
      {
        protocol: "https",
        hostname: "se-images.campuslabs.com"
      }
    ]
  }
};

export default nextConfig;

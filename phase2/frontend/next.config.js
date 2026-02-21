/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    turbo: false, // Disable Turbopack to prevent memory issues
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "https://shakirhussain1-phase2-backend.hf.space",
  },
};

module.exports = nextConfig;

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "https://shakirhussain1-phase2-backend.hf.space",
  },
};

module.exports = nextConfig;

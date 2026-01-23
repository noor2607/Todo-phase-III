/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  },
  images: {
    unoptimized: true,
  },
  // Disable static export for development
  trailingSlash: false,
  reactStrictMode: true,
}

module.exports = nextConfig
#!/usr/bin/env node

// Start Next.js dev server using Node.js
const path = require('path');
const fs = require('fs');

// Import Next.js directly
const nextConfig = require('./next.config.js');

console.log('Starting Next.js development server on port 3000...');
console.log('API Backend: http://localhost:8000');
console.log('Frontend: http://localhost:3000');
console.log('');

// Set environment
process.env.NODE_ENV = 'development';
process.env.PORT = '3000';

// Use child_process to run next dev with proper environment
const { spawnSync } = require('child_process');

const result = spawnSync('node', [
  require.resolve('next/dist/bin/next'),
  'dev'
], {
  cwd: __dirname,
  stdio: 'inherit',
  env: {
    ...process.env,
    NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  }
});

process.exit(result.status || 0);

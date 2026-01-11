#!/usr/bin/env node

// Simple script to start Next.js dev server
const { spawn } = require('child_process');
const path = require('path');

console.log('Starting Next.js development server...');

const nextBin = path.join(__dirname, 'node_modules', '.bin', 'next');
const proc = spawn(process.execPath, [nextBin, 'dev'], {
  stdio: 'inherit',
  cwd: __dirname,
});

proc.on('exit', (code) => {
  console.log('Dev server exited with code', code);
  process.exit(code);
});

#!/bin/bash

# Phase V Frontend Development Script
# Runs the Next.js development server with proper environment setup

set -e

echo "🚀 Phase V Todo Frontend - Development Mode"
echo "============================================"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local from .env.example..."
    cp .env.example .env.local
    echo "✅ .env.local created. Please update with your API URLs if needed."
fi

echo ""
echo "🔧 Environment Configuration:"
echo "   API URL: ${NEXT_PUBLIC_API_URL:-http://localhost:8000}"
echo "   WS URL:  ${NEXT_PUBLIC_WS_URL:-ws://localhost:8080}"
echo ""
echo "🌐 Starting development server..."
echo "   Open: http://localhost:3000"
echo ""

# Start Next.js dev server
npm run dev

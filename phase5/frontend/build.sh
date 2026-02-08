#!/bin/bash

# Phase V Frontend Build Script
# Builds production-ready Docker image

set -e

IMAGE_NAME="phase5-frontend"
TAG="${1:-latest}"

echo "🐳 Building Docker Image: $IMAGE_NAME:$TAG"
echo "=========================================="

# Build arguments
API_URL="${NEXT_PUBLIC_API_URL:-http://chat-api:8000}"
WS_URL="${NEXT_PUBLIC_WS_URL:-ws://websocket-service:8080}"

echo ""
echo "📝 Build Configuration:"
echo "   Image: $IMAGE_NAME:$TAG"
echo "   API URL: $API_URL"
echo "   WS URL: $WS_URL"
echo ""

# Build Docker image
docker build \
  --build-arg NEXT_PUBLIC_API_URL="$API_URL" \
  --build-arg NEXT_PUBLIC_WS_URL="$WS_URL" \
  -t "$IMAGE_NAME:$TAG" \
  .

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 To run the image:"
echo "   docker run -p 3000:3000 \\"
echo "     -e NEXT_PUBLIC_API_URL=$API_URL \\"
echo "     -e NEXT_PUBLIC_WS_URL=$WS_URL \\"
echo "     $IMAGE_NAME:$TAG"
echo ""
echo "🔍 Image size:"
docker images "$IMAGE_NAME:$TAG" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

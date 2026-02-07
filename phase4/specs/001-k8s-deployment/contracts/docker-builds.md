# Docker Build Contracts

**Feature**: Local Kubernetes Deployment
**Date**: 2026-01-30
**Purpose**: Define Docker image build specifications, requirements, and validation criteria

## Overview

This document specifies the contract for building Docker images for the Phase III Todo Chatbot frontend (Next.js) and backend (FastAPI) applications.

## Frontend Image Contract

### Image Metadata

```yaml
name: todo-frontend
tag: v1.0.0
registry: local (Minikube) or docker.io/username
baseImage: node:18-alpine (build stage), nginx:alpine or node:18-alpine (runtime stage)
targetSize: <300MB
buildTime: <3 minutes
```

### Multi-Stage Build Structure

**Stage 1: Builder**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
```

**Stage 2: Runtime (Option A - Nginx for static export)**
```dockerfile
FROM nginx:alpine
COPY --from=builder /app/out /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

**Stage 2: Runtime (Option B - Node.js for SSR)**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

### Build Arguments

```yaml
NODE_ENV: production
NEXT_PUBLIC_API_URL: http://backend-service:8000 (injected at runtime via ConfigMap)
```

### Required Files

- `package.json`: Node.js dependencies
- `package-lock.json`: Locked dependency versions
- `next.config.js`: Next.js configuration
- `tsconfig.json`: TypeScript configuration
- `.dockerignore`: Exclude node_modules, .git, .next
- `nginx.conf`: Nginx configuration (if using nginx runtime)

### Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1
```

### Security Requirements

- MUST run as non-root user (UID 1000 or `node` user)
- MUST NOT include secrets or API keys
- MUST use multi-stage build to minimize attack surface
- SHOULD use alpine base images for smaller size
- MUST define `.dockerignore` to exclude sensitive files

### Validation Criteria

```bash
# Build image
docker build -t todo-frontend:v1.0.0 -f docker/frontend.Dockerfile ../phase3/frontend

# Verify size
docker images todo-frontend:v1.0.0 | awk '{print $7}' # Should be <300MB

# Verify no secrets
docker history todo-frontend:v1.0.0 --no-trunc | grep -i "secret\|api_key\|password"

# Test locally
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 todo-frontend:v1.0.0

# Verify health endpoint
curl http://localhost:3000/health # Should return 200 OK
```

### Expected Outputs

- Docker image: `todo-frontend:v1.0.0`
- Image size: ~250-300MB (nginx) or ~350-400MB (node)
- Exposed port: 3000
- Health endpoint: `/health` (returns 200 OK)

---

## Backend Image Contract

### Image Metadata

```yaml
name: todo-backend
tag: v1.0.0
registry: local (Minikube) or docker.io/username
baseImage: python:3.11-slim (build stage), python:3.11-slim (runtime stage)
targetSize: <200MB
buildTime: <2 minutes
```

### Multi-Stage Build Structure

**Stage 1: Builder**
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
```

**Stage 2: Runtime**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER nobody
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build Arguments

```yaml
PYTHON_VERSION: 3.11
WORKERS: 1 (for development, 4 for production)
```

### Required Files

- `requirements.txt`: Python dependencies
- `src/main.py`: FastAPI application entry point
- `src/`: Application source code
- `.dockerignore`: Exclude __pycache__, .pytest_cache, .env

### Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health').raise_for_status()" || exit 1
```

### Security Requirements

- MUST run as non-root user (`nobody` or UID 65534)
- MUST NOT include .env file or secrets
- MUST use multi-stage build to exclude build dependencies
- SHOULD use slim base images for smaller size
- MUST define `.dockerignore` to exclude sensitive files

### Validation Criteria

```bash
# Build image
docker build -t todo-backend:v1.0.0 -f docker/backend.Dockerfile ../phase3/backend

# Verify size
docker images todo-backend:v1.0.0 | awk '{print $7}' # Should be <200MB

# Verify no secrets
docker history todo-backend:v1.0.0 --no-trunc | grep -i "secret\|api_key\|password"

# Test locally
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./todo.db \
  -e JWT_SECRET=test-secret \
  -e OPENAI_API_KEY=sk-test \
  todo-backend:v1.0.0

# Verify health endpoint
curl http://localhost:8000/health # Should return 200 OK
```

### Expected Outputs

- Docker image: `todo-backend:v1.0.0`
- Image size: ~150-200MB
- Exposed port: 8000
- Health endpoint: `/health` (returns 200 OK)
- API docs: `/docs` (FastAPI Swagger UI)

---

## AI Tool Integration

### Gordon (Docker AI) Commands

```bash
# Frontend Dockerfile generation
docker ai "Generate optimized multi-stage Dockerfile for Next.js 16 app with nginx runtime, expose port 3000, run as non-root"

# Backend Dockerfile generation
docker ai "Generate optimized multi-stage Dockerfile for FastAPI app with Python 3.11 slim, expose port 8000, run as nobody user"

# Image optimization
docker ai "Analyze todo-frontend:v1.0.0 image and suggest optimizations for size and security"
```

### Fallback (Claude Code)

If Gordon is unavailable, use Claude Code to generate Dockerfiles following the contracts above. Store generated files in `phase4/docker/` directory.

---

## Build Automation Script

```bash
#!/bin/bash
# scripts/build-images.sh

set -e

echo "Building frontend image..."
docker build -t todo-frontend:v1.0.0 \
  -f docker/frontend.Dockerfile \
  ../phase3/frontend

echo "Building backend image..."
docker build -t todo-backend:v1.0.0 \
  -f docker/backend.Dockerfile \
  ../phase3/backend

echo "Tagging images for Minikube..."
minikube image load todo-frontend:v1.0.0
minikube image load todo-backend:v1.0.0

echo "✅ Images built and loaded into Minikube"
docker images | grep todo-
```

---

## Image Registry Strategy

### Local Development (Minikube)

```bash
# Option 1: Load images directly into Minikube
minikube image load todo-frontend:v1.0.0
minikube image load todo-backend:v1.0.0

# Option 2: Use Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t todo-frontend:v1.0.0 -f docker/frontend.Dockerfile ../phase3/frontend
```

### Future: Docker Hub (Optional)

```bash
# Tag for Docker Hub
docker tag todo-frontend:v1.0.0 username/todo-frontend:v1.0.0
docker tag todo-backend:v1.0.0 username/todo-backend:v1.0.0

# Push to registry
docker push username/todo-frontend:v1.0.0
docker push username/todo-backend:v1.0.0
```

---

## Validation Checklist

- [ ] Dockerfiles generated via AI tools (Gordon or Claude Code)
- [ ] Multi-stage builds implemented for both images
- [ ] Image sizes meet targets (<300MB frontend, <200MB backend)
- [ ] Health check endpoints defined and tested
- [ ] No secrets found in docker history
- [ ] Containers run as non-root users
- [ ] .dockerignore files exclude sensitive data
- [ ] Images build successfully within time limits
- [ ] Images run locally and serve traffic
- [ ] Images loaded into Minikube successfully

---

## Troubleshooting

### Issue: Image too large

**Solution**: Enable Docker BuildKit for better caching and layer optimization

```bash
export DOCKER_BUILDKIT=1
docker build --no-cache -t todo-frontend:v1.0.0 -f docker/frontend.Dockerfile ../phase3/frontend
```

### Issue: Build fails on Windows

**Solution**: Ensure line endings are LF (not CRLF) in scripts and Dockerfiles

```bash
git config --global core.autocrlf input
```

### Issue: Cannot load image into Minikube

**Solution**: Verify Minikube is running and use correct command

```bash
minikube status
minikube image ls | grep todo # Verify images loaded
```

---

## Notes

- AI-generated Dockerfiles MUST be reviewed for security before use
- All build commands MUST be logged in `scripts/ai-commands.log`
- Version tags SHOULD follow semantic versioning (v1.0.0, v1.1.0, etc.)
- Production builds SHOULD use specific base image tags (not `latest`)
- Build process MUST be reproducible across different machines

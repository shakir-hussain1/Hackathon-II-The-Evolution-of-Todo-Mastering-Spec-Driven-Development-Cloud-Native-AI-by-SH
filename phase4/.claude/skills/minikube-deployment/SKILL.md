---
name: Minikube Deployment
description: Deploys containerized apps to local Kubernetes using Minikube.
version: 1.0
---

## When to Use
Use when deploying frontend and backend on Minikube cluster.

## Process
1. Start Minikube
2. Load Docker images
3. Create deployment files
4. Create service files
5. Apply configs
6. Verify pods
7. Expose services

## Output Format
- Deployment YAML
- Service YAML
- kubectl commands
- Access URL

## Example

### Input
Backend Docker image

### Output
```bash
kubectl apply -f backend.yaml
minikube service backend
```

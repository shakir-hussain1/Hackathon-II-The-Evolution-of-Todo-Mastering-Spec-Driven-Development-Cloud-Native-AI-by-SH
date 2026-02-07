# Helm Values Contract

**Feature**: Local Kubernetes Deployment
**Date**: 2026-01-30
**Purpose**: Define Helm chart values.yaml schema and configuration parameters

## Umbrella Chart Values (todo-app/values.yaml)

```yaml
global:
  namespace: default
  imagePullPolicy: IfNotPresent
  nodeSelector: {}
  tolerations: []
  affinity: {}

frontend:
  enabled: true
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: v1.0.0
  service:
    type: NodePort
    port: 80
    targetPort: 3000
    nodePort: 30080
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi
  config:
    apiUrl: "http://backend-service:8000"
    nodeEnv: production

backend:
  enabled: true
  replicaCount: 2
  image:
    repository: todo-backend
    tag: v1.0.0
  service:
    type: ClusterIP
    port: 8000
    targetPort: 8000
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 1000m
      memory: 512Mi
  secrets:
    jwtSecret: "your-jwt-secret-here"  # Override via --set
    openaiApiKey: "your-openai-key"     # Override via --set
  config:
    databaseUrl: "sqlite:///./todo.db"
    logLevel: info
```

## Validation Rules

- All image tags MUST be specified (no `latest`)
- Resource requests MUST be <= limits
- Service nodePort MUST be in range 30000-32767
- Secrets MUST be overridden at install time (not committed)

## Usage

```bash
# Install with default values
helm install todo-app ./helm/todo-app

# Override values
helm install todo-app ./helm/todo-app \
  --set backend.secrets.jwtSecret=my-secret \
  --set backend.secrets.openaiApiKey=sk-xxx \
  --set frontend.replicaCount=3

# Use values file
helm install todo-app ./helm/todo-app -f custom-values.yaml
```

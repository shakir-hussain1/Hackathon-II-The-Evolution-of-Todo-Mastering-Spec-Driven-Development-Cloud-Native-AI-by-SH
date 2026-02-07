# Kubernetes Resource Specifications

**Feature**: Local Kubernetes Deployment
**Date**: 2026-01-30
**Purpose**: Define required Kubernetes resources, labels, and annotations

## Required Labels (All Resources)

```yaml
metadata:
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/instance: <release-name>
    app.kubernetes.io/version: v1.0.0
    app.kubernetes.io/component: <frontend|backend>
    app.kubernetes.io/part-of: todo-app
    app.kubernetes.io/managed-by: Helm
```

## Deployment Specifications

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-app
      app.kubernetes.io/component: frontend
  template:
    spec:
      containers:
      - name: frontend
        image: todo-frontend:v1.0.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
        envFrom:
        - configMapRef:
            name: frontend-config
```

## Service Specifications

Frontend (NodePort):
```yaml
apiVersion: v1
kind: Service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 3000
    nodePort: 30080
```

Backend (ClusterIP):
```yaml
apiVersion: v1
kind: Service
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
```

## Health Probes

All pods MUST define:
- Liveness probe: Restarts pod if unhealthy
- Readiness probe: Removes from service if not ready
- HTTP GET to `/health` endpoint
- initialDelaySeconds: 30s (liveness), 10s (readiness)

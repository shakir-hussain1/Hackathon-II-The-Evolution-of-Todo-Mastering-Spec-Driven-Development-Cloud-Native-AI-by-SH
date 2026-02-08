---
name: cloud-deployment
description: Deploy Todo Chatbot to production cloud Kubernetes clusters with ingress and HTTPS
version: 1.0.0
category: deployment
tags: [kubernetes, cloud, production, helm, ingress, tls, https]
---

# Cloud-Deployment Skill

## Purpose
Deploy the Todo Chatbot application (frontend + backend) to production cloud Kubernetes clusters with proper ingress configuration, HTTPS/TLS certificates, and production-ready security settings.

## When to Use This Skill

Use this skill when you need to:
- Deploy the Todo Chatbot to a production cloud environment (DigitalOcean, AWS, GCP, Azure)
- Set up Kubernetes clusters for production workloads
- Configure ingress controllers and load balancers
- Enable HTTPS with TLS/SSL certificates (Let's Encrypt)
- Configure production environment variables and secrets
- Implement security best practices for cloud deployments
- Set up monitoring and logging for production systems

## Prerequisites

Before using this skill, ensure you have:
- [ ] Completed Phases 1-4 (Docker images built and tested locally)
- [ ] Cloud provider account (DigitalOcean, AWS EKS, GCP GKE, or Azure AKS)
- [ ] `kubectl` installed and configured
- [ ] `helm` installed (v3+)
- [ ] Domain name for the application (optional but recommended)
- [ ] Docker images pushed to a container registry (Docker Hub, ECR, GCR)

## Step-by-Step Cloud Deployment Process

### 1. Cloud Kubernetes Cluster Setup

#### Option A: DigitalOcean Kubernetes (DOKS)
```bash
# Install doctl CLI
# Create cluster
doctl kubernetes cluster create todo-chatbot-prod \
  --region nyc1 \
  --version 1.28.2-do.0 \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=3;auto-scale=true;min-nodes=2;max-nodes=5"

# Get kubeconfig
doctl kubernetes cluster kubeconfig save todo-chatbot-prod
```

#### Option B: AWS EKS
```bash
# Install eksctl
eksctl create cluster \
  --name todo-chatbot-prod \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed

# Update kubeconfig
aws eks update-kubeconfig --name todo-chatbot-prod --region us-east-1
```

#### Option C: GCP GKE
```bash
# Create cluster
gcloud container clusters create todo-chatbot-prod \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 5

# Get credentials
gcloud container clusters get-credentials todo-chatbot-prod --zone us-central1-a
```

### 2. Install Ingress Controller (NGINX)

```bash
# Add NGINX ingress Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX ingress controller
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.metrics.enabled=true

# Wait for external IP
kubectl get svc -n ingress-nginx -w
```

### 3. Install cert-manager (for TLS/HTTPS)

```bash
# Add cert-manager Helm repo
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.crds.yaml

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0

# Verify installation
kubectl get pods -n cert-manager
```

### 4. Configure Let's Encrypt ClusterIssuer

```yaml
# letsencrypt-prod.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

```bash
# Apply the ClusterIssuer
kubectl apply -f letsencrypt-prod.yaml
```

### 5. Push Docker Images to Registry

```bash
# Tag images for registry
docker tag todo-backend:latest your-registry/todo-backend:v1.0.0
docker tag todo-frontend:latest your-registry/todo-frontend:v1.0.0

# Push to registry
docker push your-registry/todo-backend:v1.0.0
docker push your-registry/todo-frontend:v1.0.0
```

### 6. Create Production Secrets

```bash
# Create namespace
kubectl create namespace todo-production

# Create database secret
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_PASSWORD='your-secure-password' \
  --namespace todo-production

# Create backend secrets
kubectl create secret generic backend-secret \
  --from-literal=DATABASE_URL='postgresql://postgres:password@postgres:5432/todo_db' \
  --from-literal=JWT_SECRET='your-jwt-secret-key' \
  --namespace todo-production

# Create frontend secrets (if needed)
kubectl create secret generic frontend-secret \
  --from-literal=REACT_APP_API_URL='https://api.yourdomain.com' \
  --namespace todo-production
```

### 7. Deploy with Helm

Create or update Helm values for production:

```yaml
# production-values.yaml
global:
  environment: production
  domain: yourdomain.com

backend:
  image:
    repository: your-registry/todo-backend
    tag: v1.0.0
    pullPolicy: Always

  replicas: 3

  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"

  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

  envFrom:
    - secretRef:
        name: backend-secret

  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
      nginx.ingress.kubernetes.io/ssl-redirect: "true"
    hosts:
      - host: api.yourdomain.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: backend-tls-cert
        hosts:
          - api.yourdomain.com

frontend:
  image:
    repository: your-registry/todo-frontend
    tag: v1.0.0
    pullPolicy: Always

  replicas: 3

  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "250m"

  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
      nginx.ingress.kubernetes.io/ssl-redirect: "true"
    hosts:
      - host: yourdomain.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: frontend-tls-cert
        hosts:
          - yourdomain.com

postgresql:
  enabled: true
  auth:
    existingSecret: postgres-secret
    secretKeys:
      adminPasswordKey: POSTGRES_PASSWORD
  primary:
    persistence:
      enabled: true
      size: 10Gi
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

Deploy the application:

```bash
# Install/upgrade with Helm
helm upgrade --install todo-chatbot ./helm/todo-chatbot \
  --namespace todo-production \
  --create-namespace \
  --values production-values.yaml \
  --wait \
  --timeout 10m
```

### 8. Configure DNS

Point your domain to the ingress controller's external IP:

```bash
# Get external IP
kubectl get svc -n ingress-nginx

# Create DNS A records:
# yourdomain.com -> <EXTERNAL-IP>
# api.yourdomain.com -> <EXTERNAL-IP>
```

### 9. Verify TLS Certificates

```bash
# Check certificate status
kubectl get certificate -n todo-production
kubectl describe certificate frontend-tls-cert -n todo-production
kubectl describe certificate backend-tls-cert -n todo-production

# Check certificate issuance
kubectl get certificaterequest -n todo-production
```

## Security Best Practices

### 1. Network Policies
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: todo-production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432
```

### 2. Pod Security Standards
```yaml
# Apply restricted pod security
kubectl label namespace todo-production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

### 3. Resource Quotas
```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: todo-production-quota
  namespace: todo-production
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
    persistentvolumeclaims: "5"
```

### 4. RBAC Configuration
```yaml
# rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-app
  namespace: todo-production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: todo-app-role
  namespace: todo-production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: todo-app-rolebinding
  namespace: todo-production
subjects:
- kind: ServiceAccount
  name: todo-app
  namespace: todo-production
roleRef:
  kind: Role
  name: todo-app-role
  apiGroup: rbac.authorization.k8s.io
```

## Production Environment Variables

### Backend Environment Variables
```bash
# Required
DATABASE_URL=postgresql://postgres:password@postgres:5432/todo_db
JWT_SECRET=your-jwt-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional
ENVIRONMENT=production
LOG_LEVEL=info
CORS_ORIGINS=https://yourdomain.com
MAX_CONNECTIONS_COUNT=10
MIN_CONNECTIONS_COUNT=10
```

### Frontend Environment Variables
```bash
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

## Output Format

### Deployment Checklist

- [ ] **Pre-Deployment**
  - [ ] Docker images built and tested
  - [ ] Images pushed to container registry
  - [ ] Cloud provider account set up
  - [ ] Domain name configured (if using)
  - [ ] kubectl and helm installed

- [ ] **Cluster Setup**
  - [ ] Kubernetes cluster created
  - [ ] kubeconfig configured
  - [ ] Cluster accessible via kubectl

- [ ] **Ingress & TLS**
  - [ ] NGINX ingress controller installed
  - [ ] cert-manager installed
  - [ ] ClusterIssuer configured
  - [ ] DNS records created

- [ ] **Application Deployment**
  - [ ] Namespace created
  - [ ] Secrets created
  - [ ] Helm chart deployed
  - [ ] Pods running successfully

- [ ] **Security**
  - [ ] Network policies applied
  - [ ] Pod security standards enforced
  - [ ] Resource quotas set
  - [ ] RBAC configured

- [ ] **Verification**
  - [ ] TLS certificates issued
  - [ ] HTTPS working correctly
  - [ ] Application accessible
  - [ ] Database connected
  - [ ] Monitoring enabled

### Helm Values Template

See `production-values.yaml` above for complete template.

### Verification Commands

```bash
# 1. Check cluster status
kubectl cluster-info
kubectl get nodes

# 2. Check namespace and pods
kubectl get all -n todo-production
kubectl get pods -n todo-production -w

# 3. Check ingress
kubectl get ingress -n todo-production
kubectl describe ingress -n todo-production

# 4. Check certificates
kubectl get certificate -n todo-production
kubectl describe certificate -n todo-production

# 5. Check services
kubectl get svc -n todo-production

# 6. Check logs
kubectl logs -n todo-production -l app=backend --tail=50
kubectl logs -n todo-production -l app=frontend --tail=50

# 7. Test endpoints
curl -I https://yourdomain.com
curl -I https://api.yourdomain.com/health

# 8. Check resource usage
kubectl top nodes
kubectl top pods -n todo-production

# 9. Check autoscaling
kubectl get hpa -n todo-production

# 10. Check secrets
kubectl get secrets -n todo-production
```

## Example Usage

### Input
```bash
/cloud-deployment "Deploy backend and frontend to DigitalOcean with HTTPS"
```

### Output
```
✅ Cloud Deployment Started

1. Creating DigitalOcean Kubernetes cluster...
   - Cluster: todo-chatbot-prod
   - Region: nyc1
   - Nodes: 3 (s-2vcpu-4gb)

2. Installing ingress controller...
   - NGINX ingress installed
   - External IP: 142.93.123.45

3. Installing cert-manager...
   - cert-manager v1.13.0 installed
   - ClusterIssuer configured

4. Deploying application...
   - Namespace: todo-production
   - Backend replicas: 3
   - Frontend replicas: 3
   - Database: PostgreSQL (persistent)

5. Configuring ingress + TLS...
   - Frontend: https://yourdomain.com
   - Backend: https://api.yourdomain.com
   - Certificates: Let's Encrypt

6. Verification:
   ✅ All pods running
   ✅ TLS certificates issued
   ✅ HTTPS enabled
   ✅ Application accessible

🎉 Deployment complete!

Next steps:
1. Point DNS records to 142.93.123.45
2. Wait for TLS certificates (5-10 minutes)
3. Test: https://yourdomain.com
```

## Troubleshooting

### Common Issues

1. **Certificates not issuing**
   ```bash
   kubectl describe certificaterequest -n todo-production
   kubectl logs -n cert-manager -l app=cert-manager
   ```

2. **Pods not starting**
   ```bash
   kubectl describe pod <pod-name> -n todo-production
   kubectl logs <pod-name> -n todo-production
   ```

3. **Ingress not working**
   ```bash
   kubectl describe ingress -n todo-production
   kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
   ```

4. **Database connection errors**
   ```bash
   kubectl exec -it <backend-pod> -n todo-production -- env | grep DATABASE
   kubectl logs <postgres-pod> -n todo-production
   ```

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [NGINX Ingress Documentation](https://kubernetes.github.io/ingress-nginx/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

## Version History

- **v1.0.0** (2026-02-08): Initial release with DigitalOcean, AWS, GCP support

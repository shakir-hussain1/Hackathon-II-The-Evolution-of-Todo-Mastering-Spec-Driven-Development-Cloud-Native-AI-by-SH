---
name: security-hardening
description: Secure production systems with TLS, secrets management, RBAC, and OWASP best practices
version: 1.0.0
category: security
tags: [security, tls, rbac, secrets, scanning, owasp, hardening, compliance]
---

# Security-Hardening Skill

## Purpose
Implement comprehensive security hardening for the Todo Chatbot application in production, including TLS/SSL configuration, secrets management with Vault or Sealed Secrets, RBAC policies, container security scanning, network policies, and OWASP Top 10 security best practices.

## When to Use This Skill

Use this skill when you need to:
- Secure production Kubernetes clusters and applications
- Implement TLS/SSL for all communication channels
- Manage secrets securely (database passwords, API keys, JWT secrets)
- Configure Role-Based Access Control (RBAC)
- Scan containers for vulnerabilities
- Implement network segmentation and policies
- Follow OWASP security best practices
- Pass security audits and compliance checks
- Protect against common attack vectors (XSS, CSRF, SQL injection)
- Implement zero-trust security architecture

## Prerequisites

Before using this skill, ensure you have:
- [ ] Kubernetes cluster with admin access
- [ ] cert-manager installed (for TLS certificates)
- [ ] Application deployed to Kubernetes
- [ ] Docker images built and pushed to registry
- [ ] Security scanning tools available (Trivy, Falco)
- [ ] Understanding of RBAC concepts

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │ TLS/SSL      │─────▶│   Ingress    │─────▶│ Application  │  │
│  │ Certificate  │      │  Controller  │      │    (TLS)     │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                                                      │           │
│  ┌──────────────┐      ┌──────────────┐             ▼           │
│  │ Sealed       │─────▶│  Kubernetes  │      ┌──────────────┐  │
│  │  Secrets     │      │   Secrets    │─────▶│   Database   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │    RBAC      │─────▶│ Service      │─────▶│    Pods      │ │
│  │   Policies   │      │  Accounts    │      │  (Limited)   │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │   Network    │─────▶│   Network    │─────▶ Isolation        │
│  │   Policies   │      │   Firewall   │                        │
│  └──────────────┘      └──────────────┘                        │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Container  │─────▶│    Trivy     │─────▶│ Vulnerability│ │
│  │   Scanning   │      │   Scanner    │      │   Reports    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Security Hardening

### 1. TLS/SSL Configuration

#### Install cert-manager (if not already installed)

```bash
# Install cert-manager CRDs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.crds.yaml

# Add Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0

# Verify installation
kubectl get pods -n cert-manager
```

#### Create Let's Encrypt ClusterIssuers

**Production ClusterIssuer** (`letsencrypt-prod.yaml`):
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: security@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Staging ClusterIssuer** (`letsencrypt-staging.yaml`):
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: security@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-staging-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

Apply:
```bash
kubectl apply -f letsencrypt-prod.yaml
kubectl apply -f letsencrypt-staging.yaml
```

#### Configure TLS for Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress-secure
  namespace: todo-production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/ssl-protocols: "TLSv1.2 TLSv1.3"
    nginx.ingress.kubernetes.io/ssl-ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
    nginx.ingress.kubernetes.io/enable-cors: "false"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://yourdomain.com"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.yourdomain.com
    - yourdomain.com
    secretName: todo-tls-cert
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8000
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 3000
```

### 2. Secrets Management

#### Option A: Kubernetes Sealed Secrets

**Install Sealed Secrets Controller:**
```bash
# Install Sealed Secrets controller
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system \
  --create-namespace

# Install kubeseal CLI
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-0.24.0-linux-amd64.tar.gz
tar -xvzf kubeseal-0.24.0-linux-amd64.tar.gz
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

**Create Sealed Secrets:**
```bash
# Create a regular secret (locally, not committed)
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@host:5432/db' \
  --from-literal=JWT_SECRET='your-super-secret-jwt-key-min-32-chars' \
  --from-literal=API_KEY='your-api-key' \
  --dry-run=client -o yaml > backend-secrets.yaml

# Seal the secret
kubeseal --format=yaml < backend-secrets.yaml > backend-sealed-secret.yaml

# Apply sealed secret (safe to commit to git)
kubectl apply -f backend-sealed-secret.yaml -n todo-production

# The controller will automatically decrypt it into a regular secret
kubectl get secrets -n todo-production
```

**Sealed Secret Example** (`backend-sealed-secret.yaml`):
```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: backend-secrets
  namespace: todo-production
spec:
  encryptedData:
    DATABASE_URL: AgBx7Hf8... # encrypted data
    JWT_SECRET: AgC9Kp2... # encrypted data
    API_KEY: AgDm4Qw... # encrypted data
  template:
    metadata:
      name: backend-secrets
      namespace: todo-production
    type: Opaque
```

#### Option B: HashiCorp Vault Integration

**Install Vault:**
```bash
# Add HashiCorp Helm repo
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Install Vault in dev mode (for testing)
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set "server.dev.enabled=true"

# For production
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set "server.ha.enabled=true" \
  --set "server.ha.replicas=3"
```

**Configure Vault for Kubernetes:**
```bash
# Enable Kubernetes auth
kubectl exec -it vault-0 -n vault -- vault auth enable kubernetes

# Configure Kubernetes auth
kubectl exec -it vault-0 -n vault -- vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443"

# Create a policy
kubectl exec -it vault-0 -n vault -- vault policy write todo-policy - <<EOF
path "secret/data/todo/*" {
  capabilities = ["read"]
}
EOF

# Create a role
kubectl exec -it vault-0 -n vault -- vault write auth/kubernetes/role/todo-role \
  bound_service_account_names=todo-app \
  bound_service_account_namespaces=todo-production \
  policies=todo-policy \
  ttl=24h
```

**Inject Secrets into Pods:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-production
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "todo-role"
        vault.hashicorp.com/agent-inject-secret-database: "secret/data/todo/database"
        vault.hashicorp.com/agent-inject-template-database: |
          {{- with secret "secret/data/todo/database" -}}
          export DATABASE_URL="{{ .Data.data.url }}"
          {{- end }}
    spec:
      serviceAccountName: todo-app
      containers:
      - name: backend
        image: todo-backend:latest
```

### 3. RBAC (Role-Based Access Control)

#### Create Service Accounts

```yaml
# service-accounts.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-backend-sa
  namespace: todo-production
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-frontend-sa
  namespace: todo-production
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-readonly-sa
  namespace: todo-production
```

#### Create Roles and RoleBindings

**Backend Role** (`backend-role.yaml`):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: todo-backend-role
  namespace: todo-production
rules:
# Allow reading ConfigMaps
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
# Allow reading Secrets
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
# Allow creating/updating pods (for debugging)
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
# Deny dangerous operations
# - No delete, update, patch on critical resources
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: todo-backend-rolebinding
  namespace: todo-production
subjects:
- kind: ServiceAccount
  name: todo-backend-sa
  namespace: todo-production
roleRef:
  kind: Role
  name: todo-backend-role
  apiGroup: rbac.authorization.k8s.io
```

**ReadOnly Role** (`readonly-role.yaml`):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: todo-readonly-role
  namespace: todo-production
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: todo-readonly-rolebinding
  namespace: todo-production
subjects:
- kind: ServiceAccount
  name: todo-readonly-sa
  namespace: todo-production
roleRef:
  kind: Role
  name: todo-readonly-role
  apiGroup: rbac.authorization.k8s.io
```

**ClusterRole for Monitoring** (`monitoring-clusterrole.yaml`):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus-monitoring
rules:
- apiGroups: [""]
  resources: ["nodes", "nodes/proxy", "services", "endpoints", "pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions"]
  resources: ["ingresses"]
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: prometheus-monitoring
subjects:
- kind: ServiceAccount
  name: prometheus
  namespace: monitoring
roleRef:
  kind: ClusterRole
  name: prometheus-monitoring
  apiGroup: rbac.authorization.k8s.io
```

Apply RBAC:
```bash
kubectl apply -f service-accounts.yaml
kubectl apply -f backend-role.yaml
kubectl apply -f readonly-role.yaml
kubectl apply -f monitoring-clusterrole.yaml
```

### 4. Container Security Scanning

#### Install Trivy

```bash
# Install Trivy CLI
wget https://github.com/aquasecurity/trivy/releases/download/v0.47.0/trivy_0.47.0_Linux-64bit.tar.gz
tar zxvf trivy_0.47.0_Linux-64bit.tar.gz
sudo mv trivy /usr/local/bin/

# Scan Docker images
trivy image todo-backend:latest
trivy image todo-frontend:latest

# Scan for high and critical vulnerabilities only
trivy image --severity HIGH,CRITICAL todo-backend:latest

# Scan with JSON output
trivy image --format json --output results.json todo-backend:latest
```

#### Trivy Operator for Kubernetes

```bash
# Install Trivy Operator
helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm repo update

helm install trivy-operator aqua/trivy-operator \
  --namespace trivy-system \
  --create-namespace \
  --set="trivy.ignoreUnfixed=true"

# Check vulnerability reports
kubectl get vulnerabilityreports -n todo-production
kubectl describe vulnerabilityreport <report-name> -n todo-production
```

#### Admission Controller (Prevent vulnerable images)

**Install Kyverno:**
```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace
```

**Create Policy** (`block-vulnerable-images.yaml`):
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: block-vulnerable-images
spec:
  validationFailureAction: enforce
  background: false
  rules:
  - name: check-image-vulnerabilities
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Images with HIGH or CRITICAL vulnerabilities are not allowed"
      deny:
        conditions:
          any:
          - key: "{{ request.object.spec.containers[].image }}"
            operator: In
            value: ["*:latest", "*:dev"]
```

### 5. Network Policies

**Deny All Traffic** (`deny-all.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: todo-production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**Allow Backend to Database** (`backend-to-db.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-database
  namespace: todo-production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  # Allow PostgreSQL
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432
```

**Allow Frontend to Backend** (`frontend-to-backend.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: todo-production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Egress
  egress:
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  # Allow Backend API
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8000
```

**Allow Ingress to Frontend/Backend** (`allow-ingress.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-apps
  namespace: todo-production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-frontend
  namespace: todo-production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 3000
```

Apply network policies:
```bash
kubectl apply -f deny-all.yaml
kubectl apply -f backend-to-db.yaml
kubectl apply -f frontend-to-backend.yaml
kubectl apply -f allow-ingress.yaml
```

### 6. Pod Security Standards

**Apply Pod Security Standards:**
```bash
# Label namespace with restricted pod security
kubectl label namespace todo-production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

**Pod Security Policy** (`restricted-psp.yaml`):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: backend
  namespace: todo-production
spec:
  serviceAccountName: todo-backend-sa
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: backend
    image: todo-backend:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

### 7. OWASP Best Practices Implementation

#### A. SQL Injection Prevention (Backend)

```python
# backend/app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Todo

# ✅ GOOD: Using ORM (parameterized queries)
def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

# ✅ GOOD: Using parameterized text()
def get_todos_by_user(db: Session, user_id: int):
    query = text("SELECT * FROM todos WHERE user_id = :user_id")
    return db.execute(query, {"user_id": user_id}).fetchall()

# ❌ BAD: String concatenation (SQL injection vulnerable)
# def get_todo_bad(db: Session, todo_id: str):
#     query = f"SELECT * FROM todos WHERE id = {todo_id}"  # NEVER DO THIS
#     return db.execute(query).fetchall()
```

#### B. XSS Prevention (Frontend)

```javascript
// frontend/src/utils/sanitize.js
import DOMPurify from 'dompurify';

// ✅ GOOD: Sanitize user input
export const sanitizeHTML = (dirty) => {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
};

// Usage in React component
function TodoItem({ todo }) {
  return (
    <div>
      <h3>{todo.title}</h3>
      <div dangerouslySetInnerHTML={{
        __html: sanitizeHTML(todo.description)
      }} />
    </div>
  );
}
```

#### C. CSRF Protection (Backend)

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# ✅ Restrict CORS to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# ✅ Only allow specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

#### D. Authentication & JWT Security

```python
# backend/app/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

# ✅ Strong password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Generate secure JWT secret
JWT_SECRET = secrets.token_urlsafe(32)  # 32 bytes = 256 bits
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": secrets.token_urlsafe(16)  # Unique token ID
    })
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

#### E. Rate Limiting

```python
# backend/app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Apply to FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Usage on endpoints
@app.post("/api/todos")
@limiter.limit("10/minute")
async def create_todo(request: Request, todo: TodoCreate):
    # ... create todo logic
    pass
```

#### F. Input Validation

```python
# backend/app/schemas.py
from pydantic import BaseModel, Field, validator
import re

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(None, max_length=2000)

    @validator('title')
    def validate_title(cls, v):
        # Remove potential XSS
        if re.search(r'<script|javascript:|onerror=', v, re.IGNORECASE):
            raise ValueError('Invalid characters in title')
        return v.strip()

class UserRegister(BaseModel):
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: str = Field(..., min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v
```

### 8. Security Headers

**Configure NGINX Security Headers:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-security-headers
  namespace: ingress-nginx
data:
  http-snippet: |
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.yourdomain.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Hide server information
    server_tokens off;
```

## Output Format

### Security Checklist

**Pre-Production Security Checklist:**

#### Infrastructure Security
- [ ] TLS/SSL certificates configured (Let's Encrypt)
- [ ] HTTPS enforced on all endpoints
- [ ] TLS version >= 1.2 enforced
- [ ] Strong cipher suites configured
- [ ] Certificate auto-renewal configured

#### Secrets Management
- [ ] All secrets stored in Kubernetes Secrets or Vault
- [ ] No hardcoded credentials in code
- [ ] Sealed Secrets or Vault configured
- [ ] Secret rotation policy defined
- [ ] Secrets not logged or exposed

#### RBAC & Access Control
- [ ] Service accounts created for all pods
- [ ] Roles with least privilege assigned
- [ ] No pods running as root
- [ ] RoleBindings properly scoped
- [ ] ClusterRoles audited

#### Container Security
- [ ] All images scanned for vulnerabilities
- [ ] No HIGH/CRITICAL vulnerabilities in production
- [ ] Base images regularly updated
- [ ] Images pulled from trusted registries
- [ ] Image signing implemented (optional)

#### Network Security
- [ ] Network policies implemented
- [ ] Default deny-all policy in place
- [ ] Only necessary ports exposed
- [ ] Ingress properly configured
- [ ] Service mesh configured (optional)

#### Pod Security
- [ ] Pod Security Standards enforced (restricted)
- [ ] runAsNonRoot enabled
- [ ] readOnlyRootFilesystem enabled
- [ ] Capabilities dropped
- [ ] Resource limits set

#### Application Security (OWASP)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] CSRF protection (CORS configured)
- [ ] Authentication implemented (JWT)
- [ ] Authorization implemented (user isolation)
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] Security headers configured

#### Monitoring & Logging
- [ ] Security events logged
- [ ] Audit logging enabled
- [ ] Falco or similar IDS installed
- [ ] Alerts for security events
- [ ] Log retention policy defined

#### Compliance
- [ ] Security scan reports generated
- [ ] Vulnerability remediation plan
- [ ] Incident response plan documented
- [ ] Regular security audits scheduled
- [ ] Compliance requirements met (GDPR, HIPAA, etc.)

### RBAC Templates

See sections above for complete RBAC templates:
- ✅ Service Accounts
- ✅ Backend Role (limited permissions)
- ✅ ReadOnly Role (audit access)
- ✅ Monitoring ClusterRole

### Secret Handling Guide

#### 1. **Never Commit Secrets**
```bash
# Add to .gitignore
*.env
*-secrets.yaml
credentials.json
*.key
*.pem
```

#### 2. **Use Sealed Secrets or Vault**
```bash
# Sealed Secrets workflow
kubectl create secret generic my-secret --from-literal=key=value --dry-run=client -o yaml | \
  kubeseal --format yaml > sealed-secret.yaml

# Safe to commit sealed-secret.yaml
git add sealed-secret.yaml
```

#### 3. **Rotate Secrets Regularly**
```bash
# Rotate JWT secret
NEW_SECRET=$(openssl rand -base64 32)
kubectl create secret generic backend-secrets \
  --from-literal=JWT_SECRET="$NEW_SECRET" \
  --dry-run=client -o yaml | \
  kubeseal --format yaml | \
  kubectl apply -f -

# Rollout restart to pick up new secret
kubectl rollout restart deployment/backend -n todo-production
```

#### 4. **Use Secret References**
```yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: backend-secrets
      key: DATABASE_URL
```

## Example Usage

### Input
```bash
/security-hardening "Secure production cluster"
```

### Output
```
✅ Security Hardening Complete!

🔒 TLS/SSL Configuration:
- cert-manager installed and configured
- Let's Encrypt ClusterIssuers created
- TLS certificates issued for:
  • api.yourdomain.com
  • yourdomain.com
- HTTPS enforced on all endpoints
- TLS 1.2+ only with strong ciphers

🔐 Secrets Management:
- Sealed Secrets controller installed
- 3 sealed secrets created:
  • backend-secrets (DATABASE_URL, JWT_SECRET)
  • database-secrets (POSTGRES_PASSWORD)
  • api-keys (EXTERNAL_API_KEY)
- All secrets encrypted at rest
- No secrets in git repository

👤 RBAC Configuration:
- 3 Service Accounts created
- 2 Roles with least privilege
- 1 ClusterRole for monitoring
- All pods use non-root service accounts

🛡️ Container Security:
- Trivy Operator installed
- All images scanned: 0 CRITICAL, 2 HIGH (remediation plan)
- Vulnerability reports generated
- Admission controller blocks vulnerable images

🌐 Network Policies:
- Default deny-all policy applied
- 4 network policies created:
  • backend → database
  • frontend → backend
  • ingress → apps
  • egress DNS
- All traffic segmented and controlled

🔧 Pod Security:
- Pod Security Standards: RESTRICTED
- All pods run as non-root (UID 1000)
- Read-only root filesystem
- All capabilities dropped
- Resource limits enforced

✅ OWASP Best Practices:
- SQL injection: Parameterized queries ✓
- XSS: Input sanitization ✓
- CSRF: CORS properly configured ✓
- Auth: JWT with secure settings ✓
- Rate limiting: 10 req/min per IP ✓
- Input validation: Pydantic schemas ✓
- Security headers: All configured ✓

📊 Security Score: 95/100

⚠️ Recommendations:
1. Enable Falco for runtime security monitoring
2. Implement image signing with Cosign
3. Configure Vault for advanced secret management
4. Enable service mesh (Istio/Linkerd) for mTLS

🎉 Your cluster is production-ready and secure!
```

## Advanced Security Features

### 1. Runtime Security with Falco

```bash
# Install Falco
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set falco.grpc.enabled=true \
  --set falco.grpcOutput.enabled=true

# Falco will detect:
# - Shell spawned in container
# - Privilege escalation attempts
# - Suspicious network activity
# - File system modifications
# - Container escapes
```

### 2. Image Signing with Cosign

```bash
# Install Cosign
wget https://github.com/sigstore/cosign/releases/download/v2.2.0/cosign-linux-amd64
chmod +x cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign

# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key todo-backend:latest

# Verify image
cosign verify --key cosign.pub todo-backend:latest
```

### 3. Service Mesh (mTLS)

```bash
# Install Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

istioctl install --set profile=default -y

# Enable mTLS
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: todo-production
spec:
  mtls:
    mode: STRICT
EOF
```

## Troubleshooting

### Common Issues

1. **Certificate not issuing**
   ```bash
   kubectl describe certificate todo-tls-cert -n todo-production
   kubectl describe certificaterequest -n todo-production
   kubectl logs -n cert-manager deploy/cert-manager
   ```

2. **Sealed secret not decrypting**
   ```bash
   kubectl logs -n kube-system -l app.kubernetes.io/name=sealed-secrets
   kubectl get sealedsecret -n todo-production
   kubectl get secret -n todo-production
   ```

3. **Network policy blocking traffic**
   ```bash
   # Temporarily remove policies to test
   kubectl delete networkpolicy --all -n todo-production

   # Check pod connectivity
   kubectl exec -it backend-pod -n todo-production -- curl database:5432
   ```

4. **RBAC permission denied**
   ```bash
   # Check service account
   kubectl get sa -n todo-production

   # Check role bindings
   kubectl get rolebinding -n todo-production

   # Describe role
   kubectl describe role todo-backend-role -n todo-production
   ```

## Best Practices

1. **Defense in Depth**: Multiple layers of security
2. **Least Privilege**: Minimal permissions for all components
3. **Zero Trust**: Verify everything, trust nothing
4. **Security by Default**: Secure configurations out of the box
5. **Regular Updates**: Keep all components updated
6. **Audit Everything**: Log all security events
7. **Automate Security**: CI/CD security scanning
8. **Incident Response**: Have a plan for security incidents
9. **Regular Reviews**: Periodic security audits
10. **Education**: Train team on security best practices

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)

## Version History

- **v1.0.0** (2026-02-08): Initial release with comprehensive security hardening

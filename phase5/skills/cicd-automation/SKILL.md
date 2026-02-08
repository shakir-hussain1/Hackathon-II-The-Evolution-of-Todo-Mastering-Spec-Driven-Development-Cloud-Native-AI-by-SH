---
name: cicd-automation
description: Automate testing, building, and deployment pipelines with GitHub Actions
version: 1.0.0
category: automation
tags: [cicd, github-actions, docker, kubernetes, automation, deployment, testing]
---

# CICD-Automation Skill

## Purpose
Automate the complete software delivery pipeline for the Todo Chatbot application, including automated testing, Docker image building, container registry pushes, and Kubernetes deployment with rollback capabilities.

## When to Use This Skill

Use this skill when you need to:
- Set up automated CI/CD pipelines for continuous integration and deployment
- Automate testing on every push and pull request
- Build and push Docker images automatically
- Deploy to Kubernetes clusters automatically after successful builds
- Implement automatic rollback strategies for failed deployments
- Set up multi-environment deployments (dev, staging, production)
- Enforce code quality and security checks in the pipeline
- Automate version tagging and release management

## Prerequisites

Before using this skill, ensure you have:
- [ ] GitHub repository for the Todo Chatbot project
- [ ] Docker Hub or other container registry account
- [ ] Kubernetes cluster configured (for deployment automation)
- [ ] GitHub Secrets configured for sensitive data
- [ ] Helm charts ready for the application
- [ ] Tests written for backend and frontend

## GitHub Actions Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│  1. Trigger (push/PR) → Code Checkout                       │
│  2. Run Tests (Backend + Frontend)                          │
│  3. Code Quality & Security Scans                           │
│  4. Build Docker Images                                     │
│  5. Push to Container Registry                              │
│  6. Deploy to Kubernetes                                    │
│  7. Health Check & Verification                             │
│  8. Rollback on Failure                                     │
└─────────────────────────────────────────────────────────────┘
```

## Step-by-Step Pipeline Setup

### 1. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

```bash
# Docker Registry
DOCKER_USERNAME=your-docker-username
DOCKER_PASSWORD=your-docker-password

# Kubernetes Cluster
KUBECONFIG_DATA=<base64-encoded-kubeconfig>

# Container Registry (choose one)
# Docker Hub
DOCKER_REGISTRY=docker.io

# AWS ECR
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1

# GCP GCR
GCP_PROJECT_ID=your-project-id
GCP_SA_KEY=<base64-service-account-json>

# Application Secrets
JWT_SECRET=your-jwt-secret
DATABASE_URL=your-database-url

# Notification (optional)
SLACK_WEBHOOK_URL=your-slack-webhook
```

### 2. Main CI/CD Pipeline

Create `.github/workflows/main.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
    tags:
      - 'v*'
  pull_request:
    branches:
      - main
      - develop

env:
  DOCKER_REGISTRY: docker.io
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  BACKEND_IMAGE: ${{ secrets.DOCKER_USERNAME }}/todo-backend
  FRONTEND_IMAGE: ${{ secrets.DOCKER_USERNAME }}/todo-frontend

jobs:
  # ============================================
  # JOB 1: Test Backend
  # ============================================
  test-backend:
    name: Test Backend
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio httpx

      - name: Run tests
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql://postgres:test_password@localhost:5432/test_db
          JWT_SECRET: test-secret-key-min-32-characters
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend
          name: backend-coverage

  # ============================================
  # JOB 2: Test Frontend
  # ============================================
  test-frontend:
    name: Test Frontend
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: ./frontend/package-lock.json

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run linter
        working-directory: ./frontend
        run: npm run lint

      - name: Run tests
        working-directory: ./frontend
        run: npm test -- --coverage --watchAll=false

      - name: Build frontend
        working-directory: ./frontend
        env:
          REACT_APP_API_URL: http://localhost:8000
        run: npm run build

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json
          flags: frontend
          name: frontend-coverage

  # ============================================
  # JOB 3: Security Scanning
  # ============================================
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner (Backend)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: './backend'
          format: 'sarif'
          output: 'trivy-backend-results.sarif'

      - name: Run Trivy vulnerability scanner (Frontend)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: './frontend'
          format: 'sarif'
          output: 'trivy-frontend-results.sarif'

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-backend-results.sarif'

  # ============================================
  # JOB 4: Build and Push Docker Images
  # ============================================
  build-and-push:
    name: Build and Push Docker Images
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend, security-scan]
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v'))

    outputs:
      backend-tag: ${{ steps.meta-backend.outputs.tags }}
      frontend-tag: ${{ steps.meta-frontend.outputs.tags }}
      version: ${{ steps.meta-backend.outputs.version }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata (tags, labels) for Backend
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.BACKEND_IMAGE }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Backend image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.BACKEND_IMAGE }}:buildcache
          cache-to: type=registry,ref=${{ env.BACKEND_IMAGE }}:buildcache,mode=max

      - name: Extract metadata (tags, labels) for Frontend
        id: meta-frontend
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.FRONTEND_IMAGE }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Frontend image
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.FRONTEND_IMAGE }}:buildcache
          cache-to: type=registry,ref=${{ env.FRONTEND_IMAGE }}:buildcache,mode=max
          build-args: |
            REACT_APP_API_URL=${{ secrets.REACT_APP_API_URL || 'http://localhost:8000' }}

  # ============================================
  # JOB 5: Deploy to Kubernetes
  # ============================================
  deploy:
    name: Deploy to Kubernetes
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'

      - name: Install Helm
        uses: azure/setup-helm@v3
        with:
          version: 'v3.13.0'

      - name: Configure kubectl
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBECONFIG_DATA }}" | base64 --decode > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Verify cluster connection
        run: |
          kubectl cluster-info
          kubectl get nodes

      - name: Deploy with Helm
        run: |
          # Determine environment based on branch
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            ENVIRONMENT="production"
            NAMESPACE="todo-production"
          else
            ENVIRONMENT="staging"
            NAMESPACE="todo-staging"
          fi

          # Create namespace if it doesn't exist
          kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

          # Deploy with Helm
          helm upgrade --install todo-chatbot ./helm/todo-chatbot \
            --namespace $NAMESPACE \
            --set backend.image.tag=${{ needs.build-and-push.outputs.version }} \
            --set frontend.image.tag=${{ needs.build-and-push.outputs.version }} \
            --set global.environment=$ENVIRONMENT \
            --wait \
            --timeout 10m \
            --atomic \
            --cleanup-on-fail

      - name: Verify deployment
        run: |
          NAMESPACE="todo-production"
          if [[ "${{ github.ref }}" != "refs/heads/main" ]]; then
            NAMESPACE="todo-staging"
          fi

          # Wait for rollout
          kubectl rollout status deployment/backend -n $NAMESPACE --timeout=5m
          kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=5m

          # Check pod status
          kubectl get pods -n $NAMESPACE
          kubectl get svc -n $NAMESPACE
          kubectl get ingress -n $NAMESPACE

      - name: Run smoke tests
        run: |
          NAMESPACE="todo-production"
          if [[ "${{ github.ref }}" != "refs/heads/main" ]]; then
            NAMESPACE="todo-staging"
          fi

          # Get backend service endpoint
          BACKEND_URL=$(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[?(@.metadata.name=="backend")].spec.rules[0].host}')

          # Wait for ingress to be ready
          sleep 30

          # Test health endpoint
          curl -f https://${BACKEND_URL}/health || exit 1

          echo "✅ Smoke tests passed!"

  # ============================================
  # JOB 6: Rollback on Failure
  # ============================================
  rollback:
    name: Rollback on Failure
    runs-on: ubuntu-latest
    needs: deploy
    if: failure()

    steps:
      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'

      - name: Install Helm
        uses: azure/setup-helm@v3
        with:
          version: 'v3.13.0'

      - name: Configure kubectl
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBECONFIG_DATA }}" | base64 --decode > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Rollback deployment
        run: |
          NAMESPACE="todo-production"
          if [[ "${{ github.ref }}" != "refs/heads/main" ]]; then
            NAMESPACE="todo-staging"
          fi

          echo "🔄 Rolling back deployment..."
          helm rollback todo-chatbot -n $NAMESPACE

          # Verify rollback
          kubectl rollout status deployment/backend -n $NAMESPACE --timeout=5m
          kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=5m

          echo "✅ Rollback completed successfully!"

      - name: Notify team
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            🚨 Deployment Failed and Rolled Back
            Repository: ${{ github.repository }}
            Branch: ${{ github.ref }}
            Commit: ${{ github.sha }}
            Author: ${{ github.actor }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}

  # ============================================
  # JOB 7: Notify on Success
  # ============================================
  notify-success:
    name: Notify Success
    runs-on: ubuntu-latest
    needs: deploy
    if: success()

    steps:
      - name: Send success notification
        uses: 8398a7/action-slack@v3
        with:
          status: success
          text: |
            ✅ Deployment Successful!
            Repository: ${{ github.repository }}
            Branch: ${{ github.ref }}
            Commit: ${{ github.sha }}
            Author: ${{ github.actor }}
            Environment: ${{ github.ref == 'refs/heads/main' && 'Production' || 'Staging' }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 3. Pull Request Pipeline

Create `.github/workflows/pr-validation.yml`:

```yaml
name: PR Validation

on:
  pull_request:
    branches:
      - main
      - develop

jobs:
  validate:
    name: Validate PR
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check PR title format
        run: |
          PR_TITLE="${{ github.event.pull_request.title }}"
          if ! echo "$PR_TITLE" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
            echo "❌ PR title must follow conventional commits format"
            echo "Examples: feat: add login, fix(api): resolve bug"
            exit 1
          fi

      - name: Check for merge conflicts
        run: |
          git fetch origin main
          if ! git merge-tree $(git merge-base HEAD origin/main) HEAD origin/main | grep -q "^@@"; then
            echo "✅ No merge conflicts detected"
          else
            echo "❌ Merge conflicts detected"
            exit 1
          fi

      - name: Run all tests
        uses: ./.github/workflows/main.yml
        with:
          run-tests-only: true

  size-check:
    name: Check PR Size
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check PR size
        run: |
          FILES_CHANGED=$(git diff --name-only origin/main...HEAD | wc -l)
          LINES_CHANGED=$(git diff --stat origin/main...HEAD | tail -1 | awk '{print $4+$6}')

          echo "Files changed: $FILES_CHANGED"
          echo "Lines changed: $LINES_CHANGED"

          if [ $FILES_CHANGED -gt 50 ] || [ $LINES_CHANGED -gt 1000 ]; then
            echo "⚠️ Large PR detected. Consider splitting into smaller PRs."
            echo "::warning::Large PR - $FILES_CHANGED files, $LINES_CHANGED lines changed"
          fi
```

### 4. Release Automation

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  create-release:
    name: Create GitHub Release
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git describe --abbrev=0 --tags $(git rev-list --tags --skip=1 --max-count=1) 2>/dev/null || echo "")
          if [ -z "$PREVIOUS_TAG" ]; then
            COMMITS=$(git log --pretty=format:"- %s (%h)" ${{ github.ref_name }})
          else
            COMMITS=$(git log --pretty=format:"- %s (%h)" ${PREVIOUS_TAG}..${{ github.ref_name }})
          fi
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$COMMITS" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          body: |
            ## Changes in this Release
            ${{ steps.changelog.outputs.changelog }}

            ## Docker Images
            - Backend: `${{ secrets.DOCKER_USERNAME }}/todo-backend:${{ github.ref_name }}`
            - Frontend: `${{ secrets.DOCKER_USERNAME }}/todo-frontend:${{ github.ref_name }}`

            ## Deployment
            ```bash
            helm upgrade todo-chatbot ./helm/todo-chatbot \
              --set backend.image.tag=${{ github.ref_name }} \
              --set frontend.image.tag=${{ github.ref_name }}
            ```
          draft: false
          prerelease: false
```

## Rollback Strategy

### Automatic Rollback (Built into Pipeline)

The pipeline includes automatic rollback on deployment failure using Helm's `--atomic` flag:

```yaml
helm upgrade --install todo-chatbot ./helm/todo-chatbot \
  --atomic \
  --cleanup-on-fail
```

### Manual Rollback Commands

```bash
# 1. List release history
helm history todo-chatbot -n todo-production

# 2. Rollback to previous version
helm rollback todo-chatbot -n todo-production

# 3. Rollback to specific revision
helm rollback todo-chatbot 5 -n todo-production

# 4. Check rollback status
kubectl rollout status deployment/backend -n todo-production
kubectl rollout status deployment/frontend -n todo-production

# 5. Verify pods are running
kubectl get pods -n todo-production
```

### Kubernetes Native Rollback

```bash
# Rollback backend deployment
kubectl rollout undo deployment/backend -n todo-production

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=3 -n todo-production

# Check rollback history
kubectl rollout history deployment/backend -n todo-production

# Pause rollout (for emergency)
kubectl rollout pause deployment/backend -n todo-production

# Resume rollout
kubectl rollout resume deployment/backend -n todo-production
```

## Pipeline Validation Steps

### Pre-Deployment Validation

```yaml
- name: Pre-deployment validation
  run: |
    # 1. Validate Helm chart
    helm lint ./helm/todo-chatbot

    # 2. Dry-run deployment
    helm upgrade --install todo-chatbot ./helm/todo-chatbot \
      --namespace todo-production \
      --dry-run \
      --debug

    # 3. Validate Kubernetes manifests
    helm template todo-chatbot ./helm/todo-chatbot | kubectl apply --dry-run=client -f -

    # 4. Check image availability
    docker pull ${{ env.BACKEND_IMAGE }}:${{ needs.build-and-push.outputs.version }}
    docker pull ${{ env.FRONTEND_IMAGE }}:${{ needs.build-and-push.outputs.version }}
```

### Post-Deployment Validation

```yaml
- name: Post-deployment validation
  run: |
    # 1. Check pod status
    kubectl wait --for=condition=ready pod -l app=backend -n todo-production --timeout=300s
    kubectl wait --for=condition=ready pod -l app=frontend -n todo-production --timeout=300s

    # 2. Check service endpoints
    kubectl get endpoints -n todo-production

    # 3. Test health endpoints
    BACKEND_URL=$(kubectl get ingress backend -n todo-production -o jsonpath='{.spec.rules[0].host}')
    curl -f https://${BACKEND_URL}/health

    # 4. Check logs for errors
    kubectl logs -l app=backend -n todo-production --tail=50 | grep -i error && exit 1 || true

    # 5. Verify database connectivity
    kubectl exec -it deployment/backend -n todo-production -- python -c "from app.database import engine; engine.connect()"
```

## Output Format

### GitHub Actions YAML Template

Complete templates provided above for:
- ✅ Main CI/CD Pipeline (`main.yml`)
- ✅ PR Validation Pipeline (`pr-validation.yml`)
- ✅ Release Automation (`release.yml`)

### Pipeline Validation Steps

#### 1. **Local Validation (Before Pushing)**

```bash
# Validate workflow syntax
act -l

# Test workflow locally with act
act push -W .github/workflows/main.yml

# Validate Dockerfiles
docker build -f backend/Dockerfile backend/
docker build -f frontend/Dockerfile frontend/
```

#### 2. **GitHub Actions Validation**

```bash
# Check workflow runs
gh run list

# View specific run
gh run view <run-id>

# Watch live logs
gh run watch

# Re-run failed jobs
gh run rerun <run-id>
```

#### 3. **Deployment Validation**

```bash
# Check deployment status
kubectl rollout status deployment/backend -n todo-production
kubectl get pods -n todo-production
kubectl get events -n todo-production --sort-by='.lastTimestamp'

# Test application
curl https://api.yourdomain.com/health
curl https://yourdomain.com
```

## Example Usage

### Input
```bash
/cicd-automation "Setup CI/CD pipeline for Todo Chatbot"
```

### Output
```
✅ CI/CD Pipeline Created Successfully!

📁 Files Created:
- .github/workflows/main.yml (Main CI/CD Pipeline)
- .github/workflows/pr-validation.yml (PR Validation)
- .github/workflows/release.yml (Release Automation)

🔧 Pipeline Features:
✅ Automated testing (Backend + Frontend)
✅ Security scanning (Trivy)
✅ Docker image building
✅ Container registry push
✅ Kubernetes deployment
✅ Automatic rollback on failure
✅ Slack notifications
✅ Release automation

🔐 Required GitHub Secrets:
- DOCKER_USERNAME
- DOCKER_PASSWORD
- KUBECONFIG_DATA
- JWT_SECRET
- DATABASE_URL
- SLACK_WEBHOOK_URL (optional)

📋 Pipeline Stages:
1. Test Backend (Unit + Integration)
2. Test Frontend (Unit + E2E)
3. Security Scan (Trivy)
4. Build Docker Images
5. Push to Registry
6. Deploy to Kubernetes
7. Health Checks
8. Rollback (if needed)

🚀 Next Steps:
1. Configure GitHub Secrets in repository settings
2. Push code to trigger pipeline
3. Monitor deployment at: https://github.com/<user>/<repo>/actions

🎉 Your pipeline is ready to go!
```

## Advanced Features

### 1. Multi-Environment Deployment

```yaml
strategy:
  matrix:
    environment: [dev, staging, production]
    include:
      - environment: dev
        namespace: todo-dev
        replicas: 1
      - environment: staging
        namespace: todo-staging
        replicas: 2
      - environment: production
        namespace: todo-production
        replicas: 3
```

### 2. Canary Deployment

```yaml
- name: Canary deployment
  run: |
    # Deploy canary version (10% traffic)
    helm upgrade todo-chatbot-canary ./helm/todo-chatbot \
      --set backend.replicas=1 \
      --set backend.canary.enabled=true \
      --set backend.canary.weight=10

    # Wait and monitor
    sleep 300

    # Check error rate
    ERROR_RATE=$(kubectl logs -l version=canary | grep ERROR | wc -l)
    if [ $ERROR_RATE -gt 10 ]; then
      echo "Canary deployment failed"
      helm delete todo-chatbot-canary
      exit 1
    fi

    # Promote canary to production
    helm upgrade todo-chatbot ./helm/todo-chatbot \
      --set backend.image.tag=canary
```

### 3. Blue-Green Deployment

```yaml
- name: Blue-green deployment
  run: |
    # Deploy green version
    kubectl apply -f k8s/green-deployment.yaml

    # Wait for green to be ready
    kubectl wait --for=condition=ready pod -l version=green --timeout=300s

    # Run smoke tests on green
    GREEN_IP=$(kubectl get svc backend-green -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    curl -f http://${GREEN_IP}/health

    # Switch traffic to green
    kubectl patch service backend -p '{"spec":{"selector":{"version":"green"}}}'

    # Delete blue version after verification
    sleep 60
    kubectl delete deployment backend-blue
```

## Monitoring and Notifications

### Slack Integration

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    fields: repo,message,commit,author,action,eventName,ref,workflow
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
  if: always()
```

### Email Notifications

```yaml
- name: Send email notification
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Deployment ${{ job.status }}
    body: Deployment to production ${{ job.status }}
    to: team@example.com
    from: ci-cd@example.com
```

## Troubleshooting

### Common Issues

1. **Build fails**
   ```bash
   # Check build logs
   gh run view --log

   # Test build locally
   docker build -f backend/Dockerfile backend/
   ```

2. **Tests fail**
   ```bash
   # Run tests locally
   cd backend && pytest tests/ -v
   cd frontend && npm test
   ```

3. **Deployment fails**
   ```bash
   # Check Helm status
   helm status todo-chatbot -n todo-production

   # Check pod logs
   kubectl logs -l app=backend -n todo-production --tail=100
   ```

4. **Rollback not working**
   ```bash
   # Manual rollback
   kubectl rollout undo deployment/backend -n todo-production

   # Check history
   helm history todo-chatbot -n todo-production
   ```

## Best Practices

1. **Always run tests before deployment**
2. **Use semantic versioning for tags**
3. **Implement automated rollback**
4. **Monitor deployment metrics**
5. **Keep secrets in GitHub Secrets**
6. **Use branch protection rules**
7. **Require code reviews before merge**
8. **Run security scans on every build**
9. **Use caching to speed up builds**
10. **Set up monitoring and alerting**

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Helm Chart Development](https://helm.sh/docs/chart_template_guide/)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Version History

- **v1.0.0** (2026-02-08): Initial release with full CI/CD automation

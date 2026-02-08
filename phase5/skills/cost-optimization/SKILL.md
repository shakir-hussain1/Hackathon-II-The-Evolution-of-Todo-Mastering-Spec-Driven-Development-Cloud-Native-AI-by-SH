---
name: cost-optimization
description: Optimize cloud and infrastructure costs with autoscaling, resource optimization, and budget alerts
version: 1.0.0
category: optimization
tags: [cost, optimization, autoscaling, budget, resources, efficiency, savings]
---

# Cost-Optimization Skill

## Purpose
Optimize cloud infrastructure costs for the Todo Chatbot application through intelligent resource allocation, autoscaling configuration, cost monitoring, and budget alerting. Reduce cloud spending by 30-60% while maintaining performance and reliability.

## When to Use This Skill

Use this skill when you need to:
- Reduce monthly cloud infrastructure costs
- Optimize resource utilization (CPU, memory, storage)
- Configure autoscaling to match actual demand
- Set up cost monitoring and budget alerts
- Identify and eliminate waste (idle resources, over-provisioning)
- Right-size Kubernetes pods and nodes
- Optimize storage costs
- Implement cost-efficient scaling strategies
- Prepare for cost audits or budget reviews
- Optimize development/staging environments

## Prerequisites

Before using this skill, ensure you have:
- [ ] Application deployed to Kubernetes cluster
- [ ] Metrics server installed (`kubectl top` working)
- [ ] Prometheus and Grafana installed (for monitoring)
- [ ] Cloud provider CLI configured (AWS/GCP/Azure/DigitalOcean)
- [ ] Access to cloud billing dashboard
- [ ] Understanding of application load patterns

## Cost Optimization Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Cost Optimization Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Resource   │─────▶│   Metrics    │─────▶│     HPA      │  │
│  │   Monitoring │      │   Server     │      │ (Horizontal) │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                               │                      ▼           │
│  ┌──────────────┐             ▼              ┌──────────────┐  │
│  │ Cluster      │      ┌──────────────┐      │    VPA       │  │
│  │ Autoscaler   │◀────│  Prometheus  │      │ (Vertical)   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│        ▼                      │                                  │
│  ┌──────────────┐             ▼              ┌──────────────┐  │
│  │  Node Pool   │      ┌──────────────┐      │    Cost      │  │
│  │   Scaling    │      │   Grafana    │─────▶│  Dashboard   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                               │                      │           │
│                               ▼                      ▼           │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Budget     │◀────│   Cost       │◀────│    Cloud      │ │
│  │   Alerts     │      │   Analysis   │      │   Billing    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Cost Optimization

### 1. Install Metrics Server (if not already installed)

```bash
# Check if metrics server is running
kubectl get deployment metrics-server -n kube-system

# If not installed, install it
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify installation
kubectl get pods -n kube-system | grep metrics-server
kubectl top nodes
kubectl top pods -A
```

### 2. Resource Monitoring and Analysis

#### A. Analyze Current Resource Usage

```bash
# Check node resource usage
kubectl top nodes

# Check pod resource usage by namespace
kubectl top pods -n todo-production

# Get resource requests vs actual usage
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check pod resource requests and limits
kubectl get pods -n todo-production -o custom-columns=NAME:.metadata.name,CPU-REQUEST:.spec.containers[*].resources.requests.cpu,CPU-LIMIT:.spec.containers[*].resources.limits.cpu,MEMORY-REQUEST:.spec.containers[*].resources.requests.memory,MEMORY-LIMIT:.spec.containers[*].resources.limits.memory
```

#### B. Install kube-resource-report (Resource Visualization)

```bash
# Install kube-resource-report
kubectl apply -f https://codeberg.org/hjacobs/kube-resource-report/raw/branch/main/deploy/deployment.yaml

# Port-forward to access report
kubectl port-forward -n kube-resource-report service/kube-resource-report 8080:80

# Access at http://localhost:8080
```

#### C. Identify Over-Provisioned Resources

**Create resource analysis script** (`analyze-resources.sh`):
```bash
#!/bin/bash

echo "=== Resource Utilization Analysis ==="
echo ""

for namespace in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
  echo "Namespace: $namespace"

  pods=$(kubectl get pods -n $namespace -o jsonpath='{.items[*].metadata.name}')

  for pod in $pods; do
    echo "  Pod: $pod"

    # Get CPU request vs actual
    cpu_request=$(kubectl get pod $pod -n $namespace -o jsonpath='{.spec.containers[0].resources.requests.cpu}')
    cpu_actual=$(kubectl top pod $pod -n $namespace --no-headers | awk '{print $2}')

    # Get memory request vs actual
    mem_request=$(kubectl get pod $pod -n $namespace -o jsonpath='{.spec.containers[0].resources.requests.memory}')
    mem_actual=$(kubectl top pod $pod -n $namespace --no-headers | awk '{print $3}')

    echo "    CPU: Request=$cpu_request, Actual=$cpu_actual"
    echo "    Memory: Request=$mem_request, Actual=$mem_actual"
  done
  echo ""
done
```

### 3. Horizontal Pod Autoscaling (HPA)

#### A. Install Metrics Server Prerequisites

Ensure metrics-server is running and providing metrics:
```bash
kubectl get apiservices | grep metrics
```

#### B. Create HPA for Backend

**Backend HPA** (`backend-hpa.yaml`):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: todo-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

#### C. Create HPA for Frontend

**Frontend HPA** (`frontend-hpa.yaml`):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: todo-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 75
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Pods
        value: 2
        periodSeconds: 30
```

Apply HPAs:
```bash
kubectl apply -f backend-hpa.yaml
kubectl apply -f frontend-hpa.yaml

# Verify HPA status
kubectl get hpa -n todo-production
kubectl describe hpa backend-hpa -n todo-production
```

#### D. Advanced HPA with Custom Metrics

**HPA with Request Rate** (requires Prometheus Adapter):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa-custom
  namespace: todo-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 15
  metrics:
  # CPU utilization
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Custom metric: Request rate per pod
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

### 4. Vertical Pod Autoscaling (VPA)

**Install VPA:**
```bash
# Clone VPA repository
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler

# Install VPA
./hack/vpa-up.sh

# Verify installation
kubectl get pods -n kube-system | grep vpa
```

**Create VPA for Backend** (`backend-vpa.yaml`):
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: backend-vpa
  namespace: todo-production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  updatePolicy:
    updateMode: "Auto"  # "Off", "Initial", or "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: backend
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 2Gi
      controlledResources: ["cpu", "memory"]
```

Apply VPA:
```bash
kubectl apply -f backend-vpa.yaml

# Get VPA recommendations
kubectl describe vpa backend-vpa -n todo-production
```

### 5. Cluster Autoscaling

#### A. DigitalOcean Kubernetes Autoscaling

```bash
# Enable autoscaling on node pool
doctl kubernetes cluster node-pool update <cluster-id> <pool-id> \
  --auto-scale \
  --min-nodes 2 \
  --max-nodes 10
```

#### B. AWS EKS Cluster Autoscaler

**Install Cluster Autoscaler:**
```bash
# Create IAM policy
aws iam create-policy \
  --policy-name AmazonEKSClusterAutoscalerPolicy \
  --policy-document file://cluster-autoscaler-policy.json

# Install cluster autoscaler
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Edit deployment to add cluster name
kubectl -n kube-system edit deployment.apps/cluster-autoscaler

# Add these flags:
# - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<cluster-name>
# - --balance-similar-node-groups
# - --skip-nodes-with-system-pods=false
```

#### C. GCP GKE Cluster Autoscaling

```bash
# Enable cluster autoscaler
gcloud container clusters update <cluster-name> \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10 \
  --zone <zone>
```

### 6. Resource Optimization

#### A. Right-size Pod Resources

**Optimized Backend Deployment** (`backend-optimized.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-production
spec:
  replicas: 2  # Start with minimum, let HPA handle scaling
  template:
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        resources:
          requests:
            cpu: 250m      # Reduced from 500m (based on actual usage)
            memory: 256Mi  # Reduced from 512Mi
          limits:
            cpu: 500m      # Reduced from 1000m
            memory: 512Mi  # Reduced from 1Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Optimized Frontend Deployment** (`frontend-optimized.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-production
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        resources:
          requests:
            cpu: 100m      # Reduced from 250m
            memory: 128Mi  # Reduced from 256Mi
          limits:
            cpu: 200m      # Reduced from 500m
            memory: 256Mi  # Reduced from 512Mi
```

#### B. Use Spot/Preemptible Instances

**AWS EKS Spot Instances:**
```bash
# Create spot instance node group
eksctl create nodegroup \
  --cluster=todo-chatbot-prod \
  --name=spot-workers \
  --node-type=t3.medium \
  --nodes=2 \
  --nodes-min=1 \
  --nodes-max=5 \
  --spot
```

**GCP GKE Preemptible Nodes:**
```bash
# Create preemptible node pool
gcloud container node-pools create preemptible-pool \
  --cluster=todo-chatbot-prod \
  --preemptible \
  --num-nodes=2 \
  --min-nodes=1 \
  --max-nodes=5
```

**Taint Spot/Preemptible Nodes:**
```yaml
# Add toleration to deployments that can run on spot instances
tolerations:
- key: "node.kubernetes.io/spot"
  operator: "Exists"
  effect: "NoSchedule"
```

### 7. Storage Cost Optimization

#### A. Use Storage Classes with Cost Tiers

```yaml
# cost-optimized-storage.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cost-optimized-ssd
provisioner: kubernetes.io/aws-ebs  # or appropriate provisioner
parameters:
  type: gp3  # Use gp3 instead of gp2 (cheaper)
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete
allowVolumeExpansion: true
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cost-optimized-hdd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: st1  # Throughput optimized HDD (cheapest)
reclaimPolicy: Delete
allowVolumeExpansion: true
```

#### B. Implement Storage Lifecycle Policies

```yaml
# database-pvc-optimized.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
  namespace: todo-production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: cost-optimized-ssd
  resources:
    requests:
      storage: 20Gi  # Right-sized (was 50Gi)
```

#### C. Enable Volume Snapshots for Backup

```bash
# Take snapshot instead of maintaining replicas
kubectl create volumesnapshot postgres-snapshot \
  --volume-name=postgres-pv \
  --snapshot-class=csi-snapclass

# Delete old snapshots
kubectl delete volumesnapshot postgres-snapshot-old
```

### 8. Cost Monitoring and Analysis

#### A. Install kubecost (Cost Monitoring Tool)

```bash
# Add kubecost Helm repo
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm repo update

# Install kubecost
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="<your-token>"

# Access kubecost dashboard
kubectl port-forward -n kubecost deployment/kubecost-cost-analyzer 9090:9090

# Visit http://localhost:9090
```

#### B. Create Cost Dashboard in Grafana

**Grafana Dashboard JSON** (`cost-dashboard.json`):
```json
{
  "dashboard": {
    "title": "Todo Chatbot - Cost Analysis",
    "panels": [
      {
        "title": "Monthly Cost Trend",
        "targets": [
          {
            "expr": "sum(node_cpu_hourly_cost) * 730 + sum(node_ram_hourly_cost) * 730"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Cost by Namespace",
        "targets": [
          {
            "expr": "sum by (namespace) (container_cpu_allocation * container_cpu_hourly_cost + container_memory_allocation_bytes * container_memory_hourly_cost)"
          }
        ],
        "type": "piechart"
      },
      {
        "title": "Resource Efficiency",
        "targets": [
          {
            "expr": "sum(container_cpu_usage_seconds_total) / sum(container_spec_cpu_quota) * 100"
          }
        ],
        "type": "gauge"
      },
      {
        "title": "Wasted Resources",
        "targets": [
          {
            "expr": "sum(container_spec_cpu_quota - container_cpu_usage_seconds_total)"
          }
        ],
        "type": "stat"
      }
    ]
  }
}
```

#### C. Cloud Provider Cost Analysis

**AWS Cost Explorer Query:**
```bash
# Get cost by service (last 30 days)
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-02-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE

# Get EKS-specific costs
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-02-01 \
  --granularity DAILY \
  --metrics "UnblendedCost" \
  --filter file://eks-filter.json
```

**GCP Billing Query:**
```bash
# Export billing data to BigQuery
bq query --use_legacy_sql=false '
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `project.dataset.gcp_billing_export_v1_BILLING_ACCOUNT_ID`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND project.id = "your-project-id"
GROUP BY service.description
ORDER BY total_cost DESC
'
```

### 9. Budget Alerts

#### A. Cloud Provider Budget Alerts

**AWS Budget Alert:**
```bash
# Create budget
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

**budget.json:**
```json
{
  "BudgetName": "Todo-Chatbot-Monthly-Budget",
  "BudgetLimit": {
    "Amount": "500",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

**notifications.json:**
```json
{
  "Notification": {
    "NotificationType": "ACTUAL",
    "ComparisonOperator": "GREATER_THAN",
    "Threshold": 80,
    "ThresholdType": "PERCENTAGE"
  },
  "Subscribers": [
    {
      "SubscriptionType": "EMAIL",
      "Address": "team@yourdomain.com"
    }
  ]
}
```

#### B. Kubernetes Resource Quotas

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: todo-production-quota
  namespace: todo-production
spec:
  hard:
    requests.cpu: "8"
    requests.memory: "16Gi"
    limits.cpu: "16"
    limits.memory: "32Gi"
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"
```

#### C. Prometheus Alert for High Costs

```yaml
# cost-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cost-alerts
  namespace: monitoring
spec:
  groups:
  - name: cost-optimization
    interval: 1h
    rules:
    - alert: HighMonthlyCost
      expr: |
        sum(node_cpu_hourly_cost) * 730 + sum(node_ram_hourly_cost) * 730 > 500
      for: 1h
      labels:
        severity: warning
      annotations:
        summary: "Monthly cost exceeds budget"
        description: "Estimated monthly cost is ${{ $value }}, budget is $500"

    - alert: LowResourceUtilization
      expr: |
        avg(rate(container_cpu_usage_seconds_total[1h])) / avg(container_spec_cpu_quota) < 0.3
      for: 6h
      labels:
        severity: warning
      annotations:
        summary: "Low CPU utilization detected"
        description: "Average CPU utilization is {{ $value | humanizePercentage }}"

    - alert: WastedMemory
      expr: |
        sum(container_spec_memory_limit_bytes - container_memory_usage_bytes) > 10737418240
      for: 6h
      labels:
        severity: info
      annotations:
        summary: "Significant wasted memory allocation"
        description: "{{ $value | humanize1024 }}B of allocated memory is unused"
```

### 10. Development/Staging Environment Optimization

#### A. Scale Down Non-Production During Off-Hours

**CronJob to scale down** (`scale-down-cronjob.yaml`):
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-staging
  namespace: todo-staging
spec:
  schedule: "0 18 * * 1-5"  # 6 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: scaler
          containers:
          - name: kubectl
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              kubectl scale deployment --all --replicas=0 -n todo-staging
              kubectl scale deployment --all --replicas=0 -n todo-dev
          restartPolicy: OnFailure
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-up-staging
  namespace: todo-staging
spec:
  schedule: "0 8 * * 1-5"  # 8 AM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: scaler
          containers:
          - name: kubectl
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              kubectl scale deployment backend --replicas=1 -n todo-staging
              kubectl scale deployment frontend --replicas=1 -n todo-staging
          restartPolicy: OnFailure
```

#### B. Use Cheaper Instances for Non-Production

```yaml
# staging-values.yaml (for Helm)
global:
  environment: staging

backend:
  replicas: 1  # Production: 2
  resources:
    requests:
      cpu: 100m     # Production: 250m
      memory: 128Mi # Production: 256Mi
    limits:
      cpu: 200m     # Production: 500m
      memory: 256Mi # Production: 512Mi

nodeSelector:
  node-type: spot  # Use spot instances

tolerations:
- key: "node.kubernetes.io/spot"
  operator: "Exists"
```

## Output Format

### Optimization Report

**Cost Optimization Report:**
```
═══════════════════════════════════════════════════════════
           COST OPTIMIZATION REPORT
           Todo Chatbot Application
           Date: 2026-02-08
═══════════════════════════════════════════════════════════

📊 CURRENT COST ANALYSIS
─────────────────────────────────────────────────────────

Monthly Cost Breakdown:
├── Compute (K8s Nodes)      : $320/month
├── Storage (PVs)            : $45/month
├── Load Balancer            : $18/month
├── Data Transfer            : $12/month
└── Total                    : $395/month

Resource Utilization:
├── CPU Utilization          : 35% (65% wasted)
├── Memory Utilization       : 42% (58% wasted)
├── Storage Utilization      : 60% (40% wasted)
└── Pod Count                : 12 (avg)

═══════════════════════════════════════════════════════════

✅ OPTIMIZATIONS APPLIED
─────────────────────────────────────────────────────────

1. Horizontal Pod Autoscaling (HPA)
   ├── Backend: 2-10 replicas (was fixed at 5)
   ├── Frontend: 2-8 replicas (was fixed at 4)
   └── Expected Savings: $85/month

2. Resource Right-Sizing
   ├── Backend CPU: 250m → 500m (was 500m → 1000m)
   ├── Backend Memory: 256Mi → 512Mi (was 512Mi → 1Gi)
   ├── Frontend CPU: 100m → 200m (was 250m → 500m)
   └── Expected Savings: $45/month

3. Cluster Autoscaling
   ├── Min Nodes: 2 (was 3)
   ├── Max Nodes: 10 (was 10)
   └── Expected Savings: $65/month

4. Storage Optimization
   ├── Storage Type: gp3 (was gp2)
   ├── Volume Size: 20Gi (was 50Gi)
   └── Expected Savings: $18/month

5. Spot/Preemptible Instances
   ├── Staging Environment: 100% spot
   ├── Production: 30% spot (non-critical workloads)
   └── Expected Savings: $52/month

6. Development Environment Auto-Shutdown
   ├── Shutdown: 6 PM weekdays, all weekend
   ├── Uptime: 40 hours/week (was 168 hours/week)
   └── Expected Savings: $38/month

═══════════════════════════════════════════════════════════

💰 COST SAVINGS SUMMARY
─────────────────────────────────────────────────────────

Current Monthly Cost      : $395
Optimized Monthly Cost    : $92
Monthly Savings           : $303 (77% reduction)
Annual Savings            : $3,636

Break down by category:
├── Compute Savings       : $202/month (63%)
├── Storage Savings       : $18/month (40%)
├── Dev/Staging Savings   : $83/month (90%)
└── Total Savings         : $303/month (77%)

═══════════════════════════════════════════════════════════

📋 RECOMMENDATIONS
─────────────────────────────────────────────────────────

High Priority:
✅ Applied: HPA for backend and frontend
✅ Applied: Resource right-sizing
✅ Applied: Cluster autoscaling
⚠️  Consider: Reserved instances for baseline capacity (20% discount)
⚠️  Consider: Committed use discounts (25-30% discount)

Medium Priority:
✅ Applied: Storage optimization
⚠️  Consider: Multi-region cost optimization
⚠️  Consider: CDN for static assets

Low Priority:
⚠️  Monitor: Review utilization monthly
⚠️  Monitor: Adjust HPA thresholds based on patterns

═══════════════════════════════════════════════════════════

🎯 NEXT STEPS
─────────────────────────────────────────────────────────

1. Monitor resource utilization for 7 days
2. Adjust HPA thresholds if needed
3. Review cost dashboard weekly
4. Set up budget alerts at 80% threshold
5. Schedule monthly cost review meeting

═══════════════════════════════════════════════════════════
```

### HPA Templates

See sections 3B, 3C, and 3D above for complete HPA templates:
- ✅ Backend HPA (CPU + Memory based)
- ✅ Frontend HPA (CPU + Memory based)
- ✅ Advanced HPA (Custom metrics)

### Cost-Saving Checklist

**Pre-Optimization Checklist:**

#### Compute Resources
- [ ] Analyze actual CPU usage vs requests
- [ ] Analyze actual memory usage vs requests
- [ ] Identify over-provisioned pods
- [ ] Check pod count vs actual load
- [ ] Review node instance types

#### Autoscaling
- [ ] HPA configured for all deployments
- [ ] VPA recommendations reviewed
- [ ] Cluster autoscaler enabled
- [ ] Min/max replica counts set appropriately
- [ ] Scale-down stabilization configured

#### Storage
- [ ] Storage class optimized (gp3 vs gp2)
- [ ] Volume sizes right-sized
- [ ] Unused PVs identified and deleted
- [ ] Backup strategy optimized
- [ ] Snapshot lifecycle policies set

#### Network
- [ ] Load balancer count minimized
- [ ] Internal services use ClusterIP (not LoadBalancer)
- [ ] CDN configured for static assets
- [ ] Data transfer costs analyzed

#### Development/Staging
- [ ] Auto-shutdown configured for off-hours
- [ ] Spot/preemptible instances used
- [ ] Resource quotas enforced
- [ ] Shared clusters where possible

#### Monitoring & Alerts
- [ ] Cost monitoring dashboard created
- [ ] Budget alerts configured
- [ ] Resource utilization tracked
- [ ] Monthly cost reviews scheduled

#### Cloud Provider Specific
- [ ] Reserved instances considered
- [ ] Committed use discounts evaluated
- [ ] Savings plans reviewed
- [ ] Instance family optimized

**Post-Optimization Verification:**

- [ ] Resource utilization improved (>50%)
- [ ] HPA working correctly (pods scaling)
- [ ] Cluster autoscaler working (nodes scaling)
- [ ] Cost dashboard showing reduction
- [ ] No performance degradation
- [ ] Alerts configured and tested
- [ ] Team trained on new configuration
- [ ] Documentation updated

## Example Usage

### Input
```bash
/cost-optimization "Reduce cloud costs"
```

### Output
```
✅ Cost Optimization Complete!

📊 Analysis Results:
- Current monthly cost: $395
- Wasted resources: 65% CPU, 58% memory
- Identified 6 optimization opportunities

🔧 Optimizations Applied:

1. ✅ Horizontal Pod Autoscaling
   - Backend: 2-10 replicas (CPU 70%, Memory 80%)
   - Frontend: 2-8 replicas (CPU 70%, Memory 75%)
   - Savings: $85/month

2. ✅ Resource Right-Sizing
   - Backend: 250m/256Mi → 500m/512Mi (was 500m/512Mi → 1000m/1Gi)
   - Frontend: 100m/128Mi → 200m/256Mi (was 250m/256Mi → 500m/512Mi)
   - Savings: $45/month

3. ✅ Cluster Autoscaling
   - Enabled: 2-10 nodes (was fixed at 3)
   - Savings: $65/month

4. ✅ Storage Optimization
   - Type: gp3 (was gp2)
   - Size: 20Gi (was 50Gi)
   - Savings: $18/month

5. ✅ Spot Instances
   - Staging: 100% spot
   - Production: 30% spot
   - Savings: $52/month

6. ✅ Dev Auto-Shutdown
   - Schedule: Off during nights/weekends
   - Savings: $38/month

💰 Cost Savings:
Before: $395/month
After:  $92/month
Saved:  $303/month (77% reduction)
Annual: $3,636 saved per year

📈 Resource Efficiency:
CPU Utilization: 35% → 65% (+30%)
Memory Utilization: 42% → 70% (+28%)

🚨 Budget Alerts Configured:
- Warning at 80% ($80)
- Critical at 95% ($95)
- Notifications: team@yourdomain.com

📊 Monitoring:
- Grafana cost dashboard: https://grafana.yourdomain.com/d/cost
- kubecost: kubectl port-forward -n kubecost svc/kubecost 9090

🎉 You're now running 77% more cost-efficiently!
```

## Advanced Cost Optimization Strategies

### 1. Reserved Instances / Committed Use

**AWS Reserved Instances:**
```bash
# Analyze RI recommendations
aws ce get-reservation-purchase-recommendation \
  --service "Amazon Elastic Compute Cloud - Compute" \
  --lookback-period-in-days SIXTY_DAYS \
  --term-in-years ONE \
  --payment-option NO_UPFRONT
```

**GCP Committed Use Discounts:**
```bash
# List committed use discount recommendations
gcloud recommender recommendations list \
  --project=your-project \
  --recommender=google.compute.commitment.UsageCommitmentRecommender \
  --location=us-central1
```

### 2. Karpenter (Advanced Cluster Autoscaling)

```bash
# Install Karpenter (more efficient than cluster autoscaler)
helm repo add karpenter https://charts.karpenter.sh
helm install karpenter karpenter/karpenter \
  --namespace karpenter \
  --create-namespace
```

### 3. Cost Allocation Tags

```bash
# Add cost allocation tags to resources
kubectl label nodes node-1 \
  team=backend \
  environment=production \
  cost-center=engineering
```

### 4. Fargate / Serverless Containers

For AWS EKS, consider Fargate for spiky workloads:
```yaml
# fargate-profile.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-batch-jobs
  labels:
    aws-fargate-profile: batch-jobs
```

## Troubleshooting

### Common Issues

1. **HPA not scaling**
   ```bash
   # Check metrics-server
   kubectl top pods -n todo-production

   # Check HPA status
   kubectl describe hpa backend-hpa -n todo-production

   # Check if metrics are available
   kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods
   ```

2. **Cluster autoscaler not working**
   ```bash
   # Check cluster autoscaler logs
   kubectl logs -n kube-system -l app=cluster-autoscaler

   # Check node groups
   kubectl get nodes
   ```

3. **VPA conflicts with HPA**
   ```bash
   # Use VPA in recommendation mode
   # Set updateMode: "Off" in VPA spec
   ```

4. **Spot instances terminating frequently**
   ```bash
   # Add pod disruption budget
   # Increase grace period
   # Use mixed instance types
   ```

## Best Practices

1. **Start Small**: Begin with 2 replicas, let HPA scale up
2. **Monitor First**: Analyze for 7 days before optimizing
3. **Gradual Changes**: Don't optimize everything at once
4. **Test in Staging**: Validate optimizations before production
5. **Set Alerts**: Budget alerts at 80% and 95%
6. **Regular Reviews**: Monthly cost review meetings
7. **Document Baseline**: Record costs before optimization
8. **Reserve Capacity**: Consider RIs for baseline load
9. **Use Quotas**: Prevent runaway costs with resource quotas
10. **Educate Team**: Train on cost-conscious practices

## Additional Resources

- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)
- [GCP Cost Management](https://cloud.google.com/cost-management)
- [Kubecost Documentation](https://docs.kubecost.com/)

## Version History

- **v1.0.0** (2026-02-08): Initial release with comprehensive cost optimization strategies

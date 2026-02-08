---
name: production-monitoring
description: Monitor system health, performance, and errors with Prometheus, Grafana, and centralized logging
version: 1.0.0
category: observability
tags: [monitoring, prometheus, grafana, loki, elk, alerts, observability, logging, metrics]
---

# Production-Monitoring Skill

## Purpose
Set up comprehensive production monitoring for the Todo Chatbot application using industry-standard observability tools: Prometheus for metrics collection, Grafana for visualization, Loki/ELK for centralized logging, and AlertManager for alerting.

## When to Use This Skill

Use this skill when you need to:
- Monitor application health and performance in real-time
- Track resource usage (CPU, memory, disk, network)
- Collect and visualize application metrics
- Set up centralized logging for debugging
- Configure alerts for critical issues
- Monitor Kubernetes cluster health
- Track user behavior and API performance
- Implement SLOs (Service Level Objectives)
- Debug production issues quickly
- Perform capacity planning

## Prerequisites

Before using this skill, ensure you have:
- [ ] Kubernetes cluster running (production or staging)
- [ ] Application deployed to Kubernetes
- [ ] `kubectl` and `helm` installed
- [ ] Sufficient cluster resources (2-4 GB RAM for monitoring stack)
- [ ] Storage class configured for persistent volumes
- [ ] Ingress controller installed (for Grafana access)

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Stack Architecture                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │  Application │─────▶│  Prometheus  │─────▶│   Grafana    │  │
│  │   Metrics    │      │   (Metrics)  │      │ (Dashboard)  │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                               │                                  │
│                               ▼                                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │ Application  │─────▶│     Loki     │─────▶ Grafana          │
│  │     Logs     │      │  (Logging)   │                        │
│  └──────────────┘      └──────────────┘                        │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │  Prometheus  │─────▶│ AlertManager │─────▶│ Slack/Email  │ │
│  │    Rules     │      │   (Alerts)   │      │  (Notify)    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Setup

### 1. Install kube-prometheus-stack (Prometheus + Grafana)

```bash
# Add Prometheus community Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create monitoring namespace
kubectl create namespace monitoring

# Install kube-prometheus-stack
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set grafana.adminPassword=admin \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi \
  --set alertmanager.alertmanagerSpec.storage.volumeClaimTemplate.spec.resources.requests.storage=10Gi \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false

# Verify installation
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

### 2. Expose Grafana with Ingress

Create `grafana-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - grafana.yourdomain.com
    secretName: grafana-tls-cert
  rules:
  - host: grafana.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kube-prometheus-stack-grafana
            port:
              number: 80
```

Apply ingress:
```bash
kubectl apply -f grafana-ingress.yaml

# Get Grafana admin password
kubectl get secret -n monitoring kube-prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

### 3. Install Loki for Centralized Logging

```bash
# Add Grafana Loki Helm repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Loki
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --set loki.persistence.enabled=true \
  --set loki.persistence.size=50Gi \
  --set promtail.enabled=true \
  --set grafana.enabled=false \
  --set loki.config.limits_config.retention_period=720h

# Verify installation
kubectl get pods -n monitoring | grep loki
```

### 4. Configure Application Metrics (Backend)

Add Prometheus metrics to your FastAPI backend:

**Install dependencies** (`backend/requirements.txt`):
```txt
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0
```

**Update backend code** (`backend/app/main.py`):
```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
import time

app = FastAPI()

# Initialize Prometheus instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Custom metrics
request_count = Counter(
    'todo_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'todo_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

active_users = Gauge(
    'todo_active_users',
    'Number of active users'
)

todo_count = Gauge(
    'todo_total_count',
    'Total number of todos in database'
)

db_connection_pool = Gauge(
    'todo_db_connection_pool_size',
    'Database connection pool size'
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    # Prometheus client will handle this automatically
    pass
```

### 5. Create ServiceMonitor for Backend

Create `backend-servicemonitor.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-metrics
  namespace: todo-production
  labels:
    app: backend
spec:
  selector:
    app: backend
  ports:
  - name: metrics
    port: 8000
    targetPort: 8000
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-monitor
  namespace: todo-production
  labels:
    app: backend
    release: kube-prometheus-stack
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
```

Apply:
```bash
kubectl apply -f backend-servicemonitor.yaml
```

### 6. Configure Loki Datasource in Grafana

```bash
# Get Loki service URL
LOKI_URL="http://loki:3100"

# Add Loki datasource (via Grafana UI or API)
curl -X POST http://admin:admin@grafana.yourdomain.com/api/datasources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Loki",
    "type": "loki",
    "url": "http://loki.monitoring.svc.cluster.local:3100",
    "access": "proxy",
    "isDefault": false
  }'
```

### 7. Import Grafana Dashboards

Create `grafana-dashboard-configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-dashboards
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  todo-overview.json: |
    {
      "dashboard": {
        "title": "Todo Chatbot - Overview",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(todo_requests_total[5m])"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Error Rate",
            "targets": [
              {
                "expr": "rate(todo_requests_total{status=~\"5..\"}[5m])"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Response Time (P95)",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(todo_request_duration_seconds_bucket[5m]))"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Active Users",
            "targets": [
              {
                "expr": "todo_active_users"
              }
            ],
            "type": "stat"
          },
          {
            "title": "CPU Usage",
            "targets": [
              {
                "expr": "rate(container_cpu_usage_seconds_total{namespace=\"todo-production\"}[5m])"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Memory Usage",
            "targets": [
              {
                "expr": "container_memory_usage_bytes{namespace=\"todo-production\"}"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Pod Status",
            "targets": [
              {
                "expr": "kube_pod_status_phase{namespace=\"todo-production\"}"
              }
            ],
            "type": "stat"
          },
          {
            "title": "Database Connections",
            "targets": [
              {
                "expr": "todo_db_connection_pool_size"
              }
            ],
            "type": "gauge"
          }
        ],
        "refresh": "30s",
        "time": {
          "from": "now-1h",
          "to": "now"
        }
      }
    }
```

Apply:
```bash
kubectl apply -f grafana-dashboard-configmap.yaml
```

### 8. Set Up Alert Rules

Create `prometheus-alerts.yaml`:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: todo-alerts
  namespace: monitoring
  labels:
    release: kube-prometheus-stack
spec:
  groups:
  - name: todo-chatbot-alerts
    interval: 30s
    rules:
    # High error rate
    - alert: HighErrorRate
      expr: |
        rate(todo_requests_total{status=~"5.."}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
        component: backend
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value }} errors/sec (threshold: 0.05)"

    # Slow response time
    - alert: SlowResponseTime
      expr: |
        histogram_quantile(0.95, rate(todo_request_duration_seconds_bucket[5m])) > 2
      for: 5m
      labels:
        severity: warning
        component: backend
      annotations:
        summary: "Slow API response time"
        description: "P95 response time is {{ $value }}s (threshold: 2s)"

    # Pod down
    - alert: PodDown
      expr: |
        kube_pod_status_phase{namespace="todo-production", phase!="Running"} == 1
      for: 5m
      labels:
        severity: critical
        component: infrastructure
      annotations:
        summary: "Pod is not running"
        description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is not running"

    # High CPU usage
    - alert: HighCPUUsage
      expr: |
        rate(container_cpu_usage_seconds_total{namespace="todo-production"}[5m]) > 0.8
      for: 10m
      labels:
        severity: warning
        component: infrastructure
      annotations:
        summary: "High CPU usage detected"
        description: "CPU usage is {{ $value }} (threshold: 0.8)"

    # High memory usage
    - alert: HighMemoryUsage
      expr: |
        container_memory_usage_bytes{namespace="todo-production"} / container_spec_memory_limit_bytes{namespace="todo-production"} > 0.9
      for: 5m
      labels:
        severity: warning
        component: infrastructure
      annotations:
        summary: "High memory usage detected"
        description: "Memory usage is {{ $value | humanizePercentage }} (threshold: 90%)"

    # Database connection pool exhausted
    - alert: DatabaseConnectionPoolExhausted
      expr: |
        todo_db_connection_pool_size > 8
      for: 5m
      labels:
        severity: critical
        component: database
      annotations:
        summary: "Database connection pool nearly exhausted"
        description: "Connection pool size is {{ $value }} (max: 10)"

    # Pod restart
    - alert: PodRestarting
      expr: |
        rate(kube_pod_container_status_restarts_total{namespace="todo-production"}[15m]) > 0
      for: 5m
      labels:
        severity: warning
        component: infrastructure
      annotations:
        summary: "Pod is restarting frequently"
        description: "Pod {{ $labels.pod }} has restarted {{ $value }} times in the last 15 minutes"

    # Disk space low
    - alert: DiskSpaceLow
      expr: |
        (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.1
      for: 5m
      labels:
        severity: warning
        component: infrastructure
      annotations:
        summary: "Disk space is low"
        description: "Available disk space is {{ $value | humanizePercentage }} (threshold: 10%)"

    # High request latency
    - alert: HighRequestLatency
      expr: |
        histogram_quantile(0.99, rate(todo_request_duration_seconds_bucket[5m])) > 5
      for: 5m
      labels:
        severity: critical
        component: backend
      annotations:
        summary: "Very high request latency (P99)"
        description: "P99 latency is {{ $value }}s (threshold: 5s)"

    # No active users (possible outage)
    - alert: NoActiveUsers
      expr: |
        todo_active_users == 0
      for: 10m
      labels:
        severity: warning
        component: application
      annotations:
        summary: "No active users detected"
        description: "No active users for 10 minutes - possible outage or issue"
```

Apply alerts:
```bash
kubectl apply -f prometheus-alerts.yaml
```

### 9. Configure AlertManager

Create `alertmanager-config.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-kube-prometheus-stack-alertmanager
  namespace: monitoring
type: Opaque
stringData:
  alertmanager.yaml: |
    global:
      resolve_timeout: 5m
      slack_api_url: 'YOUR_SLACK_WEBHOOK_URL'

    route:
      group_by: ['alertname', 'cluster', 'service']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 12h
      receiver: 'slack-notifications'
      routes:
      - match:
          severity: critical
        receiver: 'slack-critical'
        continue: true
      - match:
          severity: warning
        receiver: 'slack-warnings'

    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - channel: '#alerts'
        title: 'Todo Chatbot Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

    - name: 'slack-critical'
      slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

    - name: 'slack-warnings'
      slack_configs:
      - channel: '#alerts-warnings'
        title: '⚠️ WARNING: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

    - name: 'email-notifications'
      email_configs:
      - to: 'team@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'your-email@gmail.com'
        auth_identity: 'your-email@gmail.com'
        auth_password: 'your-app-password'
        headers:
          Subject: 'Todo Chatbot Alert: {{ .GroupLabels.alertname }}'

    inhibit_rules:
    - source_match:
        severity: 'critical'
      target_match:
        severity: 'warning'
      equal: ['alertname', 'cluster', 'service']
```

Apply:
```bash
kubectl apply -f alertmanager-config.yaml

# Restart AlertManager to pick up new config
kubectl rollout restart statefulset/alertmanager-kube-prometheus-stack-alertmanager -n monitoring
```

### 10. Install ELK Stack (Alternative to Loki)

If you prefer ELK over Loki:

```bash
# Add Elastic Helm repo
helm repo add elastic https://helm.elastic.co
helm repo update

# Install Elasticsearch
helm install elasticsearch elastic/elasticsearch \
  --namespace monitoring \
  --set replicas=3 \
  --set volumeClaimTemplate.resources.requests.storage=50Gi

# Install Kibana
helm install kibana elastic/kibana \
  --namespace monitoring \
  --set service.type=LoadBalancer

# Install Filebeat (log shipper)
helm install filebeat elastic/filebeat \
  --namespace monitoring \
  --set daemonset.enabled=true
```

## Output Format

### Monitoring Stack Configuration

**Complete Stack Deployed:**
```
✅ Prometheus (Metrics Collection)
✅ Grafana (Visualization)
✅ Loki (Centralized Logging)
✅ Promtail (Log Collection)
✅ AlertManager (Alerting)
✅ Node Exporter (System Metrics)
✅ Kube State Metrics (K8s Metrics)
```

**Access URLs:**
- Grafana: https://grafana.yourdomain.com
- Prometheus: http://prometheus.yourdomain.com
- AlertManager: http://alertmanager.yourdomain.com

**Default Credentials:**
- Username: `admin`
- Password: (Retrieved from secret)

### Dashboard Templates

#### 1. **Todo Chatbot Overview Dashboard**
- Request rate (total, by endpoint)
- Error rate (4xx, 5xx)
- Response time (P50, P95, P99)
- Active users count
- Todo count
- Database connections

#### 2. **Infrastructure Dashboard**
- CPU usage per pod
- Memory usage per pod
- Network I/O
- Disk usage
- Pod status and restarts

#### 3. **Database Dashboard**
- Query performance
- Connection pool stats
- Transaction rate
- Lock waits
- Cache hit ratio

#### 4. **Kubernetes Cluster Dashboard**
- Node status
- Pod distribution
- Resource quotas
- Namespace usage
- PV/PVC status

### Alert Definitions

| Alert Name | Severity | Threshold | Duration | Action |
|------------|----------|-----------|----------|--------|
| HighErrorRate | Critical | > 5% | 5m | Page on-call |
| SlowResponseTime | Warning | P95 > 2s | 5m | Investigate |
| PodDown | Critical | Pod not running | 5m | Page on-call |
| HighCPUUsage | Warning | > 80% | 10m | Scale up |
| HighMemoryUsage | Warning | > 90% | 5m | Scale up |
| DatabasePoolExhausted | Critical | > 8 connections | 5m | Investigate |
| PodRestarting | Warning | Restarts > 0 | 15m | Check logs |
| DiskSpaceLow | Warning | < 10% free | 5m | Clean up |

## Example Usage

### Input
```bash
/production-monitoring "Enable full observability stack"
```

### Output
```
✅ Production Monitoring Enabled!

📊 Monitoring Stack Installed:
- Prometheus: Collecting metrics from 15 targets
- Grafana: Available at https://grafana.yourdomain.com
- Loki: Centralized logging configured
- AlertManager: 10 alert rules configured

📈 Dashboards Created:
1. Todo Chatbot Overview
2. Infrastructure Metrics
3. Database Performance
4. Kubernetes Cluster Health

🚨 Alerts Configured:
- High Error Rate (Critical)
- Slow Response Time (Warning)
- Pod Down (Critical)
- High CPU/Memory Usage (Warning)
- Database Issues (Critical)

📱 Notifications:
- Slack: #alerts, #alerts-critical, #alerts-warnings
- Email: team@example.com

🔍 Quick Access:
- Grafana: https://grafana.yourdomain.com (admin / <password>)
- Prometheus: http://localhost:9090 (port-forward)
- AlertManager: http://localhost:9093 (port-forward)

✅ System Health: All metrics reporting correctly
✅ Logs: Centralized and queryable
✅ Alerts: Ready to fire on issues

🎉 Your monitoring stack is live!
```

## Advanced Features

### 1. Custom Metrics Exporter

Create a sidecar container for custom metrics:

```yaml
# custom-metrics-exporter.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  template:
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
      - name: metrics-exporter
        image: prom/json-exporter:latest
        args:
        - '--config.file=/etc/json-exporter/config.yml'
        ports:
        - containerPort: 7979
        volumeMounts:
        - name: config
          mountPath: /etc/json-exporter
      volumes:
      - name: config
        configMap:
          name: json-exporter-config
```

### 2. Distributed Tracing with Jaeger

```bash
# Install Jaeger
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --set allInOne.enabled=true \
  --set storage.type=memory
```

Add tracing to backend:
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent.monitoring.svc.cluster.local",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)
```

### 3. Log Aggregation Queries (Loki)

```bash
# View all logs from backend
{namespace="todo-production", app="backend"}

# Filter error logs
{namespace="todo-production", app="backend"} |= "ERROR"

# Count errors in last hour
sum(count_over_time({namespace="todo-production", app="backend"} |= "ERROR" [1h]))

# Slow queries
{namespace="todo-production", app="backend"} |= "slow query" | json | duration > 1s
```

### 4. SLO Dashboard

```yaml
# SLO definitions
apiVersion: v1
kind: ConfigMap
metadata:
  name: slo-definitions
  namespace: monitoring
data:
  slos.yaml: |
    slos:
    - name: api_availability
      description: "API should be available 99.9% of the time"
      target: 0.999
      query: |
        (sum(rate(todo_requests_total{status!~"5.."}[30d]))
        /
        sum(rate(todo_requests_total[30d])))

    - name: api_latency
      description: "95% of requests should complete within 500ms"
      target: 0.95
      query: |
        histogram_quantile(0.95, rate(todo_request_duration_seconds_bucket[30d])) < 0.5

    - name: error_budget
      description: "Error budget remaining"
      query: |
        1 - ((1 - (sum(rate(todo_requests_total{status!~"5.."}[30d])) / sum(rate(todo_requests_total[30d])))) / (1 - 0.999))
```

## Verification Commands

```bash
# 1. Check monitoring stack pods
kubectl get pods -n monitoring

# 2. Port-forward Grafana (if not using ingress)
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80

# 3. Port-forward Prometheus
kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090

# 4. Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq

# 5. Check active alerts
curl http://localhost:9090/api/v1/alerts | jq

# 6. Query metrics
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=up'

# 7. Check Loki logs
kubectl port-forward -n monitoring svc/loki 3100:3100
curl http://localhost:3100/ready

# 8. Test AlertManager
kubectl port-forward -n monitoring svc/kube-prometheus-stack-alertmanager 9093:9093
curl http://localhost:9093/api/v2/status

# 9. Check ServiceMonitor
kubectl get servicemonitor -n todo-production

# 10. Verify metrics endpoint
kubectl port-forward -n todo-production svc/backend 8000:8000
curl http://localhost:8000/metrics
```

## Troubleshooting

### Common Issues

1. **Prometheus not scraping metrics**
   ```bash
   # Check ServiceMonitor
   kubectl describe servicemonitor backend-monitor -n todo-production

   # Check Prometheus targets
   kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
   # Visit http://localhost:9090/targets
   ```

2. **Grafana dashboards not showing data**
   ```bash
   # Verify datasources
   kubectl exec -n monitoring deployment/kube-prometheus-stack-grafana -- grafana-cli admin reset-admin-password newpassword

   # Check Prometheus datasource URL
   # Should be: http://kube-prometheus-stack-prometheus.monitoring.svc.cluster.local:9090
   ```

3. **Alerts not firing**
   ```bash
   # Check PrometheusRule
   kubectl describe prometheusrule todo-alerts -n monitoring

   # Check AlertManager config
   kubectl get secret alertmanager-kube-prometheus-stack-alertmanager -n monitoring -o yaml
   ```

4. **Loki not receiving logs**
   ```bash
   # Check Promtail pods
   kubectl get pods -n monitoring | grep promtail

   # Check Promtail logs
   kubectl logs -n monitoring -l app.kubernetes.io/name=promtail
   ```

## Best Practices

1. **Set appropriate retention periods** (balance cost vs. need)
2. **Use meaningful metric names and labels**
3. **Don't over-alert** (alert fatigue is real)
4. **Set up alert routing** (critical vs. warning)
5. **Regular dashboard reviews** (ensure relevance)
6. **Monitor the monitoring stack** (meta-monitoring)
7. **Document alert runbooks**
8. **Test alerts regularly**
9. **Implement SLOs** (not just monitoring)
10. **Use log sampling** (for high-volume apps)

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [SLO Toolkit](https://landing.google.com/sre/workbook/chapters/slo-engineering-case-studies/)

## Version History

- **v1.0.0** (2026-02-08): Initial release with Prometheus, Grafana, Loki, and AlertManager

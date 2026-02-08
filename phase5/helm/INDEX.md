# Phase 5 Helm Charts - Complete Index

Navigation guide for all Helm chart files and documentation.

## 📚 Documentation Files

Start here based on your goal:

| Goal | Document | Description |
|------|----------|-------------|
| **Deploy in 10 minutes** | [QUICKSTART.md](QUICKSTART.md) | Fastest path to running application |
| **Production deployment** | [DEPLOYMENT.md](DEPLOYMENT.md) | Complete deployment guide for OKE |
| **Understand the charts** | [HELM_CHARTS_SUMMARY.md](HELM_CHARTS_SUMMARY.md) | Architecture and implementation details |
| **Configure the application** | [phase5/README.md](phase5/README.md) | Full chart documentation |
| **Troubleshoot issues** | [DEPLOYMENT.md](DEPLOYMENT.md) | Troubleshooting section |

## 🗂️ File Structure

```
helm/
├── 📄 Documentation
│   ├── INDEX.md (this file)
│   ├── QUICKSTART.md - 10-minute quick start
│   ├── DEPLOYMENT.md - Full deployment guide
│   └── HELM_CHARTS_SUMMARY.md - Implementation summary
│
├── 🔧 Deployment Scripts
│   ├── deploy-local.sh - Local/Minikube deployment
│   ├── deploy-oke.sh - Oracle OKE deployment
│   └── validate.sh - Post-deployment validation
│
└── phase5/ - Helm Chart Root
    ├── Chart.yaml - Chart metadata & dependencies
    ├── values.yaml - Default configuration
    ├── values-oke.yaml - OKE-specific overrides
    ├── .helmignore - Files to exclude
    ├── README.md - Chart documentation
    │
    ├── templates/ - Global Resources
    │   ├── NOTES.txt - Post-install instructions
    │   ├── namespace.yaml - Namespace creation
    │   ├── postgres-secret.yaml - Database credentials
    │   ├── jwt-secret.yaml - JWT authentication
    │   ├── openai-secret.yaml - OpenAI API key
    │   └── ingress.yaml - Ingress configuration
    │
    ├── components/ - Dapr Components
    │   ├── pubsub-kafka.yaml - Kafka pub/sub
    │   ├── statestore-postgresql.yaml - State store
    │   ├── secretstore-kubernetes.yaml - Secret store
    │   ├── cron-recurring-tasks.yaml - Task scheduler
    │   ├── cron-reminders.yaml - Reminder scheduler
    │   └── dapr-config.yaml - Global Dapr config
    │
    └── charts/ - Service Subcharts
        ├── chat-api/
        │   ├── Chart.yaml
        │   ├── values.yaml
        │   └── templates/
        │       ├── deployment.yaml (with Dapr annotations)
        │       ├── service.yaml
        │       ├── hpa.yaml
        │       ├── serviceaccount.yaml
        │       ├── configmap.yaml
        │       └── _helpers.tpl
        │
        ├── notification-service/ (same structure)
        ├── recurring-task-service/ (same structure)
        ├── audit-service/ (same structure)
        ├── websocket-sync-service/ (same structure)
        └── frontend/ (same structure, no Dapr)
```

## 🎯 Quick Reference

### Essential Commands

```bash
# Local deployment
cd helm
./deploy-local.sh

# OKE deployment
cd helm
./deploy-oke.sh

# Validate deployment
./validate.sh phase5 phase5

# Manual install
helm install phase5 ./phase5 -n phase5 --create-namespace

# Upgrade
helm upgrade phase5 ./phase5 -n phase5

# Uninstall
helm uninstall phase5 -n phase5
```

### Key Configuration Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `values.yaml` | Base configuration | Setting default values |
| `values-oke.yaml` | OKE overrides | Deploying to Oracle Cloud |
| `components/*.yaml` | Dapr configuration | Changing Kafka/DB settings |
| `templates/*-secret.yaml` | Secrets | Never (use external secrets) |

### Service Ports

| Service | Port | Dapr Sidecar | Health Endpoint |
|---------|------|--------------|-----------------|
| chat-api | 8000 | Yes | /health, /ready |
| notification-service | 8001 | Yes | /health, /ready |
| recurring-task-service | 8002 | Yes | /health, /ready |
| audit-service | 8003 | Yes | /health, /ready |
| websocket-sync-service | 8004 | Yes | /health, /ready |
| frontend | 3000 | No | / |

## 🔍 Finding What You Need

### I want to...

**Deploy to local Kubernetes:**
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `./deploy-local.sh`
3. Validate with `./validate.sh`

**Deploy to Oracle OKE:**
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) - Oracle OKE section
2. Build and push images to OCIR
3. Run `./deploy-oke.sh`
4. Configure DNS
5. Validate with `./validate.sh`

**Understand the architecture:**
1. Read [HELM_CHARTS_SUMMARY.md](HELM_CHARTS_SUMMARY.md)
2. Check [phase5/README.md](phase5/README.md)
3. Review `components/dapr-config.yaml`

**Change resource limits:**
1. Edit `values-oke.yaml` (production)
2. Or create custom values file
3. Upgrade deployment

**Add a new service:**
1. Copy existing subchart (e.g., `charts/chat-api`)
2. Modify templates for new service
3. Add to `Chart.yaml` dependencies
4. Update `values.yaml`
5. Add to Dapr component scopes

**Troubleshoot issues:**
1. Run `./validate.sh`
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting section
3. Review pod logs
4. Check events

**Scale services:**
1. Edit HPA settings in `values.yaml` or subchart values
2. Or manually: `kubectl scale deployment/phase5-chat-api --replicas=5 -n phase5`

**Update secrets:**
1. Create new secret: `kubectl create secret generic ...`
2. Restart pods: `kubectl rollout restart deployment -n phase5`

**Monitor application:**
1. Dapr dashboard: `dapr dashboard -k`
2. View logs: `kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f`
3. Check metrics: Port-forward to 9090 and curl `/metrics`

**Enable tracing:**
1. Deploy Zipkin (if not already)
2. Set `global.tracing.enabled=true` in values
3. Configure `global.tracing.zipkinEndpoint`
4. Access Zipkin UI

## 📋 Deployment Checklist

### Before Deployment

- [ ] Kubernetes cluster ready (OKE or local)
- [ ] kubectl configured and working
- [ ] Helm 3.8+ installed
- [ ] Dapr installed (`dapr init -k`)
- [ ] Docker images built and pushed (OKE) or loaded (local)
- [ ] Secrets prepared (don't use defaults in production)

### During Deployment

- [ ] Run appropriate script (`deploy-local.sh` or `deploy-oke.sh`)
- [ ] Or manually install with `helm install`
- [ ] Wait for all pods to be ready
- [ ] Verify Dapr components created

### After Deployment

- [ ] Run `./validate.sh` - all checks should pass
- [ ] Test health endpoints
- [ ] Access frontend (port-forward or ingress)
- [ ] Check logs for errors
- [ ] Verify autoscaling is active
- [ ] Test a complete user workflow

### Production Only

- [ ] DNS configured for domain
- [ ] TLS certificates installed
- [ ] External secrets configured
- [ ] Monitoring and alerting set up
- [ ] Backup strategy in place
- [ ] Resource quotas applied
- [ ] Network policies configured
- [ ] RBAC policies reviewed

## 🆘 Common Issues

| Issue | Quick Fix | Details |
|-------|-----------|---------|
| Pods pending | Check resources/storage | [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting |
| Image pull errors | Verify image exists, check secret | [DEPLOYMENT.md](DEPLOYMENT.md) - Image Pull Errors |
| Dapr not injecting | Check namespace labels, verify Dapr | [DEPLOYMENT.md](DEPLOYMENT.md) - Dapr Issues |
| Database connection | Check PostgreSQL pod, verify secret | [DEPLOYMENT.md](DEPLOYMENT.md) - Database Issues |
| Ingress not working | Check NGINX controller, verify DNS | [DEPLOYMENT.md](DEPLOYMENT.md) - Ingress Issues |

## 📊 Chart Components Summary

### Umbrella Chart
- **Name**: phase5
- **Version**: 1.0.0
- **Dependencies**: 8 (2 external, 6 internal)
- **Templates**: 5 (namespace, secrets, ingress)
- **Components**: 6 (Dapr components)

### Service Subcharts (6 total)
Each includes:
- Deployment (with Dapr for services)
- Service (ClusterIP)
- HPA (autoscaling)
- ServiceAccount
- ConfigMap
- Helper templates

### Infrastructure
- **PostgreSQL**: Bitnami chart v12.12.10
- **Kafka**: Bitnami chart v26.4.3

## 🔗 External References

### Helm
- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

### Dapr
- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)
- [Dapr Components](https://docs.dapr.io/reference/components-reference/)

### Kubernetes
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Oracle OKE](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)

### Tools
- [kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)

## 🎓 Learning Path

1. **Beginner**: Start with [QUICKSTART.md](QUICKSTART.md)
2. **Intermediate**: Read [phase5/README.md](phase5/README.md)
3. **Advanced**: Study [HELM_CHARTS_SUMMARY.md](HELM_CHARTS_SUMMARY.md)
4. **Expert**: Review individual chart templates

## ✨ Features Highlights

- ✅ Production-ready Helm charts
- ✅ Dapr integration with all services
- ✅ Horizontal Pod Autoscaling
- ✅ Health and readiness probes
- ✅ Security contexts and RBAC
- ✅ ConfigMaps and Secrets management
- ✅ NGINX Ingress with TLS
- ✅ PostgreSQL and Kafka (Bitnami)
- ✅ Distributed tracing (Zipkin)
- ✅ Comprehensive documentation
- ✅ Automated deployment scripts
- ✅ Validation tooling

## 📞 Getting Help

1. Check this index for relevant documentation
2. Review [QUICKSTART.md](QUICKSTART.md) for common tasks
3. See [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting
4. Run `./validate.sh` for diagnostics
5. Check pod logs and events

---

**Last Updated**: 2026-02-08
**Chart Version**: 1.0.0
**Maintained by**: Phase5 Team

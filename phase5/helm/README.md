# Phase 5 Helm Charts

Production-ready Kubernetes deployment for Phase V Cloud-Native Todo Application.

## 🚀 Quick Start

```bash
# Local deployment (10 minutes)
cd helm
./deploy-local.sh
```

**That's it!** The script will guide you through the setup.

## 📚 Documentation

Start with the right guide for your needs:

| Document | Purpose | Audience |
|----------|---------|----------|
| [INDEX.md](INDEX.md) | Navigation hub for all files | Everyone |
| [QUICKSTART.md](QUICKSTART.md) | Get running in 10 minutes | Developers |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Full deployment procedures | DevOps/SRE |
| [HELM_CHARTS_SUMMARY.md](HELM_CHARTS_SUMMARY.md) | Technical implementation | Architects |
| [phase5/README.md](phase5/README.md) | Chart reference | Platform Engineers |

## 🏗️ What's Included

### Architecture

```
┌─────────────────────────────────────────────┐
│           NGINX Ingress (TLS)               │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┴─────────────┬─────────────┐
    │                           │             │
┌───▼────┐               ┌──────▼──────┐     │
│Frontend│               │  Chat API   │     │
│Next.js │               │  (Dapr)     │     │
└────────┘               └──────┬──────┘     │
                                │            │
                    ┌───────────┴──────┐     │
                    │   Dapr Runtime   │     │
                    └───────┬──────────┘     │
                            │                │
    ┌───────────────────────┼────────────────┘
    │                       │
┌───▼──────────┐    ┌──────▼───────┐
│  PostgreSQL  │    │    Kafka     │
│  (State +    │    │  (Pub/Sub +  │
│   Data)      │    │   Events)    │
└──────────────┘    └──────────────┘
```

### Services (6 microservices)

- **chat-api** - Main API with AI chat capabilities
- **notification-service** - Push notifications and reminders
- **recurring-task-service** - Scheduled task management
- **audit-service** - Compliance and event logging
- **websocket-sync-service** - Real-time synchronization
- **frontend** - Next.js user interface

### Infrastructure

- **PostgreSQL** - Primary database (Bitnami chart)
- **Kafka** - Event streaming platform (Bitnami chart)
- **Dapr** - Microservices runtime with sidecars
- **NGINX Ingress** - Load balancing and TLS

### Dapr Components

- Pub/Sub (Kafka)
- State Store (PostgreSQL)
- Secret Store (Kubernetes)
- Cron Bindings (2x - tasks and reminders)
- Configuration (mTLS, tracing, access control)

## 📦 Files Created

**71 files total** including:

- **1 umbrella chart** with 8 dependencies
- **6 service subcharts** (each with 8 templates)
- **6 Dapr components** + 1 configuration
- **3 secrets templates**
- **3 deployment scripts** (deploy-local, deploy-oke, validate)
- **5 documentation files**

## 🎯 Features

✅ **Production Ready**
- High availability (pod anti-affinity)
- Horizontal autoscaling (2-10+ replicas)
- Rolling updates (zero downtime)
- Health and readiness probes
- Resource limits and quotas

✅ **Secure**
- Non-root containers
- Dropped capabilities
- Dapr mTLS enabled
- Secret management
- Network isolation

✅ **Observable**
- Health check endpoints
- Prometheus metrics (via Dapr)
- Distributed tracing (Zipkin)
- Structured logging
- Dapr dashboard

✅ **Cloud Native**
- Kubernetes-native resources
- Dapr sidecar pattern
- Service mesh ready
- GitOps compatible
- Multi-environment support

## 🔧 Quick Commands

```bash
# Deploy locally
./deploy-local.sh

# Deploy to OKE
./deploy-oke.sh

# Validate deployment
./validate.sh phase5 phase5

# View status
kubectl get pods -n phase5

# View logs
kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f

# Access frontend
kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000

# Dapr dashboard
dapr dashboard -k

# Uninstall
helm uninstall phase5 -n phase5
```

## 📋 Prerequisites

### Required Tools

- **kubectl** v1.24+ ([install](https://kubernetes.io/docs/tasks/tools/))
- **Helm** v3.8+ ([install](https://helm.sh/docs/intro/install/))
- **Dapr CLI** v1.12+ ([install](https://docs.dapr.io/getting-started/install-dapr-cli/))
- **Docker** (for building images)

### Infrastructure

**Local Development:**
- Minikube, kind, or Docker Desktop with Kubernetes
- 4+ CPU cores, 8GB+ RAM recommended

**Production (Oracle OKE):**
- OKE cluster with 3+ worker nodes
- Oracle Cloud CLI ([install](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm))
- OCIR access for container images

## 🚦 Deployment Flow

### Local (Minikube/kind)

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Install Dapr
dapr init -k

# 3. Build and load images
docker build -t phase5/chat-api:latest ./services/chat-api
minikube image load phase5/chat-api:latest
# ... repeat for other services

# 4. Deploy
cd helm
./deploy-local.sh

# 5. Access
kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000
```

### Oracle OKE

```bash
# 1. Configure kubectl for OKE
oci ce cluster create-kubeconfig --cluster-id <cluster-ocid> ...

# 2. Build and push images to OCIR
docker tag phase5/chat-api:1.0.0 iad.ocir.io/<tenancy>/phase5/chat-api:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/chat-api:1.0.0
# ... repeat for other services

# 3. Deploy
cd helm
./deploy-oke.sh

# 4. Configure DNS
# Point your domain to the Load Balancer IP

# 5. Access
open https://phase5.oraclecloud.com
```

## ✅ Validation

After deployment, run:

```bash
./validate.sh phase5 phase5
```

This checks:
- ✓ Namespace and Helm release
- ✓ Dapr installation and components
- ✓ Pod status (all services)
- ✓ Infrastructure (PostgreSQL, Kafka)
- ✓ Services and endpoints
- ✓ Secrets
- ✓ Ingress and Load Balancer
- ✓ Autoscaling (HPA)
- ✓ Health endpoints
- ✓ Persistent volumes

Expected result: **All checks pass** 🎉

## 🐛 Troubleshooting

### Quick Diagnostics

```bash
# Check everything
./validate.sh

# Pod status
kubectl get pods -n phase5

# Pod details
kubectl describe pod <pod-name> -n phase5

# Logs (application)
kubectl logs <pod-name> -n phase5 -c <service-name>

# Logs (Dapr sidecar)
kubectl logs <pod-name> -n phase5 -c daprd

# Events
kubectl get events -n phase5 --sort-by='.lastTimestamp'

# Dapr status
dapr status -k

# Components
kubectl get components -n phase5
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Pods pending | Check node resources: `kubectl describe nodes` |
| Image pull errors | Verify image exists and pull secret is correct |
| Dapr not injecting | Ensure Dapr is installed: `dapr status -k` |
| Database connection | Check PostgreSQL pod and secret |
| Ingress not working | Verify NGINX controller and DNS |

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting.

## 📊 Resource Requirements

### Minimum (Local Dev)

- **CPU**: 4 cores
- **Memory**: 8 GB
- **Storage**: 20 GB

### Recommended (Production)

- **CPU**: 8+ cores
- **Memory**: 16+ GB
- **Storage**: 100+ GB (for PostgreSQL and Kafka)
- **Nodes**: 3+ (for high availability)

### Per-Service Resources

| Service | Memory | CPU | Replicas |
|---------|--------|-----|----------|
| chat-api | 256Mi-512Mi | 100m-500m | 2-10 |
| notification | 128Mi-256Mi | 50m-250m | 2-8 |
| recurring-task | 128Mi-256Mi | 50m-250m | 1-4 |
| audit | 128Mi-256Mi | 50m-250m | 2-6 |
| websocket-sync | 256Mi-512Mi | 100m-500m | 2-10 |
| frontend | 256Mi-512Mi | 100m-500m | 2-10 |

Autoscaling based on CPU (70%) and memory (80%) utilization.

## 🔐 Security

- **Pod Security**: Non-root users, dropped capabilities
- **Network**: Dapr mTLS, service-to-service authentication
- **Secrets**: Kubernetes secrets (externalize in production)
- **RBAC**: Service accounts with minimal permissions
- **Ingress**: TLS termination, cert-manager integration

**⚠️ Important**: Replace default secrets in production!

## 🎓 Learn More

### Documentation

- [INDEX.md](INDEX.md) - Complete file navigation
- [QUICKSTART.md](QUICKSTART.md) - 10-minute guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment procedures
- [HELM_CHARTS_SUMMARY.md](HELM_CHARTS_SUMMARY.md) - Implementation details
- [phase5/README.md](phase5/README.md) - Chart reference

### External Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Dapr Documentation](https://docs.dapr.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Oracle OKE](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)

## 🤝 Contributing

When adding new services:

1. Copy an existing subchart template
2. Update service-specific values
3. Add to `Chart.yaml` dependencies
4. Update Dapr component scopes
5. Update documentation

## 📝 Configuration

### Values Files

- `values.yaml` - Base configuration (all environments)
- `values-oke.yaml` - Oracle OKE overrides
- Create custom files for other environments

### Customization

```bash
# Deploy with custom values
helm install phase5 ./phase5 \
  -f values.yaml \
  -f values-oke.yaml \
  -f values-custom.yaml \
  -n phase5
```

## 🚀 Next Steps

After successful deployment:

1. **CI/CD Integration** - Automate deployments
2. **Monitoring** - Deploy Prometheus and Grafana
3. **Backup** - Configure PostgreSQL backups
4. **Performance Testing** - Load test with k6
5. **Security Hardening** - Network policies, vulnerability scanning

## 📞 Support

1. Check [INDEX.md](INDEX.md) for navigation
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting
3. Run `./validate.sh` for diagnostics
4. Check pod logs and events

## 📄 License

MIT

---

**Chart Version**: 1.0.0
**Last Updated**: 2026-02-08
**Maintained by**: Phase5 Team

**Ready to deploy?** Start with [QUICKSTART.md](QUICKSTART.md)! 🚀

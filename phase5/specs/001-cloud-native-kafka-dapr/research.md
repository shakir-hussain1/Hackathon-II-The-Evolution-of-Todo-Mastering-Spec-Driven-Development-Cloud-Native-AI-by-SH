# Research & Technology Decisions: Phase V

**Feature**: 001-cloud-native-kafka-dapr
**Date**: 2026-02-08
**Purpose**: Document all technology choices, alternatives considered, and rationale for Phase V implementation

## Executive Summary

Phase V introduces **event-driven microservices** with **Kafka** for event streaming and **Dapr** for portable service abstractions. Key decisions prioritize **rapid Minikube deployment** for hackathon demo (Feb 9 deadline) while maintaining **production-ready architecture patterns**.

**Critical Path**: Minikube → Redpanda → Dapr → 6 Microservices → Helm Chart → Demo

---

## Decision 1: Kafka Provider Selection

### Context
Need Kafka-compatible message broker for event-driven architecture. Must work locally (Minikube) and optionally in cloud.

### Options Evaluated

| Option | Pros | Cons | Cost | Timeline Impact |
|--------|------|------|------|-----------------|
| **Strimzi (Kafka on K8s)** | Production Kafka, operator-based, multi-cloud | Heavy (3 brokers + ZooKeeper), slow startup (3-5 min) | Free | +2 hours setup |
| **Redpanda** | Fast startup (<1 min), lightweight, Kafka API compatible | Less mature, smaller community | Free | +30 min setup |
| **Confluent Cloud** | Managed, zero-ops, enterprise features | Costs $$$, requires account | $1+/hour | +1 hour setup |
| **Azure Event Hubs** | Kafka protocol, Azure-native | Azure lock-in, costs $$ | $10+/month | +2 hours setup |

### Decision

**Primary**: **Redpanda** for Minikube (local demo)
**Secondary**: **Strimzi** for cloud deployment (if time allows)

### Rationale

**For Minikube (Priority 1)**:
- **Speed**: Redpanda starts in <1 minute vs 3-5 minutes for Strimzi (critical for demo debugging cycles)
- **Resources**: Single container vs 4+ containers (ZooKeeper + 3 Kafka brokers) - important for laptop demo
- **Simplicity**: No ZooKeeper coordination, simpler troubleshooting
- **Compatibility**: 100% Kafka API compatible - works identically through Dapr Pub/Sub

**For Cloud (Priority 2, time-permitting)**:
- **Strimzi**: Demonstrates production Kafka patterns, Kubernetes operators, true Kafka ecosystem
- **Learning value**: More relevant for real-world cloud deployments

**Dapr Abstraction Validates**: Both Redpanda and Kafka work identically through Dapr Pub/Sub component - proving portability claim.

### Alternatives Rejected

- **Confluent Cloud**: Rejected due to cost ($$$) and hackathon doesn't need managed service
- **Azure Event Hubs**: Rejected due to Azure lock-in and added complexity for Minikube
- **RabbitMQ**: Rejected - not Kafka-compatible, different semantics

### Implementation Notes

**Minikube Deployment** (Redpanda):
```bash
# Redpanda Helm chart
helm repo add redpanda https://charts.redpanda.com/
helm install redpanda redpanda/redpanda \
  --set replicas=1 \
  --set resources.requests.memory=1Gi
```

**Cloud Deployment** (Strimzi):
```bash
# Strimzi operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'
# Then apply Kafka CR
```

---

## Decision 2: Dapr Components Configuration

### Context
Dapr provides portable abstractions. Need to select which Dapr building blocks to use and how to configure them.

### Required Dapr Components

#### 1. Pub/Sub (Kafka/Redpanda)

**Component**: `pubsub.kafka`

**Purpose**: Event publishing and subscription for all microservices

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda:9092"  # or "kafka:9092" for Strimzi
  - name: consumerGroup
    value: "todo-chatbot-consumers"
  - name: authType
    value: "none"  # SASL for production
```

**Rationale**: Core requirement for event-driven architecture. Kafka chosen over Redis Pub/Sub for durability and replay capabilities.

---

#### 2. State Management (Redis)

**Component**: `state.redis`

**Purpose**: Distributed caching (user preferences, recent tasks, session data)

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-master:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
  - name: actorStateStore
    value: "true"
```

**Rationale**: Redis for fast key-value access. Alternative PostgreSQL state store considered but Redis is faster for caching use case.

**Optional**: Can defer if time-constrained - not critical path for MVP.

---

#### 3. Secrets Store (Kubernetes)

**Component**: `secretstores.kubernetes`

**Purpose**: Retrieve secrets (DB passwords, JWT secrets, API keys) securely

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: defaultNamespace
    value: "default"
```

**Rationale**: Kubernetes Secrets for Minikube (simple). Cloud providers can override with Azure Key Vault / GCP Secret Manager / Oracle Vault without code changes.

---

#### 4. Cron Binding

**Component**: `bindings.cron`

**Purpose**: Trigger recurring task scheduler every 5 minutes

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: recurring-task-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/5 * * * *"  # Every 5 minutes
  - name: direction
    value: "input"
```

**Rationale**: Cron binding is simpler than Kubernetes CronJobs for this use case. Service listens on Dapr endpoint and processes recurring tasks.

---

#### 5. Service Invocation (Built-in)

**Component**: Built-in Dapr feature (no manifest needed)

**Purpose**: Service-to-service communication with retries and circuit breakers

**Usage**:
```python
# Chat API calls Notification Service (if needed)
dapr_client.invoke_method(
    app_id="notification-service",
    method_name="send-notification",
    data=payload
)
```

**Rationale**: Dapr service invocation provides mTLS, retries, and tracing automatically. Alternative (direct HTTP) loses these benefits.

---

### Decision Summary

**5 Dapr Components Implemented**:
1. ✅ Pub/Sub (Kafka) - CRITICAL PATH
2. ⚠️ State (Redis) - Nice to have, defer if time-constrained
3. ✅ Secrets (Kubernetes) - CRITICAL PATH
4. ✅ Cron Binding - REQUIRED for recurring tasks
5. ✅ Service Invocation - Built-in, use if needed

**Priority**: Focus on Pub/Sub and Secrets first. State and Cron are secondary.

---

## Decision 3: Cloud Platform Selection

### Context
Need cloud Kubernetes platform for potential cloud deployment (secondary goal after Minikube).

### Options Evaluated

| Platform | Free Tier | Cost After Free | K8s Version | Setup Complexity | Learning Value |
|----------|-----------|-----------------|-------------|------------------|----------------|
| **Azure AKS** | 1 free cluster | $0.10/hour | 1.28+ | Medium (Azure CLI) | High (Azure ecosystem) |
| **Google GKE** | $300 credit (expires) | $0.10/hour | 1.28+ | Medium (gcloud CLI) | High (Google invented K8s) |
| **Oracle OKE** | Always-free (2 OCPUs) | $0.05/hour | 1.28+ | Low (standard K8s) | Medium (Oracle Cloud) |
| **DigitalOcean DOKS** | No free tier | $0.01/hour/node | 1.27+ | Low (simple UI) | Low (managed, less control) |

### Decision

**Primary Target**: **Minikube** (local demo - MUST WORK)
**Secondary Target**: **Oracle OKE** (if time allows - always-free tier)

### Rationale

**Minikube Priority**:
- **Deadline**: Feb 9 - Minikube guarantees working demo regardless of cloud access
- **Reproducibility**: Judges can run locally without cloud accounts
- **Cost**: $0 - no credit card required
- **Control**: Full control over cluster configuration

**Oracle OKE Secondary**:
- **Always-free**: 2 OCPUs, 12GB RAM - no expiration (unlike GCP $300 credit)
- **Learning**: Good post-hackathon learning platform
- **Simplicity**: Standard Kubernetes, no Azure/GCP-specific complexities

**Deferred**:
- **AKS/GKE**: Valuable for learning but time-constrained. Cloud deployment is bonus, not required.

### Implementation Priority

1. **Day 1 (Feb 8-9)**: Focus 100% on Minikube
2. **Post-hackathon**: Add OKE deployment with Helm values override
3. **Future**: Add AKS/GKE with cloud-specific configurations

---

## Decision 4: Database Strategy

### Context
Microservices best practice: database-per-service. Reality: time-constrained setup.

### Options Evaluated

| Strategy | Pros | Cons | Setup Time | Microservices Alignment |
|----------|------|------|------------|-------------------------|
| **Shared PostgreSQL** | Simple, fast setup | Coupling, shared schema | 30 min | ❌ Violates pattern |
| **Separate Schemas** | Logical isolation, single instance | Still shared infrastructure | 1 hour | ⚠️ Pragmatic compromise |
| **Database-per-Service** | True isolation, independent scaling | 6 PostgreSQL instances, complex | 3-4 hours | ✅ Ideal pattern |

### Decision

**Single PostgreSQL instance with separate schemas** (pragmatic compromise)

### Rationale

**For Hackathon MVP**:
- **Time**: Setting up 6 separate PostgreSQL instances takes 3-4 hours (infra, networking, secrets)
- **Resources**: 6 PostgreSQL pods consume significant Minikube resources (6-12GB RAM)
- **Complexity**: More YAML, more secrets, more troubleshooting surface

**Microservices Compliance**:
- **Logical isolation**: Each service has its own schema/database (task_db, audit_db, notification_db)
- **Access control**: Services don't access each other's schemas (enforced by code review, not DB permissions)
- **Migration path**: Easy to split to separate instances later (connection string change only)

**Dapr Alignment**:
- Services access database via connection strings from Dapr Secrets
- Future: Can add Dapr State Store abstraction (removes direct DB access entirely)

### Schema Design

```sql
-- task_db schema (owned by Chat API)
CREATE SCHEMA task_db;
CREATE TABLE task_db.users (...);
CREATE TABLE task_db.tasks (...);
CREATE TABLE task_db.reminders (...);

-- audit_db schema (owned by Audit Service)
CREATE SCHEMA audit_db;
CREATE TABLE audit_db.audit_logs (...);

-- notification_db schema (owned by Notification Service)
CREATE SCHEMA notification_db;
CREATE TABLE notification_db.notifications (...);
```

### Future Migration

**Post-hackathon**: Split to separate databases by updating Helm values:
```yaml
# From single PostgreSQL
postgresql:
  enabled: true
  auth:
    database: todo_db

# To database-per-service
chat-api:
  database:
    host: chat-api-postgres
    name: task_db

audit-service:
  database:
    host: audit-postgres
    name: audit_db
```

---

## Decision 5: CI/CD Platform

### Context
Need automated build, test, and deployment pipelines.

### Options Evaluated

| Platform | Free Tier | Integration | Ease of Use | YAML Config |
|----------|-----------|-------------|-------------|-------------|
| **GitHub Actions** | 2000 min/month | Native GitHub | High | ✅ Yes |
| **GitLab CI** | 400 min/month | Requires GitLab | Medium | ✅ Yes |
| **Jenkins** | Unlimited (self-hosted) | Any Git | Low (complex setup) | ❌ Groovy |
| **CircleCI** | 6000 min/month | Via webhook | High | ✅ Yes |

### Decision

**GitHub Actions** (repository already on GitHub)

### Rationale

**Advantages**:
- **Integration**: Repository already on GitHub, no migration needed
- **Familiarity**: Used in Phase II/III for basic CI
- **Free tier**: 2000 minutes/month sufficient for hackathon
- **Ecosystem**: GitHub Container Registry, GitHub Releases built-in
- **YAML**: Easy to version control and review

**Pipeline Structure**:
```yaml
# .github/workflows/ci.yaml
on: [push, pull_request]
jobs:
  test:
    - Run pytest (backend)
    - Run npm test (frontend)
  build:
    - Build Docker images
    - Scan with Trivy
    - Push to registry
  deploy-minikube:
    - Deploy to local Minikube (for testing)
```

### Alternatives Rejected

- **GitLab CI**: Requires repository migration (time-consuming)
- **Jenkins**: Self-hosted complexity not worth it for hackathon
- **CircleCI**: No compelling advantage over GitHub Actions

---

## Decision 6: Monitoring Stack

### Context
Need observability for distributed microservices and event flows.

### Options Evaluated

| Stack | Components | Setup Time | Resource Usage | Demo Value |
|-------|------------|------------|----------------|------------|
| **Full Stack** | Prometheus + Grafana + Jaeger + Loki + AlertManager | 4-6 hours | 2-4GB RAM | High (impressive) |
| **Minimal** | Zipkin + Prometheus + JSON logs | 1-2 hours | 512MB-1GB | Medium (functional) |
| **Dapr Observability** | Dapr Dashboard + Zipkin | 30 min | 256MB | Medium (Dapr-native) |

### Decision

**Minimal stack with Dapr integration**: Zipkin + Prometheus + JSON logs

### Rationale

**For Hackathon Demo**:
- **Zipkin**: Visual trace of event flows (impressive for judges) - shows request through all services
- **Prometheus**: Dapr exports metrics automatically - no extra work
- **JSON logs**: `kubectl logs` sufficient for debugging during demo
- **Dapr Dashboard**: Built-in, shows sidecar health and component status

**Deferred (Post-Demo)**:
- **Grafana**: Beautiful dashboards but 2-4 hours to create meaningful visualizations
- **Loki**: Centralized logging nice-to-have, not demo-critical
- **AlertManager**: Production feature, not needed for hackathon demo

### Setup

**Zipkin** (Dapr-integrated):
```bash
# Zipkin automatically configured with Dapr
helm install zipkin openzipkin/zipkin
# Dapr config
dapr_config:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
```

**Prometheus** (Dapr metrics):
```bash
# Prometheus scrapes Dapr metrics endpoints automatically
helm install prometheus prometheus-community/prometheus
# Dapr metrics: http://localhost:9090/metrics
```

### Demo Script

1. Create task via chat interface
2. Open Zipkin UI
3. Show trace: Frontend → Chat API → Kafka → Audit Service → WebSocket Sync
4. Show timing for each hop
5. Show correlation ID linking all spans

**Impact**: Visual proof of event-driven architecture working across all services.

---

## Decision 7: Helm Chart Strategy

### Context
Need to deploy 6 microservices + infrastructure (Kafka, Redis, PostgreSQL, Zipkin) to Kubernetes.

### Options Evaluated

| Strategy | Pros | Cons | Complexity | Best Practice |
|----------|------|------|------------|---------------|
| **Raw YAML** | Simple, explicit | Hard to manage versions, no templating | Low | ❌ Not scalable |
| **Kustomize** | Overlay-based, native K8s | Limited templating, less familiar | Medium | ⚠️ K8s-native but limited |
| **Monolithic Helm Chart** | Single chart, simple | Hard to version services independently | Medium | ⚠️ Not microservices-aligned |
| **Umbrella Helm Chart** | Subcharts per service, independent versioning | More complex structure | High | ✅ Microservices best practice |

### Decision

**Umbrella Helm Chart** with subcharts per service

### Rationale

**Microservices Alignment**:
- Each service has its own subchart (can version/release independently)
- Subcharts are reusable (can extract and publish separately)
- Follows Helm best practices for complex applications

**Complexity Justified**:
- **Learning value**: Proper Helm usage for microservices
- **Scalability**: Easy to add new services (create new subchart)
- **Minikube friendly**: Still deploys with single `helm install` command

**Structure**:
```
helm/todo-chatbot/              # Umbrella chart
├── Chart.yaml                  # Parent chart metadata
├── values.yaml                 # Default values (Minikube)
├── values-minikube.yaml       # Minikube overrides
├── values-aks.yaml            # Azure overrides
├── values-gke.yaml            # GCP overrides
├── templates/
│   ├── namespace.yaml
│   └── dapr-components/       # Dapr component manifests
└── charts/                    # Subcharts
    ├── frontend/              # Next.js
    ├── chat-api/              # FastAPI
    ├── notification/
    ├── recurring-task/
    ├── audit/
    ├── websocket-sync/
    ├── postgresql/            # Bitnami PostgreSQL
    ├── redpanda/              # Redpanda Kafka
    ├── redis/                 # Redis
    └── zipkin/                # Zipkin
```

**Deployment**:
```bash
# Single command deploys entire stack
helm install todo-chatbot ./helm/todo-chatbot \
  --values ./helm/todo-chatbot/values-minikube.yaml

# Or with overrides
helm install todo-chatbot ./helm/todo-chatbot \
  --set global.environment=production \
  --set redis.enabled=false  # Disable Redis for MVP
```

### Alternatives Rejected

- **Raw YAML**: Too brittle, no templating (rejected)
- **Kustomize**: Good for simple apps, but Helm is standard for complex microservices
- **Monolithic chart**: Doesn't align with microservices independence

---

## Decision 8: Event Schema Design

### Context
Need standardized event format for Kafka messages across all services.

### Options Evaluated

| Standard | Pros | Cons | Adoption |
|----------|------|------|----------|
| **Custom JSON** | Full control, simple | No standard, reinvent wheel | Low |
| **CloudEvents** | Industry standard, tooling support | More verbose | High |
| **Avro** | Schema evolution, compact | Requires registry, complex | Medium |

### Decision

**CloudEvents 1.0 specification**

### Rationale

**Industry Standard**:
- CNCF standard for event data
- Tooling support (validators, SDKs)
- Language-agnostic

**Structure** (all events):
```json
{
  "specversion": "1.0",
  "type": "com.todo.task.created",
  "source": "chat-api-service",
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "time": "2026-02-08T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "uuid",
    "user_id": "uuid",
    "title": "Finish Phase V",
    "priority": "high",
    "due_date": "2026-02-09T23:59:59Z",
    "tags": ["hackathon", "urgent"],
    "created_at": "2026-02-08T10:30:00Z"
  },
  "correlationid": "trace-abc123",
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
}
```

**Key Fields**:
- `type`: Hierarchical event type (com.todo.task.created)
- `source`: Originating service (for debugging)
- `id`: Unique event ID (idempotency)
- `time`: ISO8601 timestamp (event time)
- `data`: Actual payload (business data)
- `correlationid`: Links related events (business trace)
- `traceparent`: W3C Trace Context (distributed tracing)

**Event Types**:
- `com.todo.task.created`
- `com.todo.task.updated`
- `com.todo.task.completed`
- `com.todo.task.deleted`
- `com.todo.reminder.due`
- `com.todo.task.sync`

### Alternatives Rejected

- **Custom JSON**: Not standard, harder to validate
- **Avro**: Requires schema registry (added complexity), overkill for hackathon

---

## Technology Stack Summary

### Confirmed Stack

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Message Broker** | Redpanda (Minikube), Strimzi (Cloud) | Latest | Fast, lightweight, Kafka-compatible |
| **Runtime Abstraction** | Dapr | 1.12+ | Portability, service abstraction, resiliency patterns |
| **Orchestration** | Kubernetes (Minikube) | 1.28+ | Industry standard, local dev parity |
| **Package Manager** | Helm | 3.13+ | Umbrella chart for microservices |
| **Database** | PostgreSQL | 15+ | ACID, mature, separate schemas per service |
| **Caching** | Redis | 7+ | Dapr state store (optional for MVP) |
| **Tracing** | Zipkin | Latest | Visual event flows, Dapr-integrated |
| **Metrics** | Prometheus | Latest | Dapr exports automatically |
| **CI/CD** | GitHub Actions | N/A | Native integration, free tier |
| **Frontend** | Next.js + React | 16+/19+ | From Phase III |
| **Backend** | FastAPI + Python | 0.110+/3.11+ | From Phase III |
| **AI** | OpenAI GPT-4 | Latest | From Phase III |

### MVP Prioritization

**MUST HAVE (P1)**:
- ✅ Redpanda (Kafka)
- ✅ Dapr (Pub/Sub, Secrets)
- ✅ PostgreSQL (single instance, separate schemas)
- ✅ Zipkin (tracing)
- ✅ Helm (umbrella chart)
- ✅ Minikube (local deployment)

**NICE TO HAVE (P2)**:
- ⚠️ Redis (Dapr state store) - defer if time-constrained
- ⚠️ Prometheus (metrics) - Dapr exports automatically, can skip dashboards
- ⚠️ Cloud deployment (OKE) - bonus, not required

**POST-DEMO (P3)**:
- ❌ Grafana (dashboards)
- ❌ Loki (centralized logging)
- ❌ AlertManager (alerting)
- ❌ Multi-cloud (AKS, GKE)

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Dapr learning curve steep | Medium | High | Use Dapr quickstarts, official examples |
| Kafka event flows complex | Medium | Medium | Start with single event type, expand gradually |
| Minikube resource exhaustion | High | High | Limit replicas to 1, use resource limits |
| Helm chart complexity | Medium | Medium | Use Bitnami subcharts where possible |
| Time overrun (1 day) | High | Critical | MVP scope ruthlessly enforced, defer P2/P3 |

### Timeline Risks

**Critical Path**: Minikube → Redpanda → Dapr Pub/Sub → Event Publishing → 1 Consumer → Demo

**Fallback Plan** (if < 6 hours remaining):
1. Skip recurring tasks (defer)
2. Skip notification service (defer)
3. Skip WebSocket sync (defer)
4. Minimum viable demo: Task CRUD + Events + Audit Log + Zipkin Trace

**Success Criteria**: Working demo of event-driven architecture with Kafka + Dapr by Feb 9 deadline.

---

## Next Actions

1. ✅ **Complete**: Research & Technology Decisions (this document)
2. 🔄 **Next**: Create `data-model.md` (database schemas)
3. 🔄 **Next**: Create `quickstart.md` (local setup guide)
4. 🔄 **Next**: Create `contracts/` (API specs, event schemas)
5. 🔄 **Next**: Run `/sp.tasks` to generate TDD task breakdown

**Timeline**: Research complete. Design phase (data model, contracts) should take 2-3 hours.

---

**Research Complete**: ✅ All 8 technology decisions documented with rationale, alternatives considered, and ADRs outlined.

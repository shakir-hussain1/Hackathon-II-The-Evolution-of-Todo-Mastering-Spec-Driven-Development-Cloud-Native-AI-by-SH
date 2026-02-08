# Feature Specification: Phase V – Advanced Cloud-Native Todo System with Kafka & Dapr

**Feature Branch**: `001-cloud-native-kafka-dapr`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Phase V – Advanced Cloud-Native Todo System with Kafka & Dapr - Event-driven microservices architecture with advanced task intelligence, Dapr-based service abstraction, production-grade Kubernetes deployment, and CI/CD automation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Advanced Task Management with Intelligence (Priority: P1)

As a user, I want to create and manage tasks with advanced features (recurring, due dates, priorities, tags) so that I can organize my work more effectively and never miss important deadlines.

**Why this priority**: Core value proposition - provides immediate user value and differentiates from basic todo apps. Forms the foundation for all event-driven features.

**Independent Test**: Can be fully tested by creating tasks with all advanced attributes through the chat interface, verifying they persist across sessions, and confirming smart search/filter/sort capabilities work correctly.

**Acceptance Scenarios**:

1. **Given** user is authenticated and in the chat interface, **When** user says "Create a high-priority task 'Finish report' due Friday with tags work and urgent", **Then** task is created with priority=high, due_date=next Friday, tags=[work, urgent], and AI confirms creation with all details
2. **Given** user has tasks with various priorities and due dates, **When** user says "Show me high priority tasks due this week", **Then** system returns filtered list of high-priority tasks with due dates in current week, sorted by due date
3. **Given** user creates a recurring task "Team standup every Monday at 9 AM", **When** the system processes the recurring pattern, **Then** task instances are automatically created for future Mondays and appear in the task list
4. **Given** user has tasks with tags, **When** user searches "find all tasks tagged 'urgent'", **Then** system returns all tasks with the 'urgent' tag using full-text search
5. **Given** a task has a due date approaching (within 24 hours), **When** the reminder system checks due dates, **Then** user receives a notification via the configured channel (in-app, email, or push)

---

### User Story 2 - Event-Driven Real-Time Synchronization (Priority: P2)

As a user accessing the application from multiple devices/tabs, I want all task changes to appear in real-time across all my sessions so that I always see the most current state of my tasks.

**Why this priority**: Differentiates cloud-native architecture from traditional apps. Demonstrates event-driven capabilities and provides excellent user experience for multi-device workflows.

**Independent Test**: Can be tested by opening two browser tabs, making changes in one tab (create/update/delete tasks), and verifying the changes appear instantly in the second tab without manual refresh.

**Acceptance Scenarios**:

1. **Given** user has two browser tabs open with the todo application, **When** user creates a task in tab 1, **Then** the new task appears in tab 2 within 2 seconds via WebSocket sync
2. **Given** user completes a task in the mobile view, **When** the completion event is published to Kafka, **Then** all connected desktop sessions receive the update and mark the task as complete
3. **Given** user deletes a task in one session, **When** the delete event propagates through the system, **Then** the task disappears from all other active sessions and the audit log records the deletion
4. **Given** the WebSocket connection is temporarily lost, **When** connection is restored, **Then** the system syncs any missed events and brings the UI to current state
5. **Given** multiple users are collaborating (future: shared lists), **When** one user updates a task, **Then** all collaborators see the update in real-time

---

### User Story 3 - Microservices Observability and Monitoring (Priority: P3)

As a DevOps engineer or system operator, I want to monitor system health, trace distributed transactions, and debug issues across microservices so that I can ensure high availability and quickly resolve problems.

**Why this priority**: Critical for production operations but doesn't block user-facing features. Essential for demonstrating cloud-native maturity and operational excellence.

**Independent Test**: Can be tested by accessing Grafana dashboards, viewing service metrics, tracing a request through Jaeger, checking alert rules in AlertManager, and querying logs in Loki/ELK with correlation IDs.

**Acceptance Scenarios**:

1. **Given** all microservices are deployed, **When** operator accesses Grafana dashboards, **Then** all service metrics (CPU, memory, request rate, error rate, latency) are visible with real-time updates
2. **Given** user creates a task through the chat interface, **When** operator traces the request through Jaeger, **Then** complete trace shows: Frontend → Chat API → Event Published → Notification Service → Audit Service with timing for each hop
3. **Given** a service experiences high error rates, **When** error threshold is exceeded, **Then** AlertManager fires an alert and sends notification to configured channels (Slack, email, PagerDuty)
4. **Given** operator needs to debug a specific user's task creation failure, **When** querying logs with correlation ID, **Then** logs from all services involved in that transaction are returned with timestamps and context
5. **Given** system is under load, **When** Kafka consumer lag increases beyond threshold, **Then** monitoring dashboard highlights the lagging consumer and HPA scales the consumer pods automatically

---

### User Story 4 - Multi-Environment Deployment with CI/CD (Priority: P4)

As a development team, we want automated deployment pipelines that can deploy to local (Minikube), staging, and production environments so that we can rapidly iterate while maintaining production stability.

**Why this priority**: Enables team velocity and demonstrates DevOps maturity. Not user-facing but critical for sustainable development.

**Independent Test**: Can be tested by pushing code to GitHub, triggering CI/CD pipeline, observing automated tests/builds/deployments, and verifying successful deployment to target environment with health checks passing.

**Acceptance Scenarios**:

1. **Given** developer pushes code to feature branch, **When** GitHub Actions CI pipeline runs, **Then** all tests pass, Docker images are built, security scans complete (Trivy), and PR is marked as ready for review
2. **Given** PR is merged to main branch, **When** CD pipeline executes, **Then** Helm charts are updated, deployed to staging environment, smoke tests run automatically, and deployment status is reported
3. **Given** staging deployment is successful, **When** manual approval is given, **Then** production deployment executes with blue-green strategy, health checks validate new pods, and traffic shifts gradually
4. **Given** production deployment encounters issues, **When** health checks fail or error rate spikes, **Then** automatic rollback is triggered, previous version is restored, and incident is logged with details
5. **Given** developer wants to test locally, **When** running `make minikube-deploy`, **Then** entire stack (Kafka, Dapr, all services, monitoring) deploys to Minikube and is accessible via localhost URLs

---

### User Story 5 - Cloud-Native Portability and Infrastructure (Priority: P5)

As a platform engineer, I want the system to deploy identically across different cloud providers (AKS, GKE, OKE) and local Minikube so that we avoid vendor lock-in and can choose the best platform for our needs.

**Why this priority**: Demonstrates cloud-native principles and Dapr's portability promise. Important for architecture validation but not immediately user-facing.

**Independent Test**: Can be tested by deploying the same Helm charts to Minikube, AKS, GKE, and OKE, verifying all services start successfully, Dapr components work correctly, and functional tests pass in all environments.

**Acceptance Scenarios**:

1. **Given** Helm charts with Dapr components, **When** deploying to AKS using Azure Managed Kafka, **Then** all services start, Dapr sidecars inject successfully, Pub/Sub connects to Azure Kafka, and system passes health checks
2. **Given** same Helm charts, **When** deploying to GKE with Confluent Cloud Kafka, **Then** Dapr reconfigures for GCP, connects to Confluent Cloud, secrets are pulled from GCP Secret Manager, and system is fully operational
3. **Given** deployment to Oracle OKE, **When** using Strimzi for Kafka, **Then** Strimzi operator provisions Kafka cluster, Dapr components connect via Kubernetes service discovery, and event flows work end-to-end
4. **Given** local Minikube deployment, **When** using Redpanda instead of Kafka, **Then** Dapr Pub/Sub adapter works with Redpanda, all event flows function identically to cloud deployments, and developer can test complete system locally
5. **Given** switching between cloud providers, **When** updating Helm values for target platform, **Then** only platform-specific settings change (managed services, ingress controllers), application code remains unchanged, and deployment succeeds

---

### Edge Cases

- **Network Partitions**: What happens when a microservice loses connection to Kafka? System MUST retry with exponential backoff via Dapr resiliency policies, eventually dead-letter the message, and alert operators.
- **Kafka Consumer Lag**: What happens when Notification Service falls behind processing events? System MUST scale horizontally via HPA based on consumer lag metrics, and monitoring MUST alert when lag exceeds threshold.
- **Concurrent Updates**: What happens when two users update the same task simultaneously? System MUST use optimistic locking with version numbers, reject stale updates with clear error messages, and force refresh.
- **Service Failures**: What happens when Audit Service is down? System MUST continue operating (events stored in Kafka), Dapr MUST implement circuit breakers, and audit events MUST be processed once service recovers.
- **Data Corruption**: What happens when an invalid event is published to Kafka? System MUST validate event schemas, send invalid events to dead-letter queue, log validation errors with correlation IDs, and alert operators.
- **Clock Skew**: What happens when due dates/reminders are evaluated across services with clock differences? System MUST use UTC timestamps consistently, tolerate small skew (< 5 seconds), and use Kafka timestamps as source of truth.
- **Large Result Sets**: What happens when user has 10,000+ tasks? System MUST implement pagination (100 tasks per page), cursor-based navigation, and efficient database queries with indexes.
- **Rapid Event Bursts**: What happens when 1000 tasks are created simultaneously (bulk import)? System MUST throttle event publishing, use Kafka partitioning for parallelism, scale consumers automatically, and maintain system responsiveness.

## Requirements *(mandatory)*

### Functional Requirements

#### Advanced Task Features

- **FR-001**: System MUST allow users to create tasks with optional due dates (date + time with timezone support)
- **FR-002**: System MUST support recurring tasks with patterns: daily, weekly (specific days), monthly (specific date or day-of-week), and custom cron expressions
- **FR-003**: System MUST support task priorities with three levels: High, Medium, Low (default: Medium)
- **FR-004**: System MUST allow users to add multiple tags to tasks (free-form text tags, case-insensitive)
- **FR-005**: System MUST provide full-text search across task titles, descriptions, and tags
- **FR-006**: System MUST support filtering tasks by: priority, due date range, tags, completion status, and creation date
- **FR-007**: System MUST support sorting tasks by: due date, priority, creation date, last modified date, and alphabetically
- **FR-008**: System MUST send reminders for tasks 24 hours before due date, 1 hour before due date, and at due date time
- **FR-009**: System MUST allow users to snooze reminders for: 1 hour, 4 hours, 24 hours, or until next day 9 AM
- **FR-010**: System MUST automatically mark recurring tasks as complete and create the next instance based on recurrence pattern

#### Event-Driven Architecture

- **FR-011**: System MUST publish events to Kafka for all task state changes: created, updated, completed, deleted
- **FR-012**: System MUST publish events to `task-events` topic with schema: {event_type, task_id, user_id, timestamp, data, correlation_id}
- **FR-013**: System MUST publish reminder notifications to `reminders` topic with schema: {task_id, user_id, due_date, reminder_type, timestamp}
- **FR-014**: System MUST publish real-time updates to `task-updates` topic for WebSocket synchronization
- **FR-015**: System MUST consume events from Kafka independently in: Notification Service, Audit Service, Recurring Task Service, WebSocket Sync Service
- **FR-016**: System MUST ensure exactly-once event processing using Kafka consumer offsets and idempotency keys
- **FR-017**: System MUST include correlation IDs in all events for distributed tracing across services
- **FR-018**: System MUST implement dead-letter queues for failed event processing with retry policies (3 attempts with exponential backoff)

#### Dapr Runtime Integration

- **FR-019**: System MUST use Dapr Pub/Sub for all Kafka interactions (no direct Kafka client libraries in application code)
- **FR-020**: System MUST use Dapr State Management API for caching frequently accessed data (user preferences, recent tasks)
- **FR-021**: System MUST use Dapr Secrets API for all secret retrieval (database passwords, API keys, JWT secrets)
- **FR-022**: System MUST use Dapr Bindings for Cron triggers in Recurring Task Service (check for due recurring tasks every 5 minutes)
- **FR-023**: System MUST use Dapr Service Invocation for synchronous service-to-service calls with built-in retries and circuit breakers
- **FR-024**: System MUST configure Dapr resiliency policies: retries (3 attempts, exponential backoff), timeouts (5s default), circuit breakers (5 consecutive failures trip)
- **FR-025**: System MUST enable Dapr distributed tracing with Zipkin/Jaeger exporter for all service calls and events

#### Microservices

- **FR-026**: Frontend Service MUST provide chat-based UI with split-view layout (chat on left, task dashboard on right) using Next.js + React
- **FR-027**: Chat API Service MUST integrate OpenAI GPT-4 for natural language processing of task commands via MCP Tools
- **FR-028**: Notification Service MUST consume `reminders` topic and send notifications via configured channels (in-app, email using SMTP, push using Firebase Cloud Messaging)
- **FR-029**: Recurring Task Service MUST process recurring task patterns using Cron bindings, create new task instances, and publish creation events
- **FR-030**: Audit Service MUST consume all topics, store audit logs in separate database, and provide queryable audit trail with retention policy (1 year)
- **FR-031**: WebSocket Sync Service MUST maintain WebSocket connections per user, consume `task-updates` topic, and broadcast updates to connected clients in real-time

#### Deployment and Operations

- **FR-032**: System MUST deploy to Minikube using Helm charts with Dapr, Kafka (Strimzi or Redpanda), PostgreSQL, and all microservices
- **FR-033**: System MUST deploy to cloud Kubernetes (AKS, GKE, or OKE) using same Helm charts with environment-specific values
- **FR-034**: System MUST use Horizontal Pod Autoscaler (HPA) for all stateless services based on CPU (70%) and memory (80%) utilization
- **FR-035**: System MUST implement health checks (liveness at `/health`, readiness at `/ready`) for all services
- **FR-036**: System MUST use Kubernetes Secrets for sensitive data, never hardcode secrets in code or config files
- **FR-037**: System MUST configure resource requests and limits for all pods (prevent resource starvation and OOMKills)
- **FR-038**: System MUST implement rolling updates with zero downtime (maxUnavailable: 0, maxSurge: 1)

#### CI/CD Automation

- **FR-039**: System MUST use GitHub Actions for CI pipeline: lint, test, build Docker images, security scan (Trivy), push to registry
- **FR-040**: System MUST use GitHub Actions for CD pipeline: deploy to staging on main branch merge, manual approval for production
- **FR-041**: System MUST run automated smoke tests post-deployment to verify system health
- **FR-042**: System MUST implement automatic rollback if health checks fail or error rate exceeds threshold (5% in 5 minutes)
- **FR-043**: System MUST tag Docker images with: git commit SHA, branch name, and `latest` for main branch
- **FR-044**: System MUST scan Docker images for vulnerabilities and fail pipeline if HIGH or CRITICAL vulnerabilities found

#### Monitoring and Observability

- **FR-045**: System MUST export metrics to Prometheus: request rate, error rate, latency (p50, p95, p99), Kafka consumer lag, pod resource usage
- **FR-046**: System MUST provide Grafana dashboards for: system overview, per-service metrics, Kafka topics, business metrics (tasks created, completion rate)
- **FR-047**: System MUST implement distributed tracing with Jaeger/Zipkin, capturing all HTTP requests and event flows with correlation IDs
- **FR-048**: System MUST use structured logging (JSON format) with fields: timestamp, level, service, correlation_id, user_id, message
- **FR-049**: System MUST forward logs to centralized logging (Loki or ELK) for aggregation and searchability
- **FR-050**: System MUST configure alerting rules in AlertManager: high error rate, service down, Kafka consumer lag, pod restarts, resource exhaustion

### Key Entities

- **Task**: Represents a todo item with attributes: id, user_id, title, description, priority (high/medium/low), due_date (optional), tags (array), is_completed, recurrence_pattern (optional), created_at, updated_at, version (for optimistic locking)
- **User**: Represents application user with attributes: id, email, hashed_password, created_at, notification_preferences (in-app, email, push)
- **Reminder**: Represents scheduled notification with attributes: id, task_id, user_id, reminder_time, reminder_type (24h_before, 1h_before, at_due_time), is_sent, sent_at
- **AuditLog**: Represents system event audit with attributes: id, event_type, entity_type, entity_id, user_id, timestamp, data (JSON), correlation_id, service_name
- **RecurringPattern**: Embedded in Task, represents recurrence with attributes: frequency (daily/weekly/monthly/custom), interval (every N days/weeks/months), days_of_week (for weekly), day_of_month (for monthly), cron_expression (for custom), next_occurrence
- **Event**: Kafka message schema with attributes: event_type, task_id, user_id, timestamp, data (task snapshot), correlation_id, idempotency_key

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with all advanced features (recurring, due dates, priorities, tags) through natural language chat in under 30 seconds
- **SC-002**: Full-text search returns relevant results in under 500 milliseconds for task collections up to 10,000 items per user
- **SC-003**: Real-time synchronization propagates task changes to all connected sessions within 2 seconds (p95 latency)
- **SC-004**: System handles 1,000 concurrent users with 100 requests per second without degradation (p95 latency under 500ms)
- **SC-005**: Reminder notifications are delivered within 5 minutes of scheduled time (99.5% on-time delivery rate)
- **SC-006**: Recurring task instances are created correctly for 100% of scheduled occurrences with zero missed instances
- **SC-007**: Event-driven workflows complete end-to-end (task created → all consumers process) within 10 seconds (p95)
- **SC-008**: System maintains 99.5% uptime across all microservices in production environment over 30-day period
- **SC-009**: Kafka consumer lag remains under 1000 messages during normal operation and under 5000 during peak load
- **SC-010**: Zero data loss occurs for committed events in Kafka (durability guarantee with replication factor 3)
- **SC-011**: Distributed traces cover 100% of user requests and event flows with complete correlation ID propagation
- **SC-012**: Deployment to any environment (Minikube, AKS, GKE, OKE) completes successfully in under 10 minutes
- **SC-013**: CI/CD pipeline executes in under 15 minutes from code push to staging deployment
- **SC-014**: Automated rollback completes within 2 minutes when triggered by health check failures
- **SC-015**: System automatically scales from 2 to 10 replicas per service based on load, returning to baseline within 10 minutes of load decrease
- **SC-016**: Security scan detects zero HIGH or CRITICAL vulnerabilities in deployed container images
- **SC-017**: All API endpoints respond with p95 latency under 500ms and p99 under 1000ms during normal load
- **SC-018**: Task search and filter operations complete in under 300ms for result sets up to 1000 items
- **SC-019**: System recovers from individual service failures within 30 seconds (health checks fail → pod restart → service restored)
- **SC-020**: 95% of users successfully complete advanced task creation on first attempt without errors

## Assumptions

Since this is a comprehensive Phase V specification building on previous phases, the following assumptions are made based on industry standards and the Phase V constitution:

1. **Phase I-IV Foundation**: Assumes successful completion of Phase I (Console App), Phase II (Full-Stack Web), Phase III (AI Chatbot), and Phase IV (Kubernetes Deployment) as described in the project README
2. **Authentication**: JWT-based authentication from Phase II/III continues to be used; no changes to auth flow required
3. **Database**: PostgreSQL database from previous phases is extended with new tables for advanced features; existing users and tasks tables are migrated
4. **AI Integration**: OpenAI GPT-4 integration from Phase III is reused; MCP Tools are extended to support new task attributes
5. **Kafka Configuration**: Default Kafka configuration includes 3 brokers, replication factor 3, 30-day retention for audit topics, 7-day retention for operational topics
6. **Dapr Version**: Dapr 1.12+ is used with default configuration for Pub/Sub (at-least-once delivery), State (strong consistency), and Secrets (file-based locally, cloud provider's secret store in cloud)
7. **Notification Channels**: In-app notifications are always supported; email/push are optional and configured via environment variables
8. **Timezone Handling**: All timestamps stored in UTC; due dates converted to user's local timezone for display (browser timezone detection)
9. **Recurring Task Limits**: Maximum recurrence limit is 2 years in the future to prevent infinite task creation; users can manually extend
10. **Event Ordering**: Kafka partitioning by user_id ensures per-user event ordering; cross-user ordering is not guaranteed
11. **Resource Limits**: Development defaults: 2 CPU cores, 4GB RAM per service; production tuned based on load testing
12. **Cloud Provider**: Primary deployment target is Azure AKS with fallback to GKE and OKE; instructions provided for all three
13. **Monitoring Stack**: Prometheus + Grafana + Jaeger for observability; Loki for logging (ELK stack as alternative)
14. **GitOps**: Helm charts stored in repository; ArgoCD or Flux can optionally be used for GitOps workflows
15. **Cost Optimization**: Free tiers and spot instances used where possible; auto-scaling minimizes cost during low usage

## Out of Scope (Not Building)

- **Mobile Native Apps**: No iOS or Android native apps; focus is on responsive web interface
- **Offline-First Clients**: Requires network connectivity; no offline mode or local-first sync
- **Custom SaaS Integrations**: No integration with third-party productivity tools (Jira, Asana, Trello, etc.)
- **Manual Infrastructure Provisioning**: All infrastructure provisioned via Kubernetes; no manual VM/server setup scripts
- **Legacy Migration Tools**: No tools for migrating data from other todo applications
- **Multi-Language Support**: UI and AI responses in English only; no i18n/l10n
- **Voice Input**: No speech-to-text for task creation via voice commands
- **Collaboration Features**: No real-time collaboration, task sharing, or team workspaces (single-user focused)
- **Attachment Support**: No file attachments to tasks
- **Calendar Integration**: No sync with Google Calendar, Outlook, or other calendar services
- **Custom Hardware Support**: Kubernetes-only; no bare-metal or IoT device deployments
- **Vendor-Specific Lock-In**: Avoiding AWS-only or GCP-only services that prevent portability
- **Machine Learning Models**: No custom ML models for task prediction or categorization (relies on GPT-4 only)
- **Blockchain/Web3**: No decentralized or blockchain-based features
- **Payment/Billing**: No subscription management or payment processing (free application)

## Constraints

- **Development Methodology**: All code MUST be generated via Claude Code following Agentic Dev Stack (Spec → Plan → Tasks → Implement); no manual coding allowed
- **Deployment Platform**: Kubernetes-only deployment; no support for VMs, containers without orchestration, or serverless platforms
- **Dapr Integration**: ALL external dependencies (Kafka, database state, secrets, external APIs) MUST go through Dapr components; no direct client libraries in application code
- **Event-Driven Requirement**: ALL state-changing operations MUST publish events to Kafka; direct service-to-service database access is forbidden
- **Cloud Budget**: Must use free tiers where available (Oracle OKE free tier, AKS free tier, GCP $300 credit); minimize cloud costs
- **Technology Stack**: Must use the exact stack defined in Phase V constitution (FastAPI, Next.js, Kafka, Dapr, PostgreSQL, Prometheus, Grafana, Jaeger)
- **Testing Strategy**: TDD (Test-First Development) is mandatory; tests written before implementation, Red-Green-Refactor cycle enforced
- **Security**: No secrets in code, configuration files, or Docker images; all secrets via Dapr Secrets API or Kubernetes Secrets
- **Stateless Services**: All application services MUST be stateless to enable horizontal scaling; state stored in database or Dapr state store only
- **Resource Limits**: Each service must declare resource requests and limits; cannot consume unbounded CPU/memory
- **Compatibility**: Helm charts MUST work on Minikube, AKS, GKE, and OKE with only environment-specific values changed
- **Timeline**: 18-day implementation window as specified (3d spec, 2d plan, 10d implementation, 3d validation)

## Technical Context (Reference Only)

*Note: The following technical details are provided for planning purposes only and are NOT part of the specification requirements. The plan phase will determine specific implementation approaches.*

**Platform Targets**:
- Local: Minikube (Kubernetes 1.28+)
- Cloud: AKS (Azure), GKE (Google Cloud), OKE (Oracle Cloud)

**Messaging**:
- Kafka 3.5+ (Strimzi operator for K8s or managed service)
- Alternative: Redpanda (Kafka-compatible, simpler for local dev)

**Runtime**:
- Dapr 1.12+ with sidecars for all services

**Reusable Agents** (for implementation):
- Architecture Agent (design patterns, microservices boundaries)
- DevOps Agent (K8s manifests, Helm charts)
- Cloud Deployment Agent (multi-cloud deployment strategies)
- Security Agent (secrets management, vulnerability scanning)
- AI Integration Agent (OpenAI GPT-4 integration)
- Testing & QA Agent (TDD workflow, integration tests)
- Documentation Agent (specs, diagrams, guides)

**Reusable Skills** (for implementation):
- Kubernetes Deployment Skill
- Helm Chart Generation Skill
- CI/CD Pipeline Skill
- Kafka Integration Skill
- Dapr Configuration Skill
- Observability Setup Skill
- Security Hardening Skill
- Cost Optimization Skill

# Tasks: Phase V – Advanced Cloud-Native Todo System with Kafka & Dapr

**Input**: Design documents from `/specs/001-cloud-native-kafka-dapr/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are OPTIONAL per the specification. Given the 1-day timeline constraint, tests are included only for critical paths as specified in the plan's "Pragmatic TDD" approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**⚠️ CRITICAL TIMELINE NOTE**: Deadline is February 9, 2026 (tomorrow). This task list prioritizes **working MVP demonstration** over complete implementation. Focus is on User Stories 1-2 (P1-P2) with 12-15 hour estimate.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

This is a microservices project with the following structure (per plan.md):
- **Backend Services**: `services/<service-name>/` (6 microservices)
- **Frontend**: `frontend/` (Next.js app)
- **Infrastructure**: `helm/phase5/` (Helm charts), `scripts/` (deployment scripts)
- **Tests**: `tests/` (integration tests), per-service `tests/` for unit tests

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, Minikube cluster, and infrastructure deployment

- [x] T001 Create Phase V project directory structure per plan.md
- [x] T002 [P] Initialize Python services with FastAPI dependencies in services/{chat-api,notification-service,recurring-task-service,audit-service,websocket-sync-service}/requirements.txt
- [x] T003 [P] Initialize Next.js frontend in frontend/ with Next.js 16+, React 19+, TypeScript, Tailwind CSS
- [x] T004 [P] Configure ESLint and Prettier for frontend in frontend/.eslintrc.json and frontend/.prettierrc
- [x] T005 [P] Configure Black, Flake8, and isort for backend services in services/*/pyproject.toml
- [x] T006 Create Minikube quickstart script at scripts/quickstart.sh per quickstart.md
- [x] T007 [P] Create Docker Compose for local development (optional fallback) in docker-compose.yml
- [x] T008 [P] Setup environment configuration templates in .env.example files for all services

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Infrastructure Deployment (Minikube)

- [ ] T009 Start Minikube cluster with 4 CPUs and 8GB RAM using scripts/quickstart.sh
- [ ] T010 Install Dapr runtime 1.12+ in Kubernetes using `dapr init --kubernetes --wait`
- [ ] T011 Deploy Redpanda (Kafka) with 3 replicas using Helm in namespace phase5
- [ ] T012 Deploy PostgreSQL 15 using Helm in namespace phase5 with credentials from postgres-secret
- [ ] T013 Create Kafka topics: task-events, reminders, task-updates using kubectl exec redpanda-0
- [ ] T014 Verify Kafka topics and partitions using `rpk topic list`

### Dapr Component Configuration

- [ ] T015 [P] Create Dapr Pub/Sub component for Kafka in helm/phase5/components/pubsub-kafka.yaml per contracts/dapr-components.yaml
- [ ] T016 [P] Create Dapr State Store component for PostgreSQL in helm/phase5/components/statestore-postgresql.yaml
- [ ] T017 [P] Create Dapr Secret Store component for Kubernetes Secrets in helm/phase5/components/secretstore-kubernetes.yaml
- [ ] T018 [P] Create Dapr Cron binding for recurring tasks in helm/phase5/components/cron-recurring-tasks.yaml (every 5 minutes)
- [ ] T019 [P] Create Dapr Cron binding for reminders in helm/phase5/components/cron-reminders.yaml (every minute)
- [ ] T020 [P] Create Dapr global configuration in helm/phase5/components/dapr-config.yaml with Zipkin tracing
- [ ] T021 Apply all Dapr components to phase5 namespace using `kubectl apply -f helm/phase5/components/`

### Kubernetes Secrets

- [ ] T022 [P] Create postgres-secret in phase5 namespace with connection string
- [ ] T023 [P] Create jwt-secret in phase5 namespace with secret key for JWT tokens
- [ ] T024 [P] Create smtp-secret in phase5 namespace with SMTP credentials (if email notifications enabled)

### Database Schema Setup

- [ ] T025 Initialize Alembic migrations for chat-api service in services/chat-api/alembic/
- [ ] T026 [P] Initialize Alembic migrations for notification-service in services/notification-service/alembic/
- [ ] T027 [P] Initialize Alembic migrations for recurring-task-service in services/recurring-task-service/alembic/
- [ ] T028 [P] Initialize Alembic migrations for audit-service in services/audit-service/alembic/
- [ ] T029 Create users table migration for chat-api in services/chat-api/alembic/versions/001_create_users.py per data-model.md
- [ ] T030 Create tasks table migration for chat-api in services/chat-api/alembic/versions/002_create_tasks.py with full-text search indexes
- [ ] T031 [P] Create reminders table migration for notification-service in services/notification-service/alembic/versions/001_create_reminders.py
- [ ] T032 [P] Create notifications table migration for notification-service in services/notification-service/alembic/versions/002_create_notifications.py
- [ ] T033 [P] Create recurring_instances table migration for recurring-task-service in services/recurring-task-service/alembic/versions/001_create_recurring_instances.py
- [ ] T034 [P] Create audit_logs table migration for audit-service in services/audit-service/alembic/versions/001_create_audit_logs.py
- [ ] T035 Run all database migrations using alembic upgrade head for each service

### Base Models and Utilities

- [ ] T036 [P] Create base SQLAlchemy model in services/chat-api/src/models/base.py with created_at, updated_at, deleted_at
- [ ] T037 [P] Create Dapr client wrapper in services/chat-api/src/utils/dapr_client.py for Pub/Sub, State, Secrets
- [ ] T038 [P] Create CloudEvents schema validator in services/chat-api/src/utils/cloudevents.py per contracts/kafka-events.yaml
- [ ] T039 [P] Create correlation ID middleware in services/chat-api/src/middleware/correlation.py for distributed tracing
- [ ] T040 [P] Create structured logging utility in services/chat-api/src/utils/logging.py with JSON format

### Authentication Foundation (from Phase III)

- [ ] T041 Create JWT authentication middleware in services/chat-api/src/middleware/auth.py
- [ ] T042 Create User model in services/chat-api/src/models/user.py per data-model.md with notification preferences
- [ ] T043 Create authentication service in services/chat-api/src/services/auth_service.py with bcrypt password hashing
- [ ] T044 Create authentication endpoints in services/chat-api/src/routes/auth.py (POST /register, POST /login)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Advanced Task Management with Intelligence (Priority: P1) 🎯 MVP

**Goal**: Provide users with advanced task features (recurring, due dates, priorities, tags, search, filters, sort) through AI chat interface

**Independent Test**: Can be fully tested by creating tasks with all advanced attributes through the chat interface, verifying they persist across sessions, and confirming smart search/filter/sort capabilities work correctly

**Estimated Time**: 6-8 hours

### Data Models for US1

- [ ] T045 [P] [US1] Create Task model in services/chat-api/src/models/task.py per data-model.md with priority, due_date, tags, recurrence_pattern
- [ ] T046 [P] [US1] Create RecurrencePattern schema in services/chat-api/src/schemas/recurrence.py with frequency, interval, days_of_week

### Services for US1

- [ ] T047 [US1] Implement TaskService in services/chat-api/src/services/task_service.py with CRUD operations
- [ ] T048 [US1] Add create_task method in TaskService that publishes com.todo.task.created event to task-events topic via Dapr Pub/Sub
- [ ] T049 [US1] Add update_task method in TaskService with optimistic locking (version field) and publishes com.todo.task.updated event
- [ ] T050 [US1] Add delete_task method in TaskService (soft delete) that publishes com.todo.task.deleted event
- [ ] T051 [US1] Add complete_task method in TaskService that publishes com.todo.task.completed event
- [ ] T052 [US1] Add search_tasks method in TaskService with PostgreSQL full-text search (GIN index on tsvector)
- [ ] T053 [US1] Add filter_tasks method in TaskService with support for priority, tags, due_date, status filters
- [ ] T054 [US1] Add sort_tasks method in TaskService with support for due_date, priority, created_at, title sorting

### API Endpoints for US1

- [ ] T055 [US1] Create task endpoints in services/chat-api/src/routes/tasks.py per contracts/api-chat-service.yaml
- [ ] T056 [P] [US1] Implement GET /api/v1/tasks with query params (status, priority, tags, due_before, due_after, sort, limit, offset)
- [ ] T057 [P] [US1] Implement POST /api/v1/tasks with CreateTaskRequest schema validation
- [ ] T058 [P] [US1] Implement GET /api/v1/tasks/{task_id} endpoint
- [ ] T059 [P] [US1] Implement PATCH /api/v1/tasks/{task_id} with UpdateTaskRequest and version conflict handling (409 response)
- [ ] T060 [P] [US1] Implement DELETE /api/v1/tasks/{task_id} endpoint (soft delete)
- [ ] T061 [P] [US1] Implement GET /api/v1/tasks/search endpoint with full-text search query parameter

### AI Chat Integration for US1

- [ ] T062 [US1] Extend OpenAI function definitions in services/chat-api/src/services/openai_service.py with advanced task parameters
- [ ] T063 [US1] Add parse_due_date function to extract due dates from natural language (e.g., "tomorrow", "next Friday", "2026-02-10")
- [ ] T064 [US1] Add parse_priority function to extract priority from keywords (e.g., "urgent" → high, "important" → high)
- [ ] T065 [US1] Add parse_tags function to extract tags from message text (e.g., #work, #urgent)
- [ ] T066 [US1] Add parse_recurrence function to parse recurring patterns (e.g., "every Monday", "daily", "weekly on Tuesday and Thursday")
- [ ] T067 [US1] Update chat endpoint POST /api/v1/chat to handle advanced task creation commands

### Frontend for US1

- [ ] T068 [US1] Create Task interface in frontend/src/types/task.ts with all advanced properties (priority, due_date, tags, recurrence)
- [ ] T069 [US1] Create TaskList component in frontend/src/components/TaskList.tsx with priority badges and due date display
- [ ] T070 [US1] Create TaskFilter component in frontend/src/components/TaskFilter.tsx with dropdowns for priority, tags, due date range
- [ ] T071 [US1] Create TaskSort component in frontend/src/components/TaskSort.tsx with sort options
- [ ] T072 [US1] Create SearchBar component in frontend/src/components/SearchBar.tsx with debounced full-text search
- [ ] T073 [US1] Create TaskCard component in frontend/src/components/TaskCard.tsx with priority color coding and due date countdown
- [ ] T074 [US1] Update ChatInterface component in frontend/src/components/ChatInterface.tsx to display tasks with advanced features
- [ ] T075 [US1] Add API client methods in frontend/src/lib/api.ts for search, filter, sort operations

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks with advanced features via chat and manage them with search/filter/sort

---

## Phase 4: User Story 2 - Event-Driven Real-Time Synchronization (Priority: P2)

**Goal**: Provide real-time synchronization across all user sessions using WebSocket and Kafka events

**Independent Test**: Can be tested by opening two browser tabs, making changes in one tab (create/update/delete tasks), and verifying the changes appear instantly in the second tab without manual refresh

**Estimated Time**: 4-6 hours

### WebSocket Sync Service

- [ ] T076 [P] [US2] Create WebSocket Sync Service structure in services/websocket-sync-service/ with FastAPI WebSocket support
- [ ] T077 [US2] Implement WebSocket connection manager in services/websocket-sync-service/src/connection_manager.py with Redis-backed connection registry
- [ ] T078 [US2] Create WebSocket endpoint in services/websocket-sync-service/src/routes/websocket.py at /ws with JWT token authentication via query param
- [ ] T079 [US2] Implement heartbeat/ping-pong mechanism in WebSocket connection to detect stale connections
- [ ] T080 [US2] Store active connections in Dapr State Store (Redis) using connection_id → user_id mapping

### Event Consumers for US2

- [ ] T081 [US2] Create Kafka consumer in services/websocket-sync-service/src/consumers/task_updates_consumer.py subscribed to task-updates topic
- [ ] T082 [US2] Implement event deduplication in task_updates_consumer using Redis cache (event_id → processed timestamp with 7-day TTL)
- [ ] T083 [US2] Implement broadcast logic in task_updates_consumer to send events to all WebSocket connections for user_id
- [ ] T084 [US2] Handle WebSocket connection failures gracefully (remove from registry, log error)

### Publishing to task-updates Topic

- [ ] T085 [US2] Update TaskService in services/chat-api/ to publish com.todo.sync.task_changed event to task-updates topic after all CRUD operations
- [ ] T086 [US2] Include full current_state in sync events per contracts/kafka-events.yaml schema

### Frontend WebSocket Client

- [ ] T087 [US2] Create WebSocket client in frontend/src/lib/websocket.ts with auto-reconnect logic
- [ ] T088 [US2] Implement connection state management (connecting, connected, disconnected, error) with React Context
- [ ] T089 [US2] Add event handlers in frontend to update task list when receiving sync events from WebSocket
- [ ] T090 [US2] Display connection status indicator in UI (green dot = connected, yellow = reconnecting, red = disconnected)
- [ ] T091 [US2] Implement optimistic UI updates (show changes immediately, rollback if event conflicts)

### Testing US2

- [ ] T092 [US2] Manual test: Open two browser tabs, create task in tab 1, verify appears in tab 2 within 2 seconds
- [ ] T093 [US2] Manual test: Disconnect WebSocket (close tab), reconnect, verify sync resumes

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - real-time sync is operational

---

## Phase 5: User Story 3 - Microservices Observability and Monitoring (Priority: P3)

**Goal**: Provide monitoring dashboards, distributed tracing, and alerting for system operators

**Independent Test**: Can be tested by accessing Grafana dashboards, viewing service metrics, tracing a request through Jaeger, checking alert rules in AlertManager, and querying logs with correlation IDs

**Estimated Time**: 3-4 hours (OPTIONAL - time permitting)

### Zipkin/Jaeger Deployment

- [ ] T094 [P] [US3] Deploy Zipkin in phase5 namespace using Helm for distributed tracing
- [ ] T095 [US3] Verify Dapr sidecars export traces to Zipkin (check dapr-config.yaml tracing configuration)
- [ ] T096 [US3] Access Zipkin UI and verify traces appear for task creation flow

### Prometheus Metrics

- [ ] T097 [P] [US3] Deploy Prometheus using kube-prometheus-stack Helm chart in monitoring namespace
- [ ] T098 [US3] Configure Prometheus to scrape Dapr sidecar metrics endpoints (port 9090 on daprd)
- [ ] T099 [US3] Add custom metrics in services/chat-api/ for task_created_total, task_completed_total counters
- [ ] T100 [US3] Add latency histograms for API endpoints in services/chat-api/

### Grafana Dashboards (OPTIONAL)

- [ ] T101 [P] [US3] Deploy Grafana via kube-prometheus-stack with admin password
- [ ] T102 [US3] Import Dapr dashboard from Grafana.com dashboard ID
- [ ] T103 [US3] Create custom dashboard for Phase V business metrics (tasks created, completion rate)
- [ ] T104 [US3] Port-forward Grafana and access at localhost:3001

### Structured Logging

- [ ] T105 [P] [US3] Ensure all services use structured JSON logging with correlation_id, user_id, service_name fields
- [ ] T106 [US3] Configure log aggregation (optional - Loki or ELK stack if time permits)

**Checkpoint**: All monitoring tools deployed and operational - operators can observe system health

---

## Phase 6: User Story 4 - Multi-Environment Deployment with CI/CD (Priority: P4)

**Goal**: Automated CI/CD pipeline for deploying to Minikube, staging, and production

**Independent Test**: Can be tested by pushing code to GitHub, triggering CI/CD pipeline, observing automated tests/builds/deployments, and verifying successful deployment to target environment with health checks passing

**Estimated Time**: 3-4 hours (OPTIONAL - time permitting)

### Dockerfile Creation

- [ ] T107 [P] [US4] Create Dockerfile for chat-api service in services/chat-api/Dockerfile with multi-stage build
- [ ] T108 [P] [US4] Create Dockerfile for notification-service in services/notification-service/Dockerfile
- [ ] T109 [P] [US4] Create Dockerfile for recurring-task-service in services/recurring-task-service/Dockerfile
- [ ] T110 [P] [US4] Create Dockerfile for audit-service in services/audit-service/Dockerfile
- [ ] T111 [P] [US4] Create Dockerfile for websocket-sync-service in services/websocket-sync-service/Dockerfile
- [ ] T112 [P] [US4] Create Dockerfile for frontend in frontend/Dockerfile with Next.js production build

### Helm Chart Structure

- [ ] T113 [US4] Create umbrella Helm chart in helm/phase5/Chart.yaml with dependencies on subcharts
- [ ] T114 [P] [US4] Create subchart for chat-api in helm/phase5/charts/chat-api/ with deployment, service, configmap
- [ ] T115 [P] [US4] Create subchart for notification-service in helm/phase5/charts/notification-service/
- [ ] T116 [P] [US4] Create subchart for recurring-task-service in helm/phase5/charts/recurring-task-service/
- [ ] T117 [P] [US4] Create subchart for audit-service in helm/phase5/charts/audit-service/
- [ ] T118 [P] [US4] Create subchart for websocket-sync-service in helm/phase5/charts/websocket-sync-service/
- [ ] T119 [P] [US4] Create subchart for frontend in helm/phase5/charts/frontend/
- [ ] T120 [US4] Add Dapr annotations to all deployment templates (dapr.io/enabled, dapr.io/app-id, dapr.io/app-port)
- [ ] T121 [US4] Configure HPA (Horizontal Pod Autoscaler) for all stateless services in Helm templates
- [ ] T122 [US4] Add health check probes (livenessProbe, readinessProbe) to all deployments

### GitHub Actions CI/CD

- [ ] T123 [P] [US4] Create GitHub Actions workflow in .github/workflows/ci.yml for linting, testing, building Docker images
- [ ] T124 [US4] Add Trivy security scanning step in CI workflow to scan Docker images for vulnerabilities
- [ ] T125 [US4] Add step to push Docker images to registry (Docker Hub or GitHub Container Registry) with tags
- [ ] T126 [P] [US4] Create GitHub Actions workflow in .github/workflows/cd.yml for deploying to staging on main branch merge
- [ ] T127 [US4] Add manual approval gate for production deployment in CD workflow
- [ ] T128 [US4] Add smoke tests step in CD workflow to verify deployment health

**Checkpoint**: CI/CD pipeline operational - automated deployments working

---

## Phase 7: User Story 5 - Cloud-Native Portability and Infrastructure (Priority: P5)

**Goal**: Deploy to multiple cloud providers (AKS, GKE, OKE) using same Helm charts with platform-specific values

**Independent Test**: Can be tested by deploying the same Helm charts to Minikube, AKS, GKE, and OKE, verifying all services start successfully, Dapr components work correctly, and functional tests pass in all environments

**Estimated Time**: 4-6 hours (OPTIONAL - post-demo)

### Cloud-Specific Helm Values

- [ ] T129 [P] [US5] Create values-minikube.yaml in helm/phase5/ for Minikube deployment with Redpanda
- [ ] T130 [P] [US5] Create values-aks.yaml in helm/phase5/ for Azure deployment with Azure Managed Kafka
- [ ] T131 [P] [US5] Create values-gke.yaml in helm/phase5/ for GCP deployment with Confluent Cloud Kafka
- [ ] T132 [P] [US5] Create values-oke.yaml in helm/phase5/ for Oracle Cloud deployment with Strimzi Kafka

### Dapr Component Overrides for Cloud

- [ ] T133 [P] [US5] Create Dapr Pub/Sub component override for Azure Kafka in helm/phase5/components/azure/pubsub-kafka.yaml
- [ ] T134 [P] [US5] Create Dapr Secret Store component override for Azure Key Vault in helm/phase5/components/azure/secretstore-azurekeyvault.yaml
- [ ] T135 [P] [US5] Create Dapr Pub/Sub component override for Confluent Cloud Kafka in helm/phase5/components/gcp/pubsub-kafka.yaml
- [ ] T136 [P] [US5] Create Dapr Secret Store component override for GCP Secret Manager in helm/phase5/components/gcp/secretstore-gcpsecretmanager.yaml

### Cloud Deployment Scripts

- [ ] T137 [P] [US5] Create cloud deployment script for AKS in scripts/deploy-aks.sh with az login and kubectl context
- [ ] T138 [P] [US5] Create cloud deployment script for GKE in scripts/deploy-gke.sh with gcloud auth and kubectl context
- [ ] T139 [P] [US5] Create cloud deployment script for OKE in scripts/deploy-oke.sh with oci cli and kubectl context

### Cloud Deployment Testing

- [ ] T140 [US5] Deploy to Oracle OKE (free tier) and verify all services healthy
- [ ] T141 [US5] Run functional tests on OKE deployment (task creation, event flow, WebSocket sync)
- [ ] T142 [US5] Document cloud deployment differences in docs/cloud-deployment.md

**Checkpoint**: Multi-cloud portability validated - system runs on Minikube and at least one cloud provider

---

## Phase 8: Recurring Tasks & Reminders (P1 Advanced Features)

**Goal**: Implement recurring task generation and reminder notifications (part of US1 but broken out due to complexity)

**Independent Test**: Create a recurring task "Daily standup at 9 AM", verify instances are created automatically, complete one instance, verify next instance is created

**Estimated Time**: 3-4 hours (MUST HAVE for MVP)

### Recurring Task Service

- [ ] T143 [US1] Create Recurring Task Service structure in services/recurring-task-service/ with FastAPI
- [ ] T144 [US1] Create RecurringInstance model in services/recurring-task-service/src/models/recurring_instance.py per data-model.md
- [ ] T145 [US1] Implement RecurringTaskProcessor in services/recurring-task-service/src/processors/recurring_processor.py
- [ ] T146 [US1] Add calculate_next_occurrence method to compute next recurring task date based on recurrence_pattern
- [ ] T147 [US1] Create Dapr input binding handler in services/recurring-task-service/src/routes/bindings.py for cron-recurring-tasks binding
- [ ] T148 [US1] Implement task creation logic: fetch tasks with recurrence_pattern and next_occurrence <= now, create new task instance, update parent task next_occurrence
- [ ] T149 [US1] Subscribe to task-events topic in services/recurring-task-service/ to listen for task.completed events
- [ ] T150 [US1] When recurring task completed, create next instance and publish task.created event

### Notification Service

- [ ] T151 [US1] Create Notification Service structure in services/notification-service/ with FastAPI
- [ ] T152 [US1] Create Reminder model in services/notification-service/src/models/reminder.py per data-model.md
- [ ] T153 [US1] Create Notification model in services/notification-service/src/models/notification.py
- [ ] T154 [US1] Implement ReminderScheduler in services/notification-service/src/schedulers/reminder_scheduler.py
- [ ] T155 [US1] Create Dapr input binding handler for cron-reminders binding in services/notification-service/src/routes/bindings.py
- [ ] T156 [US1] Query reminders with scheduled_at <= now and status=pending, send notifications, mark as sent
- [ ] T157 [US1] Implement email sender in services/notification-service/src/senders/email_sender.py using SMTP (optional - if email enabled)
- [ ] T158 [US1] Implement in-app notification in services/notification-service/src/senders/inapp_sender.py (store in notifications table)
- [ ] T159 [US1] Subscribe to task-events topic to auto-create reminders when tasks are created with due_date
- [ ] T160 [US1] When task.created event received with due_date, create reminders at 24h before, 1h before, and at due time
- [ ] T161 [US1] Publish reminder.scheduled, reminder.sent, reminder.failed events to reminders topic per contracts/kafka-events.yaml

**Checkpoint**: Recurring tasks and reminders fully functional - core Phase V value delivered

---

## Phase 9: Audit Service (Event Logging)

**Goal**: Audit all events flowing through Kafka for compliance and debugging

**Independent Test**: Create a task, check audit_logs table, verify event is recorded with correlation_id

**Estimated Time**: 2-3 hours

### Audit Service

- [ ] T162 [P] Create Audit Service structure in services/audit-service/ with FastAPI
- [ ] T163 Create AuditLog model in services/audit-service/src/models/audit_log.py per data-model.md
- [ ] T164 Create Kafka consumer in services/audit-service/src/consumers/audit_consumer.py subscribed to ALL topics (task-events, reminders, task-updates)
- [ ] T165 Implement event storage in audit_consumer: parse CloudEvents, extract fields, insert into audit_logs table
- [ ] T166 Add idempotency check using event_id field (prevent duplicate audit entries)
- [ ] T167 [P] Create audit query API in services/audit-service/src/routes/audit.py with GET /api/v1/audit endpoint
- [ ] T168 Support filtering audit logs by user_id, entity_id, event_type, timestamp range

**Checkpoint**: Audit service operational - all events being logged

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, documentation, validation, and demo preparation

### Health Checks and Reliability

- [ ] T169 [P] Add health check endpoints to all services at /health (liveness) and /ready (readiness)
- [ ] T170 Implement database connection check in /ready endpoint (query SELECT 1 from database)
- [ ] T171 Implement Kafka connection check in /ready endpoint (verify Dapr Pub/Sub component is responding)
- [ ] T172 Add graceful shutdown handlers to all services (drain in-flight requests, close connections)

### Documentation

- [ ] T173 [P] Update root README.md with Phase V overview, architecture diagram, quickstart link
- [ ] T174 [P] Create Phase V architecture diagram in docs/architecture.png showing microservices, Kafka topics, Dapr components
- [ ] T175 [P] Update quickstart.md with actual tested commands and expected outputs
- [ ] T176 [P] Create troubleshooting guide in docs/troubleshooting.md with common issues and solutions
- [ ] T177 [P] Document API endpoints in docs/api-reference.md (or link to Swagger UI)
- [ ] T178 [P] Create demo script in docs/demo-script.md with step-by-step commands for judges

### Validation and Testing

- [ ] T179 Run quickstart.sh script end-to-end and verify all pods reach Running state (2/2 containers)
- [ ] T180 Verify all Dapr components are operational using `kubectl get components -n phase5`
- [ ] T181 Manual test: Create task via chat with advanced features (priority, due_date, tags, recurring)
- [ ] T182 Manual test: Verify task persists and appears in task list with correct attributes
- [ ] T183 Manual test: Search for task using full-text search
- [ ] T184 Manual test: Filter tasks by priority=high
- [ ] T185 Manual test: Sort tasks by due_date ascending
- [ ] T186 Manual test: Open two browser tabs, create task in one, verify appears in other within 2 seconds
- [ ] T187 Manual test: Complete a recurring task, verify next instance is created
- [ ] T188 Manual test: Verify reminder is created when task with due_date is created
- [ ] T189 Check Zipkin UI for distributed traces of task creation flow
- [ ] T190 Check Kafka topics for events using `kubectl exec redpanda-0 -- rpk topic consume task-events --num 5`
- [ ] T191 Check audit_logs table for event records
- [ ] T192 Verify all services have health checks passing
- [ ] T193 Load test (optional): Use k6 or ab to generate 100 concurrent requests, verify system remains responsive

### Demo Preparation

- [ ] T194 Record 5-minute demo video showing: quickstart, chat task creation, real-time sync, recurring tasks, Zipkin traces
- [ ] T195 Prepare slides explaining Phase V architecture (microservices, Kafka, Dapr, Kubernetes)
- [ ] T196 Create demo environment with pre-populated sample tasks for impressive visual
- [ ] T197 Test demo flow from start (Minikube start) to finish (all features demonstrated) and time it

### Code Cleanup

- [ ] T198 [P] Remove debug print statements and commented-out code from all services
- [ ] T199 [P] Run linters on all code (Black, Flake8 for Python; ESLint, Prettier for TypeScript)
- [ ] T200 [P] Ensure all services have proper error handling (no unhandled exceptions)
- [ ] T201 [P] Add docstrings to all public functions and classes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - CRITICAL for MVP
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) and US1 complete
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) - OPTIONAL (monitoring)
- **User Story 4 (Phase 6)**: Depends on US1 complete - OPTIONAL (CI/CD)
- **User Story 5 (Phase 7)**: Depends on US1 complete - OPTIONAL (multi-cloud)
- **Recurring Tasks (Phase 8)**: Depends on Foundational (Phase 2) and US1 models - MUST HAVE for MVP
- **Audit Service (Phase 9)**: Depends on Foundational (Phase 2) - NICE TO HAVE
- **Polish (Phase 10)**: Depends on desired user stories being complete

### Critical Path for MVP (12-15 hours)

**MUST HAVE** (in order):
1. ✅ Phase 1: Setup (1 hour)
2. ✅ Phase 2: Foundational (3-4 hours) - Infrastructure + database + Dapr
3. ✅ Phase 3: User Story 1 - Advanced Task Management (6-8 hours) - Core value
4. ✅ Phase 8: Recurring Tasks & Reminders (3-4 hours) - Part of US1
5. ✅ Phase 10: Polish & Validation (2 hours) - Demo prep

**NICE TO HAVE** (time permitting):
- Phase 4: User Story 2 - Real-Time Sync (4-6 hours) - Demo wow factor
- Phase 9: Audit Service (2-3 hours) - Event logging
- Phase 5: User Story 3 - Monitoring (3-4 hours) - Observability

**POST-DEMO** (if additional time):
- Phase 6: User Story 4 - CI/CD (3-4 hours)
- Phase 7: User Story 5 - Multi-Cloud (4-6 hours)

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T002, T003, T004, T005, T007, T008 can all run in parallel (different files)

**Within Foundational (Phase 2)**:
- T015-T020 (Dapr components) can run in parallel
- T022-T024 (Secrets) can run in parallel
- T026-T028, T031-T034 (migrations) can run in parallel per service
- T036-T040 (base utilities) can run in parallel

**Within User Story 1 (Phase 3)**:
- T045-T046 (models) can run in parallel
- T056-T061 (API endpoints) can run in parallel after T055
- T068-T075 (frontend components) can run in parallel

**Within User Story 2 (Phase 4)**:
- T076-T080 (WebSocket setup) independent
- T087-T091 (frontend WebSocket client) can run in parallel with T081-T084

**Within Recurring Tasks (Phase 8)**:
- Recurring Task Service (T143-T150) and Notification Service (T151-T161) can be developed in parallel

**Within Polish (Phase 10)**:
- T169-T172 (health checks), T173-T178 (docs), T198-T201 (cleanup) can all run in parallel

---

## Parallel Example: User Story 1 Core Implementation

```bash
# Launch all models for US1 together:
Task T045: "Create Task model in services/chat-api/src/models/task.py"
Task T046: "Create RecurrencePattern schema in services/chat-api/src/schemas/recurrence.py"

# After TaskService created, launch all API endpoints together:
Task T056: "Implement GET /api/v1/tasks"
Task T057: "Implement POST /api/v1/tasks"
Task T058: "Implement GET /api/v1/tasks/{task_id}"
Task T059: "Implement PATCH /api/v1/tasks/{task_id}"
Task T060: "Implement DELETE /api/v1/tasks/{task_id}"
Task T061: "Implement GET /api/v1/tasks/search"

# Launch all frontend components together:
Task T068: "Create Task interface"
Task T069: "Create TaskList component"
Task T070: "Create TaskFilter component"
Task T071: "Create TaskSort component"
Task T072: "Create SearchBar component"
Task T073: "Create TaskCard component"
```

---

## Implementation Strategy

### MVP First (Critical Path - 12-15 hours)

1. ✅ **Complete Phase 1: Setup** (1 hour)
   - Project structure
   - Dependencies
   - Scripts

2. ✅ **Complete Phase 2: Foundational** (3-4 hours)
   - Minikube + Dapr + Kafka + PostgreSQL
   - Dapr components
   - Database migrations
   - Authentication

3. ✅ **Complete Phase 3: User Story 1** (6-8 hours)
   - Task models with advanced features
   - TaskService with event publishing
   - API endpoints
   - AI chat integration
   - Frontend components

4. ✅ **Complete Phase 8: Recurring Tasks & Reminders** (3-4 hours)
   - Recurring Task Service
   - Notification Service
   - Cron bindings

5. ✅ **Complete Phase 10: Polish & Validation** (2 hours)
   - Health checks
   - Documentation
   - Manual testing
   - Demo preparation

**STOP and VALIDATE**: Test complete flow, prepare demo

### Extended Demo (if time > 15 hours)

6. 🎯 **Add Phase 4: User Story 2 - Real-Time Sync** (4-6 hours)
   - WebSocket Sync Service
   - Event consumers
   - Frontend WebSocket client
   - **Demo wow factor**: Open two tabs, show real-time sync

7. 🎯 **Add Phase 9: Audit Service** (2-3 hours)
   - Audit event logging
   - Query API

8. 🎯 **Add Phase 5: User Story 3 - Monitoring** (3-4 hours)
   - Zipkin/Jaeger
   - Prometheus + Grafana (optional)

### Fallback Plan (if < 6 hours remaining)

**Minimum Viable Demo**:
- Phase 1: Setup ✅
- Phase 2: Foundational (skip Cron bindings) ✅
- Phase 3: User Story 1 (skip recurring, skip reminders) ✅
- Phase 10: Basic validation ✅

**What to skip**:
- ❌ Recurring tasks (manual creation only)
- ❌ Reminders (no notifications)
- ❌ Real-time sync (manual refresh)
- ❌ Audit service
- ❌ Monitoring

**What remains**:
- ✅ Advanced task features (priority, due_date, tags)
- ✅ Full-text search and filters
- ✅ AI chat interface
- ✅ Kafka event publishing
- ✅ Dapr integration
- ✅ Kubernetes deployment

---

## Task Summary

**Total Tasks**: 201
**MVP Critical Path**: 123 tasks (T001-T068, T179-T197)
**Parallelizable Tasks**: 82 tasks marked [P]

**By Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 36 tasks (BLOCKING)
- Phase 3 (US1 - Advanced Tasks): 31 tasks (MVP CRITICAL)
- Phase 4 (US2 - Real-Time Sync): 17 tasks (NICE TO HAVE)
- Phase 5 (US3 - Monitoring): 13 tasks (OPTIONAL)
- Phase 6 (US4 - CI/CD): 16 tasks (OPTIONAL)
- Phase 7 (US5 - Multi-Cloud): 14 tasks (POST-DEMO)
- Phase 8 (Recurring Tasks): 19 tasks (MVP CRITICAL)
- Phase 9 (Audit Service): 7 tasks (NICE TO HAVE)
- Phase 10 (Polish): 40 tasks (MVP CRITICAL)

**By Priority**:
- ✅ MUST HAVE (MVP): Phases 1, 2, 3, 8, 10 → 123 tasks → 12-15 hours
- 🎯 NICE TO HAVE: Phases 4, 9 → 24 tasks → 6-9 hours
- 📋 OPTIONAL: Phases 5, 6, 7 → 43 tasks → 10-14 hours

---

## Notes

- [P] marker indicates tasks that can run in parallel (different files, no blocking dependencies)
- [US1], [US2], etc. labels map tasks to specific user stories for traceability
- Each user story phase is designed to be independently completable and testable
- MVP critical path focuses on User Story 1 (Advanced Task Management) with recurring tasks and reminders
- Real-time sync (US2) is highly recommended if time allows (demo wow factor)
- Monitoring (US3), CI/CD (US4), and Multi-Cloud (US5) are optional enhancements
- Commit after completing each phase or logical task group
- Run validation tests after each checkpoint
- Prioritize working demo over feature completeness
- Use `/sp.implement` to execute tasks in dependency order with agent automation

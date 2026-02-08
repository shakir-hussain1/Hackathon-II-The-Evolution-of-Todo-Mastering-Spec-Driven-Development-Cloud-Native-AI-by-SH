# Demo Video Guide - Phase V Advanced Cloud-Native Todo System

**Deadline**: February 9, 2026
**Target**: 10-minute professional demo for judges
**Goal**: Showcase event-driven microservices architecture with Kafka + Dapr

---

## Recording Tools

### Option 1: OBS Studio (Recommended - Free)

**Download**: https://obsproject.com

**Setup**:
1. Install OBS Studio
2. Settings → Video → Base Resolution: 1920x1080
3. Settings → Audio → Desktop Audio + Microphone
4. Scene → Add Source → Display Capture (or Window Capture)
5. File → Start Recording

### Option 2: Loom (Easiest - Web-based)

**URL**: https://www.loom.com
- Free tier: Up to 25 videos, 5 min each (record in 2 parts if needed)
- Browser extension: Instant recording
- Auto-uploads to cloud

### Option 3: Windows Game Bar

**Built-in Windows Tool**:
- Press `Win + G` to open
- Click "Capture" → Record
- Saves to: `%USERPROFILE%\Videos\Captures`

---

## Demo Script (10 Minutes)

### Part 1: Introduction (1 minute)

**What to say**:
> "Hello, I'm presenting Phase V of the Evolution of Todo - a cloud-native, event-driven microservices system built with Kafka, Dapr, and Kubernetes."

**What to show**:
- Architecture diagram (create in draw.io or Excalidraw)
- Show directory structure:
  ```bash
  tree -L 2 phase5
  ```

**Key Points**:
- 6 microservices (chat-api, notification, recurring-task, audit, websocket-sync, frontend)
- Event-driven with Apache Kafka
- Cloud-native with Dapr abstractions
- Kubernetes orchestration

---

### Part 2: Architecture Overview (2 minutes)

**What to show**:
- Open `phase5/README.md` (scroll through)
- Show architecture diagram highlighting:
  - Microservices layer (6 services)
  - Dapr sidecars (green boxes)
  - Kafka topics (task-events, reminders, task-updates)
  - PostgreSQL database
  - Ingress/Load balancer

**What to say**:
> "The system uses the sidecar pattern with Dapr for cloud-native abstractions. All inter-service communication goes through Kafka pub/sub for loose coupling. Each service has its own Dapr sidecar handling service discovery, state management, and secrets."

**Visual**:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Chat API   │───▶│    Dapr     │───▶│   Kafka     │
│  Service    │    │  Sidecar    │    │  (Events)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

### Part 3: Kubernetes Deployment (2 minutes)

**What to show** (if deployed to cloud):
```bash
# Show cluster info
kubectl cluster-info
kubectl get nodes

# Show all Phase 5 resources
kubectl get all -n phase5

# Highlight:
# - 6 service pods (2/2 containers = app + Dapr sidecar)
# - Services, Deployments, HPA
# - PostgreSQL and Kafka pods
```

**What to say**:
> "The application is deployed to Oracle Kubernetes Engine using Helm charts. Notice each pod shows 2/2 containers - that's the application and its Dapr sidecar. We have horizontal pod autoscaling configured to handle load automatically."

**Alternative** (if using Docker Compose):
```bash
docker-compose ps
# Show all services running
```

---

### Part 4: Feature Demo - Task Management (3 minutes)

**What to do**:

1. **Open Browser** to deployed URL (or localhost:3000)

2. **Register/Login**:
   ```
   Email: demo@example.com
   Password: Demo123!
   ```

3. **Create Tasks via AI Chat**:
   - Type: `Create a high priority task "Finish demo video" due tomorrow`
   - Show task appears instantly in task list
   - Highlight:
     - ✅ Priority badge (red for high)
     - ✅ Due date countdown
     - ✅ AI parsed the intent correctly

4. **Create Recurring Task**:
   - Type: `Set up weekly team standup every Monday at 9 AM`
   - Show recurring icon/indicator
   - Explain: "Recurring task service will auto-generate instances every Monday"

5. **Use Filters**:
   - Click priority filter → Select "high"
   - Show only high-priority tasks
   - Click tags → Add "#demo" filter
   - Show real-time filtering

6. **Search**:
   - Type in search bar: "demo"
   - Show full-text search results (PostgreSQL GIN index)

7. **Complete Task**:
   - Click checkbox to complete task
   - Show status change animation
   - Explain: "This published a task.completed event to Kafka"

---

### Part 5: Real-Time Sync Demo (2 minutes)

**What to do**:

1. **Open Two Browser Tabs** side by side

2. **Tab 1** (left): Create a new task
   ```
   "Test real-time sync with WebSocket"
   ```

3. **Tab 2** (right): Watch task appear INSTANTLY

**What to say**:
> "Notice the task appeared immediately in the second tab without refresh. This is powered by our WebSocket sync service. When a task is created, the chat-api publishes an event to Kafka, the websocket-sync service consumes it, and broadcasts to all connected WebSocket clients for that user."

**Connection Status Indicator**:
- Show green dot (top-right) = Connected
- Disconnect internet briefly → Yellow (reconnecting)
- Explain: "Auto-reconnect with exponential backoff"

---

### Part 6: Event-Driven Architecture (1 minute)

**What to show**:

1. **Kafka Topics** (if accessible):
   ```bash
   kubectl exec -n phase5 kafka-0 -- kafka-console-consumer --bootstrap-server localhost:9092 --topic task-events --from-beginning --max-messages 5
   ```
   - Show CloudEvents format
   - Highlight: event type, source, data

2. **Dapr Components**:
   ```bash
   kubectl get components -n phase5
   ```
   - Show: pubsub-kafka, statestore-postgresql, secretstore, cron bindings

**What to say**:
> "Every operation publishes events. Task created? Event published. Task completed? Event published. The notification service listens for these events to send reminders. The audit service logs every event for compliance. This is true event-driven architecture."

---

### Part 7: Monitoring (1 minute - Optional)

**What to show** (if configured):

1. **Zipkin Tracing**:
   ```bash
   kubectl port-forward -n dapr-system svc/dapr-dashboard 8080:8080
   # Open http://localhost:8080
   ```
   - Show distributed trace of task creation flow
   - Highlight: chat-api → Dapr → Kafka → notification-service

2. **Health Checks**:
   ```bash
   curl http://<YOUR-URL>/health
   ```
   - Show all services responding

---

### Part 8: Closing (1 minute)

**What to say**:
> "In summary, Phase V demonstrates:
> 1. **Microservices Architecture** - 6 independent services
> 2. **Event-Driven Design** - Kafka for async communication
> 3. **Cloud-Native Patterns** - Dapr for portability across clouds
> 4. **Kubernetes Orchestration** - Production-ready deployment
> 5. **Real-Time Features** - WebSocket for instant synchronization
> 6. **Modern Frontend** - Next.js with optimistic updates
>
> All code is in GitHub, deployed to Oracle Cloud, and ready for production use. Thank you!"

**Final screen**: Show GitHub repository with README open

---

## Pre-Recording Checklist

- [ ] Close unnecessary browser tabs
- [ ] Clean desktop (hide personal files)
- [ ] Open required terminals/browsers
- [ ] Test microphone (clear audio)
- [ ] Prepare demo data (pre-create 2-3 tasks)
- [ ] Have architecture diagram ready
- [ ] Check internet connection (for cloud demo)
- [ ] Practice script 2-3 times (aim for 8-10 minutes)
- [ ] Disable notifications (Windows Focus Assist)

---

## Recording Tips

1. **Audio Quality**:
   - Use headset microphone (better than laptop mic)
   - Record in quiet room
   - Speak slowly and clearly
   - Pause briefly between sections

2. **Visual Quality**:
   - 1920x1080 resolution minimum
   - Zoom in on important text (Ctrl + mousewheel)
   - Use dark theme (easier on eyes)
   - Highlight mouse cursor (OBS: Mouse Cursor to Spotlight)

3. **Pacing**:
   - Don't rush! 10 minutes is longer than you think
   - Pause to let viewers see results
   - If you make a mistake, pause and re-record that section

4. **Editing** (optional):
   - Use DaVinci Resolve (free) to cut mistakes
   - Add title slide at start
   - Add text overlays for key points
   - Export as MP4, 1080p, 30fps

---

## Upload to YouTube

1. **Create YouTube Video**:
   - Go to: https://studio.youtube.com
   - Click "Create" → "Upload video"
   - Select your MP4 file

2. **Video Details**:
   ```
   Title: Phase V - Advanced Cloud-Native Todo System | Event-Driven Microservices with Kafka & Dapr

   Description:
   Hackathon II: The Evolution of Todo - Phase V Demonstration

   A production-ready, event-driven microservices system featuring:
   - 6 microservices (Chat API, Notification, Recurring Task, Audit, WebSocket Sync, Frontend)
   - Apache Kafka for event streaming
   - Dapr for cloud-native abstractions
   - Kubernetes orchestration
   - Real-time synchronization with WebSockets
   - AI-powered task management
   - PostgreSQL database

   GitHub: [YOUR_GITHUB_REPO_URL]
   Deployed: [YOUR_DEPLOYMENT_URL]

   Tech Stack:
   - Backend: Python 3.11, FastAPI
   - Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS
   - Infrastructure: Kubernetes, Helm, Docker
   - Event Bus: Apache Kafka
   - Cloud Platform: Oracle OKE
   - Observability: Dapr, Zipkin

   Timestamp:
   0:00 - Introduction
   1:00 - Architecture Overview
   3:00 - Kubernetes Deployment
   5:00 - Feature Demo
   7:00 - Real-Time Sync
   8:00 - Event-Driven Architecture
   9:00 - Closing
   ```

3. **Settings**:
   - Visibility: **Unlisted** (shareable link, not public)
   - Category: Science & Technology
   - Tags: microservices, kubernetes, kafka, dapr, cloud-native, event-driven

4. **Get URL**: Copy shareable link (e.g., `https://youtu.be/abc123xyz`)

---

## Fallback Plan

**If cloud deployment fails:**
1. Use Docker Compose locally
2. Record demo with localhost URLs
3. In video, explain: "Deployed to local Kubernetes cluster for demo purposes. Architecture is cloud-ready and portable to any Kubernetes environment (OKE, AKS, GKE, EKS)."
4. Show Helm charts and deployment scripts to prove cloud-readiness

---

## Final Submission

**Hackathon Submission Form**:
1. ✅ GitHub Repository URL: `https://github.com/YOUR_USERNAME/Hackathon-II-The-Evolution-of-Todo`
2. ✅ Deployed Application URL: `http://YOUR_OKE_IP` or `https://your-domain.com`
3. ✅ Demo Video URL: `https://youtu.be/abc123xyz` (YouTube unlisted)
4. ✅ README.md (comprehensive documentation)
5. ✅ Architecture diagrams
6. ✅ All 5 phases in separate directories

**Deadline**: February 9, 2026 - Submit BEFORE midnight!

Good luck! 🚀

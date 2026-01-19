# Hackathon II - The Evolution of Todo

## Mastering Spec-Driven Development & Cloud Native AI

A multi-phase evolution of a Todo application demonstrating **Spec-Driven Development**, **AI-Native Engineering**, and **Production-Ready Features** using Claude Code, SpecKit Plus, OpenAI, and modern technologies.

---

## Project Overview

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase I** | Python Console App with Agent System | **COMPLETE** ✅ |
| **Phase II** | Full-Stack Web App (Next.js + FastAPI + PostgreSQL) | **COMPLETE** ✅ |
| **Phase III** | AI-Powered Todo Chatbot (OpenAI + MCP Server) | **COMPLETE** ✅ |

---

## 🎯 Phase I: Python Console App with Intelligent Agents

### Features
A Python console application with an **intelligent agent system** for task management:

| Feature | Command | Description |
|---------|---------|-------------|
| **Add Task** | `add <title>` | Create task with title and optional description |
| **View Tasks** | `list` | Display all tasks with status indicators |
| **Update Task** | `update <id> -t <title>` | Modify task title or description |
| **Delete Task** | `delete <id>` | Remove task by ID |
| **Mark Complete** | `complete <id>` | Toggle task completion status |
| **Analytics** | `analytics` | View task metrics and insights |

### Agent System Architecture

```
┌─────────────────────────────────────────────┐
│         User Interface (Modern CLI)         │
├─────────────────────────────────────────────┤
│        AgentOrchestrator (Central Hub)      │
│    ┌──────────────────────────────────┐    │
│    │     AgentRegistry (Lookup)       │    │
│    ├──────────────────────────────────┤    │
│    │  ┌─────────────┐  ┌──────────┐  │    │
│    │  │TaskMgmtAgent│  │Analytics │  │    │
│    │  ├─────────────┤  ├──────────┤  │    │
│    │  │ Skills:     │  │ Skills:  │  │    │
│    │  │ • Create    │  │ • Metrics│  │    │
│    │  │ • List      │  │          │  │    │
│    │  │ • Update    │  │          │  │    │
│    │  │ • Delete    │  │          │  │    │
│    │  │ • Toggle    │  │          │  │    │
│    │  └─────────────┘  └──────────┘  │    │
│    └──────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│      TaskManager (Business Logic)          │
└─────────────────────────────────────────────┘
```

### Quick Start

```bash
cd phase1
python src/interactive_agent_modern.py
```

### Documentation
- **README**: [`phase1/README.md`](./phase1/README.md)
- **Agent System**: [`phase1/AGENTS_README.md`](./phase1/AGENTS_README.md)
- **Specifications**: [`phase1/specs/`](./phase1/specs/)

---

## 🚀 Phase II: Full-Stack Web Application

### Architecture Overview

**Modern Full-Stack Application with Production-Ready Infrastructure**

```
┌──────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│  Next.js 16 + React 19 + TypeScript + Tailwind CSS  │
│  • Authentication (JWT)                              │
│  • Protected Routes                                  │
│  • Modern UI Components                              │
│  • API Integration                                   │
└─────────────────┬────────────────────────────────────┘
                  │ HTTPS / REST API
┌─────────────────▼────────────────────────────────────┐
│                 Backend (FastAPI)                    │
│        FastAPI + Python 3.10+ + SQLModel            │
│  • JWT Validation Middleware                         │
│  • User Isolation & Security                         │
│  • RESTful API Endpoints                             │
│  • CORS Configuration                                │
└─────────────────┬────────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────────┐
│              Database (PostgreSQL)                   │
│                  PostgreSQL 15+                      │
│  • User data with authentication                     │
│  • Tasks with user ownership                         │
│  • Indexes for performance                           │
└──────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Next.js | 16+ |
| **Frontend** | React | 19+ |
| **Frontend** | TypeScript | 5.0+ |
| **Frontend** | Tailwind CSS | 3.4+ |
| **Backend** | FastAPI | 0.110+ |
| **Backend** | Python | 3.10+ |
| **Backend** | SQLModel | 0.0.14+ |
| **Database** | PostgreSQL | 15+ |
| **Auth** | JWT | PyJWT 2.8+ |

### Features Implemented

#### User Authentication
- ✅ User registration with email/password
- ✅ JWT token generation and validation
- ✅ Secure password hashing (bcrypt)
- ✅ Protected routes with AuthGuard
- ✅ Token refresh mechanism
- ✅ Logout functionality

#### Task Management (CRUD)
- ✅ Create tasks with title and description
- ✅ List all user tasks
- ✅ Get single task details
- ✅ Update task title/description
- ✅ Delete tasks
- ✅ Toggle task completion status

#### Security & Isolation
- ✅ Multi-user data isolation
- ✅ User-scoped database queries
- ✅ JWT validation on all protected endpoints
- ✅ CORS configuration
- ✅ No cross-user data access
- ✅ Environment variable security

### API Endpoints

#### Authentication
```
POST   /auth/signup     - Register new user
POST   /auth/login      - Login and get JWT token
POST   /auth/logout     - Logout user
```

#### Tasks (Protected)
```
POST   /api/users/{user_id}/tasks              - Create task
GET    /api/users/{user_id}/tasks              - List all tasks
GET    /api/users/{user_id}/tasks/{id}         - Get single task
PUT    /api/users/{user_id}/tasks/{id}         - Update task
DELETE /api/users/{user_id}/tasks/{id}         - Delete task
PATCH  /api/users/{user_id}/tasks/{id}/complete - Toggle status
```

### Quick Start

#### Backend (FastAPI)
```bash
cd phase2/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database URL and secrets
python main.py
```

#### Frontend (Next.js)
```bash
cd phase2/frontend
npm install
cp .env.example .env.local
# Edit .env.local with your backend API URL
npm run dev
```

### Documentation
- **Complete Guide**: [`phase2/CLAUDE.md`](./phase2/CLAUDE.md)
- **Frontend Guide**: [`phase2/frontend/CLAUDE.md`](./phase2/frontend/CLAUDE.md)
- **Backend Guide**: [`phase2/backend/CLAUDE.md`](./phase2/backend/CLAUDE.md)
- **Deployment Guide**: [`phase2/DEPLOYMENT_GUIDE.md`](./phase2/DEPLOYMENT_GUIDE.md)

---

## 🤖 Phase III: AI-Powered Todo Chatbot

### Overview

**AI-Native Todo Management with Natural Language Processing**

Phase III transforms the todo application into an intelligent chatbot that understands natural language commands and manages tasks through conversational AI.

### Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│           Frontend (Next.js Split Layout)            │
│  • Chat Interface (TodoChat)                         │
│  • Task Dashboard (TaskDashboard)                    │
│  • Real-time Task Updates                            │
│  • Context-Aware State Management                    │
└─────────────────┬────────────────────────────────────┘
                  │ REST API + WebSocket
┌─────────────────▼────────────────────────────────────┐
│              Backend (FastAPI + AI Agent)            │
│  • OpenAI GPT-4 Integration                          │
│  • Natural Language Processing                       │
│  • MCP Server (Tool Execution)                       │
│  • Conversation History Management                   │
│  • Context-Aware Task Operations                     │
└─────────────────┬────────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────────┐
│         Database (SQLite/PostgreSQL)                 │
│  • Users & Authentication                            │
│  • Tasks with User Ownership                         │
│  • Conversations & Message History                   │
│  • AI Agent Context Storage                          │
└──────────────────────────────────────────────────────┘
```

### Key Features

#### AI-Powered Chat Interface
- ✅ Natural language task management
- ✅ Conversational AI with OpenAI GPT-4
- ✅ Context-aware responses
- ✅ Multi-turn conversations
- ✅ Task intent recognition
- ✅ Smart task suggestions

#### MCP Server Integration
- ✅ Tool-based architecture (MCP Protocol)
- ✅ Task CRUD operations as tools
- ✅ Function calling with OpenAI
- ✅ Structured tool responses
- ✅ Error handling and validation

#### Enhanced UI/UX
- ✅ Split-view layout (Chat + Dashboard)
- ✅ Real-time task updates
- ✅ Task statistics and filtering
- ✅ Priority and status indicators
- ✅ Responsive design
- ✅ Modern glassmorphism UI

#### Advanced Features
- ✅ Conversation history persistence
- ✅ Context management across sessions
- ✅ Task context in AI responses
- ✅ Intelligent task parsing
- ✅ Multi-user support with isolation
- ✅ Streaming AI responses

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Model** | OpenAI GPT-4 | Natural language understanding |
| **AI Integration** | OpenAI SDK | Function calling & streaming |
| **MCP Server** | Custom FastAPI | Tool execution framework |
| **Agent Runner** | Python async | Conversation orchestration |
| **Frontend State** | React Context | Task & chat state management |
| **UI Components** | React + TypeScript | Split layout & dashboard |
| **Database** | SQLite/PostgreSQL | Data persistence |

### Chat API Endpoints

```
POST   /chat                    - Send message to AI agent
GET    /chat/history            - Get conversation history
POST   /chat/clear              - Clear conversation context
```

### Task Management via Chat

Users can interact naturally with the AI agent:

```
User: "Add a task to buy groceries"
AI: "I've added 'Buy groceries' to your task list."

User: "Show me all my pending tasks"
AI: "You have 3 pending tasks: 1. Buy groceries, 2. Call dentist..."

User: "Mark the first one as complete"
AI: "Great! I've marked 'Buy groceries' as complete."

User: "Create a high priority task to finish the report by Friday"
AI: "I've created a high priority task: 'Finish the report' with due date Friday."
```

### SpecKit Plus Integration

Phase III includes comprehensive SpecKit Plus workflows:

- ✅ Feature specifications (`specs/001-ai-todo-chatbot/`)
- ✅ Implementation plans with architecture decisions
- ✅ Task breakdown with acceptance criteria
- ✅ Prompt History Records (PHRs)
- ✅ Constitution and coding principles
- ✅ Reusable agent templates
- ✅ Custom skills for validation

### Quick Start

#### Backend Setup
```bash
cd phase3/backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
python src/main.py
```

#### Frontend Setup
```bash
cd phase3/frontend
npm install
cp .env.local.example .env.local
# Configure backend API URL
npm run dev
```

### Configuration

**Required Environment Variables (Backend):**
```env
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite+aiosqlite:///./todo.db
JWT_SECRET=your-secure-secret-key
```

**Required Environment Variables (Frontend):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Documentation
- **Quick Start**: [`phase3/QUICKSTART.md`](./phase3/QUICKSTART.md)
- **Project Guide**: [`phase3/CLAUDE.md`](./phase3/CLAUDE.md)
- **Feature Spec**: [`phase3/specs/001-ai-todo-chatbot/spec.md`](./phase3/specs/001-ai-todo-chatbot/spec.md)
- **Implementation Plan**: [`phase3/specs/001-ai-todo-chatbot/plan.md`](./phase3/specs/001-ai-todo-chatbot/plan.md)
- **Data Model**: [`phase3/specs/001-ai-todo-chatbot/data-model.md`](./phase3/specs/001-ai-todo-chatbot/data-model.md)

---

## 🤖 Claude Code Agent Ecosystem

### Specialized Development Agents

We've built **7 specialized agents** to ensure code quality, security, and developer experience across all phases:

| Agent | Purpose | Key Focus Areas |
|-------|---------|----------------|
| **workflow-orchestrator** | Ensures proper development workflow | Spec → Plan → Tasks → Implementation |
| **spec-compliance-enforcer** | Verifies implementation matches specs | Requirements traceability |
| **frontend-ui-dashboard** | Modernizes UI/UX for SaaS apps | Component design, responsiveness |
| **backend-architect** | Validates FastAPI backend architecture | API design, data models, middleware |
| **auth-security-validator** | Reviews authentication & security | JWT, user isolation, SQL injection |
| **qa-validator** | Comprehensive testing & validation | Integration tests, edge cases |
| **dx-docs-improver** | Optimizes documentation & DX | README clarity, setup guides |

### Agent Documentation

Each agent has comprehensive documentation:
- **Agent Config**: `.claude/agents/{agent-name}.md`
- **Specification**: `specs/agents/{agent-name}.md`
- **History (PHR)**: `history/agents/{agent-name}.phr.md`

---

## 📁 Project Structure

```
hackathon-ii-todo/
├── .claude/                          # Claude Code Configuration
│   ├── agents/                       # 7 Specialized Agents
│   │   ├── workflow-orchestrator.md
│   │   ├── spec-compliance-enforcer.md
│   │   ├── frontend-ui-dashboard.md
│   │   ├── backend-architect.md
│   │   ├── auth-security-validator.md
│   │   ├── qa-validator.md
│   │   └── dx-docs-improver.md
│   └── skill/                        # Reusable Skills
│
├── .specify/                         # SpecKit Plus Configuration
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/                    # Spec, Plan, Task templates
│   └── scripts/                      # PowerShell automation
│
├── phase1/                           # Phase I: Python Console App
│   ├── src/
│   │   ├── agents/                   # Agent System
│   │   ├── skills/                   # Reusable Skills
│   │   ├── models/
│   │   ├── services/
│   │   └── cli/
│   ├── tests/                        # 87 tests, 100% passing
│   ├── specs/                        # Specifications
│   ├── AGENTS_README.md
│   └── README.md
│
├── phase2/                           # Phase II: Full-Stack Web App
│   ├── frontend/                     # Next.js 16 Application
│   │   ├── src/
│   │   │   ├── app/                  # Next.js App Router
│   │   │   ├── components/           # React Components
│   │   │   └── utils/                # API Client, Auth
│   │   ├── CLAUDE.md
│   │   └── package.json
│   │
│   ├── backend/                      # FastAPI Application
│   │   ├── src/
│   │   │   ├── api/                  # REST API Routes
│   │   │   ├── db/                   # Database Models
│   │   │   ├── middleware/           # JWT Auth Middleware
│   │   │   └── services/             # Business Logic
│   │   ├── main.py
│   │   ├── start.sh
│   │   ├── CLAUDE.md
│   │   └── requirements.txt
│   │
│   ├── specs/                        # Phase II Specifications
│   ├── tests/                        # Integration Tests
│   ├── DEPLOYMENT_GUIDE.md
│   ├── render.yaml
│   └── CLAUDE.md
│
├── phase3/                           # Phase III: AI Chatbot
│   ├── .claude/                      # Phase 3 Agent System
│   │   ├── agents/                   # Specialized agents
│   │   ├── commands/                 # SpecKit Plus commands
│   │   └── skill/                    # Custom skills
│   │
│   ├── .specify/                     # SpecKit Plus for Phase 3
│   │   ├── memory/
│   │   │   └── constitution.md       # Project principles
│   │   ├── templates/                # Spec templates
│   │   └── scripts/                  # Automation scripts
│   │
│   ├── backend/                      # AI-Powered Backend
│   │   ├── src/
│   │   │   ├── agent/                # OpenAI Agent System
│   │   │   │   ├── prompts.py        # AI prompts
│   │   │   │   └── runner.py         # Agent orchestration
│   │   │   ├── api/
│   │   │   │   ├── auth.py           # Authentication
│   │   │   │   ├── chat.py           # Chat endpoints
│   │   │   │   ├── tasks.py          # Task API
│   │   │   │   └── middleware.py     # JWT middleware
│   │   │   ├── mcp/                  # MCP Server
│   │   │   │   ├── server.py         # MCP protocol
│   │   │   │   └── tools.py          # Task tools
│   │   │   ├── db/                   # Database layer
│   │   │   └── models/               # Data models
│   │   ├── scripts/                  # Utility scripts
│   │   └── requirements.txt
│   │
│   ├── frontend/                     # Enhanced Frontend
│   │   ├── src/
│   │   │   ├── app/                  # Next.js pages
│   │   │   ├── components/
│   │   │   │   ├── TodoChat.tsx      # AI chat interface
│   │   │   │   ├── SplitLayout.tsx   # Split view layout
│   │   │   │   ├── TaskDashboard.tsx # Task overview
│   │   │   │   ├── TaskTable.tsx     # Task list
│   │   │   │   ├── TaskStats.tsx     # Statistics
│   │   │   │   ├── TaskFilters.tsx   # Filtering
│   │   │   │   └── TaskRow.tsx       # Task item
│   │   │   └── contexts/
│   │   │       └── TaskContext.tsx   # State management
│   │   └── package.json
│   │
│   ├── specs/                        # Phase III Specifications
│   │   └── 001-ai-todo-chatbot/
│   │       ├── spec.md               # Feature specification
│   │       ├── plan.md               # Implementation plan
│   │       ├── tasks.md              # Task breakdown
│   │       ├── data-model.md         # Database schema
│   │       ├── contracts/            # API contracts
│   │       └── checklists/           # Acceptance criteria
│   │
│   ├── history/                      # Prompt History Records
│   │   └── prompts/
│   │       └── 001-ai-todo-chatbot/
│   │
│   ├── QUICKSTART.md                 # Quick start guide
│   ├── CLAUDE.md                     # Project documentation
│   └── FINAL_FIX_WORKING.md          # Implementation notes
│
├── specs/                            # Project Specifications
│   ├── agents/                       # Agent Specifications
│   └── skills/                       # Skill Specifications
│
├── history/                          # Prompt History Records
│   ├── agents/                       # Agent PHRs
│   ├── prompts/                      # Implementation PHRs
│   └── skills/                       # Skill PHRs
│
└── README.md                         # This File
```

---

## 🎯 Development Methodology

### Spec-Driven Development Workflow

1. **Specify** (`/sp.specify`) - Create feature specification
2. **Plan** (`/sp.plan`) - Generate implementation plan
3. **Tasks** (`/sp.tasks`) - Break into TDD tasks
4. **Implement** (`/sp.implement`) - Generate code via Claude Code
5. **Validate** (Agents) - Automated quality checks
6. **Document** (PHRs) - Record development history

### Key Principles

- ✅ **No Manual Coding** - All code generated by Claude Code
- ✅ **TDD Mandatory** - Red-Green-Refactor cycle enforced
- ✅ **Spec as Source of Truth** - Implementation follows specs exactly
- ✅ **AI-Native Engineering** - Claude Code for all production code
- ✅ **Security First** - JWT, user isolation, validation
- ✅ **Agent-Validated** - 7 specialized agents ensure quality
- ✅ **Documentation Required** - PHRs for every major change

---

## 📊 Quality Metrics

### Phase I (Python Console App)
| Metric | Value |
|--------|-------|
| Tests | 87 (100% passing) |
| Code Coverage | 77% overall, 100% core logic |
| Agents | 2 specialized (TaskMgmt, Analytics) |
| Skills | 6 reusable |
| Documentation | 1,600+ lines |

### Phase II (Full-Stack Web App)
| Metric | Value |
|--------|-------|
| Frontend | Next.js 16 + React 19 |
| Backend | FastAPI + SQLModel |
| Database | PostgreSQL |
| API Endpoints | 9 (3 auth + 6 tasks) |
| User Isolation | 100% enforced |
| Security | JWT + bcrypt + CORS |
| Documentation | 3,000+ lines |

### Phase III (AI Chatbot)
| Metric | Value |
|--------|-------|
| AI Model | OpenAI GPT-4 |
| MCP Tools | 6 task operations |
| Chat Interface | Real-time streaming |
| UI Components | 8 custom React components |
| Context Management | Conversation history |
| Split Layout | Chat + Dashboard |
| Specifications | 2,000+ lines |
| Agent System | 7 specialized agents |

### Agent Ecosystem (All Phases)
| Metric | Value |
|--------|-------|
| Specialized Agents | 7 total |
| Agent Documentation | 2,100+ lines |
| Agent PHRs | 1,900+ lines |
| Coverage Areas | Workflow, Spec, Frontend, Backend, Auth, QA, Docs |

---

## 🛡️ Security Features

### Authentication & Authorization
- ✅ JWT token-based authentication
- ✅ Secure password hashing (bcrypt)
- ✅ Token expiration and refresh
- ✅ Protected API endpoints
- ✅ User session management

### Data Isolation
- ✅ User-scoped database queries
- ✅ Row-level security enforcement
- ✅ No cross-user data access
- ✅ Authorization middleware validation
- ✅ User ID verification on every request

### Security Best Practices
- ✅ Environment variables for secrets
- ✅ No hardcoded credentials
- ✅ CORS configuration
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (SQLModel)
- ✅ OpenAI API key security
- ✅ Rate limiting ready

---

## 🔧 Setup & Installation

### Prerequisites
- **Python**: 3.10+ (for backend)
- **Node.js**: 18+ (for frontend)
- **Git**: Latest version
- **PostgreSQL**: 15+ (for production) or SQLite (for development)
- **OpenAI API Key**: Required for Phase III

### Phase I Setup (Python Console App)
```bash
cd phase1
pip install pytest pytest-cov rich
python src/interactive_agent_modern.py
```

### Phase II Setup (Full-Stack App)

#### Backend
```bash
cd phase2/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python main.py
```

#### Frontend
```bash
cd phase2/frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev
```

### Phase III Setup (AI Chatbot)

#### Backend
```bash
cd phase3/backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key and configuration
python src/main.py
```

#### Frontend
```bash
cd phase3/frontend
npm install
cp .env.local.example .env.local
# Add backend API URL
npm run dev
```

---

## 🎯 Project Status

```
Phase I:   ✅ COMPLETE (Python Console App with Agents)
Phase II:  ✅ COMPLETE (Full-Stack Web Application)
Phase III: ✅ COMPLETE (AI-Powered Todo Chatbot)
```

**Current Version**: Phase III v1.0
**All Phases Complete**: ✅ Yes
**Production Ready**: ✅ Yes
**Documentation**: ✅ Complete

---

## 📈 Recent Updates

### Phase III Completion (2026-01-19) 🎉
```
Complete Phase 3: AI Todo Chatbot with full-stack implementation

✓ OpenAI GPT-4 integration for natural language understanding
✓ MCP Server with 6 task management tools
✓ Split-view UI with chat and dashboard
✓ Real-time AI streaming responses
✓ Context-aware conversation management
✓ 8 new React components (TodoChat, TaskDashboard, etc.)
✓ Enhanced state management with React Context
✓ Complete SpecKit Plus workflow documentation
✓ 7 specialized agents for quality assurance
✓ Comprehensive specifications (2,000+ lines)

Total Lines Added: 22,000+
Total Files: 154 new files
```

### Previous Updates
- **Phase II Complete**: Full-stack web app with Next.js + FastAPI
- **Agent System**: 7 specialized agents for code quality
- **Security**: JWT authentication + user isolation
- **Documentation**: 6,000+ lines across all phases

---

## 🎯 Key Features Summary

### Phase I Features
✅ Intelligent agent system (TaskManagement, Analytics)
✅ 6 reusable skills (CRUD + metrics)
✅ Modern CLI with Rich library
✅ Comprehensive testing (87 tests)
✅ Execution history tracking
✅ Registry-based architecture

### Phase II Features
✅ Next.js 16 frontend with React 19
✅ FastAPI backend with SQLModel
✅ PostgreSQL database support
✅ JWT authentication
✅ Multi-user data isolation
✅ Protected routes & API endpoints
✅ Modern UI with Tailwind CSS
✅ CRUD operations for tasks
✅ User registration & login

### Phase III Features
✅ OpenAI GPT-4 integration
✅ Natural language task management
✅ MCP Server with tool execution
✅ Real-time chat interface
✅ Split-view layout (Chat + Dashboard)
✅ Context-aware AI responses
✅ Conversation history persistence
✅ Task statistics and analytics
✅ Priority and status management
✅ Streaming AI responses
✅ Enhanced UI/UX with glassmorphism
✅ Complete SpecKit Plus integration

---

## 📚 Documentation

### Project Documentation
- **Root README**: This file - complete project overview
- **Phase I README**: [`phase1/README.md`](./phase1/README.md)
- **Phase I Agents**: [`phase1/AGENTS_README.md`](./phase1/AGENTS_README.md)
- **Phase II Guide**: [`phase2/CLAUDE.md`](./phase2/CLAUDE.md)
- **Phase II Deployment**: [`phase2/DEPLOYMENT_GUIDE.md`](./phase2/DEPLOYMENT_GUIDE.md)
- **Phase III Quick Start**: [`phase3/QUICKSTART.md`](./phase3/QUICKSTART.md)
- **Phase III Guide**: [`phase3/CLAUDE.md`](./phase3/CLAUDE.md)

### Development Guides
- **Frontend Guide (Phase II)**: [`phase2/frontend/CLAUDE.md`](./phase2/frontend/CLAUDE.md)
- **Backend Guide (Phase II)**: [`phase2/backend/CLAUDE.md`](./phase2/backend/CLAUDE.md)
- **Phase III Spec**: [`phase3/specs/001-ai-todo-chatbot/spec.md`](./phase3/specs/001-ai-todo-chatbot/spec.md)
- **Phase III Plan**: [`phase3/specs/001-ai-todo-chatbot/plan.md`](./phase3/specs/001-ai-todo-chatbot/plan.md)

### Agent Documentation
- **Agent Specs**: `specs/agents/*.md` - 7 agent specifications
- **Agent PHRs**: `history/agents/*.phr.md` - Prompt history records
- **Agent Configs**: `.claude/agents/*.md` - Claude Code configs

---

## 🤝 Contributing

This project follows **Spec-Driven Development** principles:

1. **Specify First** - Create detailed specifications
2. **Plan Implementation** - Design architecture and approach
3. **Break into Tasks** - TDD task breakdown
4. **Generate Code** - Use Claude Code for implementation
5. **Agent Validation** - Automated quality checks
6. **Test Coverage** - Comprehensive test suites
7. **Document Everything** - PHRs, specs, and guides

---

## 👨‍💻 Author

**Shakir Hussain**
GitHub: [@shakir-hussain1](https://github.com/shakir-hussain1)

---

## 📄 License

This project is part of Hackathon II - Spec-Driven Development Challenge.

---

## 🔗 Quick Links

### Phase I Documentation
- 📚 [Phase I README](./phase1/README.md)
- 📚 [Agent System Guide](./phase1/AGENTS_README.md)
- 📝 [Phase I Spec](./phase1/specs/spec.md)

### Phase II Documentation
- 📚 [Phase II Full-Stack Guide](./phase2/CLAUDE.md)
- 🚀 [Deployment Guide](./phase2/DEPLOYMENT_GUIDE.md)
- 🎨 [Frontend Guide](./phase2/frontend/CLAUDE.md)
- ⚙️ [Backend Guide](./phase2/backend/CLAUDE.md)
- 📝 [Phase II Specs](./phase2/specs/)

### Phase III Documentation
- 📚 [Phase III Quick Start](./phase3/QUICKSTART.md)
- 📚 [Phase III Project Guide](./phase3/CLAUDE.md)
- 📝 [AI Chatbot Spec](./phase3/specs/001-ai-todo-chatbot/spec.md)
- 📝 [Implementation Plan](./phase3/specs/001-ai-todo-chatbot/plan.md)
- 📝 [Data Model](./phase3/specs/001-ai-todo-chatbot/data-model.md)

### Agent System
- 🤖 [Agent Specs](./specs/agents/)
- 🤖 [Agent PHRs](./history/agents/)

### Code
- 💻 [Phase I Source](./phase1/src/)
- 💻 [Phase II Frontend](./phase2/frontend/src/)
- 💻 [Phase II Backend](./phase2/backend/src/)
- 💻 [Phase III Frontend](./phase3/frontend/src/)
- 💻 [Phase III Backend](./phase3/backend/src/)

### Testing
- 🧪 [Phase I Tests](./phase1/tests/)
- 🧪 [Phase II Tests](./phase2/tests/)

---

**Last Updated**: January 19, 2026
**Latest Version**: Phase III v1.0 - AI-Powered Todo Chatbot
**Status**: All Phases Complete ✅
**Documentation**: Complete 📚 | Agent-Validated ✅

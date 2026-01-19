# Phase III - AI Todo Chatbot: Quick Start Guide

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ and npm installed
- Neon PostgreSQL database (or any PostgreSQL instance)
- OpenAI API key

## Backend Setup

### 1. Install Backend Dependencies

```bash
cd phase3/backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database?sslmode=require
OPENAI_API_KEY=sk-your-api-key-here
JWT_SECRET=your-generated-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Initialize Database

Run database migrations:

```bash
python -m src.db.migrate
```

This creates all required tables (users, tasks, conversations, messages).

### 4. Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

**Verify backend is running:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "environment": "development"}
```

## Frontend Setup

### 1. Install Frontend Dependencies

```bash
cd phase3/frontend
npm install
```

### 2. Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## First Usage

### 1. Create an Account

1. Open browser to `http://localhost:3000`
2. You'll be redirected to the login page
3. Click "Sign up"
4. Enter email and password (min 6 characters)
5. Click "Create Account"

You'll be automatically logged in and redirected to the chat interface.

### 2. Start Chatting with AI

Try these example commands:

**Adding tasks:**
- "Add buy groceries"
- "Remind me to call mom"
- "Create task: finish project report"

**Viewing tasks:**
- "Show me my tasks"
- "What's on my todo list?"
- "List all pending tasks"

**Completing tasks:**
- "Mark buy groceries as done"
- "Complete the first task"
- "Finish the report task"

**Updating tasks:**
- "Change 'buy groceries' to 'buy groceries and household items'"
- "Update the report task"

**Deleting tasks:**
- "Delete the groceries task"
- "Remove completed tasks"

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND (Next.js 14)                                            │
│  ├── TodoChat Component (OpenAI ChatKit UI)                      │
│  ├── API Client (JWT auth, error handling)                       │
│  └── Login/Signup Pages                                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTPS + JWT
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND (FastAPI)                                                │
│  ├── Auth Middleware (JWT verification, user_id matching)        │
│  ├── Rate Limiting (60 requests/minute per user)                 │
│  └── Chat Endpoint (/api/{user_id}/chat)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ AI AGENT (OpenAI Agents SDK)                                     │
│  ├── Load Conversation History from DB                           │
│  ├── Natural Language Understanding                              │
│  ├── Tool Selection & Invocation                                 │
│  └── Response Generation                                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ MCP SERVER (Model Context Protocol)                              │
│  ├── add_task(user_id, title, description)                       │
│  ├── list_tasks(user_id, status?)                                │
│  ├── update_task(user_id, task_id, title?, description?)         │
│  ├── complete_task(user_id, task_id)                             │
│  └── delete_task(user_id, task_id)                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ DATABASE (Neon PostgreSQL)                                       │
│  ├── users (auth data)                                           │
│  ├── tasks (user_id, title, description, status, timestamps)     │
│  ├── conversations (user_id, timestamps)                         │
│  └── messages (conversation_id, role, content, tool_calls)       │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ Stateless Architecture
- Zero in-memory state between requests
- All conversation context loaded from database
- Scales horizontally without session affinity

### ✅ User Isolation
- Defense in depth security:
  - JWT validation at middleware layer
  - user_id validation at tool layer
  - All DB queries filtered by user_id
- Users can only access their own data

### ✅ Conversation Persistence
- Full chat history stored in database
- Messages ordered by sequence number
- Tool calls logged for audit trail

### ✅ Natural Language Interface
- Understands various phrasings for commands
- Handles ambiguous requests with clarification
- Provides friendly, conversational responses

## Troubleshooting

### Backend won't start

**Error: "Database connection failed"**
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Test connection: `psql $DATABASE_URL`

**Error: "OpenAI API key invalid"**
- Verify OPENAI_API_KEY in `.env`
- Check key has not expired
- Test API key: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`

### Frontend issues

**Error: "Network Error" when sending messages**
- Verify backend is running at `http://localhost:8000`
- Check NEXT_PUBLIC_API_URL in `.env.local`
- Check browser console for CORS errors

**Error: "Session expired" after login**
- Check JWT_SECRET matches between backend restarts
- Verify JWT_EXPIRATION_HOURS is set correctly
- Clear browser localStorage and login again

### Agent not responding correctly

**Agent doesn't use tools:**
- Check OpenAI API key has access to function calling
- Verify model is `gpt-4o-mini` or higher
- Check agent prompts in `backend/src/agent/prompts.py`

**Tool errors:**
- Check backend logs for MCP tool errors
- Verify database operations are working
- Test tools directly via API

## Production Deployment

### Backend (Render/Railway/Heroku)

1. Set environment variables in platform dashboard
2. Ensure DATABASE_URL points to production database
3. Set `DEBUG=false` and `ENVIRONMENT=production`
4. Use production-grade JWT_SECRET
5. Configure CORS_ORIGINS to frontend domain

### Frontend (Vercel/Netlify)

1. Set `NEXT_PUBLIC_API_URL` to backend URL
2. Deploy with `npm run build`
3. Ensure HTTPS is enabled
4. Configure custom domain if needed

### Database (Neon/Supabase)

1. Use connection pooling for production
2. Enable SSL mode (`sslmode=require`)
3. Set up regular backups
4. Monitor connection limits

### Security Checklist

- [ ] Strong JWT_SECRET (32+ characters, random)
- [ ] HTTPS enabled on both frontend and backend
- [ ] Rate limiting configured
- [ ] CORS origins restricted to production domains
- [ ] Database credentials secured
- [ ] OpenAI API key secured
- [ ] Error messages don't expose sensitive data
- [ ] Logging configured for audit trail

## Development Tips

### Backend Development

**Run tests:**
```bash
cd backend
pytest tests/
```

**Format code:**
```bash
black src/
flake8 src/
```

**Watch database logs:**
```bash
# In config.py, set DEBUG=true
# Logs all SQL queries
```

### Frontend Development

**Format code:**
```bash
npm run lint
prettier --write "src/**/*.{ts,tsx}"
```

**Build for production:**
```bash
npm run build
npm run start
```

## API Documentation

Once backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Support

For issues or questions:
1. Check backend logs: `uvicorn` console output
2. Check frontend logs: Browser DevTools console
3. Review error messages for specific guidance
4. Verify all environment variables are set correctly

## Next Steps

- Add more task fields (priority, due date, tags)
- Implement search and filtering
- Add task sharing and collaboration
- Integrate with calendar apps
- Add voice input support
- Implement task reminders
- Add analytics and insights

---

**Built with:**
- **OpenAI Agents SDK** for natural language understanding
- **MCP (Model Context Protocol)** for deterministic tool execution
- **FastAPI** for high-performance async backend
- **Next.js 14** for modern frontend with RSC
- **Neon PostgreSQL** for serverless database
- **Better Auth** for secure authentication

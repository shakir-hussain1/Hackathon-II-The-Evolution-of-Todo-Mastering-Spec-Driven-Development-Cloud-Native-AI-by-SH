# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 001-ai-todo-chatbot
**Date**: 2026-01-13
**Purpose**: Local development setup and testing guide

## Prerequisites

### Required Software

- **Python**: 3.11+ ([Download](https://www.python.org/downloads/))
- **Node.js**: 18+ ([Download](https://nodejs.org/))
- **PostgreSQL**: 14+ (or Neon account for cloud database)
- **Git**: Latest version
- **Code Editor**: VS Code recommended

### Required Accounts

- **OpenAI API Key**: [Get API key](https://platform.openai.com/api-keys)
- **Neon PostgreSQL**: [Create free account](https://neon.tech/) (or use local PostgreSQL)
- **Better Auth**: Setup in project (no external account needed)

## Project Structure

```
phase3/
├── backend/               # FastAPI Python backend
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/              # Next.js frontend
│   ├── src/
│   ├── package.json
│   ├── .env.local.example
│   └── README.md
└── README.md             # This file
```

## Quick Setup (5 Minutes)

### 1. Clone and Navigate

```bash
cd phase3
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Required variables:
# - DATABASE_URL (Neon PostgreSQL connection string)
# - OPENAI_API_KEY (OpenAI API key)
# - JWT_SECRET (generate with: python -c "import secrets; print(secrets.token_hex(32))")
```

### 3. Database Setup

```bash
# Run migrations to create tables
python -m src.db.migrate

# (Optional) Seed test data
python -m src.db.seed
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 5. Start Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### 6. Open Application

Visit [http://localhost:3000](http://localhost:3000) in your browser.

## Detailed Setup

### Backend Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database?sslmode=require

# OpenAI
OPENAI_API_KEY=sk-...your-api-key...

# Authentication
JWT_SECRET=your-generated-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Generate JWT_SECRET**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Get Neon DATABASE_URL**:
1. Go to [Neon Console](https://console.neon.tech/)
2. Create project
3. Copy connection string from dashboard
4. Replace `postgresql://` with `postgresql+asyncpg://`
5. Add `?sslmode=require` at the end

### Frontend Environment Variables (.env.local)

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-generated-secret-key-here

# Environment
NODE_ENV=development
```

**Generate BETTER_AUTH_SECRET**:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## Development Workflow

### Running Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Development mode with hot reload
uvicorn src.main:app --reload --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Backend will be available at**: http://localhost:8000
**API Documentation**: http://localhost:8000/docs (Swagger UI)

### Running Frontend

```bash
cd frontend

# Development mode
npm run dev

# Production build
npm run build
npm start
```

**Frontend will be available at**: http://localhost:3000

### Running Tests

**Backend Tests**:
```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/test_chat_api.py -v
```

**Frontend Tests**:
```bash
cd frontend
npm test

# Watch mode
npm test -- --watch
```

## Creating Your First User

### Option 1: Via Frontend UI

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email and password
4. Confirm email (if email verification enabled)
5. Log in

### Option 2: Via API (for testing)

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

Response:
```json
{
  "user": {
    "id": "user-uuid",
    "email": "test@example.com"
  },
  "token": "jwt-token-here"
}
```

## Testing the Chat API

### 1. Get JWT Token

Log in to get a JWT token:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

Save the token from response.

### 2. Send Chat Messages

**Add a task**:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add buy groceries to my todo list"
  }'
```

**List tasks**:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me all my tasks"
  }'
```

**Complete a task**:
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Mark buy groceries as complete"
  }'
```

## Database Management

### View Database

**Using Neon Console**:
1. Go to [Neon Console](https://console.neon.tech/)
2. Select your project
3. Click "SQL Editor"
4. Run queries

**Using psql (local PostgreSQL)**:
```bash
psql postgresql://user:password@localhost:5432/database

# List tables
\dt

# View users
SELECT * FROM users;

# View tasks
SELECT * FROM tasks WHERE user_id = 'user-uuid';

# View conversations
SELECT * FROM conversations WHERE user_id = 'user-uuid';

# View messages
SELECT * FROM messages WHERE conversation_id = 'conversation-uuid' ORDER BY sequence_number;
```

### Reset Database

```bash
cd backend

# Drop all tables and recreate
python -m src.db.reset

# Re-run migrations
python -m src.db.migrate

# Re-seed test data
python -m src.db.seed
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Ensure you're in the backend directory and virtual environment is activated:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: "Connection to database failed"

**Solution**: Check DATABASE_URL in .env:
- Verify connection string format: `postgresql+asyncpg://...`
- Ensure database exists in Neon console
- Check firewall/network settings
- Test connection: `python -c "import asyncpg; asyncpg.connect('your-url')"`

### Issue: "OpenAI API key not found"

**Solution**: Set OPENAI_API_KEY in backend/.env:
```bash
OPENAI_API_KEY=sk-...your-key...
```

### Issue: "JWT token validation failed"

**Solution**: Ensure JWT_SECRET matches between backend and frontend:
- Generate a new secret if needed
- Set same secret in backend/.env and frontend/.env.local
- Clear browser cookies and log in again

### Issue: "CORS error when calling API from frontend"

**Solution**: Add frontend URL to CORS_ORIGINS in backend/.env:
```bash
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Issue: "Port already in use"

**Solution**: Kill existing process or use different port:
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows

# Or use different port
uvicorn src.main:app --reload --port 8001
```

## Development Tips

### Hot Reload

- **Backend**: FastAPI auto-reloads on file changes (with `--reload` flag)
- **Frontend**: Next.js auto-reloads on file changes in dev mode

### Debugging

**Backend (VS Code)**:
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

**Frontend (VS Code)**:
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    }
  ]
}
```

### Logging

**Backend logs**:
- Console output from `uvicorn` command
- Set `DEBUG=true` in .env for detailed logs
- SQL queries logged with `echo=True` in engine config

**Frontend logs**:
- Browser console (F12 → Console tab)
- Terminal output from `npm run dev`

## Next Steps

1. **Implement Backend**: Follow tasks.md to implement FastAPI endpoints, MCP tools, and agent integration
2. **Implement Frontend**: Integrate OpenAI ChatKit with backend API
3. **Test Locally**: Verify all 5 CRUD operations work via natural language
4. **Deploy**: Deploy backend to Render, frontend to Vercel (see deployment guide)

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Agents SDK](https://github.com/openai/openai-python)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com/)
- [Neon PostgreSQL Docs](https://neon.tech/docs/)

## Support

For issues or questions:
1. Check [Common Issues](#common-issues--solutions) above
2. Review API documentation at http://localhost:8000/docs
3. Check logs in terminal and browser console
4. Refer to feature specification at `specs/001-ai-todo-chatbot/spec.md`

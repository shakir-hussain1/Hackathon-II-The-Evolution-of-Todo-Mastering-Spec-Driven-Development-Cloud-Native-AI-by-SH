# 🚀 Phase 2 Todo - Complete Local Setup Guide

**Last Updated**: January 10, 2026
**Status**: Ready to Run
**Time to Setup**: ~5 minutes

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- ✅ **Node.js 18+** and **npm** installed ([Download](https://nodejs.org/))
- ✅ **Git** installed (optional, for version control)

Check your versions:
```bash
python --version    # Should be 3.10 or higher
node --version      # Should be 18.0 or higher
npm --version       # Should be 9.0 or higher
```

---

## 🎯 Quick Start (3 Commands)

If you're in a hurry, run these 3 commands in **separate terminals**:

### Terminal 1 - Backend:
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\backend
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend
npm run dev
```

### Terminal 3 - Open Browser:
```bash
start http://localhost:3000
```

✅ **Done!** Jump to [Step 5: Using the Application](#step-5-using-the-application)

---

## 📖 Detailed Step-by-Step Guide

### Step 1: Setup Backend (Python FastAPI)

#### 1.1 Navigate to Backend Directory
Open **Command Prompt** or **PowerShell** and run:
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\backend
```

#### 1.2 Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows Command Prompt)
venv\Scripts\activate

# OR activate it (Windows PowerShell)
venv\Scripts\Activate.ps1

# OR activate it (Git Bash)
source venv/Scripts/activate
```

You should see `(venv)` in your terminal prompt.

#### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLModel (database ORM)
- PyJWT (authentication)
- And other dependencies

**Expected output:**
```
Successfully installed fastapi-0.110.0 uvicorn-0.27.0 ...
```

#### 1.4 Check Backend Environment File
The backend already has a `.env` file configured. Verify it exists:
```bash
# Windows
type .env

# Git Bash/Linux
cat .env
```

You should see:
```env
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET=your-secret-key-change-in-production-min-32-chars-long
BETTER_AUTH_SECRET=your-better-auth-secret-change-in-production
DEBUG=True
HOST=127.0.0.1
PORT=8000
```

#### 1.5 Start Backend Server
```bash
python -m uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
Starting up FastAPI application...
[OK] Database tables created
INFO:     Application startup complete.
```

✅ **Backend is running!** Keep this terminal open.

**Test it:**
Open browser to http://127.0.0.1:8000/health - You should see:
```json
{"status":"ok","message":"API is running"}
```

---

### Step 2: Setup Frontend (Next.js)

#### 2.1 Open a NEW Terminal
**Important:** Don't close the backend terminal. Open a second terminal window.

#### 2.2 Navigate to Frontend Directory
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend
```

#### 2.3 Install Node Dependencies
```bash
npm install
```

This installs:
- Next.js 16+ (React framework)
- React 19+
- TypeScript
- Tailwind CSS
- And other dependencies

**Expected output:**
```
added 345 packages in 45s
```

**Note:** If you see `npm ERR!`, try:
```bash
npm install --legacy-peer-deps
```

#### 2.4 Check Frontend Environment File
Verify the `.env.local` file exists:
```bash
# Windows
type .env.local

# Git Bash/Linux
cat .env.local
```

You should see:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

If the file doesn't exist, create it:
```bash
echo NEXT_PUBLIC_API_URL=http://127.0.0.1:8000 > .env.local
```

#### 2.5 Start Frontend Development Server
```bash
npm run dev
```

**Expected output:**
```
▲ Next.js 16.1.1 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.x.x:3000

✓ Starting...
✓ Ready in 10.9s
```

✅ **Frontend is running!** Keep this terminal open too.

---

### Step 3: Verify Both Servers Are Running

You should now have **2 terminals open**:

**Terminal 1 (Backend):**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 (Frontend):**
```
▲ Next.js 16.1.1
- Local:         http://localhost:3000
```

---

### Step 4: Open the Application

#### 4.1 Open Your Browser
Navigate to:
```
http://localhost:3000
```

#### 4.2 You Should See
The home page will automatically redirect you to the **login page**:
```
http://localhost:3000/auth/login
```

You'll see a beautiful gradient background with:
- Login form
- Email and password fields
- "Login" button
- "Don't have an account? Sign Up" link

---

### Step 5: Using the Application

#### Option A: Create a New Account

1. **Click "Sign Up"** link at the bottom
2. **Enter your details:**
   - Email: `yourname@example.com`
   - Password: `YourPassword123!`
   - Username: `yourname`
3. **Click "Create Account"**
4. You'll be automatically logged in and redirected to the dashboard

#### Option B: Use Test Account

If you want to use the test account I created during testing:
- **Email:** `livetest@example.com`
- **Password:** `LiveTest123!`

---

### Step 6: Explore the Dashboard

Once logged in, you'll see:

#### **Left Panel - Create Task Form:**
- Title field (required)
- Description field (optional)
- Character counters with progress bars
- "Create Task" button

#### **Right Panel - Your Tasks:**
- Filter buttons (All / Pending / Done)
- Sort dropdown (Newest First / Oldest First)
- Task list with:
  - Checkbox to mark complete/incomplete
  - Task title and description
  - Status badge
  - Delete button (shows on hover)

#### **Bottom Stats:**
- Total Tasks counter
- In Progress counter
- Completed counter

---

### Step 7: Test the Features

#### Create a Task:
1. Type in the title field: `"Buy groceries"`
2. Add description: `"Milk, eggs, bread, and butter"`
3. Click **"Create Task"**
4. See success message and task appears in the list

#### Mark Task Complete:
1. Click the **checkbox** next to the task
2. Task gets a green background
3. Title gets strikethrough
4. Status changes to "Complete"

#### Filter Tasks:
- Click **"Pending"** to see only incomplete tasks
- Click **"Done"** to see only completed tasks
- Click **"All"** to see everything

#### Delete a Task:
1. Hover over a task card
2. Click the **red trash icon** on the right
3. Task is removed

#### Logout:
- Click the **"Logout"** button in the top-right corner
- You'll be redirected to the login page

---

## 🛑 Stopping the Servers

When you're done:

### Stop Frontend:
In the frontend terminal, press:
```
CTRL + C
```

### Stop Backend:
In the backend terminal, press:
```
CTRL + C
```

---

## 🔄 Restarting Later

Next time you want to use the app:

### Terminal 1 - Backend:
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\backend
venv\Scripts\activate  # If using virtual environment
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```bash
cd E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend
npm run dev
```

### Browser:
```
http://localhost:3000
```

---

## 📁 Project Structure

```
phase2/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # Entry point
│   ├── requirements.txt       # Python dependencies
│   ├── todo.db               # SQLite database (auto-created)
│   └── src/                  # Source code
│       ├── api/routes/       # API endpoints
│       ├── middleware/       # JWT authentication
│       └── services/         # Business logic
│
├── frontend/                  # Next.js frontend
│   ├── package.json          # Node dependencies
│   ├── src/app/             # Pages
│   │   ├── auth/           # Login/Signup pages
│   │   └── dashboard/      # Main dashboard
│   ├── src/components/      # React components
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthGuard.tsx
│   └── src/utils/           # Utilities
│       ├── api-client.ts   # API wrapper
│       └── auth.ts         # Token management
│
└── LOCAL_SETUP_COMPLETE.md   # This file
```

---

## 🔍 API Endpoints

Once running, you can test the API directly:

### Health Check:
```bash
curl http://127.0.0.1:8000/health
```

### Signup:
```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123!\",\"username\":\"testuser\"}"
```

### Login:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123!\"}"
```

### Create Task (requires JWT token):
```bash
curl -X POST http://127.0.0.1:8000/api/users/{user_id}/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "{\"title\":\"My Task\",\"description\":\"Task details\"}"
```

---

## 🐛 Troubleshooting

### Backend Issues:

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
- Solution: Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

**Error: `Address already in use`**
- Solution: Port 8000 is already in use. Either:
  - Stop other process using port 8000
  - Or use different port: `python -m uvicorn main:app --reload --port 8001`
  - Then update frontend `.env.local` to `NEXT_PUBLIC_API_URL=http://127.0.0.1:8001`

**Error: `sqlite3.OperationalError: database is locked`**
- Solution: Close all terminals and restart. Only run one backend instance.

### Frontend Issues:

**Error: `npm ERR! ERESOLVE unable to resolve dependency tree`**
- Solution: Run `npm install --legacy-peer-deps`

**Error: `Port 3000 is already in use`**
- Solution: Either:
  - Stop other process using port 3000
  - Or run on different port: `npm run dev -- -p 3001`
  - Then open `http://localhost:3001` in browser

**Error: `Cannot connect to backend` / `Network Error`**
- Solution:
  - Make sure backend is running on port 8000
  - Check `.env.local` has correct API URL
  - Verify `http://127.0.0.1:8000/health` works in browser

**Blank page or continuous loading:**
- Solution:
  - Clear browser cache (Ctrl+Shift+Delete)
  - Check browser console for errors (F12)
  - Make sure both backend and frontend are running

---

## 📊 Database

The application uses **SQLite** database stored at:
```
E:\Hackathon-II-The-Evolution-of-Todo\phase2\backend\todo.db
```

### View Database Contents:
```bash
cd backend
sqlite3 todo.db
.tables          # List all tables
SELECT * FROM users;   # View all users
SELECT * FROM tasks;   # View all tasks
.quit            # Exit sqlite3
```

### Reset Database:
If you want to start fresh, delete the database:
```bash
cd backend
del todo.db      # Windows
rm todo.db       # Git Bash/Linux
```

Next time you start the backend, it will create a new empty database.

---

## 🎨 Customization

### Change API Port:
**Backend:** Edit `backend/.env`
```env
PORT=8001
```

**Frontend:** Edit `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8001
```

### Change Frontend Port:
```bash
npm run dev -- -p 3001
```

### Disable Debug Mode:
Edit `backend/.env`:
```env
DEBUG=False
```

---

## 📚 Additional Resources

- **Backend API Docs:** http://127.0.0.1:8000/docs (Swagger UI)
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Next.js Documentation:** https://nextjs.org/docs
- **React Documentation:** https://react.dev/

---

## ✅ Summary Checklist

Before you start, make sure:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser open to http://localhost:3000

---

## 🎉 Success!

If you can see the login page and create tasks, **congratulations!** Your Phase 2 Todo application is fully functional.

**Enjoy your stylish, modern, colorful task manager!** 🚀✨

---

**Need Help?**
- Check the troubleshooting section above
- Review terminal output for error messages
- Make sure both servers are running simultaneously
- Verify ports 3000 and 8000 are not blocked by firewall

**Last Updated:** January 10, 2026

# ⚡ Quick Start - Unified Dashboard

**New Design**: Everything in ONE form/table interface!

---

## 🔧 Step 1: Fix Backend (One-Time Setup)

### Option A: Run This Batch File
```bash
cd phase2/backend
INSTALL_DEPS.bat
```

### Option B: Manual Commands
```bash
cd phase2/backend
python -m venv venv
venv\Scripts\activate
venv\Scripts\pip install fastapi uvicorn sqlmodel sqlalchemy psycopg2-binary PyJWT pydantic pydantic-settings python-dotenv python-multipart typing-extensions passlib "bcrypt>=4.0.0,<5.0.0"
```

---

## 🚀 Step 2: Start Backend

```bash
cd phase2/backend
venv\Scripts\activate
python main.py
```

**Wait for**: `INFO: Uvicorn running on http://0.0.0.0:8000`

---

## 🎨 Step 3: Start Frontend (New Terminal)

```bash
cd phase2/frontend
npm run dev
```

**Wait for**: `Local: http://localhost:3000`

---

## ✨ Step 4: Open & Test

**Open**: http://localhost:3000

---

## 🎯 New Unified Dashboard Features

### Everything in ONE Interface:

```
┌─────────────────────────────────────────────┐
│  STATS: Total: 1 | Pending: 1 | Done: 0     │
├─────────────────────────────────────────────┤
│  ➕ ADD NEW TASK                             │
│  [Title] [Description] [➕ Add Task]        │
├─────────────────────────────────────────────┤
│  FILTER: [All] [Pending] [Completed]        │
├─────────────────────────────────────────────┤
│  TASK LIST:                                  │
│  ☑ Buy groceries        [✏️ Edit] [🗑️ Delete] │
│    Rice, Sugar                               │
└─────────────────────────────────────────────┘
```

### All Features Integrated:

1. **Add Task**: Form at top - type and click "Add Task"
2. **View Tasks**: List below with all details
3. **Mark Complete**: Click checkbox ☑
4. **Edit Task**: Click "Edit" → Inline editing appears
5. **Delete Task**: Click "Delete" → Simple confirm
6. **Filter**: Click All/Pending/Completed buttons
7. **Stats**: Real-time counts at top

---

## 🧪 Test Flow:

1. **Sign Up**: test@example.com / TestPassword123!
2. **Add Task**:
   - Type "Buy groceries" in Title
   - Type "Rice, Sugar" in Description
   - Click "➕ Add Task"
3. **See Task**: Appears immediately in list below
4. **Edit Task**:
   - Click "✏️ Edit" button
   - Fields become editable inline
   - Change text
   - Click "✓ Save"
5. **Mark Complete**: Click the checkbox ☑
6. **Delete**: Click "🗑️ Delete" → Confirm

---

## 💡 Key Differences (vs Old Version):

| Feature | Old | New |
|---------|-----|-----|
| Add Task | Separate form sidebar | Top of same view |
| Edit Task | Modal popup | Inline editing |
| All Features | Scattered | ONE unified form |
| Layout | Side-by-side cards | Single clean table |

---

## ❌ If Backend Fails to Install:

Try this:
```bash
cd phase2/backend

# Delete old venv completely
rmdir /s /q venv

# Create fresh
python -m venv venv

# Activate
venv\Scripts\activate

# Install one by one
pip install fastapi
pip install uvicorn
pip install sqlmodel
pip install sqlalchemy
pip install psycopg2-binary
pip install PyJWT
pip install pydantic
pip install pydantic-settings
pip install python-dotenv
pip install python-multipart
pip install passlib
pip install "bcrypt==4.0.1"
```

---

**Ready!** Now start backend → start frontend → open browser! 🎉

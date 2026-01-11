# Frontend CLAUDE.md – Next.js Development Guide

**Project**: Hackathon II – Phase II
**Framework**: Next.js 16+ with App Router
**Language**: TypeScript 5.0+
**Status**: Implementation Ready

---

## Overview

The Phase II frontend is a Next.js application with:
- **Authentication**: Better Auth signup/login pages, JWT token storage
- **Protected Routes**: Dashboard and task management protected with AuthGuard
- **API Client**: Fetch wrapper that automatically attaches JWT to requests
- **Components**: Reusable TaskList, TaskForm, AuthGuard components
- **State**: React hooks (useState, useEffect) for local state
- **Types**: Full TypeScript coverage for all API interactions

---

## File Structure

```
frontend/
├── CLAUDE.md                          # This file
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.example
├── src/
│   ├── app/                           # Next.js App Router
│   │   ├── layout.tsx                 # Root layout
│   │   ├── page.tsx                   # Home page (redirect to /dashboard)
│   │   ├── auth/
│   │   │   ├── layout.tsx             # Auth layout (no protection)
│   │   │   ├── signup/
│   │   │   │   └── page.tsx           # T016: Signup form (Better Auth)
│   │   │   └── login/
│   │   │       └── page.tsx           # T017: Login form (Better Auth)
│   │   └── dashboard/
│   │       ├── layout.tsx             # T031: Protected layout with AuthGuard
│   │       └── page.tsx               # T027: Dashboard with TaskList + TaskForm
│   │
│   ├── components/
│   │   ├── TaskList.tsx               # T025: Display user's tasks
│   │   ├── TaskForm.tsx               # T026: Create/edit task form
│   │   └── AuthGuard.tsx              # T030: Route protection component
│   │
│   └── utils/
│       ├── api-client.ts              # T010: Fetch wrapper with JWT attachment
│       ├── auth.ts                    # T009: Token storage/retrieval
│       └── types.ts                   # Shared TypeScript types
│
└── public/
    └── (static assets)
```

---

## Environment Variables

**File**: `.env.example`

```env
# API Server URL (backend running locally or deployed)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Usage in Code**:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
```

---

## Key Patterns

### 1. Token Storage & Retrieval (T009)

**File**: `src/utils/auth.ts`

```typescript
// Get token from localStorage
export async function getToken(): Promise<string | null> {
  if (typeof window === "undefined") return null; // SSR safety
  return localStorage.getItem("token");
}

// Save token to localStorage
export async function setToken(token: string): Promise<void> {
  if (typeof window === "undefined") return;
  localStorage.setItem("token", token);
}

// Clear token on logout
export async function clearToken(): Promise<void> {
  if (typeof window === "undefined") return;
  localStorage.removeItem("token");
}

// Check if user is authenticated
export async function isAuthenticated(): Promise<boolean> {
  const token = await getToken();
  return !!token;
}
```

### 2. API Client with JWT Attachment (T010)

**File**: `src/utils/api-client.ts`

```typescript
import { getToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = await getToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  // Attach JWT to every request (except auth endpoints)
  if (token && !endpoint.includes("/auth/")) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${API_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json();
    throw {
      status: response.status,
      ...error,
    };
  }

  return response.json();
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string) =>
    apiCall<T>(endpoint, { method: "GET" }),

  post: <T>(endpoint: string, body: any) =>
    apiCall<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    }),

  put: <T>(endpoint: string, body: any) =>
    apiCall<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  patch: <T>(endpoint: string, body: any) =>
    apiCall<T>(endpoint, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),

  delete: <T>(endpoint: string) =>
    apiCall<T>(endpoint, { method: "DELETE" }),
};
```

### 3. TypeScript Types

**File**: `src/utils/types.ts`

```typescript
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  status: "incomplete" | "complete";
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  email: string;
}

export interface AuthResponse {
  success: boolean;
  user: User;
  token: string;
}

export type TaskStatus = "incomplete" | "complete";
```

### 4. Protected Routes with AuthGuard (T030)

**File**: `src/components/AuthGuard.tsx`

```typescript
"use client"; // Client component for useRouter

import { useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/utils/auth";

interface AuthGuardProps {
  children: ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();
  const [isAuthed, setIsAuthed] = (useState < boolean) | (false);
  const [isLoading, setIsLoading] = (useState < boolean) | (true);

  useEffect(() => {
    async function checkAuth() {
      const authed = await isAuthenticated();
      if (!authed) {
        router.push("/auth/login");
      } else {
        setIsAuthed(true);
      }
      setIsLoading(false);
    }

    checkAuth();
  }, [router]);

  if (isLoading) return <div>Loading...</div>;
  if (!isAuthed) return null;

  return <>{children}</>;
}
```

### 5. Protected Dashboard Layout (T031)

**File**: `src/app/dashboard/layout.tsx`

```typescript
import { AuthGuard } from "@/components/AuthGuard";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold">Todo Dashboard</h1>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 py-8">
          {children}
        </main>
      </div>
    </AuthGuard>
  );
}
```

### 6. TaskList Component (T025)

**File**: `src/components/TaskList.tsx`

```typescript
"use client";

import { useEffect, useState } from "react";
import { api } from "@/utils/api-client";
import { Task } from "@/utils/types";

interface TaskListProps {
  userId: string;
  onTaskClick?: (task: Task) => void;
}

export function TaskList({ userId, onTaskClick }: TaskListProps) {
  const [tasks, setTasks] = (useState < Task[]) | ([]);
  const [loading, setLoading] = (useState < boolean) | (true);
  const [error, setError] = (useState < string | null) | (null);

  useEffect(() => {
    async function fetchTasks() {
      try {
        const response = await api.get<{ data: Task[] }>(
          `/api/users/${userId}/tasks`
        );
        setTasks(response.data || []);
      } catch (err: any) {
        setError(err.message || "Failed to load tasks");
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, [userId]);

  if (loading) return <div>Loading tasks...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return (
    <div className="space-y-2">
      {tasks.length === 0 ? (
        <p className="text-gray-500">No tasks yet. Create one to get started!</p>
      ) : (
        tasks.map((task) => (
          <div
            key={task.id}
            className={`p-4 border rounded cursor-pointer ${
              task.status === "complete" ? "bg-green-50" : "bg-white"
            }`}
            onClick={() => onTaskClick?.(task)}
          >
            <h3 className={task.status === "complete" ? "line-through" : ""}>
              {task.title}
            </h3>
            {task.description && (
              <p className="text-gray-600 text-sm">{task.description}</p>
            )}
            <span className="text-xs text-gray-400">
              Status: {task.status}
            </span>
          </div>
        ))
      )}
    </div>
  );
}
```

### 7. TaskForm Component (T026)

**File**: `src/components/TaskForm.tsx`

```typescript
"use client";

import { useState } from "react";
import { api } from "@/utils/api-client";
import { Task } from "@/utils/types";

interface TaskFormProps {
  userId: string;
  task?: Task;
  onSuccess?: (task: Task) => void;
}

export function TaskForm({ userId, task, onSuccess }: TaskFormProps) {
  const [title, setTitle] = (useState < string) | (task?.title || "");
  const [description, setDescription] = (useState < string) | (
    task?.description || ""
  );
  const [loading, setLoading] = (useState < boolean) | (false);
  const [error, setError] = (useState < string | null) | (null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (task) {
        // Update existing task
        const response = await api.put<{ data: Task }>(
          `/api/users/${userId}/tasks/${task.id}`,
          { title, description }
        );
        onSuccess?.(response.data);
      } else {
        // Create new task
        const response = await api.post<{ data: Task }>(
          `/api/users/${userId}/tasks`,
          { title, description }
        );
        onSuccess?.(response.data);
      }
      setTitle("");
      setDescription("");
    } catch (err: any) {
      setError(err.message || "Failed to save task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-600 p-2 bg-red-50">{error}</div>}

      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
        required
        maxLength={255}
        className="w-full px-4 py-2 border rounded"
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Task description (optional)"
        maxLength={10000}
        className="w-full px-4 py-2 border rounded h-24"
      />

      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "Saving..." : task ? "Update Task" : "Create Task"}
      </button>
    </form>
  );
}
```

### 8. Signup Page (T016)

**File**: `src/app/auth/signup/page.tsx`

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/utils/api-client";
import { setToken } from "@/utils/auth";
import type { AuthResponse } from "@/utils/types";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = (useState < string) | ("");
  const [password, setPassword] = (useState < string) | ("");
  const [error, setError] = (useState < string | null) | (null);
  const [loading, setLoading] = (useState < boolean) | (false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post<AuthResponse>("/auth/signup", {
        email,
        password,
      });

      // Store JWT token
      await setToken(response.token);

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-8 border rounded">
      <h1 className="text-2xl font-bold mb-6">Sign Up</h1>

      {error && <div className="text-red-600 p-2 bg-red-50 mb-4">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          className="w-full px-4 py-2 border rounded"
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          className="w-full px-4 py-2 border rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {loading ? "Signing up..." : "Sign Up"}
        </button>
      </form>

      <p className="mt-4 text-center">
        Already have an account?{" "}
        <a href="/auth/login" className="text-blue-600">
          Login
        </a>
      </p>
    </div>
  );
}
```

### 9. Login Page (T017)

**File**: `src/app/auth/login/page.tsx`

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/utils/api-client";
import { setToken } from "@/utils/auth";
import type { AuthResponse } from "@/utils/types";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = (useState < string) | ("");
  const [password, setPassword] = (useState < string) | ("");
  const [error, setError] = (useState < string | null) | (null);
  const [loading, setLoading] = (useState < boolean) | (false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post<AuthResponse>("/auth/login", {
        email,
        password,
      });

      // Store JWT token
      await setToken(response.token);

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-8 border rounded">
      <h1 className="text-2xl font-bold mb-6">Login</h1>

      {error && <div className="text-red-600 p-2 bg-red-50 mb-4">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          className="w-full px-4 py-2 border rounded"
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          className="w-full px-4 py-2 border rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      <p className="mt-4 text-center">
        Don't have an account?{" "}
        <a href="/auth/signup" className="text-blue-600">
          Sign Up
        </a>
      </p>
    </div>
  );
}
```

### 10. Dashboard Page (T027)

**File**: `src/app/dashboard/page.tsx`

```typescript
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { TaskList } from "@/components/TaskList";
import { TaskForm } from "@/components/TaskForm";
import { getToken, clearToken } from "@/utils/auth";
import jwt_decode from "jwt-decode";

interface DecodedToken {
  sub: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [userId, setUserId] = (useState < string | null) | (null);
  const [refreshKey, setRefreshKey] = (useState < number) | (0);

  useEffect(() => {
    async function extractUserId() {
      const token = await getToken();
      if (!token) {
        router.push("/auth/login");
        return;
      }

      try {
        const decoded = jwt_decode<DecodedToken>(token);
        setUserId(decoded.sub);
      } catch {
        await clearToken();
        router.push("/auth/login");
      }
    }

    extractUserId();
  }, [router]);

  const handleLogout = async () => {
    await clearToken();
    router.push("/auth/login");
  };

  if (!userId) return <div>Loading...</div>;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Tasks</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Logout
        </button>
      </div>

      <div className="grid grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">Create Task</h2>
          <TaskForm
            userId={userId}
            onSuccess={() => setRefreshKey((k) => k + 1)}
          />
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
          <TaskList key={refreshKey} userId={userId} />
        </div>
      </div>
    </div>
  );
}
```

---

## Development Rules

### 1. Use "use client" Directive
- Interactive components with hooks: `"use client"`
- Pages with forms/state: `"use client"`
- Static pages: Server components (default)

```typescript
"use client"; // Required for useState, useEffect, onClick handlers
```

### 2. API Calls Pattern
- Always use `api.get()`, `api.post()`, `api.put()`, `api.delete()` from api-client
- Include error handling with try-catch
- Attach user_id to URL: `/api/users/{userId}/tasks`
- JWT automatically attached by api-client middleware

```typescript
try {
  const response = await api.get<Task[]>(`/api/users/${userId}/tasks`);
} catch (error) {
  // Handle error
}
```

### 3. Protected Routes
- Wrap protected pages in AuthGuard component
- Check token existence and validity
- Redirect to /auth/login if not authenticated

```typescript
// In layout.tsx or page.tsx
<AuthGuard>
  {/* Protected content */}
</AuthGuard>
```

### 4. Component Organization
- Functional components with hooks
- Props typed with TypeScript interfaces
- Use React best practices (dependencies in useEffect)

### 5. Error Handling
```typescript
try {
  // API call or operation
} catch (error: any) {
  // Log error (optional)
  // Show user-friendly message
  // Redirect if 401
  if (error.status === 401) {
    router.push("/auth/login");
  } else {
    toast.error(error.message || "Something went wrong");
  }
}
```

### 6. TypeScript Coverage
- All functions typed with return types
- All props interfaces defined
- Import types properly:
  ```typescript
  import type { Task } from "@/utils/types";
  ```

### 7. Styling
- Use Tailwind CSS classes
- Responsive design (mobile-first)
- Consistent colors and spacing
- Accessible elements (labels, ARIA)

---

## Environment Setup

### .env.example
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### package.json Dependencies
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.0.0",
    "jwt-decode": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/node": "^20.0.0",
    "tailwindcss": "^3.0.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0"
  }
}
```

---

## Key Points to Remember

1. **Always attach JWT**: Every API call (except signup/login) gets JWT via api-client
2. **Use user_id from token**: Extract from JWT `sub` claim, use in URL
3. **Protect routes**: Dashboard and task management routes require AuthGuard
4. **Handle 401**: If JWT expired, redirect to login
5. **Handle 403**: If user_id mismatch, show access denied
6. **Type everything**: Full TypeScript coverage for type safety
7. **No hardcoded API URLs**: Use NEXT_PUBLIC_API_URL env variable

---

## Testing Checklist

Before completing frontend implementation:

- [ ] Signup form works → creates user in Better Auth
- [ ] JWT token received and stored
- [ ] Login form works → retrieves existing user
- [ ] Dashboard accessible only after login
- [ ] Task creation form works
- [ ] Task list displays user's tasks only
- [ ] Edit task updates via API
- [ ] Delete task removes from list
- [ ] Toggle completion works
- [ ] Logout clears token
- [ ] Expired token redirects to login
- [ ] 403 error shows permission denied message

---

**Last Updated**: January 4, 2026
**Ready for**: Task T016-T017 (Signup/Login), T025-T026 (Components), T027 (Dashboard), T030-T031 (Auth/Protection)

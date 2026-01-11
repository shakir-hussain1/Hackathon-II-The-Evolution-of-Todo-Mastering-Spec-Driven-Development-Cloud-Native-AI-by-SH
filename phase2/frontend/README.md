# Phase II Frontend - Next.js Todo Application

This is the frontend application for the Phase II full-stack Todo web application.

## Overview

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.0+
- **UI Framework**: React 19+
- **Styling**: Tailwind CSS
- **Authentication**: JWT (stored in localStorage)

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   └── signup/
│   │   └── dashboard/
│   ├── components/             # Reusable React components
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── AuthGuard.tsx
│   └── utils/                  # Utility functions
│       ├── auth.ts             # Token storage/retrieval
│       ├── api-client.ts       # API client with JWT
│       └── types.ts            # TypeScript types
├── public/                     # Static assets
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Setup Instructions

### 1. Create Environment File

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
# Backend API server URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 3. Run Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server (hot reload) |
| `npm run build` | Build for production |
| `npm run start` | Run production build |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Run TypeScript type check |

## Key Features

### Authentication
- ✅ User signup with Better Auth
- ✅ User login with credentials
- ✅ JWT token stored in localStorage
- ✅ Token automatically attached to API requests
- ✅ Logout clears token

### Task Management
- ✅ View all user's tasks
- ✅ Create new tasks
- ✅ Edit task title/description
- ✅ Delete tasks
- ✅ Mark tasks complete/incomplete

### Security & UX
- ✅ Protected routes (login required)
- ✅ AuthGuard component for route protection
- ✅ Graceful error handling
- ✅ User-friendly error messages

## Architecture

### Pages (App Router)
- `/auth/signup` - User registration
- `/auth/login` - User login
- `/dashboard` - Main task management (protected)

### Components
- `<AuthGuard>` - Protects routes, checks for valid token
- `<TaskList>` - Displays user's tasks, handles delete/toggle
- `<TaskForm>` - Create/edit tasks

### Utilities
- `auth.ts` - Token storage/retrieval, authentication checks
- `api-client.ts` - Fetch wrapper with automatic JWT attachment
- `types.ts` - TypeScript interfaces for type safety

## Development Rules

### JWT Attachment
The API client automatically attaches JWT to all requests (except auth endpoints):

```typescript
// API client handles this automatically
const response = await api.get("/api/users/123/tasks");
// Header automatically includes: Authorization: Bearer <token>
```

### Protected Routes
Wrap components in `<AuthGuard>` to require authentication:

```typescript
import { AuthGuard } from "@/components/AuthGuard";

export default function Dashboard() {
  return (
    <AuthGuard>
      {/* Content only shown to authenticated users */}
    </AuthGuard>
  );
}
```

### Error Handling
Handle API errors (401 = login redirect, 403 = permission denied):

```typescript
try {
  const response = await api.get("/api/users/123/tasks");
} catch (error: any) {
  if (error.status === 401) {
    router.push("/auth/login");
  } else if (error.status === 403) {
    toast.error("Access denied");
  } else {
    toast.error("Something went wrong");
  }
}
```

## Environment Variables

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Backend API server URL |

## Building for Production

```bash
# Create optimized build
npm run build

# Run production server
npm start
```

## TypeScript

Full TypeScript support with strict type checking:

```bash
npm run type-check
```

All components and utilities are fully typed. See `src/utils/types.ts` for shared types.

## Styling

Uses Tailwind CSS for styling. Configure in your Next.js project.

Classes are used directly on elements:
```tsx
<button className="px-4 py-2 bg-blue-600 text-white rounded">
  Click me
</button>
```

## Debugging

### Browser DevTools
- Open DevTools (F12)
- Check Console for errors
- Check Network tab for API requests
- Check Application tab > LocalStorage for JWT token

### Server Logs
- Development server shows logs in terminal
- Check for errors in the Next.js dev server output

## Common Issues

### JWT Not Attaching to Requests
- Check that token is stored: Open DevTools > Application > LocalStorage, look for `token` key
- Check that API URL is correct: See `.env.local`

### 401 Unauthorized Errors
- Token may be expired
- Try logging out and logging back in
- Check backend is running

### 403 Forbidden Errors
- User ID in URL doesn't match JWT user ID
- Check you're accessing your own resources

## Testing

See `package.json` for testing setup (Jest, React Testing Library).

## Deployment

Frontend can be deployed to:
- Vercel (recommended for Next.js)
- AWS Amplify
- Netlify
- Docker container

See `specs/001-fullstack-web-app/plan.md` for deployment instructions.

## Support

For issues or questions:
1. Check `frontend/CLAUDE.md` for development patterns
2. Review `specs/api/rest-endpoints.md` for API contract
3. See `src/utils/types.ts` for TypeScript interfaces

## Next Steps

After setup is complete:
1. Ensure backend is running at `NEXT_PUBLIC_API_URL`
2. Create `.env.local` with correct API URL
3. Run `npm run dev` and navigate to http://localhost:3000
4. Sign up for an account
5. Create your first task!

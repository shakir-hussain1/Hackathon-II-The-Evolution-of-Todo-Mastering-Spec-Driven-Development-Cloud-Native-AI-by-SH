# Phase V Todo - Frontend

Next.js frontend for the Phase V Advanced Cloud-Native Todo System.

## Features

- **AI Chat Interface**: Natural language task management
- **Real-time Sync**: WebSocket-based live updates
- **Advanced Filtering**: Filter by status, priority, tags, due dates
- **Full-text Search**: Debounced search across task titles and descriptions
- **Recurring Tasks**: Support for daily, weekly, monthly, yearly patterns
- **Priority Management**: High, medium, low priority with color coding
- **Tag Support**: Organize tasks with custom tags
- **Responsive Design**: Mobile-first Tailwind CSS design
- **Optimistic UI**: Instant feedback with background sync

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Zustand**: Lightweight state management
- **Axios**: HTTP client for API calls
- **date-fns**: Date manipulation and formatting
- **WebSocket**: Real-time event handling

## Getting Started

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

### Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8080
NODE_ENV=development
```

### Building

```bash
# Production build
npm run build

# Start production server
npm start
```

### Docker

```bash
# Build image
docker build -t phase5-frontend:latest .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://chat-api:8000 \
  -e NEXT_PUBLIC_WS_URL=ws://websocket-service:8080 \
  phase5-frontend:latest
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Main dashboard
│   ├── login/             # Login page
│   └── register/          # Registration page
├── components/            # React components
│   ├── ChatInterface.tsx  # AI chat UI
│   ├── TaskList.tsx       # Task list with filters
│   ├── TaskCard.tsx       # Individual task card
│   ├── TaskFilter.tsx     # Filter controls
│   ├── TaskSort.tsx       # Sort dropdown
│   ├── SearchBar.tsx      # Debounced search
│   └── ConnectionStatus.tsx # WebSocket status
├── lib/                   # Core utilities
│   ├── api.ts            # API client (axios)
│   ├── websocket.ts      # WebSocket client
│   ├── store.ts          # Zustand stores
│   └── utils.ts          # Helper functions
└── types/                 # TypeScript definitions
    ├── task.ts           # Task interfaces
    ├── auth.ts           # Auth interfaces
    └── chat.ts           # Chat interfaces
```

## API Integration

The frontend integrates with the Chat API service:

- **Base URL**: `/api/v1`
- **Authentication**: JWT Bearer tokens
- **Endpoints**:
  - `POST /auth/login` - User authentication
  - `POST /auth/register` - User registration
  - `GET /tasks` - List tasks with filters
  - `POST /tasks` - Create task
  - `PATCH /tasks/:id` - Update task
  - `DELETE /tasks/:id` - Delete task
  - `GET /tasks/search` - Full-text search
  - `POST /chat` - AI chat messages

## WebSocket Events

Real-time updates via WebSocket:

- `task.created` - New task created
- `task.updated` - Task modified
- `task.deleted` - Task removed

## Component Features

### ChatInterface
- Message history with scrolling
- Loading states with animations
- Action indicators for task operations
- Keyboard shortcuts (Enter to send)

### TaskCard
- Checkbox for quick completion toggle
- Priority badges with color coding
- Due date countdown
- Tag display
- Recurrence indicators
- Delete confirmation

### TaskFilter
- Status filter (pending, completed, archived)
- Priority filter (high, medium, low)
- Tag filter (comma-separated)
- Date range filters (due_before, due_after)
- Clear filters button

### SearchBar
- Debounced input (300ms)
- Clear button
- Search icon
- Full-text search across title and description

## Styling

Tailwind CSS with custom configuration:

- **Priority Colors**:
  - High: Red (#ef4444)
  - Medium: Yellow (#f59e0b)
  - Low: Green (#10b981)

- **Responsive Breakpoints**:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px

## State Management

Zustand stores:

- **TaskStore**: Tasks, filters, search
- **AuthStore**: User, token, authentication
- **ConnectionStore**: WebSocket status

## Performance Optimizations

- Debounced search (300ms)
- Optimistic UI updates
- WebSocket auto-reconnect with exponential backoff
- Lazy loading for components
- Image optimization with Next.js
- Static generation for public pages

## Deployment

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: frontend
        image: phase5-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://chat-api:8000"
        - name: NEXT_PUBLIC_WS_URL
          value: "ws://websocket-service:8080"
```

## License

MIT

# UI Component Specifications

**Project**: Hackathon II – The Evolution of Todo – Phase II
**Category**: Frontend Components
**Status**: Implemented
**Created**: January 11, 2026

---

## Overview

This document specifies all React components used in the Phase II frontend, including their props, behavior, and styling requirements.

---

## Core Components

### 1. TaskList Component

**Purpose**: Display user's tasks with filtering, sorting, and actions

**File**: `frontend/src/components/TaskList.tsx`

**Props Interface**:
```typescript
interface TaskListProps {
  userId: string;              // Authenticated user's ID
  refreshKey?: number;         // Trigger task refresh
  onTaskDeleted?: () => void;  // Callback when task deleted
  onTaskToggled?: () => void;  // Callback when task toggled
  onTasksLoaded?: (tasks: Task[]) => void;  // Callback with loaded tasks
  onTaskUpdated?: () => void;  // Callback when task updated
}
```

**Features**:
- Fetches tasks from API on mount and when refreshKey changes
- Displays tasks in clean table format
- Provides filtering: All, Pending, Completed
- Provides sorting: Newest First, Oldest First
- Inline toggle completion via checkbox
- Edit button opens TaskEditModal
- Delete button shows ConfirmDialog
- Empty state when no tasks
- Loading state with spinner
- Error state with message

**States**:
```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [loading, setLoading] = useState<boolean>(true);
const [error, setError] = useState<string | null>(null);
const [togglingTaskId, setTogglingTaskId] = useState<number | null>(null);
const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
const [filter, setFilter] = useState<"all" | "incomplete" | "complete">("all");
const [sortBy, setSortBy] = useState<"recent" | "oldest">("recent");
const [editingTask, setEditingTask] = useState<Task | null>(null);
const [showEditModal, setShowEditModal] = useState<boolean>(false);
const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);
const [showDeleteConfirm, setShowDeleteConfirm] = useState<boolean>(false);
```

**API Integration**:
- GET `/api/users/{userId}/tasks` - Fetch all tasks
- PATCH `/api/users/{userId}/tasks/{id}/complete` - Toggle completion
- DELETE `/api/users/{userId}/tasks/{id}` - Delete task (via confirmation)

**Styling**:
- Table layout with header row
- Status column with animated checkbox
- Task info with title and description
- Date column (hidden on mobile)
- Actions column with Edit and Delete buttons
- Filter buttons with active state highlighting
- Sort dropdown
- Responsive: table on desktop, consider cards on mobile

---

### 2. TaskForm Component

**Purpose**: Create new tasks with title and description

**File**: `frontend/src/components/TaskForm.tsx`

**Props Interface**:
```typescript
interface TaskFormProps {
  userId: string;                      // Authenticated user's ID
  onTaskCreated?: (task: Task) => void;  // Callback with created task
}
```

**Features**:
- Title input (required, max 255 characters)
- Description textarea (optional, max 10,000 characters)
- Character count indicators
- Real-time validation
- Success message on creation
- Error message on failure
- Loading state during submission
- Auto-clear form on success

**States**:
```typescript
const [title, setTitle] = useState<string>("");
const [description, setDescription] = useState<string>("");
const [error, setError] = useState<string | null>(null);
const [success, setSuccess] = useState<boolean>(false);
const [loading, setLoading] = useState<boolean>(false);
```

**API Integration**:
- POST `/api/users/{userId}/tasks` - Create task

**Validation**:
- Title must not be empty (trim whitespace)
- Title max 255 characters
- Description max 10,000 characters

**Styling**:
- Clean form layout with labels
- Gradient submit button
- Green success message with checkmark
- Red error message
- Character counters
- Disabled state during loading

---

### 3. TaskEditModal Component

**Purpose**: Edit existing tasks in a modal dialog

**File**: `frontend/src/components/TaskEditModal.tsx`

**Props Interface**:
```typescript
interface TaskEditModalProps {
  open: boolean;                       // Whether modal is visible
  task: Task | null;                   // Task to edit (null if closed)
  userId: string;                      // Authenticated user's ID
  onClose: () => void;                 // Callback to close modal
  onTaskUpdated: (task: Task) => void; // Callback with updated task
}
```

**Features**:
- Modal overlay with backdrop
- Close button (X) in header
- Title input (pre-filled with current value)
- Description textarea (pre-filled with current value)
- Character count indicators
- Cancel button (closes modal)
- Update button (saves changes)
- Loading state during save
- Error message on failure
- Auto-close on success

**States**:
```typescript
const [title, setTitle] = useState<string>("");
const [description, setDescription] = useState<string>("");
const [error, setError] = useState<string | null>(null);
const [loading, setLoading] = useState<boolean>(false);
```

**API Integration**:
- PUT `/api/users/{userId}/tasks/{id}` - Update task

**Validation**:
- Title must not be empty (trim whitespace)
- Title max 255 characters
- Description max 10,000 characters

**Styling**:
- Full-screen overlay with centered modal
- White rounded modal card
- Header with title and close button
- Form content with inputs
- Footer with Cancel and Update buttons
- Responsive: max-width on large screens

**Behavior**:
- Clicking backdrop closes modal (if not loading)
- ESC key closes modal (handled by browser default)
- Form reset on task change
- Disabled interactions while loading

---

### 4. ConfirmDialog Component

**Purpose**: Reusable confirmation dialog for destructive actions

**File**: `frontend/src/components/ConfirmDialog.tsx`

**Props Interface**:
```typescript
interface ConfirmDialogProps {
  open: boolean;                       // Whether dialog is visible
  title: string;                       // Dialog title
  message: string | ReactNode;         // Dialog message (text or JSX)
  confirmText?: string;                // Confirm button text (default: "Confirm")
  cancelText?: string;                 // Cancel button text (default: "Cancel")
  confirmButtonClass?: string;         // Custom class for confirm button
  onConfirm: () => void;               // Callback on confirm
  onCancel: () => void;                // Callback on cancel
  loading?: boolean;                   // Loading state (default: false)
}
```

**Features**:
- Modal overlay with backdrop
- Warning icon (exclamation triangle)
- Title text (bold, centered)
- Message content (flexible: string or JSX)
- Cancel button (gray)
- Confirm button (customizable color, default red)
- Loading state (spinner in confirm button)
- Backdrop click closes dialog (if not loading)

**Usage Examples**:
```typescript
// Delete confirmation
<ConfirmDialog
  open={showDeleteConfirm}
  title="Delete Task?"
  message={
    <div>
      <p>Are you sure you want to delete "{task.title}"?</p>
      <p className="text-sm mt-2">This action cannot be undone.</p>
    </div>
  }
  confirmText="Delete"
  cancelText="Cancel"
  confirmButtonClass="bg-red-500 hover:bg-red-600"
  onConfirm={handleDeleteConfirm}
  onCancel={handleDeleteCancel}
  loading={deleting}
/>

// Logout confirmation
<ConfirmDialog
  open={showLogoutConfirm}
  title="Log Out?"
  message="Are you sure you want to log out?"
  confirmText="Log Out"
  cancelText="Stay"
  confirmButtonClass="bg-gray-800 hover:bg-gray-900"
  onConfirm={handleLogout}
  onCancel={handleLogoutCancel}
/>
```

**Styling**:
- Full-screen overlay with centered dialog
- White rounded dialog card
- Red circular icon background
- Centered text alignment
- Flex button layout
- Responsive sizing

---

### 5. AuthGuard Component

**Purpose**: Protect routes requiring authentication

**File**: `frontend/src/components/AuthGuard.tsx`

**Props Interface**:
```typescript
interface AuthGuardProps {
  children: ReactNode;  // Protected content
}
```

**Features**:
- Checks for JWT token in localStorage
- Redirects to /auth/login if no token
- Shows loading state while checking
- Prevents flash of protected content

**States**:
```typescript
const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
const [loading, setLoading] = useState<boolean>(true);
```

**Behavior**:
- Runs auth check on mount
- If token exists: render children
- If no token: redirect to login
- While checking: show loading spinner

**Usage**:
```typescript
export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}
```

---

### 6. ErrorBoundary Component

**Purpose**: Catch React errors and display fallback UI

**File**: `frontend/src/components/ErrorBoundary.tsx`

**Props Interface**:
```typescript
interface ErrorBoundaryProps {
  children: ReactNode;
}
```

**Features**:
- Catches errors in child components
- Displays error fallback UI
- Logs error details to console
- Provides "Reload" button to recover

**State**:
```typescript
const [hasError, setHasError] = useState<boolean>(false);
const [error, setError] = useState<Error | null>(null);
```

**Fallback UI**:
- Error icon
- "Something went wrong" message
- Error details (in development only)
- "Reload Page" button

---

## Component Composition

### Dashboard Page Composition

```
DashboardPage (Protected Route)
├── AuthGuard (Route Protection)
│   └── DashboardContent
│       ├── Header
│       │   ├── Title
│       │   └── Logout Button
│       ├── Main Content
│       │   ├── TaskForm (Create)
│       │   │   └── Form inputs
│       │   └── TaskList (Display)
│       │       ├── Filter Buttons
│       │       ├── Sort Dropdown
│       │       ├── Task Table
│       │       │   ├── Status Checkbox
│       │       │   ├── Task Info
│       │       │   ├── Date
│       │       │   └── Actions (Edit, Delete)
│       │       ├── TaskEditModal (Edit)
│       │       └── ConfirmDialog (Delete)
│       └── Stats Cards
│           ├── Total Tasks
│           ├── Pending Tasks
│           └── Completed Tasks
```

---

## Component Styling Guidelines

### Color Palette

**Primary Actions**:
- Blue-Purple Gradient: `from-blue-500 to-purple-500`
- Hover: `from-blue-600 to-purple-600`

**Status Colors**:
- Pending/Incomplete: Amber/Orange (`from-amber-500 to-orange-600`)
- Complete: Green/Emerald (`from-green-500 to-emerald-600`)
- All: Blue (`from-blue-500 to-blue-600`)

**Destructive Actions**:
- Delete: Red (`bg-red-500 hover:bg-red-600`)
- Warning: Red icon with red-100 background

**Neutral**:
- Cancel: Gray (`bg-gray-200 hover:bg-gray-300`)
- Borders: Gray-200 (`border-gray-200`)
- Text: Gray-900 (primary), Gray-600 (secondary), Gray-500 (tertiary)

### Typography

**Headings**:
- H1: `text-3xl font-bold` (Page titles)
- H2: `text-xl font-bold` (Section titles)
- H3: `text-lg font-semibold` (Component titles)

**Body Text**:
- Primary: `text-base text-gray-900`
- Secondary: `text-sm text-gray-600`
- Tertiary: `text-xs text-gray-500`

### Spacing

**Component Padding**:
- Cards: `p-6`
- Forms: `space-y-4`
- Buttons: `px-4 py-2.5`

**Gaps**:
- Grid: `gap-4` or `gap-6`
- Button groups: `gap-2` or `gap-3`

### Transitions

**Standard**:
- Colors: `transition-colors duration-200`
- All: `transition-all duration-200`
- Transforms: `transition-transform`

**Hover Effects**:
- Buttons: Scale or color change
- Cards: Shadow increase
- Interactive elements: Color change

### Responsive Breakpoints

**Tailwind Breakpoints**:
- Mobile: Default (< 640px)
- Tablet: `sm:` (≥ 640px)
- Desktop: `md:` (≥ 768px)
- Large: `lg:` (≥ 1024px)

**Responsive Patterns**:
- Grid columns: `grid-cols-1 lg:grid-cols-2`
- Hide on mobile: `hidden md:block`
- Show on mobile: `block md:hidden`

---

## Accessibility Requirements

### Semantic HTML

- Use proper heading hierarchy (h1 → h2 → h3)
- Use `<button>` for clickable actions
- Use `<form>` for data submission
- Use `<label>` for form inputs

### ARIA Attributes

- `aria-label` for icon-only buttons
- `aria-disabled` for disabled interactive elements
- `role` attributes where appropriate

### Keyboard Navigation

- All interactive elements focusable
- Tab order logical
- Enter/Space activates buttons
- ESC closes modals

### Focus States

- Visible focus rings: `focus:ring-2 focus:ring-blue-500`
- Remove default outline: `outline-none`
- Custom focus styles for all interactive elements

---

## Testing Checklist

### TaskList Component

- [ ] Fetches tasks on mount
- [ ] Displays empty state when no tasks
- [ ] Filters work (All, Pending, Completed)
- [ ] Sorting works (Newest, Oldest)
- [ ] Toggle completion updates status
- [ ] Edit button opens modal with task data
- [ ] Delete button shows confirmation
- [ ] Confirmation delete removes task
- [ ] Error states display correctly
- [ ] Loading states display correctly

### TaskForm Component

- [ ] Creates task with valid data
- [ ] Validates empty title
- [ ] Validates max length (title 255, description 10,000)
- [ ] Shows success message on creation
- [ ] Shows error message on failure
- [ ] Clears form after success
- [ ] Character counters update correctly
- [ ] Disabled during submission

### TaskEditModal Component

- [ ] Opens with pre-filled data
- [ ] Closes on backdrop click
- [ ] Closes on X button click
- [ ] Closes on Cancel button
- [ ] Updates task on submit
- [ ] Validates input
- [ ] Shows error on failure
- [ ] Disabled during submission

### ConfirmDialog Component

- [ ] Opens on trigger
- [ ] Closes on backdrop click (if not loading)
- [ ] Closes on Cancel button
- [ ] Calls onConfirm on Confirm button
- [ ] Calls onCancel on Cancel button
- [ ] Shows loading state
- [ ] Prevents interaction while loading

### AuthGuard Component

- [ ] Redirects to login if no token
- [ ] Shows loading while checking
- [ ] Renders children if authenticated
- [ ] Checks auth on mount

---

**Status**: Implemented
**Last Updated**: January 11, 2026
**Phase**: Phase II – Full-Stack Web Application

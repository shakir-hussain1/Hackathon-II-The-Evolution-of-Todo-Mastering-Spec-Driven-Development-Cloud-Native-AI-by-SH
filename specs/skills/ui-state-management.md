# UI State Management Skill - Specification

## Skill Overview
**Name:** ui-state-management
**Type:** Frontend Quality Skill
**Category:** User Experience & State

## Purpose
Standardizes UI states across the application to ensure consistent user experience by defining and implementing loading, empty, and error states while preventing silent failures.

## Input Requirements
- Component implementations
- API integration code
- State management logic
- UI/UX specifications
- User feedback requirements

## Core Functions

### 1. Loading State Definition
- Define loading indicators
- Specify skeleton screens
- Set loading timeouts
- Review loading UX patterns
- Validate loading feedback

### 2. Empty State Definition
- Define empty state designs
- Create helpful messaging
- Add call-to-action elements
- Review placeholder content
- Ensure consistent styling

### 3. Error State Definition
- Define error display patterns
- Create user-friendly messages
- Add retry mechanisms
- Review error recovery flows
- Validate error logging

### 4. UX Pattern Consistency
- Ensure state patterns are reusable
- Validate consistent messaging
- Review visual consistency
- Check animation consistency
- Verify accessibility

### 5. Silent Failure Prevention
- Detect missing error handling
- Find unhandled promise rejections
- Identify missing loading states
- Check for empty state gaps
- Validate user feedback loops

## UI State Standards

### Loading States
```typescript
// ✓ CORRECT - All loading scenarios covered
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadTodos()
  }, [])

  const loadTodos = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getTodos()
      setTodos(data)
    } catch (err) {
      setError('Failed to load todos')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <LoadingSpinner />  // ✓ Loading feedback
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={loadTodos} />  // ✓ Error state
  }

  if (todos.length === 0) {
    return <EmptyState message="No todos yet" onAdd={openCreateDialog} />  // ✓ Empty state
  }

  return <TodoItems todos={todos} />
}

// ✗ INCORRECT - No loading or error states
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])

  useEffect(() => {
    api.getTodos().then(setTodos)  // Silent failures, no loading indicator
  }, [])

  return <TodoItems todos={todos} />  // Blank screen while loading
}
```

### Empty States
```typescript
// ✓ CORRECT - Helpful empty state
function EmptyTodoList() {
  return (
    <div className="empty-state">
      <IllustrationIcon />
      <h3>No todos yet</h3>
      <p>Get started by creating your first todo item</p>
      <Button onClick={onCreateTodo}>
        Create Todo
      </Button>
    </div>
  )
}

// ✗ INCORRECT - Unhelpful empty state
function EmptyTodoList() {
  return <div>No data</div>  // Not helpful, no CTA
}

// ✗ INCORRECT - Missing empty state
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => <TodoItem key={todo.id} todo={todo} />)}
    </ul>
  )  // Shows empty list, no message
}
```

### Error States
```typescript
// ✓ CORRECT - User-friendly error with retry
function ErrorState({ error, onRetry }) {
  const getMessage = (error) => {
    if (error.response?.status === 404) {
      return 'The item you're looking for doesn't exist'
    } else if (error.response?.status === 403) {
      return 'You don't have permission to access this'
    } else if (error.request) {
      return 'Network error. Please check your connection.'
    } else {
      return 'Something went wrong. Please try again.'
    }
  }

  return (
    <div className="error-state">
      <ErrorIcon />
      <h3>Oops!</h3>
      <p>{getMessage(error)}</p>
      <Button onClick={onRetry}>Try Again</Button>
    </div>
  )
}

// ✗ INCORRECT - Technical error exposed
function ErrorState({ error }) {
  return <div>Error: {error.message}</div>  // Shows technical details
}

// ✗ INCORRECT - No retry option
function ErrorState({ error }) {
  return <div>Something went wrong</div>  // User stuck
}

// ✗ INCORRECT - Silent failure
try {
  await api.deleteTodo(id)
} catch (error) {
  console.error(error)  // User sees nothing
}
```

### Optimistic Updates
```typescript
// ✓ CORRECT - Optimistic update with rollback
const handleToggle = async (todo: Todo) => {
  const previousTodos = [...todos]
  const optimisticTodos = todos.map(t =>
    t.id === todo.id ? { ...t, completed: !t.completed } : t
  )
  setTodos(optimisticTodos)  // Immediate UI update

  try {
    await api.updateTodo(todo.id, { completed: !todo.completed })
  } catch (error) {
    setTodos(previousTodos)  // Rollback on error
    showError('Failed to update todo')
  }
}

// ✗ INCORRECT - No optimistic update (feels slow)
const handleToggle = async (todo: Todo) => {
  setLoading(true)
  await api.updateTodo(todo.id, { completed: !todo.completed })
  await loadTodos()  // Slow, unnecessary refetch
  setLoading(false)
}
```

## Validation Process

### Step 1: Component Audit
1. List all components that fetch data
2. Identify components with user actions
3. Check for async operations
4. Map all state transitions
5. Document current state handling

### Step 2: State Coverage Analysis
1. Check for loading state presence
2. Verify empty state handling
3. Validate error state implementation
4. Test optimistic update patterns
5. Review success feedback

### Step 3: User Flow Testing
1. Test loading scenarios
2. Trigger empty states
3. Force error conditions
4. Check network failures
5. Verify timeout handling

### Step 4: Consistency Check
1. Compare loading patterns
2. Review empty state designs
3. Validate error message tone
4. Check visual consistency
5. Verify accessibility

### Step 5: Silent Failure Detection
1. Disable backend and test UI
2. Check for unhandled errors
3. Find missing loading indicators
4. Test error recovery
5. Verify user feedback

## Output Format

### UI State Checklist
```markdown
## UI STATE MANAGEMENT CHECKLIST

**Overall Status:** [COMPLETE | PARTIAL | MISSING]
**Components Analyzed:** 15
**Fully Compliant:** 8 (53%)
**Missing States:** 7 (47%)

### ✓ Compliant Components
1. **TodoList**
   - Loading State: ✓ Skeleton screen
   - Empty State: ✓ Helpful message + CTA
   - Error State: ✓ User-friendly with retry
   - Optimistic Updates: ✓ Implemented
   - Accessibility: ✓ ARIA labels present

2. **TodoDetail**
   - Loading State: ✓ Spinner
   - Error State: ✓ Error boundary catches errors
   - Not Found State: ✓ 404 handling
   - Accessibility: ✓ Keyboard navigation

### ⚠ Partial Implementation
3. **TodoForm**
   - Loading State: ✓ Button disabled while saving
   - Error State: ⚠ Generic "Error" message
   - Success Feedback: ✗ Missing confirmation
   - **Fix:** Add specific error messages and success toast

### ✗ Missing States
4. **UserProfile**
   - Loading State: ✗ Blank screen while loading
   - Error State: ✗ Silent failure
   - Empty State: ✓ Shows message
   - **Fix:** Add loading spinner and error display

5. **SearchResults**
   - Loading State: ✗ No indication while searching
   - Empty State: ✗ Just shows empty list
   - Error State: ✗ No error handling
   - **Fix:** Add all three states
```

### Missing UX States
```markdown
## MISSING UX STATES

### CRITICAL (No user feedback)
1. **TodoList Delete Action**
   - Component: src/components/TodoList.tsx:89
   - Issue: Delete happens silently
   - Impact: User unsure if action succeeded
   - Fix: Add optimistic update + success toast
   ```typescript
   const handleDelete = async (id: number) => {
     // Optimistic removal
     setTodos(todos.filter(t => t.id !== id))
     try {
       await api.deleteTodo(id)
       showSuccess('Todo deleted')  // Add this
     } catch (error) {
       setTodos(previousTodos)  // Rollback
       showError('Failed to delete todo')  // Add this
     }
   }
   ```

2. **LoginForm Submission**
   - Component: src/components/LoginForm.tsx:45
   - Issue: No loading state during login
   - Impact: Users click multiple times
   - Fix: Disable button and show loading
   ```typescript
   <Button
     disabled={loading}
     onClick={handleLogin}
   >
     {loading ? 'Logging in...' : 'Login'}
   </Button>
   ```

### HIGH (Poor UX)
3. **TodoList Empty State**
   - Component: src/components/TodoList.tsx:67
   - Issue: Shows "No todos" with no CTA
   - Impact: New users confused
   - Fix: Add helpful message and create button

4. **Profile Form Error**
   - Component: src/components/ProfileForm.tsx:102
   - Issue: Shows technical error message
   - Impact: User doesn't know how to fix
   - Fix: Map error codes to user-friendly messages
```

### Improvement Recommendations
```markdown
## IMPROVEMENT RECOMMENDATIONS

### 1. Create Reusable State Components
```typescript
// components/ui/LoadingState.tsx
export function LoadingState({ message = 'Loading...' }) {
  return (
    <div className="loading-state">
      <Spinner />
      <p>{message}</p>
    </div>
  )
}

// components/ui/EmptyState.tsx
export function EmptyState({ title, message, action }) {
  return (
    <div className="empty-state">
      <IllustrationIcon />
      <h3>{title}</h3>
      <p>{message}</p>
      {action && <Button {...action} />}
    </div>
  )
}

// components/ui/ErrorState.tsx
export function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state">
      <ErrorIcon />
      <h3>Oops!</h3>
      <p>{getUserFriendlyMessage(error)}</p>
      {onRetry && <Button onClick={onRetry}>Try Again</Button>}
    </div>
  )
}
```

### 2. Use Custom Hook for Async State
```typescript
function useAsync<T>(asyncFn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const execute = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await asyncFn()
      setData(result)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { execute() }, [])

  return { data, loading, error, refetch: execute }
}

// Usage
function TodoList() {
  const { data: todos, loading, error, refetch } = useAsync(api.getTodos)

  if (loading) return <LoadingState />
  if (error) return <ErrorState error={error} onRetry={refetch} />
  if (!todos || todos.length === 0) return <EmptyState title="No todos" />

  return <TodoItems todos={todos} />
}
```

### 3. Implement Toast Notifications
```typescript
// For success/error feedback
showSuccess('Todo created successfully')
showError('Failed to update todo')
showWarning('Unsaved changes')
showInfo('You have 5 pending todos')
```

### 4. Add Loading Skeletons
```typescript
// Better than spinners for list views
function TodoListSkeleton() {
  return (
    <div>
      {[1, 2, 3, 4, 5].map(i => (
        <div key={i} className="skeleton-item">
          <div className="skeleton-text skeleton-title" />
          <div className="skeleton-text skeleton-description" />
        </div>
      ))}
    </div>
  )
}
```

### 5. Standardize Error Messages
```typescript
const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'Please log in to continue.',
  FORBIDDEN: 'You don\'t have permission to do that.',
  NOT_FOUND: 'The item you\'re looking for doesn\'t exist.',
  SERVER_ERROR: 'Something went wrong on our end. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
}
```
```

## Common UX Issues

### Issue 1: Blank Screen While Loading
**Problem:** Component shows nothing while fetching data
**Impact:** User thinks app is broken
**Fix:** Add loading skeleton or spinner immediately

### Issue 2: Silent Errors
**Problem:** Errors caught but not shown to user
**Impact:** User doesn't know action failed
**Fix:** Always display user-friendly error message

### Issue 3: No Empty State
**Problem:** Empty list shows blank or just container
**Impact:** User confused, doesn't know what to do
**Fix:** Add helpful message and CTA

### Issue 4: Technical Error Messages
**Problem:** Shows stack trace or technical details
**Impact:** User confused and scared
**Fix:** Map to user-friendly messages

### Issue 5: No Loading Feedback on Actions
**Problem:** Button click has no visual feedback
**Impact:** User clicks multiple times
**Fix:** Disable button and show loading state

## Integration Points

### Works With
- frontend-ui-dashboard agent
- frontend-api-integration skill
- error-normalization-handling skill
- api-contract-validation skill

### Validates
- Component state handling
- User feedback mechanisms
- Error display patterns
- Loading indicators

### Provides
- State pattern templates
- UX improvement recommendations
- Consistency guidelines
- Accessibility standards

## Success Metrics
- **Loading States:** 100% async operations show loading
- **Empty States:** 100% list views have empty state
- **Error States:** 100% errors displayed to user
- **Silent Failures:** 0
- **User Feedback:** 100% actions provide feedback

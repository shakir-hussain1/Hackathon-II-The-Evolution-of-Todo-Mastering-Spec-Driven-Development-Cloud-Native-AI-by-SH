/**
 * API client for backend communication.
 * Handles authentication, error handling, and request/response formatting.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get JWT token from localStorage
 */
export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

/**
 * Set JWT token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('auth_token', token);
}

/**
 * Clear JWT token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('auth_token');
}

/**
 * Get current user ID from JWT token
 */
export function getUserIdFromToken(): string | null {
  const token = getAuthToken();
  if (!token) return null;

  try {
    // Decode JWT (basic decode, validation happens on backend)
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub || null;
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
}

/**
 * API Error class for consistent error handling
 */
export class ApiError extends Error {
  constructor(
    public status: number,
    public message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Register a new user
 */
export async function register(email: string, password: string): Promise<{
  token: string;
  user: { id: string; email: string };
}> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Registration failed' }));
    throw new ApiError(response.status, error.error || error.message || 'Registration failed', error);
  }

  const data = await response.json();
  setAuthToken(data.token);

  // Store user ID for session tracking (prevents cross-user conversation leakage)
  if (data.user && data.user.id) {
    localStorage.setItem('current_user_id', data.user.id);
  }

  // Clear old conversation ID to start fresh
  localStorage.removeItem('conversation_id');

  return data;
}

/**
 * Login user
 */
export async function login(email: string, password: string): Promise<{
  token: string;
  user: { id: string; email: string };
}> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Login failed' }));
    throw new ApiError(response.status, error.error || error.message || 'Login failed', error);
  }

  const data = await response.json();
  setAuthToken(data.token);

  // Store user ID for session tracking (prevents cross-user conversation leakage)
  if (data.user && data.user.id) {
    localStorage.setItem('current_user_id', data.user.id);
  }

  // Clear old conversation ID to start fresh
  localStorage.removeItem('conversation_id');

  return data;
}

/**
 * Logout user
 */
export function logout(): void {
  clearAuthToken();
  // Clear user session tracking
  localStorage.removeItem('current_user_id');
  localStorage.removeItem('conversation_id');
}

/**
 * Send chat message to backend
 */
export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<{
  response: string;
  conversation_id: string;
  message_id: string;
  tool_calls?: any;
}> {
  const token = getAuthToken();
  const userId = getUserIdFromToken();

  if (!token || !userId) {
    throw new ApiError(401, 'Not authenticated. Please login.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      throw new ApiError(401, 'Session expired. Please login again.');
    }

    const error = await response.json().catch(() => ({ error: 'Failed to send message' }));
    throw new ApiError(
      response.status,
      error.error || error.message || 'Failed to send message',
      error
    );
  }

  return await response.json();
}

/**
 * Load conversation history
 */
export async function loadConversationHistory(conversationId: string): Promise<{
  conversation_id: string;
  messages: Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    tool_calls?: any;
    created_at: string;
  }>;
}> {
  const token = getAuthToken();
  const userId = getUserIdFromToken();

  if (!token || !userId) {
    throw new ApiError(401, 'Not authenticated. Please login.');
  }

  const response = await fetch(
    `${API_BASE_URL}/api/${userId}/conversations/${conversationId}/history`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      throw new ApiError(401, 'Session expired. Please login again.');
    }

    const error = await response.json().catch(() => ({ error: 'Failed to load conversation' }));
    throw new ApiError(
      response.status,
      error.error || error.message || 'Failed to load conversation',
      error
    );
  }

  return await response.json();
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getAuthToken() !== null;
}

// ===== TASK MANAGEMENT (Dashboard API) =====

/**
 * Task interface matching backend response
 */
export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

/**
 * Get all tasks for current user
 */
export async function getTasks(status?: 'pending' | 'completed'): Promise<Task[]> {
  const token = getAuthToken();
  const userId = getUserIdFromToken();

  if (!token || !userId) {
    throw new ApiError(401, 'Not authenticated. Please login.');
  }

  const url = new URL(`${API_BASE_URL}/api/${userId}/tasks`);
  if (status) {
    url.searchParams.append('status', status);
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      throw new ApiError(401, 'Session expired. Please login again.');
    }

    const error = await response.json().catch(() => ({ error: 'Failed to fetch tasks' }));
    throw new ApiError(
      response.status,
      error.error || error.message || 'Failed to fetch tasks',
      error
    );
  }

  return await response.json();
}

/**
 * Update task (title, description, or status)
 */
export async function updateTaskDirect(
  taskId: string,
  updates: {
    title?: string;
    description?: string;
    status?: 'pending' | 'completed';
  }
): Promise<Task> {
  const token = getAuthToken();
  const userId = getUserIdFromToken();

  if (!token || !userId) {
    throw new ApiError(401, 'Not authenticated. Please login.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      throw new ApiError(401, 'Session expired. Please login again.');
    }

    const error = await response.json().catch(() => ({ error: 'Failed to update task' }));
    throw new ApiError(
      response.status,
      error.error || error.message || 'Failed to update task',
      error
    );
  }

  return await response.json();
}

/**
 * Complete a task (shorthand for updateTaskDirect with status: 'completed')
 */
export async function completeTaskDirect(taskId: string): Promise<Task> {
  return updateTaskDirect(taskId, { status: 'completed' });
}

/**
 * Delete a task
 */
export async function deleteTaskDirect(taskId: string): Promise<void> {
  const token = getAuthToken();
  const userId = getUserIdFromToken();

  if (!token || !userId) {
    throw new ApiError(401, 'Not authenticated. Please login.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthToken();
      throw new ApiError(401, 'Session expired. Please login again.');
    }

    const error = await response.json().catch(() => ({ error: 'Failed to delete task' }));
    throw new ApiError(
      response.status,
      error.error || error.message || 'Failed to delete task',
      error
    );
  }
}

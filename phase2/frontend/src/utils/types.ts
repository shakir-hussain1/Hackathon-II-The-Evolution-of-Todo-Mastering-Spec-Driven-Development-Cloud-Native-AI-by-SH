/**
 * TypeScript types and interfaces for Phase II frontend.
 *
 * Shared types used across components and API client.
 */

/**
 * Task object representing a user's todo item.
 */
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

/**
 * User object representing an authenticated user.
 */
export interface User {
  id: string;
  email: string;
}

/**
 * Response from signup or login endpoints.
 */
export interface AuthResponse {
  success: boolean;
  user: User;
  token: string;
}

/**
 * Request payload for creating a task.
 */
export interface TaskCreateRequest {
  title: string;
  description?: string;
}

/**
 * Request payload for updating a task.
 */
export interface TaskUpdateRequest {
  title?: string;
  description?: string;
}

/**
 * Task status enum.
 */
export type TaskStatus = "incomplete" | "complete";

/**
 * Generic list response from API.
 */
export interface ListResponse<T> {
  success: boolean;
  data: T[];
}

/**
 * Generic single item response from API.
 */
export interface ItemResponse<T> {
  success: boolean;
  data: T;
}

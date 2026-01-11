/**
 * API client for communicating with the Phase II backend.
 *
 * Automatically attaches JWT token to every request (except auth endpoints).
 * Provides convenience methods for GET, POST, PUT, PATCH, DELETE operations.
 */

import { getToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Response format from API.
 *
 * All API responses follow this structure.
 */
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

/**
 * Error object extended with HTTP status.
 */
export interface ApiError {
  status: number;
  success: boolean;
  error?: string;
  message?: string;
}

/**
 * Main API call function.
 *
 * Handles:
 * - Attaching JWT token from localStorage to Authorization header
 * - Parsing JSON responses
 * - Error handling with proper error format
 *
 * @param endpoint - API endpoint path (e.g., "/api/users/123/tasks")
 * @param options - Fetch options (method, headers, body, etc.)
 * @returns Promise<ApiResponse<T>> - Parsed API response
 * @throws ApiError - On non-2xx responses or network errors
 */
export async function apiCall<T = unknown>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  // Get JWT token
  const token = await getToken();

  // Prepare headers
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  // Attach JWT to all requests except auth endpoints
  if (token && !endpoint.includes("/auth/")) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Construct full URL
  const url = `${API_URL}${endpoint}`;

  try {
    // Make the request
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle successful responses
    if (response.ok) {
      // 204 No Content - no response body
      if (response.status === 204) {
        return { success: true };
      }

      const data = await response.json();
      return data;
    }

    // Handle error responses
    let errorData: any = {
      success: false,
      error: "unknown_error",
      message: response.statusText,
    };

    try {
      errorData = await response.json();
    } catch {
      // If response is not JSON, use default error
    }

    const error: any = new Error(errorData.message || response.statusText);
    error.status = response.status;
    error.success = false;
    error.error = errorData.error;
    error.message = errorData.message;

    throw error;
  } catch (error: any) {
    // Network or parsing error
    if (error instanceof TypeError) {
      const networkError: any = new Error("Network error: unable to connect to server");
      networkError.status = 0;
      networkError.success = false;
      throw networkError;
    }

    // Re-throw API errors
    throw error;
  }
}

/**
 * Convenience methods for common HTTP operations.
 *
 * Usage:
 *   const tasks = await api.get("/api/users/123/tasks");
 *   const task = await api.post("/api/users/123/tasks", { title: "Buy milk" });
 *   const updated = await api.put("/api/users/123/tasks/1", { title: "Updated" });
 *   await api.delete("/api/users/123/tasks/1");
 */
export const api = {
  /**
   * GET request
   *
   * @param endpoint - API endpoint path
   * @returns Promise<ApiResponse<T>>
   */
  get: <T = unknown>(endpoint: string): Promise<ApiResponse<T>> =>
    apiCall<T>(endpoint, { method: "GET" }),

  /**
   * POST request
   *
   * @param endpoint - API endpoint path
   * @param body - Request body (will be JSON stringified)
   * @returns Promise<ApiResponse<T>>
   */
  post: <T = unknown>(
    endpoint: string,
    body: unknown
  ): Promise<ApiResponse<T>> =>
    apiCall<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    }),

  /**
   * PUT request
   *
   * @param endpoint - API endpoint path
   * @param body - Request body (will be JSON stringified)
   * @returns Promise<ApiResponse<T>>
   */
  put: <T = unknown>(
    endpoint: string,
    body: unknown
  ): Promise<ApiResponse<T>> =>
    apiCall<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  /**
   * PATCH request
   *
   * @param endpoint - API endpoint path
   * @param body - Request body (will be JSON stringified)
   * @returns Promise<ApiResponse<T>>
   */
  patch: <T = unknown>(
    endpoint: string,
    body?: unknown
  ): Promise<ApiResponse<T>> =>
    apiCall<T>(endpoint, {
      method: "PATCH",
      ...(body && { body: JSON.stringify(body) }),
    }),

  /**
   * DELETE request
   *
   * @param endpoint - API endpoint path
   * @returns Promise<ApiResponse<T>>
   */
  delete: <T = unknown>(endpoint: string): Promise<ApiResponse<T>> =>
    apiCall<T>(endpoint, { method: "DELETE" }),
};

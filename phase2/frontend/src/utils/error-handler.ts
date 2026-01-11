/**
 * T032: Comprehensive Error Handling
 *
 * Utility functions for handling different types of API and authentication errors.
 * Provides consistent error messages and recovery suggestions.
 *
 * Handles:
 * - 401 Unauthorized (missing/invalid JWT)
 * - 403 Forbidden (user_id mismatch/access denied)
 * - 404 Not Found (resource doesn't exist)
 * - 400 Bad Request (validation errors)
 * - 500 Server Error (internal errors)
 * - Network errors (connection issues)
 */

import { clearToken } from "./auth";

export enum ErrorCode {
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  BAD_REQUEST = 400,
  SERVER_ERROR = 500,
  NETWORK_ERROR = 0,
  UNKNOWN_ERROR = -1,
}

export interface ApiError {
  code: ErrorCode;
  message: string;
  detail?: string;
  userMessage: string;
  recoveryAction?: () => void | Promise<void>;
  shouldLogout?: boolean;
  shouldRetry?: boolean;
}

/**
 * Custom API Error class for type-safe error handling.
 */
export class CustomApiError extends Error implements ApiError {
  code: ErrorCode;
  detail?: string;
  userMessage: string;
  recoveryAction?: () => void | Promise<void>;
  shouldLogout: boolean = false;
  shouldRetry: boolean = false;

  constructor(
    code: ErrorCode,
    message: string,
    userMessage: string,
    detail?: string
  ) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.message = message;
    this.userMessage = userMessage;
    this.detail = detail;
  }
}

/**
 * Parse error response from API or network.
 *
 * Converts raw error data to standardized ApiError format.
 *
 * @param error - Error object or response
 * @param defaultMessage - Fallback message if parsing fails
 * @returns Standardized ApiError object
 */
export function parseError(error: any, defaultMessage: string = "An error occurred"): ApiError {
  // Network error (no response)
  if (!error.status) {
    return {
      code: ErrorCode.NETWORK_ERROR,
      message: error.message || "Network error",
      userMessage: "Connection failed. Please check your internet connection.",
      shouldRetry: true,
    };
  }

  const { status, detail, message } = error;
  const errorMessage = detail || message || defaultMessage;

  switch (status) {
    case 401:
      return {
        code: ErrorCode.UNAUTHORIZED,
        message: errorMessage,
        userMessage: "Your session has expired. Please log in again.",
        detail: "Missing or invalid authentication token",
        shouldLogout: true,
        shouldRetry: false,
        recoveryAction: async () => {
          await clearToken();
          window.location.href = "/auth/login";
        },
      };

    case 403:
      return {
        code: ErrorCode.FORBIDDEN,
        message: errorMessage,
        userMessage: "You don't have permission to access this resource.",
        detail: "Access denied",
        shouldLogout: false,
        shouldRetry: false,
      };

    case 404:
      return {
        code: ErrorCode.NOT_FOUND,
        message: errorMessage,
        userMessage: "The resource you're looking for doesn't exist.",
        detail: "Resource not found",
        shouldLogout: false,
        shouldRetry: false,
      };

    case 400:
      return {
        code: ErrorCode.BAD_REQUEST,
        message: errorMessage,
        userMessage: `Invalid request: ${errorMessage}`,
        detail: "Validation error",
        shouldLogout: false,
        shouldRetry: false,
      };

    case 500:
      return {
        code: ErrorCode.SERVER_ERROR,
        message: errorMessage,
        userMessage: "Server error. Please try again later.",
        detail: "Internal server error",
        shouldLogout: false,
        shouldRetry: true,
      };

    default:
      return {
        code: ErrorCode.UNKNOWN_ERROR,
        message: errorMessage,
        userMessage: defaultMessage,
        shouldLogout: false,
        shouldRetry: false,
      };
  }
}

/**
 * Check if error is authentication-related (401).
 */
export function isAuthenticationError(error: any): boolean {
  return error?.status === 401 || error?.code === ErrorCode.UNAUTHORIZED;
}

/**
 * Check if error is authorization-related (403).
 */
export function isAuthorizationError(error: any): boolean {
  return error?.status === 403 || error?.code === ErrorCode.FORBIDDEN;
}

/**
 * Check if error is validation-related (400).
 */
export function isValidationError(error: any): boolean {
  return error?.status === 400 || error?.code === ErrorCode.BAD_REQUEST;
}

/**
 * Check if error is retriable (network error or 500).
 */
export function isRetriableError(error: any): boolean {
  const code = error?.status || error?.code;
  return code === 500 || code === ErrorCode.NETWORK_ERROR;
}

/**
 * Log error to console (with formatting).
 */
export function logError(error: ApiError | CustomApiError): void {
  console.error(`[${error.code}] ${error.message}`, {
    detail: error.detail,
    userMessage: error.userMessage,
  });
}

/**
 * Extract user-friendly error message.
 *
 * Handles various error formats and returns a message suitable for end users.
 */
export function getUserMessage(error: any): string {
  if (error instanceof CustomApiError || (error && error.userMessage)) {
    return error.userMessage;
  }

  if (error?.detail) {
    return error.detail;
  }

  if (error?.message) {
    return error.message;
  }

  return "An unexpected error occurred. Please try again.";
}

/**
 * Handle authentication errors (401).
 *
 * Clears token and redirects to login.
 */
export async function handleAuthenticationError(): Promise<void> {
  try {
    await clearToken();
    window.location.href = "/auth/login";
  } catch (err) {
    console.error("Error handling authentication failure:", err);
    window.location.href = "/auth/login";
  }
}

/**
 * Handle authorization errors (403).
 *
 * Shows permission denied message to user.
 */
export function handleAuthorizationError(error: any): string {
  if (error?.detail?.includes("user_id")) {
    return "You don't have permission to access this resource. This might be another user's data.";
  }

  return "You don't have permission to perform this action.";
}

/**
 * Retry async operation with exponential backoff.
 *
 * @param fn - Async function to retry
 * @param maxAttempts - Maximum number of attempts
 * @param initialDelay - Initial delay in ms
 * @returns Promise resolving to function result
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  initialDelay: number = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Don't retry on auth/authz errors
      if (error && typeof error === "object") {
        const err = error as any;
        if (err.status === 401 || err.status === 403) {
          throw error;
        }
      }

      // Wait before retrying (exponential backoff)
      if (attempt < maxAttempts) {
        const delay = initialDelay * Math.pow(2, attempt - 1);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw (
    lastError ||
    new Error(`Failed after ${maxAttempts} attempts`)
  );
}

/**
 * Create standardized error response object.
 */
export function createErrorResponse(
  code: ErrorCode,
  message: string,
  detail?: string
): ApiError {
  return {
    code,
    message,
    detail,
    userMessage: getUserMessage({ message, detail }),
  };
}

/**
 * Safe error handler for use in catch blocks.
 *
 * Ensures all errors are converted to ApiError format.
 *
 * @param error - Any error object
 * @returns ApiError object
 */
export function safeErrorHandler(error: any): ApiError {
  try {
    // Already a custom error
    if (error instanceof CustomApiError) {
      return error;
    }

    // Parse raw error response
    if (error?.status) {
      return parseError(error);
    }

    // Network or unknown error
    return {
      code: ErrorCode.UNKNOWN_ERROR,
      message: error?.message || "Unknown error",
      userMessage: "An unexpected error occurred. Please try again.",
      shouldRetry: false,
    };
  } catch (err) {
    // Fallback for parsing errors
    return {
      code: ErrorCode.UNKNOWN_ERROR,
      message: "Error handling failure",
      userMessage: "An unexpected error occurred. Please try again.",
      shouldRetry: false,
    };
  }
}

/**
 * Error Boundary Component
 *
 * Catches React errors and displays user-friendly error messages.
 * Complements T032: Comprehensive error handling.
 */

"use client";

import React, { ReactNode, useState } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: (error: Error, reset: () => void) => ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

/**
 * Error Boundary for catching and handling React component errors.
 *
 * Usage:
 *   <ErrorBoundary>
 *     <YourComponent />
 *   </ErrorBoundary>
 */
export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.resetError);
      }

      return <DefaultErrorFallback error={this.state.error} onReset={this.resetError} />;
    }

    return this.props.children;
  }
}

/**
 * Default error fallback UI.
 */
interface DefaultErrorFallbackProps {
  error: Error;
  onReset: () => void;
}

function DefaultErrorFallback({ error, onReset }: DefaultErrorFallbackProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <div className="text-red-600 mb-4">
          <svg
            className="w-16 h-16 mx-auto"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4v2m0 6a9 9 0 110-18 9 9 0 010 18z"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">Something Went Wrong</h2>
        <p className="text-gray-600 text-center mb-4 text-sm">{error.message}</p>
        <div className="space-y-2">
          <button
            onClick={onReset}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Try Again
          </button>
          <button
            onClick={() => (window.location.href = "/")}
            className="w-full px-4 py-2 bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition-colors font-medium"
          >
            Go Home
          </button>
        </div>
      </div>
    </div>
  );
}

/**
 * Functional Error Handler Hook.
 *
 * For use in functional components instead of class-based ErrorBoundary.
 */
export function useErrorHandler() {
  const [error, setError] = useState<Error | null>(null);

  const handleError = (err: unknown) => {
    const error = err instanceof Error ? err : new Error(String(err));
    setError(error);
    console.error("Error handled:", error);
  };

  const resetError = () => {
    setError(null);
  };

  return { error, handleError, resetError };
}

/**
 * Display error message component.
 *
 * Reusable component for displaying error messages in the UI.
 */
interface ErrorMessageProps {
  error: string | null;
  onDismiss?: () => void;
  variant?: "error" | "warning" | "info";
}

export function ErrorMessage({
  error,
  onDismiss,
  variant = "error",
}: ErrorMessageProps) {
  if (!error) return null;

  const bgColor = {
    error: "bg-red-50",
    warning: "bg-yellow-50",
    info: "bg-blue-50",
  }[variant];

  const borderColor = {
    error: "border-red-200",
    warning: "border-yellow-200",
    info: "border-blue-200",
  }[variant];

  const textColor = {
    error: "text-red-800",
    warning: "text-yellow-800",
    info: "text-blue-800",
  }[variant];

  const iconColor = {
    error: "text-red-600",
    warning: "text-yellow-600",
    info: "text-blue-600",
  }[variant];

  return (
    <div className={`mb-4 p-4 ${bgColor} border ${borderColor} rounded-lg`}>
      <div className="flex items-start gap-3">
        <div className={`flex-shrink-0 mt-0.5 ${iconColor}`}>
          <svg
            className="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            {variant === "error" && (
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            )}
            {variant === "warning" && (
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            )}
            {variant === "info" && (
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            )}
          </svg>
        </div>
        <div className="flex-1">
          <p className={`text-sm font-medium ${textColor}`}>{error}</p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className={`flex-shrink-0 ${iconColor} hover:opacity-75`}
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

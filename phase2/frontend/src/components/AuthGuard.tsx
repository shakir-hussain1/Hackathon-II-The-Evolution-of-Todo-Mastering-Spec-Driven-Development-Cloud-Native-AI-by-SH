/**
 * T030: AuthGuard Component
 *
 * Route protection component that ensures only authenticated users can access protected pages.
 * Redirects unauthenticated users to the login page.
 *
 * Features:
 * - JWT token verification
 * - Automatic redirect to login if not authenticated
 * - Loading state while checking authentication
 * - Error boundary for authentication errors
 */

"use client";

import { useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/utils/auth";

interface AuthGuardProps {
  children: ReactNode;
  fallback?: ReactNode;
  onAuthError?: (error: Error) => void;
}

export function AuthGuard({
  children,
  fallback,
  onAuthError,
}: AuthGuardProps) {
  const router = useRouter();
  const [isAuthed, setIsAuthed] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [authError, setAuthError] = useState<string | null>(null);

  /**
   * Check authentication status on component mount.
   *
   * Verifies JWT token exists in localStorage.
   * If no token, redirects to login page.
   */
  useEffect(() => {
    async function checkAuth() {
      try {
        setIsLoading(true);

        // Check if user has valid token
        const authed = await isAuthenticated();

        if (!authed) {
          // No token found, redirect to login
          setAuthError("Not authenticated");
          router.push("/auth/login");
          return;
        }

        // User is authenticated
        setIsAuthed(true);
        setAuthError(null);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Authentication check failed";
        setAuthError(errorMessage);
        setIsAuthed(false);

        // Call error callback if provided
        if (onAuthError && error instanceof Error) {
          onAuthError(error);
        }

        // Redirect to login on error
        router.push("/auth/login");
      } finally {
        setIsLoading(false);
      }
    }

    checkAuth();
  }, [router, onAuthError]);

  /**
   * Loading state
   * Shows loading indicator while checking authentication
   */
  if (isLoading) {
    return (
      fallback || (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600">Checking authentication...</p>
          </div>
        </div>
      )
    );
  }

  /**
   * Error state
   * Shows error message if authentication check failed
   */
  if (authError && !isAuthed) {
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
                d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">
            Authentication Required
          </h2>
          <p className="text-gray-600 text-center mb-6">{authError}</p>
          <button
            onClick={() => router.push("/auth/login")}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  /**
   * Not authenticated state
   * This state prevents content flashing before redirect
   */
  if (!isAuthed) {
    return null;
  }

  /**
   * Authenticated state
   * Render protected content
   */
  return <>{children}</>;
}

/**
 * Higher-order component for protecting pages.
 *
 * Usage:
 *   export default withAuth(MyProtectedPage);
 */
export function withAuth<P extends object>(
  Component: React.ComponentType<P>
) {
  return function AuthenticatedComponent(props: P) {
    return (
      <AuthGuard>
        <Component {...props} />
      </AuthGuard>
    );
  };
}

/**
 * Hook to check if user is authenticated.
 *
 * Usage:
 *   const isAuthed = useAuthCheck();
 *   if (!isAuthed) return <div>Loading...</div>;
 */
export function useAuthCheck(): [boolean, boolean, string | null] {
  const [isAuthed, setIsAuthed] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function checkAuth() {
      try {
        const authed = await isAuthenticated();
        setIsAuthed(authed);
        setError(null);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Authentication check failed";
        setError(errorMessage);
        setIsAuthed(false);
      } finally {
        setIsLoading(false);
      }
    }

    checkAuth();
  }, []);

  return [isAuthed, isLoading, error];
}

/**
 * Component for checking authentication with custom render.
 *
 * Usage:
 *   <AuthCheck>
 *     {(isAuthed, isLoading) => (
 *       isLoading ? <Loading /> : isAuthed ? <Protected /> : <Login />
 *     )}
 *   </AuthCheck>
 */
interface AuthCheckProps {
  children: (isAuthed: boolean, isLoading: boolean, error: string | null) => ReactNode;
}

export function AuthCheck({ children }: AuthCheckProps) {
  const [isAuthed, isLoading, error] = useAuthCheck();
  return <>{children(isAuthed, isLoading, error)}</>;
}

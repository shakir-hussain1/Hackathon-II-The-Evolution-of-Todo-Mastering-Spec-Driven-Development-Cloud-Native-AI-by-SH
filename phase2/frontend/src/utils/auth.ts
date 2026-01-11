/**
 * Authentication utilities for token storage and retrieval.
 *
 * Provides functions to manage JWT tokens in localStorage.
 * Used by API client to attach token to requests and by components
 * to check authentication status.
 */

const TOKEN_KEY = "token";

/**
 * Get JWT token from localStorage.
 *
 * Safe for SSR - returns null if called during server-side rendering.
 *
 * @returns Promise<string | null> - JWT token or null if not found
 */
export async function getToken(): Promise<string | null> {
  if (typeof window === "undefined") {
    // Server-side rendering - no localStorage available
    return null;
  }

  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error("Error retrieving token from localStorage:", error);
    return null;
  }
}

/**
 * Save JWT token to localStorage.
 *
 * Safe for SSR - no-op if called during server-side rendering.
 *
 * @param token - JWT token string to store
 * @returns Promise<void>
 */
export async function setToken(token: string): Promise<void> {
  if (typeof window === "undefined") {
    // Server-side rendering - no localStorage available
    return;
  }

  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch (error) {
    console.error("Error saving token to localStorage:", error);
    throw error;
  }
}

/**
 * Remove JWT token from localStorage (logout).
 *
 * Safe for SSR - no-op if called during server-side rendering.
 *
 * @returns Promise<void>
 */
export async function clearToken(): Promise<void> {
  if (typeof window === "undefined") {
    // Server-side rendering - no localStorage available
    return;
  }

  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch (error) {
    console.error("Error clearing token from localStorage:", error);
    throw error;
  }
}

/**
 * Check if user is authenticated by checking for token presence.
 *
 * Note: This only checks for token existence, not validity.
 * For full validation, use the API client which will get 401 for expired tokens.
 *
 * @returns Promise<boolean> - True if token exists, false otherwise
 */
export async function isAuthenticated(): Promise<boolean> {
  const token = await getToken();
  return !!token;
}

/**
 * Extract user_id from JWT token claims.
 *
 * Decodes the JWT payload and extracts the "sub" claim which contains user_id.
 * Does not verify signature - for verification, rely on backend middleware.
 *
 * @returns Promise<string | null> - User ID from token or null if not found
 */
export async function getUserIdFromToken(): Promise<string | null> {
  const token = await getToken();
  if (!token) {
    return null;
  }

  try {
    // JWT format: header.payload.signature
    const parts = token.split(".");
    if (parts.length !== 3) {
      console.error("Invalid token format");
      return null;
    }

    // Decode payload (add padding if needed)
    const payload = parts[1];
    const padded = payload + "==".substring(0, (4 - (payload.length % 4)) % 4);
    const decoded = JSON.parse(atob(padded));

    // "sub" claim contains user_id
    return decoded.sub || null;
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
}

/**
 * Check if JWT token has expired.
 *
 * Checks the "exp" claim (expiration time in Unix timestamp).
 * Does not verify signature - for verification, rely on backend middleware.
 *
 * @returns Promise<boolean> - True if token is expired, false otherwise
 */
export async function isTokenExpired(): Promise<boolean> {
  const token = await getToken();
  if (!token) {
    return true;
  }

  try {
    const parts = token.split(".");
    if (parts.length !== 3) {
      return true;
    }

    const payload = parts[1];
    const padded = payload + "==".substring(0, (4 - (payload.length % 4)) % 4);
    const decoded = JSON.parse(atob(padded));

    const exp = decoded.exp;
    if (!exp) {
      return true;
    }

    // exp is in seconds, current time is in milliseconds
    const now = Math.floor(Date.now() / 1000);
    return exp < now;
  } catch (error) {
    console.error("Error checking token expiration:", error);
    return true;
  }
}

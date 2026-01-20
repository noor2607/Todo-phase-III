// Token storage and management utilities
import { jwtDecode } from 'jwt-decode'; // We'll need to install this package

// Interface for decoded JWT token
export interface DecodedToken {
  sub: string; // user ID
  email: string;
  username: string;
  exp: number; // expiration time
  iat: number; // issued at time
  [key: string]: any; // allow for additional claims
}

/**
 * Store authentication token in secure browser storage
 * @param token JWT token string
 */
export const storeAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('authToken', token);
  }
};

/**
 * Retrieve authentication token from browser storage
 * @returns JWT token string or null if not found
 */
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
};

/**
 * Remove authentication token from browser storage
 */
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
};

/**
 * Decode JWT token to extract user information
 * @param token JWT token string
 * @returns Decoded token object or null if invalid
 */
export const decodeToken = (token: string): DecodedToken | null => {
  try {
    if (!token) return null;
    return jwtDecode<DecodedToken>(token);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

/**
 * Check if the token is expired
 * @param token JWT token string
 * @returns true if token is expired, false otherwise
 */
export const isTokenExpired = (token: string): boolean => {
  const decodedToken = decodeToken(token);
  if (!decodedToken || !decodedToken.exp) {
    return true; // If there's no expiration, treat as expired
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  return decodedToken.exp < currentTime;
};

/**
 * Get token expiration time
 * @param token JWT token string
 * @returns Expiration timestamp or null if invalid
 */
export const getTokenExpiration = (token: string): number | null => {
  const decodedToken = decodeToken(token);
  return decodedToken?.exp || null;
};

/**
 * Check if token is about to expire (within 5 minutes)
 * @param token JWT token string
 * @returns true if token is about to expire, false otherwise
 */
export const isTokenExpiringSoon = (token: string): boolean => {
  const decodedToken = decodeToken(token);
  if (!decodedToken || !decodedToken.exp) {
    return true; // If there's no expiration, treat as expiring soon
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  const fiveMinutesInSeconds = 5 * 60; // 5 minutes in seconds

  return (decodedToken.exp - currentTime) < fiveMinutesInSeconds;
};

/**
 * Store user information in browser storage
 * @param user User object to store
 */
export const storeUser = (user: any): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user', JSON.stringify(user));
  }
};

/**
 * Retrieve user information from browser storage
 * @returns User object or null if not found
 */
export const getUser = (): any | null => {
  if (typeof window !== 'undefined') {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
  return null;
};

/**
 * Remove user information from browser storage
 */
export const removeUser = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user');
  }
};

/**
 * Check if user is authenticated
 * @returns true if user is authenticated, false otherwise
 */
export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return !!token && !isTokenExpired(token);
};

/**
 * Complete logout process - clear all authentication data
 */
export const logout = (): void => {
  removeAuthToken();
  removeUser();

  // Optionally redirect to login page
  if (typeof window !== 'undefined') {
    window.location.href = '/signin';
  }
};

/**
 * Refresh the authentication token
 * @returns New token if refresh is successful, null otherwise
 */
export const refreshToken = async (): Promise<string | null> => {
  // In a real implementation, this would call the backend refresh endpoint
  // For now, we'll return null to indicate refresh is not implemented
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      return null;
    }

    // Call the refresh API endpoint
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      const newToken = data.token;

      // Store the new token
      storeAuthToken(newToken);
      return newToken;
    } else {
      // If refresh fails, log out the user
      logout();
      return null;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    logout(); // If there's an error refreshing, log out the user
    return null;
  }
};

/**
 * Validate and potentially refresh the token if needed
 * @returns true if token is valid or successfully refreshed, false otherwise
 */
export const validateAndRefreshToken = async (): Promise<boolean> => {
  const token = getAuthToken();
  if (!token) {
    return false;
  }

  // If token is expiring soon, try to refresh it
  if (isTokenExpiringSoon(token)) {
    const newToken = await refreshToken();
    return !!newToken;
  }

  // If token is not expired, it's valid
  return !isTokenExpired(token);
};
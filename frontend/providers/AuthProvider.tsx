'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { isAuthenticated, logout as authLogout, getAuthToken } from '../lib/auth';

interface AuthContextType {
  user: any | null;
  loading: boolean;
  login: (userData: any) => void;
  logout: () => void;
  checkAuthStatus: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkInitialAuth = async () => {
      try {
        // Verify token with the backend as well
        const token = getAuthToken();
        if (token) {
          // Try to verify the token with the backend
          try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/verify`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
            });

            if (!response.ok) {
              // Token is invalid according to backend, log out user
              console.warn('Token verification failed with backend. Logging out.');
              authLogout();
              setUser(null);
              return;
            }

            const result = await response.json();
            if (result.success) {
              // Token is valid, retrieve user data
              const userData = localStorage.getItem('user');
              if (userData) {
                setUser(JSON.parse(userData));
              } else {
                // If no user data in localStorage but token exists,
                // try to fetch user profile from backend
                const profileResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/profile`, {
                  method: 'GET',
                  headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                  },
                });

                if (profileResponse.ok) {
                  const profileData = await profileResponse.json();
                  setUser(profileData.data || { id: 'unknown', email: 'unknown' });
                  // Store user data in localStorage for future use
                  localStorage.setItem('user', JSON.stringify(profileData.data || { id: 'unknown', email: 'unknown' }));
                } else {
                  console.warn('Could not fetch user profile. Logging out.');
                  authLogout();
                  setUser(null);
                  return;
                }
              }
            } else {
              // Token verification failed
              console.warn('Token verification failed. Logging out.');
              authLogout();
              setUser(null);
            }
          } catch (backendError) {
            console.error('Error verifying token with backend:', backendError);
            // If we can't reach the backend, we'll fall back to local verification
            const authenticated = isAuthenticated();
            if (authenticated) {
              const userData = localStorage.getItem('user');
              if (userData) {
                setUser(JSON.parse(userData));
              } else {
                console.warn('Token exists locally but no user data found. Logging out.');
                authLogout();
                setUser(null);
              }
            } else {
              setUser(null);
            }
          }
        } else {
          // No token in localStorage
          setUser(null);
        }
      } catch (error) {
        console.error('Error checking initial auth status:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkInitialAuth();
  }, []);

  const login = (userData: any) => {
    setUser(userData);
    // Store user data in localStorage
    localStorage.setItem('user_data', JSON.stringify(userData));
  };

  const logout = async () => {
    setUser(null);
    // Clear auth state using the logout function from auth library
    authLogout();
    // Remove user data from localStorage
    localStorage.removeItem('user_data');
  };

  const checkAuthStatus = async (): Promise<boolean> => {
    const authenticated = await isAuthenticated();
    if (!authenticated) {
      setUser(null);
    }
    return authenticated;
  };

  const value = {
    user,
    loading,
    login,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
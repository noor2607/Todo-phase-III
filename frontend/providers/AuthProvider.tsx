'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { isAuthenticated, logout as authLogout } from '../lib/auth';

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
        const authenticated = await isAuthenticated();
        if (authenticated) {
          // In a real implementation, we would fetch user data
          // For now, we'll retrieve user data from localStorage or use mock data
          const userData = localStorage.getItem('user_data');
          if (userData) {
            setUser(JSON.parse(userData));
          } else {
            setUser({ id: 'mock-user-id', email: 'user@example.com' });
          }
        } else {
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
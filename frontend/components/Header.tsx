'use client';

import Link from 'next/link';
import { useAuth } from '../providers/AuthProvider';

const Header = () => {
  const { user, logout, loading } = useAuth();

  const handleLogout = async () => {
    await logout();
    // Redirect to home or login page
    window.location.href = '/';
  };

  return (
    <header className="bg-primary-500 text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Link href="/" className="text-xl font-bold">Todo App</Link>
        </div>

        <nav className="flex space-x-6">
          <Link href="/" className="hover:underline">Home</Link>
          <Link href="/features" className="hover:underline">Features</Link>

          {loading ? (
            <div className="h-6 w-20 bg-gray-300 rounded animate-pulse"></div>
          ) : user ? (
            <>
              <Link href="/tasks" className="hover:underline">Tasks</Link>
              <button onClick={handleLogout} className="hover:underline">Sign Out</button>
            </>
          ) : (
            <>
              <Link href="/signin" className="hover:underline">Sign In</Link>
              <Link href="/signup" className="hover:underline">Sign Up</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
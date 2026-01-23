'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../providers/AuthProvider';

interface ChatbotIconProps {
  onClick: () => void;
}

const ChatbotIcon = ({ onClick }: ChatbotIconProps) => {
  const { user } = useAuth();
  const router = useRouter();
  const [showTooltip, setShowTooltip] = useState(false);

  const handleClick = () => {
    if (user) {
      // If user is authenticated, open the chat interface
      onClick();
    } else {
      // If user is not authenticated, show tooltip or redirect to login
      setShowTooltip(true);
      setTimeout(() => setShowTooltip(false), 3000);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <button
        onClick={handleClick}
        onMouseEnter={() => !user && setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        className="w-14 h-14 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        aria-label={user ? "Open AI Assistant" : "Sign in to use AI Assistant"}
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
          <path fillRule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.587 2.674 6.192.232.226.277.428.254.543a3.73 3.73 0 01-.814 1.686.75.75 0 00.44 1.223zM8.25 10.875a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25zM10.875 12a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0zm4.875-1.125a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25z" clipRule="evenodd" />
        </svg>
      </button>

      {/* Tooltip for unauthenticated users */}
      {showTooltip && !user && (
        <div
          className="absolute bottom-16 right-0 bg-gray-800 text-white text-xs rounded py-2 px-3 whitespace-nowrap animate-fadeIn"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          onClick={() => {
            router.push('/signin');
            setShowTooltip(false);
          }}
        >
          Sign in to use AI Assistant
          <div className="absolute bottom-0 right-4 transform translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-800"></div>
        </div>
      )}
    </div>
  );
};

export default ChatbotIcon;
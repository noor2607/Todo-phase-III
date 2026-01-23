'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import TodoChat from '../src/components/TodoChat';

export default function HomePage() {
  // In a real application, these would come from your auth context/state
  const [userId, setUserId] = useState(null);
  const [authToken, setAuthToken] = useState('');
  const [showChat, setShowChat] = useState(false);

  // In a real app, you'd get the user info from your auth provider
  useEffect(() => {
    // Simulate getting user info from auth system
    // In a real app, this would come from your auth provider
    const mockUserInfo = {
      id: 1,
      token: 'mock-jwt-token' // In real app, this would be a real JWT from auth provider
    };

    setUserId(mockUserInfo.id);
    setAuthToken(mockUserInfo.token);
  }, []);

  if (!userId || !authToken) {
    return (
      <div className="loading-container">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      {!showChat ? (
        <div className="dashboard">
          <header className="page-header">
            <h1>Todo Dashboard</h1>
            <p>Your task management center</p>
          </header>

          <main className="dashboard-main">
            <div className="dashboard-content">
              <h2>Welcome to Your Todo Dashboard</h2>
              <p>Click the AI assistant icon to manage your tasks with natural language</p>

              <div className="bot-icon-container" onClick={() => setShowChat(true)}>
                <div className="bot-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="bot-icon-svg">
                    <path fillRule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.587 2.674 6.192.232.226.277.428.254.543a3.73 3.73 0 01-.814 1.686.75.75 0 00.44 1.223zM8.25 10.875a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25zM10.875 12a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0zm4.875-1.125a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25z" clipRule="evenodd" />
                  </svg>
                </div>
                <p>AI Assistant</p>
              </div>
            </div>
          </main>

          <footer className="page-footer">
            <p>Powered by AI • Your tasks are securely stored and processed</p>
          </footer>
        </div>
      ) : (
        <div className="chat-interface">
          <header className="chat-header">
            <button onClick={() => setShowChat(false)} className="back-button">
              ← Back to Dashboard
            </button>
            <h1>Todo AI Assistant</h1>
            <p>Manage your tasks with natural language</p>
          </header>

          <main className="page-main">
            <TodoChat userId={userId} authToken={authToken} />
          </main>

          <footer className="page-footer">
            <p>Powered by AI • Your tasks are securely stored and processed</p>
          </footer>
        </div>
      )}
    </div>
  );
}
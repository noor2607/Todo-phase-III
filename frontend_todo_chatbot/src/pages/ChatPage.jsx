import React, { useState, useEffect } from 'react';
import TodoChat from '../components/TodoChat';
import '../styles/global.css';

const ChatPage = () => {
  // In a real application, these would come from your auth context/state
  const [userId, setUserId] = useState(1); // Example user ID
  const [authToken, setAuthToken] = useState(''); // Example auth token

  // In a real app, you'd get the user info from your auth provider
  useEffect(() => {
    // Simulate getting user info from auth system
    const userInfo = {
      id: 1,
      token: 'fake-jwt-token-for-demo' // In real app, this would be a real JWT
    };

    setUserId(userInfo.id);
    setAuthToken(userInfo.token);
  }, []);

  return (
    <div className="chat-page">
      <header className="chat-header">
        <h1>Todo AI Assistant</h1>
        <p>Manage your tasks with natural language</p>
      </header>

      <main className="chat-main">
        <TodoChat userId={userId} authToken={authToken} />
      </main>

      <footer className="chat-footer">
        <p>Powered by AI • Your tasks are securely stored and processed</p>
      </footer>
    </div>
  );
};

export default ChatPage;
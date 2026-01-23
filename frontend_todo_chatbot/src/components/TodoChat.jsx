import React, { useState, useEffect, useRef } from 'react';
import './TodoChat.css';

const TodoChat = ({ userId, authToken }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Fetch existing conversations for the user
  useEffect(() => {
    fetchConversations();
  }, [userId]);

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchConversations = async () => {
    try {
      // In a real implementation, we would fetch conversations from the backend
      // For now, we'll simulate with an empty list
      setConversations([]);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request to the backend
      const requestBody = {
        conversation_id: currentConversationId || null,
        message: inputValue
      };

      // Call the backend API
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update current conversation ID
      if (data.conversation_id) {
        setCurrentConversationId(data.conversation_id);
      }

      // Add assistant response to the chat
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        toolCalls: data.tool_calls || []
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Process any tool calls
      if (data.tool_calls && data.tool_calls.length > 0) {
        processToolCalls(data.tool_calls);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an issue processing your request. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const processToolCalls = (toolCalls) => {
    // Process any tool calls returned by the AI agent
    toolCalls.forEach(toolCall => {
      console.log(`Tool called: ${toolCall.name}`, toolCall.arguments, toolCall.result);
    });
  };

  const startNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([]);
  };

  const selectConversation = (conversationId) => {
    setCurrentConversationId(conversationId);
    // In a real implementation, we would load the conversation messages
    setMessages([]);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="todo-chat-container">
      <div className="conversations-panel">
        <div className="conversations-header">
          <h3>Conversations</h3>
          <button onClick={startNewConversation} className="new-conversation-btn">
            + New
          </button>
        </div>
        <div className="conversations-list">
          {conversations.map(conv => (
            <div
              key={conv.id}
              className={`conversation-item ${currentConversationId === conv.id ? 'active' : ''}`}
              onClick={() => selectConversation(conv.id)}
            >
              <div className="conversation-preview">
                {conv.preview || 'New conversation'}
              </div>
              <div className="conversation-date">
                {new Date(conv.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="chat-area">
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h2>Hello! How can I help you manage your tasks today?</h2>
              <p>You can ask me to add, list, update, or complete tasks using natural language.</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role} ${message.isError ? 'error' : ''}`}
              >
                <div className="message-content">
                  {message.content}
                  {message.toolCalls && message.toolCalls.length > 0 && (
                    <div className="tool-calls">
                      {message.toolCalls.map((call, idx) => (
                        <div key={idx} className="tool-call">
                          <strong>{call.name}</strong>: {JSON.stringify(call.arguments)}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <div className="message-timestamp">
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <span className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your task request here (e.g., 'Add a task to buy groceries')..."
            disabled={isLoading}
            rows={3}
          />
          <button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TodoChat;
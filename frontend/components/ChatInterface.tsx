'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../providers/AuthProvider';
import { chatApi, ApiResponse } from '../lib/api'; // Use the chat API client that points to main backend

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isError?: boolean;
}

interface ChatInterfaceProps {
  isOpen: boolean;
  onClose: () => void;
  onTaskAction?: () => void; // Callback to trigger task refresh after AI operations
}


interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: any[];
}

const ChatInterface = ({ isOpen, onClose, onTaskAction }: ChatInterfaceProps) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. How can I help you manage your tasks today?',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request to the backend
      const requestBody = {
        conversation_id: null, // Will be handled by backend for new conversations
        message: inputValue
      };

      // Call the backend API using the chat API client (which now points to main backend)
      const response = await chatApi.post(`/api/chat`, requestBody);

      // Handle different possible response structures from the backend
      let chatResponse;

      // Check if response follows ApiResponse<ChatResponse> structure
      if (response.data && typeof response.data === 'object') {
        if ('data' in response.data && response.data.data) {
          // It's wrapped in ApiResponse
          chatResponse = response.data.data;
        } else {
          // Direct ChatResponse structure
          chatResponse = response.data;
        }
      } else {
        throw new Error('Invalid response format from chat API');
      }

      if (!chatResponse) {
        throw new Error('Invalid response from chat API');
      }

      // Ensure we have the expected properties
      const assistantResponse = chatResponse.response || 'I processed your request.';
      const toolCalls = chatResponse.tool_calls || [];

      // Check if the response indicates that the AI service is unavailable
      if (assistantResponse.toLowerCase().includes('ai service is currently unavailable') ||
          assistantResponse.toLowerCase().includes('cohere_api_key')) {
        // Show a special message to the user indicating setup is needed
        const setupMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `${assistantResponse}\n\nNote: You can still manage tasks manually using the task interface.`,
          timestamp: new Date(),
          isError: true
        };

        setMessages(prev => [...prev, setupMessage]);
        return; // Exit early as this is an informational message, not an error
      }

      // Add assistant response to the chat
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: assistantResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if the response contains task creation tool calls
      // and trigger the callback if provided
      if (onTaskAction && Array.isArray(toolCalls) && toolCalls.length > 0) {
        const hasTaskCreationCall = toolCalls.some(toolCall =>
          toolCall.name &&
          (toolCall.name === 'add_task' ||
           toolCall.name.includes('add_task') ||
           toolCall.result?.success === true)
        );

        if (hasTaskCreationCall) {
          // Small delay to ensure the task is persisted in the database
          setTimeout(() => {
            onTaskAction();
          }, 500);
        }
      }
    } catch (error: any) {
      console.error('Error sending message:', error);

      let errorMessageText = 'Sorry, I encountered an issue processing your request. Please try again.';

      // Handle different types of errors
      if (error.response) {
        // Server responded with error status
        const status = error.response.status;
        switch (status) {
          case 401:
            errorMessageText = 'Authentication failed. Please log in again.';
            // Redirect to login
            setTimeout(() => {
              localStorage.removeItem('authToken');
              localStorage.removeItem('user');
              window.location.href = '/signin';
            }, 2000);
            break;
          case 403:
            errorMessageText = 'Access denied. You can only access your own data.';
            break;
          case 404:
            errorMessageText = 'The requested resource was not found.';
            break;
          case 422:
            errorMessageText = 'Invalid request format. Please check your input.';
            break;
          case 500:
            errorMessageText = 'Server error. The AI service may be temporarily unavailable.';
            break;
          default:
            errorMessageText = `Server error (${status}). Please try again later.`;
        }
      } else if (error.request) {
        // Request was made but no response received
        errorMessageText = 'Network error. Please check your connection and try again.';
      } else {
        // Something else happened
        errorMessageText = 'An unexpected error occurred. Please try again.';
      }

      // Add error message to the chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: errorMessageText,
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={onClose}
      ></div>

      {/* Chat Container */}
      <div className="absolute bottom-24 right-6 w-full max-w-md h-[70vh] bg-white rounded-xl shadow-xl flex flex-col">
        {/* Header */}
        <div className="bg-indigo-600 text-white p-4 rounded-t-xl flex justify-between items-center">
          <h3 className="font-semibold text-lg">AI Task Assistant</h3>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`mb-4 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-indigo-500 text-white'
                    : message.isError
                      ? 'bg-red-100 text-red-800'
                      : 'bg-white text-gray-800 border border-gray-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="mb-4 flex justify-start">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-white text-gray-800 border border-gray-200">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <div className="flex items-end space-x-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me to add, list, update, or complete tasks..."
              disabled={isLoading}
              className="flex-1 border border-gray-300 rounded-lg p-3 h-16 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading || !user}
              className={`h-12 w-12 flex items-center justify-center rounded-full ${
                inputValue.trim() && !isLoading && user
                  ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              } transition-colors duration-200`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Example: "Add a task to buy groceries" or "Show me my tasks"
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
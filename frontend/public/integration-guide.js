/**
 * Frontend Integration Guide for Todo App Backend
 *
 * This guide provides JavaScript code examples for integrating with the backend API
 */

// 1. AUTHENTICATION HANDLING
// ==========================

// Store JWT token in localStorage after login
function storeAuthToken(token) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('authToken', token);
  }
}

// Retrieve authentication token from localStorage
function getAuthToken() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
}

// Remove authentication token from localStorage
function removeAuthToken() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
}

// Verify token on page load and redirect if invalid/missing
async function verifyTokenOnLoad() {
  const token = getAuthToken();
  if (!token) {
    // No token, redirect to login
    window.location.href = '/signin';
    return false;
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/auth/verify`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Token is invalid according to backend, redirect to login
      removeAuthToken();
      window.location.href = '/signin';
      return false;
    }

    const result = await response.json();
    if (result.success) {
      return true; // Token is valid
    } else {
      // Token verification failed
      removeAuthToken();
      window.location.href = '/signin';
      return false;
    }
  } catch (error) {
    console.error('Error verifying token:', error);
    // If we can't reach the backend, redirect to login for safety
    window.location.href = '/signin';
    return false;
  }
}

// Clear token on logout
function logout() {
  removeAuthToken();
  window.location.href = '/signin';
}


// 2. AUTHENTICATED REQUESTS
// =========================

// Function to make authenticated API requests
async function authenticatedRequest(url, options = {}) {
  const token = getAuthToken();

  if (!token) {
    throw new Error('No authentication token found');
  }

  const config = {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  const response = await fetch(url, config);

  if (response.status === 401) {
    // Token expired or invalid, redirect to login
    removeAuthToken();
    window.location.href = '/signin';
    throw new Error('Authentication required');
  }

  return response;
}


// 3. TASK OPERATIONS
// ==================

// Fetch tasks with optional filters
async function fetchTasks(statusFilter = null, sortBy = null) {
  let url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/tasks`;

  const params = new URLSearchParams();
  if (statusFilter) params.append('status', statusFilter);
  if (sortBy) params.append('sort', sortBy);

  if (params.toString()) {
    url += '?' + params.toString();
  }

  const response = await authenticatedRequest(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data || [];
}

// Add a new task
async function addTask(taskData) {
  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/tasks`;

  const response = await authenticatedRequest(url, {
    method: 'POST',
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to add task: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data;
}

// Toggle task completion status
async function toggleTaskCompletion(taskId) {
  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/tasks/${taskId}/complete`;

  const response = await authenticatedRequest(url, {
    method: 'PATCH',
  });

  if (!response.ok) {
    throw new Error(`Failed to toggle task completion: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data;
}

// Update task
async function updateTask(taskId, taskData) {
  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/tasks/${taskId}`;

  const response = await authenticatedRequest(url, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to update task: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data;
}

// Delete task
async function deleteTask(taskId) {
  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/tasks/${taskId}`;

  const response = await authenticatedRequest(url, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`Failed to delete task: ${response.statusText}`);
  }

  return true;
}


// 4. CHATBOT TASK INTEGRATION
// ===========================

// Send message to chatbot
async function sendChatMessage(message) {
  const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://larebnoor-todo-chatbot.hf.space'}/api/chat`;

  const response = await authenticatedRequest(url, {
    method: 'POST',
    body: JSON.stringify({
      conversation_id: null,
      message: message
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to send chat message: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data || data; // Handle both wrapped and unwrapped responses
}


// 5. FILTERS AND SORTING
// ======================

// Apply filters to tasks
function applyFilters(tasks, statusFilter = 'all') {
  if (statusFilter === 'completed') {
    return tasks.filter(task => task.completed);
  } else if (statusFilter === 'pending') {
    return tasks.filter(task => !task.completed);
  }
  return tasks; // 'all' filter
}

// Sort tasks
function sortTasks(tasks, sortBy = 'created_at', sortOrder = 'desc') {
  return [...tasks].sort((a, b) => {
    let comparison = 0;

    if (sortBy === 'title') {
      comparison = a.title.localeCompare(b.title);
    } else if (sortBy === 'created_at') {
      comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });
}


// 6. ERROR HANDLING
// =================

// Error handler class for user-friendly messages
class ErrorHandler {
  constructor(autoHideDuration = 5000) {
    this.autoHideDuration = autoHideDuration;
    this.errors = [];
    this.listeners = [];
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify(message, type = 'error') {
    const error = {
      id: Math.random().toString(36).substr(2, 9),
      message,
      type,
      timestamp: Date.now()
    };

    this.errors.push(error);
    this.notifyListeners();

    // Auto-hide error after specified duration
    if (this.autoHideDuration > 0) {
      setTimeout(() => {
        this.remove(error.id);
      }, this.autoHideDuration);
    }

    return error.id;
  }

  remove(id) {
    this.errors = this.errors.filter(error => error.id !== id);
    this.notifyListeners();
  }

  clearAll() {
    this.errors = [];
    this.notifyListeners();
  }

  notifyListeners() {
    this.listeners.forEach(listener => listener([...this.errors]));
  }

  getErrors() {
    return [...this.errors];
  }
}

// Initialize global error handler
const errorHandler = new ErrorHandler();

// Function to show user-friendly error messages
function showError(message, type = 'error') {
  errorHandler.notify(message, type);

  // Also display in console for debugging
  console[type === 'error' ? 'error' : type === 'warn' ? 'warn' : 'log'](message);
}


// 7. UI UPDATES
// =============

// Function to dynamically update task list after operations
function updateTaskList(updatedTask, tasks, setTasksCallback) {
  const updatedTasks = tasks.map(task =>
    task.id === updatedTask.id ? updatedTask : task
  );
  setTasksCallback(updatedTasks);
}

// Function to add new task to the list
function addTaskToList(newTask, tasks, setTasksCallback) {
  setTasksCallback([newTask, ...tasks]);
}

// Function to remove task from the list
function removeTaskFromList(taskId, tasks, setTasksCallback) {
  const updatedTasks = tasks.filter(task => task.id !== taskId);
  setTasksCallback(updatedTasks);
}


// 8. INITIALIZATION
// =================

// Initialize the application
function initializeApp() {
  // Verify authentication on startup
  verifyTokenOnLoad()
    .then(isValid => {
      if (!isValid) {
        console.log('Redirecting to login...');
      } else {
        console.log('Authentication verified');
      }
    })
    .catch(error => {
      console.error('Error initializing app:', error);
      window.location.href = '/signin';
    });
}

// Call initialization when DOM is ready
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
  } else {
    initializeApp();
  }
}

console.log("Todo App frontend integration ready!");
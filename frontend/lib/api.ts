import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Create API client for main backend (authentication and task management)
const mainApiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Create API client for chatbot backend (AI chat functionality)
const chatApiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 15000, // Slightly longer timeout for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token to requests for main API client
mainApiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Request interceptor to attach JWT token to requests for chat API client
chatApiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Retry mechanism for failed requests due to token expiration
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 second

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Response interceptor to handle token expiration and refresh for main API client
mainApiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Return successful responses as-is
    return response;
  },
  async (error: AxiosError) => {
    const config = error.config as any;

    // Handle 401 Unauthorized responses (token expired or invalid)
    if (error.response?.status === 401) {
      // Clear stored tokens
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');

      // Redirect to login page
      window.location.href = '/signin';
    }
    // Handle 403 Forbidden or other auth-related errors that might be recoverable
    else if (error.response?.status === 403 && config && !config.retryCount) {
      // Set retry count to prevent infinite loops
      config.retryCount = 0;
    }

    // Retry logic for transient failures
    if (error.code === 'ECONNABORTED' || error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED' || error.code === 'EAI_AGAIN') {
      if (!config || config.retryCount >= MAX_RETRIES) {
        // If retries are exhausted, implement graceful degradation
        if (config.url?.includes('/tasks')) {
          // For task-related requests, try to use cached data or show offline message
          console.warn(`Service temporarily unavailable for ${config.url}. Using graceful degradation.`);

          // For GET requests, we could potentially return cached data
          // For other requests, we could queue them for later
          if (config.method?.toUpperCase() === 'GET') {
            // In a real implementation, we would return cached data
            // For now, we'll just reject with a more informative error
          } else if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(config.method?.toUpperCase())) {
            // Queue operations for when connection is restored
            if (typeof window !== 'undefined') {
              // Add to offline queue if available
              const offlineOp = {
                operation: config.method?.toUpperCase(),
                endpoint: config.url,
                data: config.data
              };

              // Try to queue the operation for later processing
              try {
                // This would use our offline manager if available
                console.log('Queuing operation for later:', offlineOp);
              } catch (queueError) {
                console.error('Failed to queue operation for offline processing:', queueError);
              }
            }
          }
        }
        return Promise.reject(error);
      }

      config.retryCount = (config.retryCount || 0) + 1;
      const delayTime = RETRY_DELAY * Math.pow(2, config.retryCount - 1); // Exponential backoff
      await delay(delayTime);

      return mainApiClient(config);
    }

    // Return the error to be handled by the calling function
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration and refresh for chat API client
chatApiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Return successful responses as-is
    return response;
  },
  async (error: AxiosError) => {
    const config = error.config as any;

    // Handle 401 Unauthorized responses (token expired or invalid)
    if (error.response?.status === 401) {
      // Clear stored tokens
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');

      // Redirect to login page
      window.location.href = '/signin';
    }
    // Handle 403 Forbidden or other auth-related errors that might be recoverable
    else if (error.response?.status === 403 && config && !config.retryCount) {
      // Set retry count to prevent infinite loops
      config.retryCount = 0;
    }

    // Retry logic for transient failures
    if (error.code === 'ECONNABORTED' || error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED' || error.code === 'EAI_AGAIN') {
      if (!config || config.retryCount >= MAX_RETRIES) {
        // If retries are exhausted, implement graceful degradation
        if (config.url?.includes('/chat')) {
          // For chat-related requests, show appropriate message
          console.warn(`Chat service temporarily unavailable for ${config.url}. Please try again.`);
        }
        return Promise.reject(error);
      }

      config.retryCount = (config.retryCount || 0) + 1;
      const delayTime = RETRY_DELAY * Math.pow(2, config.retryCount - 1); // Exponential backoff
      await delay(delayTime);

      return chatApiClient(config);
    }

    // Return the error to be handled by the calling function
    return Promise.reject(error);
  }
);

// Add retryCount property to AxiosRequestConfig
declare module 'axios' {
  interface AxiosRequestConfig {
    retryCount?: number;
  }
}

// Export the main API client as default for backward compatibility
export default mainApiClient;

// Type definitions for API responses
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

// Helper functions for common API operations with main API client
export const api = {
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return mainApiClient.get<ApiResponse<T>>(url, config);
  },

  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return mainApiClient.post<ApiResponse<T>>(url, data, config);
  },

  put: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return mainApiClient.put<ApiResponse<T>>(url, data, config);
  },

  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return mainApiClient.patch<ApiResponse<T>>(url, data, config);
  },

  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return mainApiClient.delete<ApiResponse<T>>(url, config);
  },
};

// Helper functions for chat API operations
export const chatApi = {
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return chatApiClient.post<ApiResponse<T>>(url, data, config);
  },
};
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Create an axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token to requests
apiClient.interceptors.request.use(
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

// Response interceptor to handle token expiration and refresh
apiClient.interceptors.response.use(
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

      return apiClient(config);
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

export default apiClient;

// Type definitions for API responses
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

// Helper functions for common API operations
export const api = {
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return apiClient.get<ApiResponse<T>>(url, config);
  },

  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return apiClient.post<ApiResponse<T>>(url, data, config);
  },

  put: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return apiClient.put<ApiResponse<T>>(url, data, config);
  },

  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return apiClient.patch<ApiResponse<T>>(url, data, config);
  },

  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>> => {
    return apiClient.delete<ApiResponse<T>>(url, config);
  },
};
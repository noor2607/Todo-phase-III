// Offline capability manager for handling operations when network is unavailable

interface OfflineOperation {
  id: string;
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  endpoint: string;
  data?: any;
  timestamp: number;
}

class OfflineManager {
  private static readonly OFFLINE_QUEUE_KEY = 'offline_operations_queue';
  private static readonly IS_ONLINE_KEY = 'is_online_status';

  /**
   * Check if the application is currently online
   * @returns true if online, false if offline
   */
  static isOnline(): boolean {
    // First check navigator.onLine
    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      return false;
    }

    // Then check our stored status
    if (typeof window !== 'undefined') {
      const storedStatus = localStorage.getItem(this.IS_ONLINE_KEY);
      return storedStatus ? JSON.parse(storedStatus) : true;
    }

    return true;
  }

  /**
   * Mark the application as offline
   */
  static setOffline(): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.IS_ONLINE_KEY, JSON.stringify(false));
    }
  }

  /**
   * Mark the application as online
   */
  static setOnline(): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.IS_ONLINE_KEY, JSON.stringify(true));
    }
  }

  /**
   * Add an operation to the offline queue
   * @param operation The operation to queue for later execution
   */
  static addToQueue(operation: Omit<OfflineOperation, 'id' | 'timestamp'>): string {
    const id = this.generateId();
    const offlineOp: OfflineOperation = {
      ...operation,
      id,
      timestamp: Date.now()
    };

    const queue = this.getQueue();
    queue.push(offlineOp);
    this.saveQueue(queue);

    return id;
  }

  /**
   * Remove an operation from the queue
   * @param id The ID of the operation to remove
   */
  static removeFromQueue(id: string): void {
    const queue = this.getQueue();
    const updatedQueue = queue.filter(op => op.id !== id);
    this.saveQueue(updatedQueue);
  }

  /**
   * Get all operations in the offline queue
   * @returns Array of queued operations
   */
  static getQueue(): OfflineOperation[] {
    if (typeof window !== 'undefined') {
      const queueStr = localStorage.getItem(this.OFFLINE_QUEUE_KEY);
      return queueStr ? JSON.parse(queueStr) : [];
    }
    return [];
  }

  /**
   * Clear all operations from the queue
   */
  static clearQueue(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.OFFLINE_QUEUE_KEY);
    }
  }

  /**
   * Process all operations in the offline queue when back online
   */
  static async processQueue(): Promise<void> {
    const queue = this.getQueue();

    for (const operation of queue) {
      try {
        // Attempt to execute the operation
        await this.executeOperation(operation);
        // If successful, remove from queue
        this.removeFromQueue(operation.id);
      } catch (error) {
        console.error(`Failed to execute offline operation ${operation.id}:`, error);
        // Keep the operation in the queue for later retry
      }
    }
  }

  /**
   * Execute a single offline operation
   * @param operation The operation to execute
   */
  private static async executeOperation(operation: OfflineOperation): Promise<void> {
    const options: RequestInit = {
      method: operation.operation,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      }
    };

    if (operation.data) {
      options.body = JSON.stringify(operation.data);
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}${operation.endpoint}`, options);

    if (!response.ok) {
      throw new Error(`Failed to execute operation: ${response.statusText}`);
    }
  }

  /**
   * Generate a unique ID for an offline operation
   * @returns Unique identifier string
   */
  private static generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Save the queue to localStorage
   * @param queue The queue to save
   */
  private static saveQueue(queue: OfflineOperation[]): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.OFFLINE_QUEUE_KEY, JSON.stringify(queue));
    }
  }

  /**
   * Listen for online/offline events
   * @param onOnline Callback function when back online
   * @param onOffline Callback function when offline
   */
  static listenForConnectivityChanges(onOnline?: () => void, onOffline?: () => void): void {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.setOnline();
        if (onOnline) onOnline();
      });

      window.addEventListener('offline', () => {
        this.setOffline();
        if (onOffline) onOffline();
      });
    }
  }
}

export default OfflineManager;
// Error handling utilities for displaying user-friendly messages

interface ErrorDisplay {
  id: string;
  message: string;
  type: 'error' | 'warning' | 'info';
  autoHideDuration?: number;
}

class ErrorHandler {
  private static activeErrors: ErrorDisplay[] = [];
  private static listeners: ((errors: ErrorDisplay[]) => void)[] = [];

  static subscribe(listener: (errors: ErrorDisplay[]) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  static notify(message: string, type: 'error' | 'warning' | 'info' = 'error', autoHideDuration: number = 5000) {
    const error: ErrorDisplay = {
      id: Math.random().toString(36).substr(2, 9),
      message,
      type,
      autoHideDuration
    };

    this.activeErrors.push(error);
    this.notifyListeners();

    // Auto-hide error after specified duration
    if (autoHideDuration > 0) {
      setTimeout(() => {
        this.remove(error.id);
      }, autoHideDuration);
    }

    return error.id;
  }

  static remove(id: string) {
    this.activeErrors = this.activeErrors.filter(error => error.id !== id);
    this.notifyListeners();
  }

  static clearAll() {
    this.activeErrors = [];
    this.notifyListeners();
  }

  private static notifyListeners() {
    this.listeners.forEach(listener => listener([...this.activeErrors]));
  }

  static getErrors(): ErrorDisplay[] {
    return [...this.activeErrors];
  }
}

export default ErrorHandler;
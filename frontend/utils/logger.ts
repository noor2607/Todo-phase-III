// Logger utility for frontend error logging

// Define log levels
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error'
}

// Define logger configuration interface
interface LoggerConfig {
  level: LogLevel;
  enabled: boolean;
  prefix?: string;
}

// Default logger configuration
const DEFAULT_CONFIG: LoggerConfig = {
  level: LogLevel.INFO,
  enabled: true,
  prefix: '[TODO_APP]'
};

class Logger {
  private config: LoggerConfig;

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Log a debug message
   * @param message The message to log
   * @param data Optional data to include with the log
   */
  debug(message: string, data?: any): void {
    this.log(LogLevel.DEBUG, message, data);
  }

  /**
   * Log an info message
   * @param message The message to log
   * @param data Optional data to include with the log
   */
  info(message: string, data?: any): void {
    this.log(LogLevel.INFO, message, data);
  }

  /**
   * Log a warning message
   * @param message The message to log
   * @param data Optional data to include with the log
   */
  warn(message: string, data?: any): void {
    this.log(LogLevel.WARN, message, data);
  }

  /**
   * Log an error message
   * @param message The message to log
   * @param data Optional data to include with the log
   */
  error(message: string, data?: any): void {
    this.log(LogLevel.ERROR, message, data);
  }

  /**
   * Internal logging method that checks log level and enabled status
   * @param level The log level
   * @param message The message to log
   * @param data Optional data to include with the log
   */
  private log(level: LogLevel, message: string, data?: any): void {
    if (!this.config.enabled || !this.shouldLog(level)) {
      return;
    }

    const timestamp = new Date().toISOString();
    const prefix = this.config.prefix ? `${this.config.prefix} ` : '';
    const logMessage = `${prefix}[${level.toUpperCase()}] ${timestamp} - ${message}`;

    switch (level) {
      case LogLevel.DEBUG:
        console.debug(logMessage, data || '');
        break;
      case LogLevel.INFO:
        console.info(logMessage, data || '');
        break;
      case LogLevel.WARN:
        console.warn(logMessage, data || '');
        break;
      case LogLevel.ERROR:
        console.error(logMessage, data || '');
        break;
      default:
        console.log(logMessage, data || '');
        break;
    }
  }

  /**
   * Check if a log level should be logged based on the current configuration
   * @param level The log level to check
   * @returns True if the level should be logged, false otherwise
   */
  private shouldLog(level: LogLevel): boolean {
    const levels: LogLevel[] = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR];
    const currentLevelIndex = levels.indexOf(this.config.level);
    const messageLevelIndex = levels.indexOf(level);

    return messageLevelIndex >= currentLevelIndex;
  }

  /**
   * Update the logger configuration
   * @param config The new configuration
   */
  updateConfig(config: Partial<LoggerConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Enable or disable the logger
   * @param enabled Whether to enable the logger
   */
  setEnabled(enabled: boolean): void {
    this.updateConfig({ enabled });
  }

  /**
   * Set the log level
   * @param level The new log level
   */
  setLevel(level: LogLevel): void {
    this.updateConfig({ level });
  }
}

// Create a singleton logger instance
const logger = new Logger();

// Export the logger instance and LogLevel enum
export default logger;
export { logger };
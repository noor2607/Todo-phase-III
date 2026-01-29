'use client';

import { useState, useEffect } from 'react';
import ErrorHandler from '../utils/errorHandler';

interface ErrorDisplayProps {
  position?: 'top-right' | 'bottom-right' | 'top-left' | 'bottom-left';
}

const ErrorDisplay = ({ position = 'top-right' }: ErrorDisplayProps) => {
  const [errors, setErrors] = useState(ErrorHandler.getErrors());

  useEffect(() => {
    const unsubscribe = ErrorHandler.subscribe(setErrors);
    return unsubscribe;
  }, []);

  const getPositionClasses = () => {
    switch (position) {
      case 'top-left':
        return 'top-4 left-4';
      case 'top-right':
        return 'top-4 right-4';
      case 'bottom-left':
        return 'bottom-4 left-4';
      case 'bottom-right':
      default:
        return 'top-4 right-4';
    }
  };

  const getTypeClasses = (type: string) => {
    switch (type) {
      case 'error':
        return 'bg-red-100 border-red-400 text-red-700';
      case 'warning':
        return 'bg-yellow-100 border-yellow-400 text-yellow-700';
      case 'info':
        return 'bg-blue-100 border-blue-400 text-blue-700';
      default:
        return 'bg-gray-100 border-gray-400 text-gray-700';
    }
  };

  return (
    <div className={`fixed ${getPositionClasses()} z-50 space-y-2`}>
      {errors.map((error) => (
        <div
          key={error.id}
          className={`border px-4 py-3 rounded relative max-w-sm ${getTypeClasses(error.type)}`}
        >
          <span className="block sm:inline">{error.message}</span>
          <button
            onClick={() => ErrorHandler.remove(error.id)}
            className="absolute top-0 bottom-0 right-0 px-4 py-3"
          >
            <svg
              className="fill-current h-6 w-6 text-current"
              role="button"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
            >
              <title>Close</title>
              <path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z" />
            </svg>
          </button>
        </div>
      ))}
    </div>
  );
};

export default ErrorDisplay;
import { useState } from 'react';
import { taskService } from '../services/taskService';
import { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  onUpdate: (task: Task) => void;
}

const TaskCard = ({ task, onEdit, onDelete, onUpdate }: TaskCardProps) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handleToggleCompleted = async () => {
    setIsUpdating(true);
    try {
      const response = await taskService.toggleTaskCompletion(Number(task.id));
      onUpdate(response);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDeleteConfirm = async () => {
    setIsDeleting(true);
    try {
      const success = await taskService.deleteTask(task.id);
      if (success) {
        onDelete(String(task.id));
      }
    } catch (error: any) {
      console.error('Error deleting task:', error);

      // Determine error message based on error type
      let errorMessage = 'Failed to delete task. Please try again.';
      if (error.response?.status === 401) {
        errorMessage = 'Session expired. Please log in again.';
      } else if (error.response?.status === 403) {
        errorMessage = 'Access denied. Cannot delete this task.';
      } else if (error.response?.status === 404) {
        errorMessage = 'Task not found.';
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error. Please try again later.';
      }

      // Use error handler to show user-friendly message
      import('../utils/errorHandler').then(module => {
        module.default.notify(errorMessage, 'error');
      });
    } finally {
      setIsDeleting(false);
      setShowDeleteModal(false);
    }
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow duration-300 relative">
      <div className="flex justify-between items-start">
        <div className="flex items-start">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompleted}
            disabled={isUpdating}
            className="mt-1 h-5 w-5 text-primary-500 rounded focus:ring-primary-500"
          />
          <div className="ml-3">
            <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-2 text-gray-600 ${task.completed ? 'line-through' : ''}`}>
                {task.description}
              </p>
            )}
            <div className="mt-3 text-xs text-gray-500">
              Created: {new Date(task.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(task)}
            className="text-blue-500 hover:text-blue-700"
            title="Edit task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>

          <button
            onClick={handleDeleteClick}
            disabled={isDeleting}
            className={`${isDeleting ? 'text-gray-400' : 'text-red-500 hover:text-red-700'}`}
            title="Delete task"
          >
            {isDeleting ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 animate-spin" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Confirm Deletion</h3>
              <button
                onClick={handleDeleteCancel}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the task "{task.title}"? This action cannot be undone.
            </p>

            <div className="flex justify-end space-x-3">
              <button
                onClick={handleDeleteCancel}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-md transition duration-300"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteConfirm}
                disabled={isDeleting}
                className={`px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-medium rounded-md transition duration-300 ${
                  isDeleting ? 'opacity-70 cursor-not-allowed' : ''
                }`}
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskCard;
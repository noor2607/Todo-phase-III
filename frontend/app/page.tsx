'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../providers/AuthProvider';
import { taskService } from '../services/taskService';
import { Task } from '../types/task';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';
import Filters from '../components/Filters';
import Header from '../components/Header';
import Footer from '../components/Footer';

interface FilterOptions {
  status: 'all' | 'pending' | 'completed';
  sortBy: 'created_at' | 'title';
  sortOrder: 'asc' | 'desc';
}

export default function HomePage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filters, setFilters] = useState<FilterOptions>({
    status: 'all',
    sortBy: 'created_at',
    sortOrder: 'desc'
  });

  useEffect(() => {
    if (user && !authLoading) {
      loadTasks();
    }
  }, [user, authLoading]);

  useEffect(() => {
    // Apply filters when tasks or filters change
    let result = [...tasks];

    // Apply status filter
    if (filters.status !== 'all') {
      result = result.filter(task =>
        filters.status === 'completed' ? task.completed : !task.completed
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;
      if (filters.sortBy === 'title') {
        comparison = a.title.localeCompare(b.title);
      } else if (filters.sortBy === 'created_at') {
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
      }

      return filters.sortOrder === 'asc' ? comparison : -comparison;
    });

    setFilteredTasks(result);
  }, [tasks, filters]);

  const loadTasks = async () => {
    try {
      setTasksLoading(true);
      const tasksData = await taskService.getTasks();
      setTasks(tasksData || []);
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setTasksLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
    setShowTaskForm(false);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    setEditingTask(null);
  };

  const handleTaskDeleted = (deletedTaskId: string) => {
    const idAsNumber = Number(deletedTaskId);
    setTasks(tasks.filter(task => task.id !== idAsNumber));
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
    setShowTaskForm(false);
  };

  const handleFilterChange = (newFilters: FilterOptions) => {
    setFilters(newFilters);
  };

  const handleAddTaskClick = () => {
    if (!user) {
      // If user is not authenticated, redirect to sign in
      router.push('/signin');
      return;
    }
    setShowTaskForm(true);
  };

  // Show loading state while checking auth status
  if (authLoading) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex-grow flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Checking authentication status...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Show hero section to all users, and task section to authenticated users
  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="container mx-auto px-4 py-8 flex-grow">
        {/* Hero Section - Visible to all users */}
        <section className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 text-gray-800">Manage Your Tasks Effortlessly</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            A simple, secure, and intuitive todo application to help you stay organized and productive.
          </p>

          <div className="flex justify-center space-x-4">
            {!user && (
              <>
                <a
                  href="/signup"
                  className="bg-primary-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full text-lg transition duration-300"
                >
                  Get Started
                </a>
                <a
                  href="/signin"
                  className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-full text-lg transition duration-300"
                >
                  Sign In
                </a>
              </>
            )}
            {user && (
              <button
                onClick={handleAddTaskClick}
                className="bg-primary-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full text-lg transition duration-300"
              >
                Add New Task
              </button>
            )}
          </div>
        </section>

        {/* Features Section - Visible to all users */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Features That Make Life Easier</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md text-center">
              <div className="text-primary-500 text-4xl mb-4">✓</div>
              <h3 className="text-xl font-semibold mb-2">Simple Task Management</h3>
              <p className="text-gray-600">
                Easily create, update, and manage your tasks with our intuitive interface.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md text-center">
              <div className="text-primary-500 text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold mb-2">Secure & Private</h3>
              <p className="text-gray-600">
                Your data is protected with industry-standard security measures and user isolation.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md text-center">
              <div className="text-primary-500 text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">Fast & Responsive</h3>
              <p className="text-gray-600">
                Enjoy seamless performance across all your devices with our responsive design.
              </p>
            </div>
          </div>
        </section>

        {/* Task Management Section - Visible to authenticated users */}
        {user && (
          <section className="mb-12">
            <h2 className="text-3xl font-bold mb-4 text-gray-800">Your Tasks</h2>

            {tasksLoading ? (
              // Loading skeletons for task lists
              <div className="animate-pulse">
                {[...Array(3)].map((_, idx) => (
                  <div key={idx} className="bg-white shadow rounded-lg p-6 mb-4">
                    <div className="h-6 bg-gray-300 rounded w-3/4 mb-3"></div>
                    <div className="h-4 bg-gray-300 rounded w-full mb-2"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : (
              <>
                <div className="flex justify-between items-center mb-8">
                  <h3 className="text-xl font-semibold text-gray-700">
                    {filteredTasks.length} {filteredTasks.length === 1 ? 'Task' : 'Tasks'}
                  </h3>
                  <button
                    onClick={handleAddTaskClick}
                    className="bg-primary-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-md transition duration-300"
                  >
                    Add Task
                  </button>
                </div>

                <Filters onFilterChange={handleFilterChange} />

                {filteredTasks.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg shadow">
                    <h2 className="text-2xl font-semibold text-gray-600 mb-4">
                      {tasks.length === 0 ? 'No tasks yet' : 'No tasks match your filters'}
                    </h2>
                    {tasks.length === 0 && (
                      <>
                        <p className="text-gray-500 mb-6">Get started by creating your first task!</p>
                        <button
                          onClick={handleAddTaskClick}
                          className="bg-primary-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-md transition duration-300"
                        >
                          Create Your First Task
                        </button>
                      </>
                    )}
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredTasks.map(task => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        onEdit={handleEditTask}
                        onDelete={handleTaskDeleted}
                        onUpdate={handleTaskUpdated}
                      />
                    ))}
                  </div>
                )}
              </>
            )}
          </section>
        )}

        {/* Show message to non-authenticated users encouraging them to sign up */}
        {!user && !tasksLoading && (
          <section className="bg-gray-100 p-8 rounded-lg text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Ready to Manage Your Tasks?</h2>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              Sign up or sign in to create, manage, and track your tasks efficiently.
            </p>
            <div className="flex justify-center space-x-4">
              <a
                href="/signup"
                className="bg-primary-500 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-md transition duration-300"
              >
                Create Account
              </a>
              <a
                href="/signin"
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-6 rounded-md transition duration-300"
              >
                Sign In
              </a>
            </div>
          </section>
        )}
      </main>

      {/* Task Form Modal */}
      {showTaskForm && (
        <TaskForm
          task={editingTask}
          onClose={handleCancelEdit}
          onSuccess={editingTask ? handleTaskUpdated : handleTaskCreated}
        />
      )}

      <Footer />
    </div>
  );
}
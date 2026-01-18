// Task-related type definitions

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // ISO string format
  user_id: string;
  created_at: string; // ISO string format
  updated_at: string; // ISO string format
}

export interface CreateTaskData {
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // ISO string format
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // ISO string format
}
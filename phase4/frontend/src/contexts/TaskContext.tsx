'use client';

/**
 * TaskContext provides global task state management.
 * Handles fetching, updating, and refreshing tasks across the app.
 */

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { Task, getTasks, completeTaskDirect, deleteTaskDirect, updateTaskDirect } from '@/lib/api';

interface TaskContextType {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  refreshTasks: () => Promise<void>;
  completeTask: (taskId: string) => Promise<void>;
  deleteTask: (taskId: string) => Promise<void>;
  updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export function TaskProvider({ children }: { children: React.ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch all tasks from API
   */
  const refreshTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const fetchedTasks = await getTasks();
      setTasks(fetchedTasks);
    } catch (err: any) {
      console.error('Failed to fetch tasks:', err);
      setError(err.message || 'Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Complete a task (optimistic update)
   */
  const completeTask = useCallback(async (taskId: string) => {
    // Optimistic update
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              status: 'completed' as const,
              completed_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            }
          : task
      )
    );

    try {
      // Backend sync
      await completeTaskDirect(taskId);
      // Refresh to get accurate server state
      await refreshTasks();
    } catch (err: any) {
      console.error('Failed to complete task:', err);
      // Revert on error
      await refreshTasks();
      throw err;
    }
  }, [refreshTasks]);

  /**
   * Delete a task (optimistic update)
   */
  const deleteTask = useCallback(async (taskId: string) => {
    // Optimistic update
    setTasks((prev) => prev.filter((task) => task.id !== taskId));

    try {
      // Backend sync
      await deleteTaskDirect(taskId);
    } catch (err: any) {
      console.error('Failed to delete task:', err);
      // Revert on error
      await refreshTasks();
      throw err;
    }
  }, [refreshTasks]);

  /**
   * Update a task (optimistic update)
   */
  const updateTask = useCallback(async (taskId: string, updates: Partial<Task>) => {
    // Optimistic update
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              ...updates,
              updated_at: new Date().toISOString(),
            }
          : task
      )
    );

    try {
      // Backend sync
      await updateTaskDirect(taskId, updates);
      // Refresh to get accurate server state
      await refreshTasks();
    } catch (err: any) {
      console.error('Failed to update task:', err);
      // Revert on error
      await refreshTasks();
      throw err;
    }
  }, [refreshTasks]);

  // Initial load on mount
  useEffect(() => {
    refreshTasks();
  }, [refreshTasks]);

  // Polling fallback (every 10 seconds - reduced to minimize server load)
  useEffect(() => {
    const interval = setInterval(() => {
      refreshTasks();
    }, 10000);

    return () => clearInterval(interval);
  }, [refreshTasks]);

  const value: TaskContextType = {
    tasks,
    isLoading,
    error,
    refreshTasks,
    completeTask,
    deleteTask,
    updateTask,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
}

/**
 * Hook to access task context
 */
export function useTasks() {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTasks must be used within a TaskProvider');
  }
  return context;
}

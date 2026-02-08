'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';
import { useTaskStore } from '@/lib/store';
import type { Task } from '@/types/task';
import { formatDueDate, getPriorityColor, cn } from '@/lib/utils';
import { isPast, parseISO } from 'date-fns';

interface TaskCardProps {
  task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const updateTask = useTaskStore((state) => state.updateTask);
  const removeTask = useTaskStore((state) => state.removeTask);

  const handleToggleComplete = async () => {
    try {
      const newStatus = task.status === 'completed' ? 'pending' : 'completed';
      const updated = await apiClient.updateTask(task.id, {
        status: newStatus,
        version: task.version,
      });
      updateTask(updated);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setIsDeleting(true);
    try {
      await apiClient.deleteTask(task.id);
      removeTask(task.id);
    } catch (error) {
      console.error('Failed to delete task:', error);
      setIsDeleting(false);
    }
  };

  const isOverdue = task.due_date && isPast(parseISO(task.due_date)) && task.status === 'pending';

  return (
    <div
      className={cn(
        'bg-white rounded-lg shadow-sm border-2 p-4 hover:shadow-md transition-shadow',
        isOverdue ? 'border-red-300' : 'border-gray-200',
        task.status === 'completed' && 'opacity-75'
      )}
    >
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.status === 'completed'}
          onChange={handleToggleComplete}
          className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <h3
              className={cn(
                'text-lg font-semibold text-gray-900',
                task.status === 'completed' && 'line-through text-gray-500'
              )}
            >
              {task.title}
            </h3>

            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="text-gray-400 hover:text-red-600 transition-colors"
              title="Delete task"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>

          {task.description && (
            <p className="mt-1 text-sm text-gray-600 line-clamp-2">{task.description}</p>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span
              className={cn(
                'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
                getPriorityColor(task.priority)
              )}
            >
              {task.priority}
            </span>

            {task.due_date && (
              <span
                className={cn(
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  isOverdue ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                )}
              >
                {formatDueDate(task.due_date)}
              </span>
            )}

            {task.recurrence_pattern && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                <svg className="mr-1 h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                {task.recurrence_pattern.frequency}
              </span>
            )}

            {task.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                #{tag}
              </span>
            ))}
          </div>

          <div className="mt-2 text-xs text-gray-500">
            Created {new Date(task.created_at).toLocaleDateString()}
            {task.completed_at && (
              <> • Completed {new Date(task.completed_at).toLocaleDateString()}</>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

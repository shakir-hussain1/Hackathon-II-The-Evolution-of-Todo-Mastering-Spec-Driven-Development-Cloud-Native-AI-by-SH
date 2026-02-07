'use client';

/**
 * TaskRow component - Individual task row with actions.
 * Features: Status badge, hover effects, complete/delete actions, expandable description.
 */

import React, { useState, useEffect } from 'react';
import { Task } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';

interface TaskRowProps {
  task: Task;
  onComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
}

export default function TaskRow({ task, onComplete, onDelete }: TaskRowProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const [currentTime, setCurrentTime] = useState(Date.now());

  // Update time display every minute for accurate relative time
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(Date.now());
    }, 60000); // Update every 60 seconds

    return () => clearInterval(interval);
  }, []);

  const handleComplete = async () => {
    if (task.status === 'completed') return;

    try {
      setIsCompleting(true);
      await onComplete(task.id);
    } catch (err) {
      console.error('Failed to complete task:', err);
    } finally {
      setIsCompleting(false);
    }
  };

  const handleDelete = async () => {
    try {
      setIsDeleting(true);
      await onDelete(task.id);
    } catch (err) {
      console.error('Failed to delete task:', err);
      setIsDeleting(false);
    }
  };

  // Calculate relative time based on current time (updates every minute)
  // Using currentTime state to trigger recalculation
  const relativeTime = React.useMemo(() => {
    return formatDistanceToNow(new Date(task.created_at), {
      addSuffix: true,
      includeSeconds: false
    });
  }, [task.created_at, currentTime]);

  return (
    <tr className={`border-b border-slate-200 hover:bg-gradient-to-r hover:from-blue-50/30 hover:to-indigo-50/30 transition-all duration-200 ${isDeleting ? 'opacity-50' : ''} group`}>
      {/* Title */}
      <td className="px-6 py-5">
        <div className="flex flex-col">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-left font-semibold text-slate-900 hover:text-indigo-600 transition-colors group-hover:translate-x-1 transition-transform"
          >
            {task.title}
          </button>
          {isExpanded && task.description && (
            <p className="mt-2 text-sm text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 animate-fadeIn">
              {task.description}
            </p>
          )}
        </div>
      </td>

      {/* Status */}
      <td className="px-6 py-5">
        {task.status === 'pending' ? (
          <span className="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-amber-100 to-orange-100 text-amber-800 border-2 border-amber-200 shadow-sm">
            ⏳ Pending
          </span>
        ) : (
          <span className="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-emerald-100 to-green-100 text-emerald-800 border-2 border-emerald-200 shadow-sm">
            ✅ Completed
          </span>
        )}
      </td>

      {/* Created */}
      <td className="px-6 py-5 text-sm text-slate-600 font-medium">
        {relativeTime}
      </td>

      {/* Actions */}
      <td className="px-6 py-5">
        <div className="flex items-center gap-3">
          {task.status === 'pending' && (
            <button
              onClick={handleComplete}
              disabled={isCompleting}
              className="px-3 py-1.5 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold text-xs rounded-lg hover:from-emerald-600 hover:to-green-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
              title="Mark as complete"
            >
              {isCompleting ? (
                <span className="flex items-center space-x-1">
                  <svg className="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Wait...</span>
                </span>
              ) : (
                '✓ Complete'
              )}
            </button>
          )}
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-3 py-1.5 bg-gradient-to-r from-red-500 to-rose-600 text-white font-semibold text-xs rounded-lg hover:from-red-600 hover:to-rose-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Delete task"
          >
            {isDeleting ? (
              <span className="flex items-center space-x-1">
                <svg className="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Wait...</span>
              </span>
            ) : (
              '✕ Delete'
            )}
          </button>
        </div>
      </td>
    </tr>
  );
}

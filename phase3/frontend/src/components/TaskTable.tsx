'use client';

/**
 * TaskTable component - Modern table displaying tasks.
 * Features: Loading skeleton, empty state, responsive design.
 */

import React from 'react';
import { Task } from '@/lib/api';
import TaskRow from './TaskRow';

interface TaskTableProps {
  tasks: Task[];
  isLoading: boolean;
  onComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
}

export default function TaskTable({ tasks, isLoading, onComplete, onDelete }: TaskTableProps) {
  if (isLoading) {
    return (
      <div className="overflow-hidden rounded-2xl border-2 border-slate-200 bg-white shadow-lg">
        <div className="animate-pulse">
          <div className="border-b border-slate-200 bg-gradient-to-r from-slate-50 to-gray-50 px-6 py-4">
            <div className="h-4 bg-slate-300 rounded-lg w-1/4"></div>
          </div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="border-b border-slate-200 px-6 py-5">
              <div className="h-5 bg-slate-200 rounded-lg w-3/4 mb-3"></div>
              <div className="h-4 bg-slate-100 rounded-lg w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="overflow-hidden rounded-2xl border-2 border-slate-200 bg-white shadow-lg">
        <div className="px-6 py-16 text-center">
          <div className="w-24 h-24 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 flex items-center justify-center shadow-lg">
            <span className="text-5xl">📝</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-3">No tasks yet</h3>
          <p className="text-slate-600 max-w-sm mx-auto leading-relaxed">
            Use the chat to add your first task or start managing your todos!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border-2 border-slate-200 bg-white shadow-xl">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-gradient-to-r from-slate-50 to-gray-50">
          <tr>
            <th scope="col" className="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider">
              Task
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider">
              Status
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider">
              Created
            </th>
            <th scope="col" className="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {tasks.map((task) => (
            <TaskRow
              key={task.id}
              task={task}
              onComplete={onComplete}
              onDelete={onDelete}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

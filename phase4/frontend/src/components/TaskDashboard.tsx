'use client';

/**
 * TaskDashboard component - Main dashboard orchestrating all task components.
 * Features: Stats, filters, table with state management integration.
 */

import React, { useState, useMemo } from 'react';
import { useTasks } from '@/contexts/TaskContext';
import TaskStats from './TaskStats';
import TaskFilters from './TaskFilters';
import TaskTable from './TaskTable';

type FilterType = 'all' | 'pending' | 'completed';

export default function TaskDashboard() {
  const { tasks, isLoading, error, completeTask, deleteTask } = useTasks();
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');

  // Calculate stats
  const stats = useMemo(() => {
    const totalTasks = tasks.length;
    const pendingTasks = tasks.filter((t) => t.status === 'pending').length;
    const completedTasks = tasks.filter((t) => t.status === 'completed').length;

    return { totalTasks, pendingTasks, completedTasks };
  }, [tasks]);

  // Filter tasks based on active filter
  const filteredTasks = useMemo(() => {
    if (activeFilter === 'all') return tasks;
    return tasks.filter((task) => task.status === activeFilter);
  }, [tasks, activeFilter]);

  return (
    <div className="h-full flex flex-col bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/60 px-6 py-5 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg">
            <span className="text-xl">📊</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Task Dashboard
            </h2>
            <p className="text-sm text-slate-600 mt-0.5">Manage and track your todos</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-5 text-red-700 shadow-lg animate-fadeIn">
            <p className="font-bold flex items-center">
              <span className="mr-2">⚠️</span>
              Error loading tasks
            </p>
            <p className="text-sm mt-2">{error}</p>
          </div>
        )}

        {/* Stats */}
        <TaskStats
          totalTasks={stats.totalTasks}
          pendingTasks={stats.pendingTasks}
          completedTasks={stats.completedTasks}
        />

        {/* Filters */}
        <TaskFilters
          activeFilter={activeFilter}
          onFilterChange={setActiveFilter}
          counts={{
            all: stats.totalTasks,
            pending: stats.pendingTasks,
            completed: stats.completedTasks,
          }}
        />

        {/* Task Table */}
        <TaskTable
          tasks={filteredTasks}
          isLoading={isLoading}
          onComplete={completeTask}
          onDelete={deleteTask}
        />
      </div>
    </div>
  );
}

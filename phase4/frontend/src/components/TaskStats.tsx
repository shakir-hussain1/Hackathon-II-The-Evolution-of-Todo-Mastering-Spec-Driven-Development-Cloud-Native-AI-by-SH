'use client';

/**
 * TaskStats component - Colorful stat cards.
 * Features: Total tasks, pending count, completion rate with gradient icons.
 */

import React from 'react';

interface TaskStatsProps {
  totalTasks: number;
  pendingTasks: number;
  completedTasks: number;
}

export default function TaskStats({ totalTasks, pendingTasks, completedTasks }: TaskStatsProps) {
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const stats = [
    {
      label: 'Total Tasks',
      value: totalTasks,
      icon: '📋',
      gradient: 'from-blue-500 via-blue-600 to-indigo-600',
      bgGradient: 'from-blue-50 to-indigo-50',
      textColor: 'text-blue-700',
      ringColor: 'ring-blue-200',
    },
    {
      label: 'Pending',
      value: pendingTasks,
      icon: '⏳',
      gradient: 'from-amber-500 via-orange-500 to-amber-600',
      bgGradient: 'from-amber-50 to-orange-50',
      textColor: 'text-amber-700',
      ringColor: 'ring-amber-200',
    },
    {
      label: 'Completion Rate',
      value: `${completionRate}%`,
      icon: '🎯',
      gradient: 'from-emerald-500 via-green-500 to-emerald-600',
      bgGradient: 'from-emerald-50 to-green-50',
      textColor: 'text-emerald-700',
      ringColor: 'ring-emerald-200',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
      {stats.map((stat, index) => (
        <div
          key={index}
          className={`bg-gradient-to-br ${stat.bgGradient} rounded-2xl p-6 border-2 border-white shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 ring-2 ${stat.ringColor} ring-opacity-50`}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm font-semibold text-slate-600 mb-2 uppercase tracking-wide">{stat.label}</p>
              <p className={`text-4xl font-black ${stat.textColor} tracking-tight`}>{stat.value}</p>
            </div>
            <div className={`bg-gradient-to-br ${stat.gradient} rounded-2xl w-16 h-16 flex items-center justify-center shadow-xl transform transition-transform hover:scale-110 hover:rotate-6`}>
              <span className="text-3xl filter drop-shadow-lg">{stat.icon}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

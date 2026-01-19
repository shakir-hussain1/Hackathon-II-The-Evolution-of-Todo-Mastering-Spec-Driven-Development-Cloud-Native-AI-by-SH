'use client';

/**
 * TaskFilters component - Pill-style filter tabs.
 * Features: All/Pending/Completed filters with count badges.
 */

import React from 'react';

type FilterType = 'all' | 'pending' | 'completed';

interface TaskFiltersProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  counts: {
    all: number;
    pending: number;
    completed: number;
  };
}

export default function TaskFilters({ activeFilter, onFilterChange, counts }: TaskFiltersProps) {
  const filters: { type: FilterType; label: string; count: number }[] = [
    { type: 'all', label: 'All Tasks', count: counts.all },
    { type: 'pending', label: 'Pending', count: counts.pending },
    { type: 'completed', label: 'Completed', count: counts.completed },
  ];

  return (
    <div className="flex flex-wrap gap-3">
      {filters.map((filter) => (
        <button
          key={filter.type}
          onClick={() => onFilterChange(filter.type)}
          className={`
            px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 transform hover:-translate-y-0.5
            ${
              activeFilter === filter.type
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50 scale-105'
                : 'bg-white text-slate-700 hover:bg-slate-50 shadow-md hover:shadow-lg border-2 border-slate-200'
            }
          `}
        >
          {filter.label}
          <span
            className={`
              ml-2.5 px-2.5 py-1 rounded-lg text-xs font-black
              ${
                activeFilter === filter.type
                  ? 'bg-indigo-500 text-white'
                  : 'bg-slate-200 text-slate-700'
              }
            `}
          >
            {filter.count}
          </span>
        </button>
      ))}
    </div>
  );
}

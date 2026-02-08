'use client';

import { useTaskStore } from '@/lib/store';

const sortOptions = [
  { value: 'created_desc', label: 'Newest First' },
  { value: 'created_asc', label: 'Oldest First' },
  { value: 'due_asc', label: 'Due Date (Soon)' },
  { value: 'due_desc', label: 'Due Date (Later)' },
  { value: 'priority_desc', label: 'Priority (High)' },
  { value: 'priority_asc', label: 'Priority (Low)' },
  { value: 'title_asc', label: 'Title (A-Z)' },
  { value: 'title_desc', label: 'Title (Z-A)' },
];

export default function TaskSort() {
  const filters = useTaskStore((state) => state.filters);
  const setFilters = useTaskStore((state) => state.setFilters);

  return (
    <div className="flex items-center gap-2">
      <label className="text-sm font-medium text-gray-700">Sort by:</label>
      <select
        value={filters.sort || 'created_desc'}
        onChange={(e) => setFilters({ ...filters, sort: e.target.value as typeof filters.sort })}
        className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
      >
        {sortOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

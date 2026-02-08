export interface RecurrencePattern {
  frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  days_of_week?: number[];
  day_of_month?: number;
  end_date?: string;
  occurrences_count?: number;
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed' | 'archived';
  priority: 'high' | 'medium' | 'low';
  due_date?: string;
  tags: string[];
  recurrence_pattern?: RecurrencePattern;
  next_occurrence?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
  version: number;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string;
  tags?: string[];
  recurrence_pattern?: RecurrencePattern;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed' | 'archived';
  priority?: 'high' | 'medium' | 'low';
  due_date?: string | null;
  tags?: string[];
  recurrence_pattern?: RecurrencePattern | null;
  version?: number;
}

export interface TaskListResponse {
  tasks: Task[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
    has_more: boolean;
  };
}

export interface TaskFilters {
  status?: 'pending' | 'completed' | 'archived';
  priority?: 'high' | 'medium' | 'low';
  tags?: string;
  due_before?: string;
  due_after?: string;
  sort?: 'created_asc' | 'created_desc' | 'due_asc' | 'due_desc' | 'priority_asc' | 'priority_desc' | 'title_asc' | 'title_desc';
  limit?: number;
  offset?: number;
}

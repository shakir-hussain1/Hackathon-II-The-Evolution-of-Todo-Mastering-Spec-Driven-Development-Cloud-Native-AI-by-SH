/**
 * T026: TaskForm Component - Simplified Clean Design
 */

"use client";

import { useState } from "react";
import { api } from "@/utils/api-client";
import type { TaskCreateRequest, ItemResponse, Task } from "@/utils/types";

interface TaskFormProps {
  userId: string;
  onTaskCreated?: (task: Task) => void;
}

export function TaskForm({ userId, onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);

    if (!title.trim()) {
      setError("Task title is required");
      setLoading(false);
      return;
    }

    try {
      const taskData: TaskCreateRequest = {
        title: title.trim(),
        ...(description.trim() && { description: description.trim() }),
      };

      const response = await api.post<ItemResponse<Task>>(
        `/api/users/${userId}/tasks`,
        taskData
      );

      const newTask = response.data as Task;

      // Reset form
      setTitle("");
      setDescription("");
      setSuccess(true);

      // Call callback
      onTaskCreated?.(newTask);

      // Clear success after 3s
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Success */}
      {success && (
        <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm">
          ✓ Task created successfully!
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
          {error}
        </div>
      )}

      {/* Title */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          maxLength={255}
          required
          disabled={loading}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all disabled:bg-gray-100"
        />
        <p className="text-xs text-gray-500 mt-1">{title.length}/255</p>
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description <span className="text-gray-400 text-xs">(optional)</span>
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details..."
          maxLength={10000}
          rows={3}
          disabled={loading}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all disabled:bg-gray-100 resize-none"
        />
        <p className="text-xs text-gray-500 mt-1">{description.length}/10,000</p>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="w-full px-4 py-2.5 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-medium rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
      >
        {loading ? "Creating..." : "Create Task"}
      </button>
    </form>
  );
}

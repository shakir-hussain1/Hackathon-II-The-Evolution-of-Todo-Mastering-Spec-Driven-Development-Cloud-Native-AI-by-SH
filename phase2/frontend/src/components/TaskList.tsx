/**
 * T025: TaskList Component - Clean Table Design
 */

"use client";

import { useEffect, useState } from "react";
import { api } from "@/utils/api-client";
import type { Task, ItemResponse } from "@/utils/types";
import { ConfirmDialog } from "./ConfirmDialog";
import { TaskEditModal } from "./TaskEditModal";

interface TaskListProps {
  userId: string;
  refreshKey?: number;
  onTaskDeleted?: () => void;
  onTaskToggled?: () => void;
  onTasksLoaded?: (tasks: Task[]) => void;
  onTaskUpdated?: () => void;
}

export function TaskList({
  userId,
  refreshKey = 0,
  onTaskDeleted,
  onTaskToggled,
  onTasksLoaded,
  onTaskUpdated,
}: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [togglingTaskId, setTogglingTaskId] = useState<number | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [filter, setFilter] = useState<"all" | "incomplete" | "complete">("all");
  const [sortBy, setSortBy] = useState<"recent" | "oldest">("recent");

  // Edit modal state
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showEditModal, setShowEditModal] = useState<boolean>(false);

  // Delete confirmation state
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<boolean>(false);

  useEffect(() => {
    fetchTasks();
  }, [userId, refreshKey]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.get<{ data: Task[] }>(
        `/api/users/${userId}/tasks`
      );

      const loadedTasks = response.data || [];
      setTasks(loadedTasks);

      // Notify parent component of loaded tasks
      if (onTasksLoaded) {
        onTasksLoaded(loadedTasks);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTask = async (taskId: number) => {
    try {
      setTogglingTaskId(taskId);

      const response = await api.patch<ItemResponse<Task>>(
        `/api/users/${userId}/tasks/${taskId}/complete`
      );

      setTasks(
        tasks.map((t) =>
          t.id === taskId ? (response.data as Task) : t
        )
      );

      onTaskToggled?.();
    } catch (err: any) {
      setError(err.message || "Failed to toggle task");
    } finally {
      setTogglingTaskId(null);
    }
  };

  const handleDeleteClick = (task: Task) => {
    setTaskToDelete(task);
    setShowDeleteConfirm(true);
  };

  const handleDeleteConfirm = async () => {
    if (!taskToDelete) return;

    try {
      setDeletingTaskId(taskToDelete.id);

      await api.delete(`/api/users/${userId}/tasks/${taskToDelete.id}`);

      setTasks(tasks.filter((t) => t.id !== taskToDelete.id));

      // Notify parent
      onTaskDeleted?.();

      // Close dialog
      setShowDeleteConfirm(false);
      setTaskToDelete(null);
    } catch (err: any) {
      setError(err.message || "Failed to delete task");
    } finally {
      setDeletingTaskId(null);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteConfirm(false);
    setTaskToDelete(null);
  };

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
    setShowEditModal(true);
  };

  const handleEditClose = () => {
    setShowEditModal(false);
    setEditingTask(null);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    // Update task in local state
    setTasks(tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)));

    // Notify parent
    onTaskUpdated?.();

    // Notify parent with updated tasks list
    if (onTasksLoaded) {
      const updatedTasks = tasks.map((t) =>
        t.id === updatedTask.id ? updatedTask : t
      );
      onTasksLoaded(updatedTasks);
    }
  };

  // Filter and sort
  const filteredTasks = tasks
    .filter((task) => {
      if (filter === "all") return true;
      return task.status === filter;
    })
    .sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      return sortBy === "recent" ? dateB - dateA : dateA - dateB;
    });

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
        <p className="mt-4 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center justify-between pb-4 border-b border-gray-200">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter("all")}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
              filter === "all"
                ? "bg-blue-500 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter("incomplete")}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
              filter === "incomplete"
                ? "bg-amber-500 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter("complete")}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
              filter === "complete"
                ? "bg-green-500 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            Completed
          </button>
        </div>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as any)}
          className="px-4 py-2 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-700 focus:ring-2 focus:ring-blue-500 outline-none"
        >
          <option value="recent">Newest First</option>
          <option value="oldest">Oldest First</option>
        </select>
      </div>

      {/* Task Table */}
      {filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p className="text-gray-600 font-medium">No tasks found</p>
          <p className="text-gray-500 text-sm mt-1">Create your first task to get started</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Status</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 text-sm">Task</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700 text-sm hidden md:table-cell">Date</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700 text-sm">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredTasks.map((task) => (
                <tr key={task.id} className="hover:bg-gray-50 transition-colors">
                  {/* Status */}
                  <td className="py-3 px-4">
                    <button
                      onClick={() => handleToggleTask(task.id)}
                      disabled={togglingTaskId === task.id}
                      className="group relative"
                    >
                      {task.status === "complete" ? (
                        <div className="w-6 h-6 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center text-white shadow-sm group-hover:scale-110 transition-transform">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                      ) : (
                        <div className="w-6 h-6 border-2 border-gray-300 rounded-full group-hover:border-blue-500 group-hover:scale-110 transition-all"></div>
                      )}
                    </button>
                  </td>

                  {/* Task Info */}
                  <td className="py-3 px-4">
                    <div>
                      <p className={`font-medium ${task.status === "complete" ? "line-through text-gray-400" : "text-gray-900"}`}>
                        {task.title}
                      </p>
                      {task.description && (
                        <p className="text-sm text-gray-500 mt-1 line-clamp-2">{task.description}</p>
                      )}
                    </div>
                  </td>

                  {/* Date */}
                  <td className="py-3 px-4 text-sm text-gray-500 hidden md:table-cell">
                    {new Date(task.created_at).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    })}
                  </td>

                  {/* Actions */}
                  <td className="py-3 px-4 text-right">
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => handleEditClick(task)}
                        className="px-3 py-1.5 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-lg transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteClick(task)}
                        disabled={deletingTaskId === task.id}
                        className="px-3 py-1.5 bg-red-500 hover:bg-red-600 text-white text-sm rounded-lg transition-colors disabled:opacity-50"
                      >
                        {deletingTaskId === task.id ? "..." : "Delete"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Task Count */}
      {filteredTasks.length > 0 && (
        <p className="text-sm text-gray-500 text-center pt-4 border-t border-gray-200">
          Showing {filteredTasks.length} task{filteredTasks.length !== 1 ? "s" : ""}
        </p>
      )}

      {/* Edit Modal */}
      <TaskEditModal
        open={showEditModal}
        task={editingTask}
        userId={userId}
        onClose={handleEditClose}
        onTaskUpdated={handleTaskUpdated}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        open={showDeleteConfirm}
        title="Delete Task?"
        message={
          taskToDelete ? (
            <div>
              <p className="mb-2">Are you sure you want to delete this task?</p>
              <p className="font-semibold text-gray-900">"{taskToDelete.title}"</p>
              <p className="mt-2 text-sm">This action cannot be undone.</p>
            </div>
          ) : (
            "Are you sure you want to delete this task?"
          )
        }
        confirmText="Delete"
        cancelText="Cancel"
        confirmButtonClass="bg-red-500 hover:bg-red-600"
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
        loading={deletingTaskId !== null}
      />
    </div>
  );
}

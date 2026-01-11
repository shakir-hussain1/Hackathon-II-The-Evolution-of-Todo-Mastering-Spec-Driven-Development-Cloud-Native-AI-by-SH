/**
 * Unified Dashboard - All Features in One Form/Table
 *
 * Everything integrated: Add, Edit, List, Complete, Delete
 * No modals, no separate components, everything in one view
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AuthGuard } from "@/components/AuthGuard";
import { api } from "@/utils/api-client";
import { clearToken, getUserIdFromToken } from "@/utils/auth";
import type { Task } from "@/utils/types";

function UnifiedDashboard() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Create new task state
  const [newTitle, setNewTitle] = useState<string>("");
  const [newDescription, setNewDescription] = useState<string>("");
  const [creating, setCreating] = useState<boolean>(false);

  // Edit task state
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState<string>("");
  const [editDescription, setEditDescription] = useState<string>("");

  // UI state
  const [filter, setFilter] = useState<"all" | "incomplete" | "complete">("all");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function init() {
      try {
        const id = await getUserIdFromToken();
        if (!id) {
          router.push("/auth/login");
          return;
        }
        setUserId(id);
        await fetchTasks(id);
      } catch (error) {
        console.error("Error:", error);
        router.push("/auth/login");
      }
    }
    init();
  }, [router]);

  const fetchTasks = async (uid: string) => {
    try {
      setLoading(true);
      const response = await api.get<{ data: Task[] }>(`/api/users/${uid}/tasks`);
      setTasks(response.data || []);
    } catch (err: any) {
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId || !newTitle.trim()) return;

    try {
      setCreating(true);
      setError(null);

      const response = await api.post(`/api/users/${userId}/tasks`, {
        title: newTitle.trim(),
        description: newDescription.trim() || null,
      });

      setTasks([response.data, ...tasks]);
      setNewTitle("");
      setNewDescription("");
      setSuccess("Task created!");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to create task");
    } finally {
      setCreating(false);
    }
  };

  const handleEditClick = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  const handleSaveEdit = async (taskId: number) => {
    if (!userId || !editTitle.trim()) return;

    try {
      const response = await api.put(`/api/users/${userId}/tasks/${taskId}`, {
        title: editTitle.trim(),
        description: editDescription.trim() || null,
      });

      setTasks(tasks.map((t) => (t.id === taskId ? response.data : t)));
      setEditingId(null);
      setSuccess("Task updated!");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to update task");
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditTitle("");
    setEditDescription("");
  };

  const handleToggleComplete = async (task: Task) => {
    if (!userId) return;

    try {
      const response = await api.patch(`/api/users/${userId}/tasks/${task.id}/complete`);
      setTasks(tasks.map((t) => (t.id === task.id ? response.data : t)));
    } catch (err: any) {
      setError(err.message || "Failed to toggle task");
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!userId) return;
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      await api.delete(`/api/users/${userId}/tasks/${taskId}`);
      setTasks(tasks.filter((t) => t.id !== taskId));
      setSuccess("Task deleted!");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to delete task");
    }
  };

  const handleLogout = async () => {
    await clearToken();
    router.push("/auth/login");
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === "all") return true;
    return task.status === filter;
  });

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === "incomplete").length,
    completed: tasks.filter((t) => t.status === "complete").length,
  };

  if (loading && !userId) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-4 mx-auto"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Professional Header */}
      <div className="bg-white border-b-2 border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center shadow-md">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Task Manager</h1>
                <p className="text-sm text-gray-600">Organize your work efficiently</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-medium shadow-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Clean Professional Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Total Tasks Card */}
          <div className="bg-white border-2 border-blue-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">TOTAL</span>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-1">{stats.total}</p>
            <p className="text-sm text-gray-600">All tasks</p>
          </div>

          {/* Pending Card */}
          <div className="bg-white border-2 border-orange-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg className="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span className="text-xs font-semibold text-orange-600 bg-orange-50 px-3 py-1 rounded-full">PENDING</span>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-1">{stats.pending}</p>
            <p className="text-sm text-gray-600">In progress</p>
          </div>

          {/* Completed Card */}
          <div className="bg-white border-2 border-green-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg className="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span className="text-xs font-semibold text-green-600 bg-green-50 px-3 py-1 rounded-full">DONE</span>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-1">{stats.completed}</p>
            <p className="text-sm text-gray-600">Completed</p>
          </div>
        </div>

        {/* Clean Messages */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-600 text-red-900 px-5 py-4 rounded-lg mb-4 flex items-center gap-3 shadow-sm">
            <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">{error}</span>
          </div>
        )}
        {success && (
          <div className="bg-green-50 border-l-4 border-green-600 text-green-900 px-5 py-4 rounded-lg mb-4 flex items-center gap-3 shadow-sm">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">{success}</span>
          </div>
        )}

        {/* Clean Task Form */}
        <div className="bg-white border-2 border-gray-200 rounded-lg shadow-sm overflow-hidden">
          {/* Add New Task Form */}
          <form onSubmit={handleCreateTask} className="bg-blue-50 border-b-2 border-blue-200 p-5">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <h2 className="text-lg font-bold text-gray-900">Add New Task</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <input
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="Task title *"
                maxLength={255}
                required
                disabled={creating}
                className="px-4 py-2.5 bg-white border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none placeholder-gray-500 text-gray-900 font-medium transition-colors"
              />
              <input
                type="text"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Description (optional)"
                maxLength={500}
                disabled={creating}
                className="px-4 py-2.5 bg-white border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none placeholder-gray-500 text-gray-900 font-medium transition-colors"
              />
              <button
                type="submit"
                disabled={creating || !newTitle.trim()}
                className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
              >
                {creating ? "Adding..." : "Add Task"}
              </button>
            </div>
          </form>

          {/* Filter Buttons */}
          <div className="p-4 border-b-2 border-gray-200 flex flex-wrap items-center gap-2 bg-gray-50">
            <span className="text-sm font-semibold text-gray-700 mr-2">Filter:</span>
            <button
              onClick={() => setFilter("all")}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                filter === "all"
                  ? "bg-blue-600 text-white shadow-sm"
                  : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-300"
              }`}
            >
              All ({stats.total})
            </button>
            <button
              onClick={() => setFilter("incomplete")}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                filter === "incomplete"
                  ? "bg-orange-600 text-white shadow-sm"
                  : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-300"
              }`}
            >
              Pending ({stats.pending})
            </button>
            <button
              onClick={() => setFilter("complete")}
              className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                filter === "complete"
                  ? "bg-green-600 text-white shadow-sm"
                  : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-300"
              }`}
            >
              Completed ({stats.completed})
            </button>
          </div>

          {/* Task List/Table */}
          <div className="divide-y divide-gray-200">
            {loading ? (
              <div className="p-10 text-center">
                <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-gray-600 font-medium">Loading tasks...</p>
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="p-12 text-center">
                <div className="w-20 h-20 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p className="text-lg font-semibold text-gray-800 mb-1">No tasks found</p>
                <p className="text-sm text-gray-500">
                  {filter === "all" ? "Create your first task above to get started" : `No ${filter} tasks yet`}
                </p>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className="p-4 hover:bg-gray-50 transition-colors"
                >
                  {editingId === task.id ? (
                    /* Clean Edit Mode */
                    <div className="bg-blue-50 border-2 border-blue-300 p-4 rounded-lg grid grid-cols-1 md:grid-cols-3 gap-3">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        placeholder="Task title *"
                        maxLength={255}
                        className="px-4 py-2.5 bg-white border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-gray-900 font-medium"
                      />
                      <input
                        type="text"
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        placeholder="Description (optional)"
                        maxLength={500}
                        className="px-4 py-2.5 bg-white border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-gray-900 font-medium"
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleSaveEdit(task.id)}
                          className="flex-1 px-4 py-2.5 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors"
                        >
                          Save
                        </button>
                        <button
                          onClick={handleCancelEdit}
                          className="px-4 py-2.5 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded-lg font-semibold transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    /* Clean Display Mode */
                    <div className="flex items-start gap-4">
                      {/* Clean Checkbox */}
                      <button
                        onClick={() => handleToggleComplete(task)}
                        className="mt-1 flex-shrink-0"
                      >
                        {task.status === "complete" ? (
                          <div className="w-7 h-7 bg-green-600 rounded-lg flex items-center justify-center shadow-sm hover:bg-green-700 transition-colors">
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                        ) : (
                          <div className="w-7 h-7 border-2 border-gray-300 rounded-lg hover:border-gray-400 hover:bg-gray-50 transition-colors"></div>
                        )}
                      </button>

                      {/* Task Content */}
                      <div className="flex-1 min-w-0">
                        <h3
                          className={`text-base font-semibold ${
                            task.status === "complete"
                              ? "line-through text-gray-400"
                              : "text-gray-900"
                          }`}
                        >
                          {task.title}
                        </h3>
                        {task.description && (
                          <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                        )}
                        <div className="flex items-center gap-3 mt-2">
                          <span className={`px-3 py-1 rounded-lg text-xs font-semibold ${
                            task.status === "complete"
                              ? "bg-green-100 text-green-700"
                              : "bg-orange-100 text-orange-700"
                          }`}>
                            {task.status === "complete" ? "Completed" : "Pending"}
                          </span>
                          <span className="text-xs text-gray-500 flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {new Date(task.created_at).toLocaleDateString("en-US", {
                              month: "short",
                              day: "numeric",
                              year: "numeric",
                            })}
                          </span>
                        </div>
                      </div>

                      {/* Clean Action Buttons */}
                      <div className="flex gap-2 flex-shrink-0">
                        <button
                          onClick={() => handleEditClick(task)}
                          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition-colors shadow-sm"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(task.id)}
                          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-semibold transition-colors shadow-sm"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <AuthGuard>
      <UnifiedDashboard />
    </AuthGuard>
  );
}

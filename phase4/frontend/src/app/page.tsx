'use client';

/**
 * Main page - Entry point for authenticated users.
 * Renders split layout with chat and dashboard.
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TodoChat from '@/components/TodoChat';
import TaskDashboard from '@/components/TaskDashboard';
import SplitLayout from '@/components/SplitLayout';
import { TaskProvider } from '@/contexts/TaskContext';
import { isAuthenticated, logout } from '@/lib/api';

export default function HomePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const authenticated = isAuthenticated();
      setIsAuth(authenticated);

      if (!authenticated) {
        // Redirect to login if not authenticated
        router.push('/login');
      } else {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = () => {
    // Clear authentication and chat history
    logout();
    // Clear conversation history and user tracking
    localStorage.removeItem('conversation_id');
    localStorage.removeItem('current_user_id');
    router.push('/login');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuth) {
    return null; // Will redirect to login
  }

  return (
    <TaskProvider>
      <div className="relative h-screen bg-gradient-to-br from-slate-100 via-gray-100 to-slate-200">
        {/* Logout button */}
        <button
          onClick={handleLogout}
          className="absolute top-5 right-6 z-50 bg-gradient-to-r from-red-500 to-rose-600 text-white px-5 py-2.5 rounded-xl hover:from-red-600 hover:to-rose-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-semibold flex items-center space-x-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Logout</span>
        </button>

        {/* Split Layout with Chat and Dashboard */}
        <SplitLayout
          chatComponent={<TodoChat />}
          dashboardComponent={<TaskDashboard />}
        />
      </div>
    </TaskProvider>
  );
}

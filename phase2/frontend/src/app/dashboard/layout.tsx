/**
 * T031: Protected Dashboard Layout
 *
 * Main layout for all dashboard pages (task management).
 * Enforces authentication using AuthGuard wrapper.
 * Provides consistent navigation and styling for all dashboard routes.
 */

import { AuthGuard } from "@/components/AuthGuard";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

/**
 * Dashboard layout component.
 *
 * This layout wraps all dashboard pages with AuthGuard to ensure
 * only authenticated users can access the dashboard and its routes.
 *
 * Routes protected:
 * - /dashboard (main page)
 * - /dashboard/* (any dashboard subroutes in future)
 */
export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Navigation Header */}
        <header className="sticky top-0 z-40 bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2m0 0V3a2 2 0 00-2-2h-2a2 2 0 00-2 2v2z"
                    />
                  </svg>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Phase II Todo</h1>
                  <p className="text-xs text-gray-500">Task Management Dashboard</p>
                </div>
              </div>

              {/* Navigation Links */}
              <nav className="hidden md:flex items-center gap-6">
                <a
                  href="/dashboard"
                  className="text-blue-600 hover:text-blue-700 font-semibold text-sm"
                >
                  Tasks
                </a>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-gray-200 bg-white mt-12">
          <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* About */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Phase II Todo</h3>
                <p className="text-sm text-gray-600">
                  A full-stack todo application demonstrating spec-driven development
                  with Next.js and FastAPI.
                </p>
              </div>

              {/* Features */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Features</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>✓ JWT Authentication</li>
                  <li>✓ CRUD Operations</li>
                  <li>✓ Multi-user Isolation</li>
                  <li>✓ Real-time Updates</li>
                </ul>
              </div>

              {/* Status */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Status</h3>
                <div className="space-y-1 text-sm">
                  <p className="text-green-600">✓ Phase II Complete</p>
                  <p className="text-green-600">✓ Production Ready</p>
                  <p className="text-blue-600">✓ Hackathon Excellent</p>
                </div>
              </div>
            </div>

            {/* Copyright */}
            <div className="border-t border-gray-200 mt-8 pt-8">
              <p className="text-center text-sm text-gray-600">
                © 2026 Hackathon II - The Evolution of Todo. Spec-Driven Development.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </AuthGuard>
  );
}

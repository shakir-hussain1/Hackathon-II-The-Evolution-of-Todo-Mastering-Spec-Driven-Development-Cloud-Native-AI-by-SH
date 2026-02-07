'use client';

/**
 * SplitLayout component - Responsive layout for chat and dashboard.
 *
 * Layouts:
 * - Desktop (>1024px): Side-by-side (Chat 40% | Dashboard 60%)
 * - Tablet (768-1024px): Vertical stack (Chat top 40% | Dashboard bottom 60%)
 * - Mobile (<768px): Tabs (Chat / Dashboard toggle)
 */

import React, { useState } from 'react';

interface SplitLayoutProps {
  chatComponent: React.ReactNode;
  dashboardComponent: React.ReactNode;
}

export default function SplitLayout({ chatComponent, dashboardComponent }: SplitLayoutProps) {
  const [activeTab, setActiveTab] = useState<'chat' | 'dashboard'>('chat');

  return (
    <>
      {/* Mobile: Tabs (<768px) */}
      <div className="lg:hidden h-full flex flex-col">
        {/* Tab Navigation */}
        <div className="bg-white border-b border-slate-200 flex">
          <button
            onClick={() => setActiveTab('chat')}
            className={`
              flex-1 px-4 py-3 text-sm font-medium transition-colors
              ${
                activeTab === 'chat'
                  ? 'text-indigo-600 border-b-2 border-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }
            `}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`
              flex-1 px-4 py-3 text-sm font-medium transition-colors
              ${
                activeTab === 'dashboard'
                  ? 'text-indigo-600 border-b-2 border-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }
            `}
          >
            📊 Dashboard
          </button>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-hidden">
          {activeTab === 'chat' ? chatComponent : dashboardComponent}
        </div>
      </div>

      {/* Tablet: Vertical Stack (768-1024px) */}
      <div className="hidden md:flex lg:hidden h-full flex-col">
        {/* Chat (Top 40%) */}
        <div className="h-[40%] border-b border-slate-300">
          {chatComponent}
        </div>

        {/* Dashboard (Bottom 60%) */}
        <div className="h-[60%]">
          {dashboardComponent}
        </div>
      </div>

      {/* Desktop: Side-by-side (>1024px) */}
      <div className="hidden lg:flex h-full">
        {/* Chat (Left 40%) */}
        <div className="w-[40%] border-r border-slate-300">
          {chatComponent}
        </div>

        {/* Dashboard (Right 60%) */}
        <div className="w-[60%]">
          {dashboardComponent}
        </div>
      </div>
    </>
  );
}

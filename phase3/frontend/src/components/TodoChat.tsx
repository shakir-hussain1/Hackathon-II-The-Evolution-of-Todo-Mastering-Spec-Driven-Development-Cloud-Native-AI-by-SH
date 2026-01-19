'use client';

/**
 * TodoChat component - Main chat interface for task management.
 * Integrates OpenAI ChatKit for UI and backend API for functionality.
 */

import { useState, useEffect, useRef } from 'react';
import { sendMessage, loadConversationHistory, ApiError } from '@/lib/api';
import { useTasks } from '@/contexts/TaskContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at?: string;
}

export default function TodoChat() {
  const { refreshTasks } = useTasks();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history on mount (if exists)
  useEffect(() => {
    const loadHistory = async () => {
      const savedConversationId = localStorage.getItem('conversation_id');
      const savedUserId = localStorage.getItem('current_user_id');

      // Get current user ID from token
      const token = localStorage.getItem('auth_token');
      let currentUserId = null;
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          currentUserId = payload.sub;
        } catch (error) {
          console.error('Failed to decode token:', error);
        }
      }

      // Clear conversation if user changed or no user
      if (!currentUserId || savedUserId !== currentUserId) {
        localStorage.removeItem('conversation_id');
        localStorage.setItem('current_user_id', currentUserId || '');
        return;
      }

      // Load conversation history
      if (savedConversationId) {
        try {
          setIsLoading(true);
          const history = await loadConversationHistory(savedConversationId);
          setMessages(history.messages);
          setConversationId(history.conversation_id);
        } catch (error) {
          console.error('Failed to load conversation history:', error);
          // If loading fails, start fresh
          localStorage.removeItem('conversation_id');
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadHistory();
  }, []);

  // Handle message send
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError(null);

    // Optimistic UI update - add user message immediately
    const tempUserMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMessage]);
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await sendMessage(userMessage, conversationId || undefined);

      // Save conversation ID for persistence
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
        localStorage.setItem('conversation_id', response.conversation_id);
      }

      // Update messages with real IDs and add assistant response
      setMessages((prev) => {
        const withoutTemp = prev.filter((msg) => msg.id !== tempUserMessage.id);
        return [
          ...withoutTemp,
          {
            id: tempUserMessage.id, // Keep temp ID for user message
            role: 'user',
            content: userMessage,
            created_at: new Date().toISOString(),
          },
          {
            id: response.message_id,
            role: 'assistant',
            content: response.response,
            created_at: new Date().toISOString(),
          },
        ];
      });

      // Refresh dashboard after successful message
      refreshTasks();
    } catch (error) {
      console.error('Failed to send message:', error);

      // Remove optimistic user message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== tempUserMessage.id));

      // Display user-friendly error
      if (error instanceof ApiError) {
        setError(error.message);

        // If authentication error, prompt to refresh
        if (error.status === 401) {
          setTimeout(() => {
            window.location.href = '/login';
          }, 2000);
        }
      } else {
        setError('Failed to send message. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  // Handle Enter key (with Shift+Enter for new line)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e as any);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/60 px-6 py-5 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg">
            <span className="text-xl">✨</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              AI Todo Assistant
            </h1>
            <p className="text-sm text-slate-600 mt-0.5">
              Manage your tasks naturally through conversation
            </p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl shadow-indigo-500/30 animate-pulse">
                <span className="text-4xl">💬</span>
              </div>
              <h2 className="text-2xl font-bold text-slate-900 mb-3">
                Welcome to your AI Todo Assistant!
              </h2>
              <p className="text-slate-600 mb-6 leading-relaxed">
                I can help you manage your tasks through natural conversation. Try saying:
              </p>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 shadow-lg border border-slate-200/60">
                <ul className="text-sm text-slate-700 space-y-3 text-left">
                  <li className="flex items-start space-x-3">
                    <span className="text-indigo-500 font-bold">•</span>
                    <span>"Add buy groceries to my list"</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-purple-500 font-bold">•</span>
                    <span>"Show me my tasks"</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-pink-500 font-bold">•</span>
                    <span>"Mark the first task as complete"</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-blue-500 font-bold">•</span>
                    <span>"Update my report task"</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
          >
            <div
              className={`max-w-[75%] rounded-2xl px-5 py-3.5 shadow-md transition-all hover:shadow-lg ${
                message.role === 'user'
                  ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white'
                  : 'bg-white text-slate-900 border border-slate-200/60'
              }`}
            >
              <p className="whitespace-pre-wrap break-words leading-relaxed">{message.content}</p>
              {message.created_at && (
                <p
                  className={`text-xs mt-2 ${
                    message.role === 'user' ? 'text-indigo-200' : 'text-slate-500'
                  }`}
                >
                  {new Date(message.created_at).toLocaleTimeString()}
                </p>
              )}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start animate-fadeIn">
            <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-2xl px-5 py-4 shadow-lg">
              <div className="flex items-center space-x-3">
                <div className="flex space-x-1.5">
                  <div className="w-2.5 h-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full animate-bounce"></div>
                  <div className="w-2.5 h-2.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2.5 h-2.5 bg-gradient-to-r from-pink-500 to-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-sm text-slate-700 font-medium">Assistant is thinking...</span>
              </div>
            </div>
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="flex justify-center animate-fadeIn">
            <div className="bg-red-50 border-2 border-red-200 text-red-800 rounded-2xl px-5 py-4 max-w-md shadow-lg">
              <p className="text-sm font-bold flex items-center">
                <span className="mr-2">⚠️</span>
                Error
              </p>
              <p className="text-sm mt-1.5">{error}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Container */}
      <div className="bg-white/80 backdrop-blur-sm border-t border-slate-200/60 px-6 py-5 shadow-lg">
        <form onSubmit={handleSendMessage} className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (e.g., 'Add buy groceries')"
              disabled={isLoading}
              className="w-full border-2 border-slate-300 rounded-xl px-5 py-3.5 pr-12 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-slate-100 disabled:cursor-not-allowed transition-all shadow-sm hover:shadow-md placeholder-slate-400"
            />
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
          </div>
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-7 py-3.5 rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:from-slate-300 disabled:to-slate-400 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 active:translate-y-0"
          >
            {isLoading ? (
              <span className="flex items-center space-x-2">
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Sending</span>
              </span>
            ) : (
              <span className="flex items-center space-x-2">
                <span>Send</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </span>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

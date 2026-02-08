'use client';

import { useEffect } from 'react';
import { useConnectionStore } from '@/lib/store';
import { getWebSocketClient } from '@/lib/websocket';

export default function ConnectionStatus() {
  const status = useConnectionStore((state) => state.status);
  const setStatus = useConnectionStore((state) => state.setStatus);

  useEffect(() => {
    const ws = getWebSocketClient();
    const cleanup = ws.onConnectionStatus(setStatus);

    return () => {
      cleanup();
    };
  }, [setStatus]);

  const statusConfig = {
    connected: {
      color: 'bg-green-500',
      text: 'Connected',
      pulse: false,
    },
    disconnected: {
      color: 'bg-red-500',
      text: 'Disconnected',
      pulse: false,
    },
    reconnecting: {
      color: 'bg-yellow-500',
      text: 'Reconnecting...',
      pulse: true,
    },
  };

  const config = statusConfig[status];

  return (
    <div className="flex items-center gap-2 text-sm">
      <div className="relative">
        <div className={`w-3 h-3 rounded-full ${config.color}`} />
        {config.pulse && (
          <div className={`absolute inset-0 w-3 h-3 rounded-full ${config.color} animate-ping opacity-75`} />
        )}
      </div>
      <span className="text-gray-600">{config.text}</span>
    </div>
  );
}

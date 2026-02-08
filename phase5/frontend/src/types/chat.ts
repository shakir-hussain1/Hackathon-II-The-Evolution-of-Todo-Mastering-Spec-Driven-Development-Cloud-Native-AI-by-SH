export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  actions?: ChatAction[];
}

export interface ChatAction {
  type: 'task_created' | 'task_updated' | 'task_deleted' | 'search_performed';
  task_id?: string;
  details?: Record<string, unknown>;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  actions?: ChatAction[];
  conversation_id: string;
}

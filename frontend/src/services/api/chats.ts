import { request } from './client'

export type Message = { id: number; role: 'user' | 'assistant'; content: string; created_at: string }
export type Recommendation = { vehicle_id: string; vehicle_name: string; fit_summary: string; advantages: string[]; considerations: string[]; price_summary: string; specifications: Record<string, string | number | null>; match_reasons: string[] }
export type Chat = { id: number; title: string | null; created_at: string; updated_at: string }
export type ChatDetail = Chat & { messages: Message[]; preferences: Record<string, unknown> | null }
export type ChatResponse = { conversation_id: number; user_message: Message; assistant_message: Message; recommendations: Recommendation[]; follow_up_required: boolean; available_actions: string[]; disclaimer: string }

export const chatsApi = {
  list: () => request<{ items: Chat[] }>('/api/chats'),
  create: (title?: string) => request<Chat>('/api/chats', { method: 'POST', body: JSON.stringify({ title }) }),
  detail: (id: number) => request<ChatDetail>(`/api/chats/${id}`),
  send: (id: number, content: string) => request<ChatResponse>(`/api/chats/${id}/messages`, { method: 'POST', body: JSON.stringify({ content }) }),
  remove: (id: number) => request<void>(`/api/chats/${id}`, { method: 'DELETE' }),
}

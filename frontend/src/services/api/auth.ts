import { request } from './client'

export type User = { id: number; name: string; email: string; created_at: string }
export type Credentials = { email: string; password: string }

export const authApi = {
  me: () => request<User>('/api/auth/me'),
  register: (payload: { name: string; email: string; password: string; password_confirmation: string }) => request<User>('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload: Credentials) => request<User>('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request<void>('/api/auth/logout', { method: 'POST' }),
}

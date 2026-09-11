export type ApiError = { error?: { code?: string; message?: string; fields?: Record<string, string> } }

export class RequestError extends Error {
  code?: string
  fields?: Record<string, string>

  constructor(message: string, payload?: ApiError) {
    super(message)
    this.code = payload?.error?.code
    this.fields = payload?.error?.fields
  }
}

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
  })
  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as ApiError
    throw new RequestError(payload.error?.message ?? 'Something went wrong. Please try again.', payload)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

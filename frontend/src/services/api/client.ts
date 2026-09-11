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

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(path, {
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

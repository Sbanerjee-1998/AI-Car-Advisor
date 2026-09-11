import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { App } from '../src/app/App'

vi.mock('../src/services/api/auth', () => ({
  authApi: { me: vi.fn().mockRejectedValue(new Error('signed out')), login: vi.fn(), register: vi.fn(), logout: vi.fn() },
}))

describe('auth entry', () => {
  it('renders the sign-in workspace when no session exists', async () => {
    render(<App />)
    expect(await screen.findByText('Welcome back')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /enter workspace/i })).toBeInTheDocument()
  })
})

import { useState } from 'react'
import { ArrowRight, LockKeyhole, Sparkles } from 'lucide-react'
import { ErrorMessage } from '../../components/ErrorMessage'
import { authApi, type User } from '../../services/api/auth'
import { RequestError } from '../../services/api/client'

export function AuthPanel({ onAuthenticated }: { onAuthenticated: (user: User) => void }) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(event: React.FormEvent) {
    event.preventDefault()
    setError('')
    if (mode === 'register' && password !== confirmation) return setError('Passwords need to match.')
    setLoading(true)
    try {
      const user = mode === 'login' ? await authApi.login({ email, password }) : await authApi.register({ name, email, password, password_confirmation: confirmation })
      onAuthenticated(user)
    } catch (caught) {
      setError(caught instanceof RequestError ? caught.message : 'We could not sign you in.')
    } finally {
      setLoading(false)
    }
  }

  return <main className="auth-page">
    <section className="auth-intro">
      <div className="eyebrow"><Sparkles size={14} /> Grounded car discovery</div>
      <h1>Find the car that fits your real life.</h1>
      <p>Tell us how you drive. Get a short, explainable list from a curated Indian vehicle catalog.</p>
      <div className="signal-row"><span>30 curated cars</span><span>Private conversations</span><span>Useful trade-offs</span></div>
    </section>
    <section className="auth-card">
      <div className="auth-card-header"><div className="icon-tile"><LockKeyhole size={18} /></div><div><p className="section-kicker">Your garage brief</p><h2>{mode === 'login' ? 'Welcome back' : 'Start with your needs'}</h2></div></div>
      <div className="mode-switch" role="tablist"><button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>Sign in</button><button className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>Create account</button></div>
      <form onSubmit={submit}>
        {mode === 'register' && <label>Name<input value={name} onChange={(event) => setName(event.target.value)} placeholder="Your name" required /></label>}
        <label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" required /></label>
        <label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="At least 8 characters" minLength={8} required /></label>
        {mode === 'register' && <label>Confirm password<input type="password" value={confirmation} onChange={(event) => setConfirmation(event.target.value)} placeholder="Repeat password" minLength={8} required /></label>}
        <ErrorMessage message={error} />
        <button className="primary-button" disabled={loading}>{loading ? 'Working...' : mode === 'login' ? 'Enter workspace' : 'Create my workspace'}<ArrowRight size={17} /></button>
      </form>
    </section>
  </main>
}

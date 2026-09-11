import { useEffect, useState } from 'react'
import { AuthPanel } from '../features/auth/AuthPanel'
import { Workspace } from '../features/chat/Workspace'
import { authApi, type User } from '../services/api/auth'

export function App() {
  const [user, setUser] = useState<User | null>(null)
  const [checking, setChecking] = useState(true)
  useEffect(() => { authApi.me().then(setUser).catch(() => setUser(null)).finally(() => setChecking(false)) }, [])
  if (checking) return <div className="boot-screen">Loading your garage brief...</div>
  return user ? <Workspace user={user} onLoggedOut={() => setUser(null)} /> : <AuthPanel onAuthenticated={setUser} />
}

import type { ReactNode } from 'react'

export function AsyncState({ loading, empty, children }: { loading?: boolean; empty?: boolean; children: ReactNode }) {
  if (loading) return <div className="state-panel" role="status">Loading your workspace...</div>
  if (empty) return <div className="state-panel">Nothing here yet.</div>
  return children
}

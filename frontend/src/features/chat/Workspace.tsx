import { useEffect, useState } from 'react'
import { CarFront, ChevronRight, LogOut, MessageSquarePlus, PanelLeftClose, PanelLeftOpen, Send, Settings2 } from 'lucide-react'
import { AsyncState } from '../../components/AsyncState'
import { ErrorMessage } from '../../components/ErrorMessage'
import { authApi, type User } from '../../services/api/auth'
import { RequestError } from '../../services/api/client'
import { chatsApi, type Chat, type ChatDetail, type ChatResponse } from '../../services/api/chats'
import { RecommendationList } from '../cars/RecommendationList'

export function Workspace({ user, onLoggedOut }: { user: User; onLoggedOut: () => void }) {
  const [chats, setChats] = useState<Chat[]>([])
  const [current, setCurrent] = useState<ChatDetail | null>(null)
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null)
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const [sidebar, setSidebar] = useState(true)

  useEffect(() => { void loadChats() }, [])

  async function loadChats() {
    setLoading(true)
    try {
      const result = await chatsApi.list()
      setChats(result.items)
      if (result.items[0]) await openChat(result.items[0].id)
    } catch (caught) { setError(caught instanceof RequestError ? caught.message : 'We could not load your workspace.') } finally { setLoading(false) }
  }

  async function openChat(id: number) {
    setLastResponse(null)
    setCurrent(await chatsApi.detail(id))
  }

  async function newChat() {
    const chat = await chatsApi.create()
    setChats((items) => [chat, ...items])
    setCurrent({ ...chat, messages: [], preferences: null })
    setLastResponse(null)
  }

  async function send(event: React.FormEvent) {
    event.preventDefault()
    const content = draft.trim()
    if (!content || !current || sending) return
    setSending(true); setError(''); setDraft('')
    try {
      const response = await chatsApi.send(current.id, content)
      setLastResponse(response)
      setCurrent((chat) => chat ? { ...chat, title: chat.title ?? content.slice(0, 60), messages: [...chat.messages, response.user_message, response.assistant_message], updated_at: response.assistant_message.created_at } : chat)
      setChats((items) => items.map((chat) => chat.id === current.id ? { ...chat, title: chat.title ?? content.slice(0, 60), updated_at: response.assistant_message.created_at } : chat))
    } catch (caught) { setDraft(content); setError(caught instanceof RequestError ? caught.message : 'Your message could not be sent.') } finally { setSending(false) }
  }

  async function logout() { await authApi.logout(); onLoggedOut() }
  const visibleMessages = current?.messages ?? []

  return <div className="app-shell">
    <aside className={`sidebar ${sidebar ? '' : 'collapsed'}`}><div className="brand"><div className="brand-mark"><CarFront size={20} /></div>{sidebar && <div><strong>Car Advisor</strong><span>grounded by design</span></div>}</div>{sidebar && <><button className="new-chat" onClick={() => void newChat()}><MessageSquarePlus size={16} /> New conversation</button><div className="sidebar-label">Recent conversations</div><nav>{chats.map((chat) => <button className={`chat-link ${current?.id === chat.id ? 'selected' : ''}`} key={chat.id} onClick={() => void openChat(chat.id)}><MessageSquarePlus size={15} /><span>{chat.title || 'Untitled conversation'}</span><ChevronRight size={14} /></button>)}</nav></>}<div className="sidebar-footer">{sidebar && <div className="profile"><div className="avatar">{user.name.slice(0, 1)}</div><div><strong>{user.name}</strong><span>{user.email}</span></div></div>}<button className="quiet-button" onClick={() => void logout()} aria-label="Sign out"><LogOut size={16} />{sidebar && 'Sign out'}</button></div></aside>
    <main className="workspace"><header className="workspace-header"><button className="icon-button" onClick={() => setSidebar((value) => !value)} aria-label="Toggle sidebar">{sidebar ? <PanelLeftClose size={19} /> : <PanelLeftOpen size={19} />}</button><div><p className="section-kicker">Personal vehicle studio</p><h1>{current?.title || 'What are you looking for?'}</h1></div><button className="icon-button" aria-label="Preferences"><Settings2 size={18} /></button></header><AsyncState loading={loading}><div className="chat-canvas"><div className="welcome-block"><span className="welcome-mark">✦</span><p className="section-kicker">A better starting point</p><h2>Make the brief human.</h2><p>Share your budget, daily distance, family size, and what you never want to compromise on. I will keep the shortlist focused.</p><div className="prompt-row"><button onClick={() => setDraft('I need a comfortable automatic SUV for my family under 15 lakh')}>Automatic SUV under 15 lakh</button><button onClick={() => setDraft('I drive 40 km daily and want an electric car')}>EV for a daily commute</button></div></div><div className="transcript">{visibleMessages.map((message) => <div className={`message ${message.role}`} key={message.id}><div className="message-label">{message.role === 'user' ? 'You' : 'Advisor'}</div><p>{message.content}</p></div>)}{sending && <div className="message assistant"><div className="message-label">Advisor</div><p className="thinking">Thinking through the trade-offs...</p></div>}</div>{lastResponse && <><RecommendationList recommendations={lastResponse.recommendations} /><p className="disclaimer">{lastResponse.disclaimer}</p></>}<ErrorMessage message={error} /><form className="composer" onSubmit={send}><textarea value={draft} onChange={(event) => setDraft(event.target.value)} placeholder="Describe the car you need..." rows={2} maxLength={4000} /><button className="send-button" disabled={sending || !draft.trim()} aria-label="Send message"><Send size={18} /></button></form></div></AsyncState></main>
  </div>
}

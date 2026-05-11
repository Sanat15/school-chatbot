import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './Chat.css'

const defaultProfile = {
  avatar: '🧑‍🎓',
  bio: 'Loves learning!',
  school: 'Sunrise Public School',
  gender: 'male',
}

export default function Chat({ auth, onLogout }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [profile, setProfile] = useState(() => {
    try {
      const saved = localStorage.getItem(`profile_${auth.username}`)
      return saved ? JSON.parse(saved) : defaultProfile
    } catch {
      return defaultProfile
    }
  })
  const [showProfile, setShowProfile] = useState(false)
  const [editProfile, setEditProfile] = useState(profile)
  const bottomRef = useRef()

  const greeting =
    auth.role === 'parent'
      ? `Hi ${auth.username} ${profile.gender === 'female' ? "Ma'am" : 'Sir'}! 👋`
      : `Hi ${auth.username}! 👋`

  useEffect(() => {
    setMessages([{
      role: 'bot',
      text: `${greeting} I'm your school assistant. Ask me about your timetable, marks, or assignments! 📚`,
    }])
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    const text = input.trim()
    if (!text || loading) return
    setMessages(prev => [...prev, { role: 'user', text }])
    setInput('')
    setLoading(true)
    try {
      const res = await axios.post(
        '/api/chat/query',
        { question: text },
        { headers: { Authorization: `Bearer ${auth.token}` } }
      )
      setMessages(prev => [...prev, { role: 'bot', text: res.data.response }])
    } catch (err) {
      if (err.response?.status === 401) {
        onLogout()
        return
      }
      const msg = err.response?.data?.detail || 'Sorry, something went wrong. Please try again.'
      setMessages(prev => [...prev, { role: 'bot', text: msg }])
    } finally {
      setLoading(false)
    }
  }

  const openEditModal = () => {
    setEditProfile(profile)
    setShowProfile(true)
  }

  const saveProfile = () => {
    setProfile(editProfile)
    localStorage.setItem(`profile_${auth.username}`, JSON.stringify(editProfile))
    setShowProfile(false)
  }

  return (
    <div className="chat-page">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-top">
          <div className="avatar">{profile.avatar}</div>
          <h2 className="greeting">{greeting}</h2>
          <span className={`role-badge ${auth.role}`}>
            {auth.role === 'student' ? '🎒 Student' : '👨‍👩‍👧 Parent'}
          </span>
          <div className="profile-info">
            <div className="info-row">🏫 {profile.school}</div>
            <div className="info-row">💬 {profile.bio}</div>
          </div>
          <button className="edit-btn" onClick={openEditModal}>✏️ Edit Profile</button>
        </div>
        <button className="logout-btn" onClick={onLogout}>🚪 Logout</button>
      </div>

      {/* Chat area */}
      <div className="chat-main">
        <div className="chat-header">
          <span className="bot-icon">🤖</span>
          <div>
            <div className="bot-name">School Assistant</div>
            <div className="bot-status"><span className="dot" />Online</div>
          </div>
        </div>

        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`bubble-wrap ${msg.role}`}>
              {msg.role === 'bot' && <span className="bubble-icon">🤖</span>}
              <div className={`bubble ${msg.role}`}>{msg.text}</div>
              {msg.role === 'user' && <span className="bubble-icon">{profile.avatar}</span>}
            </div>
          ))}
          {loading && (
            <div className="bubble-wrap bot">
              <span className="bubble-icon">🤖</span>
              <div className="bubble bot typing">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-input-bar">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about timetable, marks, assignments..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>
            Send 📤
          </button>
        </div>
      </div>

      {/* Profile modal */}
      {showProfile && (
        <div className="modal-overlay" onClick={() => setShowProfile(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>✏️ Edit Profile</h2>
            <label>Avatar (emoji)</label>
            <input
              value={editProfile.avatar}
              onChange={e => setEditProfile({ ...editProfile, avatar: e.target.value })}
            />
            <label>Bio</label>
            <input
              value={editProfile.bio}
              onChange={e => setEditProfile({ ...editProfile, bio: e.target.value })}
            />
            <label>School Name</label>
            <input
              value={editProfile.school}
              onChange={e => setEditProfile({ ...editProfile, school: e.target.value })}
            />
            {auth.role === 'parent' && (
              <>
                <label>Gender (for greeting)</label>
                <select
                  value={editProfile.gender}
                  onChange={e => setEditProfile({ ...editProfile, gender: e.target.value })}
                >
                  <option value="male">Sir</option>
                  <option value="female">Ma'am</option>
                </select>
              </>
            )}
            <div className="modal-btns">
              <button className="save-btn" onClick={saveProfile}>💾 Save</button>
              <button className="cancel-btn" onClick={() => setShowProfile(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

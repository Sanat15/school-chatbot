import { useState } from 'react'
import axios from 'axios'
import './Login.css'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async () => {
    if (!username.trim() || !password) {
      setError('Please enter your username and password')
      return
    }
    setLoading(true)
    setError('')
    try {
      const form = new URLSearchParams()
      form.append('username', username.trim())
      form.append('password', password)
      const res = await axios.post('/api/login', form)
      onLogin({ token: res.data.access_token, role: res.data.role, username: username.trim() })
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid username or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="doodles">
        <span>📐</span><span>✏️</span><span>📏</span><span>🔬</span>
        <span>📚</span><span>🎨</span><span>📖</span><span>🔭</span>
        <span>➕</span><span>🧮</span><span>📝</span><span>🖍️</span>
      </div>

      <div className="login-card">
        <div className="login-logo">🏫</div>
        <h1 className="login-title">School Assistant</h1>
        <p className="login-tagline">Your smart school buddy! 📚</p>

        <div className="login-form">
          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
              disabled={loading}
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
              disabled={loading}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="login-btn" onClick={handleLogin} disabled={loading}>
            {loading ? 'Logging in...' : 'Login 🚀'}
          </button>
        </div>

        <p className="login-footer">Sunrise Public School © 2026</p>
      </div>
    </div>
  )
}

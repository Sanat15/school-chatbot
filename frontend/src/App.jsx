import { useState } from 'react'
import Login from './pages/Login'
import Chat from './pages/Chat'

function App() {
  const [auth, setAuth] = useState(() => {
    try {
      const saved = sessionStorage.getItem('auth')
      return saved ? JSON.parse(saved) : null
    } catch {
      return null
    }
  })

  const handleLogin = (authData) => {
    sessionStorage.setItem('auth', JSON.stringify(authData))
    setAuth(authData)
  }

  const handleLogout = () => {
    sessionStorage.removeItem('auth')
    setAuth(null)
  }

  return auth
    ? <Chat auth={auth} onLogout={handleLogout} />
    : <Login onLogin={handleLogin} />
}

export default App

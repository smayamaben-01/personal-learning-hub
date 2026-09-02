import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'

function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-white">
        Home page — placeholder
      </h1>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  )
}

export default App
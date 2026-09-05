import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import DsaTracker from './pages/DsaTracker'
import CompanyTracker from './pages/CompanyTracker'
import Notes from './pages/Notes'
import Profile from './pages/Profile'
import PasswordChange from './pages/PasswordChange'
import Goals from './pages/Goals'

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
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Dashboard />} />
      <Route path="/dsa" element={<DsaTracker />} />
      <Route path="/companies" element={<CompanyTracker />} />
      <Route path="/notes" element={<Notes />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/profile/password" element={<PasswordChange />} />
      <Route path="/goals" element={<Goals />} />
    </Routes>
  )
}

export default App
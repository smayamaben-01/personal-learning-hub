import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  PieChart, Pie, Cell, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { api } from '../api/client'
import { Link } from 'react-router-dom'

const COLORS = ['#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe', '#e0e7ff']

function Card({ title, children }) {
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
      <h2 className="mb-4 text-sm font-semibold text-slate-600 dark:text-slate-300">{title}</h2>
      {children}
    </div>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await api.get('/dashboard/stats')
        setStats(res.data)
      } catch (err) {
        setError(err.message || 'Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [])

  async function handleLogout() {
    try {
      await api.post('/auth/logout', {})
    } finally {
      navigate('/login')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <nav className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-4">
        <span className="text-lg font-semibold text-slate-900 dark:text-white">Personal Learning Hub</span>
        <div className="flex flex-wrap items-center gap-4">
            <Link to="/dsa" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            DSA Tracker
            </Link>
            <Link to="/companies" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            Companies
            </Link>
            <Link to="/notes" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            Notes
            </Link>
            <Link to="/goals" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            Goals
            </Link>
            <Link to="/profile" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
            Profile
            </Link>
        <button
          onClick={handleLogout}
          className="rounded-lg bg-slate-100 dark:bg-slate-800 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
        >
          Logout
        </button>
        </div>
      </nav>

      <main className="mx-auto max-w-6xl px-4 py-8">
        {loading && <p className="text-slate-500 dark:text-slate-400">Loading dashboard…</p>}
        {error && <p className="text-red-600 dark:text-red-400">{error}</p>}

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card title="Total Questions Solved">
              <p className="text-5xl font-bold text-indigo-600 dark:text-indigo-400">
                {stats.total_questions_solved}
              </p>
            </Card>

            <Card title="DSA Topics by Status">
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={stats.topics_by_status}
                    dataKey="count"
                    nameKey="status"
                    outerRadius={80}
                    label
                  >
                    {stats.topics_by_status.map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            <Card title="Company Application Funnel">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart
                  data={[
                    { stage: 'Applied', count: stats.company_funnel.applied },
                    { stage: 'OA', count: stats.company_funnel.oa },
                    { stage: 'Interview', count: stats.company_funnel.interview },
                    { stage: 'Selected', count: stats.company_funnel.selected },
                    { stage: 'Rejected', count: stats.company_funnel.rejected },
                  ]}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="stage" fontSize={12} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card title="Notes Per Week">
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={stats.notes_per_week}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week_number" fontSize={12} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Line type="monotone" dataKey="notes_count" stroke="#6366f1" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </Card>

            <Card title="Topics Ranked by Questions Solved">
              <ul className="space-y-2">
                {stats.topics_ranked.map((t) => (
                  <li
                    key={t.topic_name}
                    className="flex items-center justify-between rounded-lg bg-slate-50 dark:bg-slate-800 px-3 py-2"
                  >
                    <span className="text-sm text-slate-700 dark:text-slate-200">{t.topic_name}</span>
                    <span className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
                      {t.questions_solved}
                    </span>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        )}
      </main>
    </div>
  )
}
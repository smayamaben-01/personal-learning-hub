// Goals.jsx
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export default function Goals() {
  const [goals, setGoals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [description, setDescription] = useState('')
  const [targetCount, setTargetCount] = useState('')
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    fetchGoals()
  }, [])

  async function fetchGoals() {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/goals')
      setGoals(res.data)
    } catch (err) {
      setError(err.message || 'Failed to load goals')
    } finally {
      setLoading(false)
    }
  }

  async function handleAddGoal(e) {
    e.preventDefault()
    if (!description.trim() || !targetCount) return
    setAdding(true)
    setError('')
    try {
      const res = await api.post('/goals', {
        description: description.trim(),
        target_count: Number(targetCount),
      })
      setGoals((prev) => [...prev, res.data])
      setDescription('')
      setTargetCount('')
    } catch (err) {
      setError(err.message || 'Failed to add goal')
    } finally {
      setAdding(false)
    }
  }

  async function handleIncrement(goal) {
    const newCount = goal.current_count + 1
    try {
      const res = await api.put(`/goals/${goal.id}`, { current_count: newCount })
      setGoals((prev) => prev.map((g) => (g.id === goal.id ? res.data : g)))
    } catch (err) {
      setError(err.message || 'Failed to update goal')
    }
  }

  async function handleDelete(goalId) {
    try {
      await api.delete(`/goals/${goalId}`)
      setGoals((prev) => prev.filter((g) => g.id !== goalId))
    } catch (err) {
      setError(err.message || 'Failed to delete goal')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <nav className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-4">
        <span className="text-lg font-semibold text-slate-900 dark:text-white">Personal Learning Hub</span>
        <Link
          to="/"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
        >
          ← Dashboard
        </Link>
      </nav>

      <main className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="mb-6 text-2xl font-semibold text-slate-900 dark:text-white">This Week's Goals</h1>

        <form onSubmit={handleAddGoal} className="mb-6 flex flex-wrap gap-3">
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Goal description (e.g. Solve 10 DSA problems)"
            maxLength={255}
            className="flex-1 min-w-[200px] rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          />
          <input
            type="number"
            min="1"
            value={targetCount}
            onChange={(e) => setTargetCount(e.target.value)}
            placeholder="Target"
            className="w-24 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          />
          <button
            type="submit"
            disabled={adding}
            className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:opacity-60 dark:bg-indigo-500 dark:hover:bg-indigo-400"
          >
            {adding ? 'Adding…' : 'Add'}
          </button>
        </form>

        {error && (
          <p className="mb-4 rounded-xl border border-red-200 dark:border-red-900/60 bg-red-50 dark:bg-red-950/50 px-3.5 py-2.5 text-sm text-red-700 dark:text-red-400">
            {error}
          </p>
        )}

        {loading ? (
          <p className="text-slate-500 dark:text-slate-400">Loading…</p>
        ) : goals.length === 0 ? (
          <p className="text-slate-500 dark:text-slate-400">No goals for this week yet — add one above.</p>
        ) : (
          <ul className="space-y-3">
            {goals.map((goal) => {
              const pct = Math.min(100, Math.round((goal.current_count / goal.target_count) * 100))
              const done = goal.current_count >= goal.target_count
              return (
                <li
                  key={goal.id}
                  className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm"
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <span className="font-medium text-slate-900 dark:text-white">{goal.description}</span>

                    <div className="flex items-center gap-3">
                      <span className="text-sm text-slate-500 dark:text-slate-400">
                        {goal.current_count} / {goal.target_count}
                      </span>
                      <button
                        onClick={() => handleIncrement(goal)}
                        disabled={done}
                        className="rounded-lg bg-indigo-50 dark:bg-indigo-900/40 px-3 py-1.5 text-sm font-medium text-indigo-600 dark:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-900/70 disabled:opacity-50"
                      >
                        +1
                      </button>
                      <button
                        onClick={() => handleDelete(goal.id)}
                        className="text-sm font-medium text-red-600 hover:text-red-500 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Delete
                      </button>
                    </div>
                  </div>

                  <div className="mt-3 h-2 w-full rounded-full bg-slate-100 dark:bg-slate-800">
                    <div
                      className={`h-2 rounded-full ${done ? 'bg-emerald-500' : 'bg-indigo-500'}`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </li>
              )
            })}
          </ul>
        )}
      </main>
    </div>
  )
}
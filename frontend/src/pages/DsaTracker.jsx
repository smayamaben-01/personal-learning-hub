import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

const STATUSES = ['Not Started', 'In Progress', 'Completed']

const STATUS_STYLES = {
  'Not Started': 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300',
  'In Progress': 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  'Completed': 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
}

export default function DsaTracker() {
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newTopicName, setNewTopicName] = useState('')
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    fetchTopics()
  }, [])

  async function fetchTopics() {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/dsa-topics')
      setTopics(res.data)
    } catch (err) {
      setError(err.message || 'Failed to load topics')
    } finally {
      setLoading(false)
    }
  }

  async function handleAddTopic(e) {
    e.preventDefault()
    if (!newTopicName.trim()) return
    setAdding(true)
    setError('')
    try {
      const res = await api.post('/dsa-topics', { topic_name: newTopicName.trim() })
      setTopics((prev) => [...prev, res.data])
      setNewTopicName('')
    } catch (err) {
      setError(err.message || 'Failed to add topic')
    } finally {
      setAdding(false)
    }
  }

  async function handleStatusChange(topic, newStatus) {
    try {
      const res = await api.put(`/dsa-topics/${topic.id}`, {
        status: newStatus,
        questions_solved: topic.questions_solved,
      })
      setTopics((prev) => prev.map((t) => (t.id === topic.id ? res.data : t)))
    } catch (err) {
      setError(err.message || 'Failed to update topic')
    }
  }

  async function handleQuestionsChange(topic, newCount) {
    try {
      const res = await api.put(`/dsa-topics/${topic.id}`, {
        status: topic.status,
        questions_solved: newCount,
      })
      setTopics((prev) => prev.map((t) => (t.id === topic.id ? res.data : t)))
    } catch (err) {
      setError(err.message || 'Failed to update topic')
    }
  }

  async function handleDelete(topicId) {
    try {
      await api.delete(`/dsa-topics/${topicId}`)
      setTopics((prev) => prev.filter((t) => t.id !== topicId))
    } catch (err) {
      setError(err.message || 'Failed to delete topic')
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
        <h1 className="mb-6 text-2xl font-semibold text-slate-900 dark:text-white">DSA Tracker</h1>

        <form onSubmit={handleAddTopic} className="mb-6 flex gap-3">
          <input
            type="text"
            value={newTopicName}
            onChange={(e) => setNewTopicName(e.target.value)}
            placeholder="Add a new topic (e.g. Graphs)"
            className="flex-1 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
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
        ) : topics.length === 0 ? (
          <p className="text-slate-500 dark:text-slate-400">No topics yet — add one above.</p>
        ) : (
          <ul className="space-y-3">
            {topics.map((topic) => (
              <li
                key={topic.id}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="font-medium text-slate-900 dark:text-white">{topic.topic_name}</span>

                  <div className="flex flex-wrap items-center gap-3">
                    <select
                      value={topic.status}
                      onChange={(e) => handleStatusChange(topic, e.target.value)}
                      className={`rounded-lg border-none px-3 py-1.5 text-sm font-medium outline-none ${STATUS_STYLES[topic.status]}`}
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>

                    <input
                      type="number"
                      min="0"
                      value={topic.questions_solved}
                      onChange={(e) => handleQuestionsChange(topic, Number(e.target.value))}
                      className="w-20 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-2.5 py-1.5 text-sm text-slate-900 dark:text-slate-100 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
                    />

                    <button
                      onClick={() => handleDelete(topic.id)}
                      className="text-sm font-medium text-red-600 hover:text-red-500 dark:text-red-400 dark:hover:text-red-300"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  )
}
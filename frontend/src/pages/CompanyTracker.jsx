import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

const STATUSES = ['Applied', 'OA', 'Interview', 'Rejected', 'Selected']

const STATUS_STYLES = {
  'Applied': 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300',
  'OA': 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  'Interview': 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  'Rejected': 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300',
  'Selected': 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
}

export default function CompanyTracker() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newCompanyName, setNewCompanyName] = useState('')
  const [newStatus, setNewStatus] = useState('Applied')
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    fetchCompanies()
  }, [])

  async function fetchCompanies() {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/companies')
      setCompanies(res.data)
    } catch (err) {
      setError(err.message || 'Failed to load companies')
    } finally {
      setLoading(false)
    }
  }

  async function handleAddCompany(e) {
    e.preventDefault()
    if (!newCompanyName.trim()) return
    setAdding(true)
    setError('')
    try {
      const res = await api.post('/companies', {
        company_name: newCompanyName.trim(),
        status: newStatus,
      })
      setCompanies((prev) => [...prev, res.data])
      setNewCompanyName('')
      setNewStatus('Applied')
    } catch (err) {
      setError(err.message || 'Failed to add company')
    } finally {
      setAdding(false)
    }
  }

  async function handleStatusChange(company, status) {
    try {
      const res = await api.put(`/companies/${company.id}`, { status })
      setCompanies((prev) => prev.map((c) => (c.id === company.id ? res.data : c)))
    } catch (err) {
      setError(err.message || 'Failed to update company')
    }
  }

  async function handleDelete(companyId) {
    try {
      await api.delete(`/companies/${companyId}`)
      setCompanies((prev) => prev.filter((c) => c.id !== companyId))
    } catch (err) {
      setError(err.message || 'Failed to delete company')
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
        <h1 className="mb-6 text-2xl font-semibold text-slate-900 dark:text-white">Company Tracker</h1>

        <form onSubmit={handleAddCompany} className="mb-6 flex flex-wrap gap-3">
          <input
            type="text"
            value={newCompanyName}
            onChange={(e) => setNewCompanyName(e.target.value)}
            placeholder="Company name (e.g. Google)"
            className="flex-1 min-w-[200px] rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          />
          <select
            value={newStatus}
            onChange={(e) => setNewStatus(e.target.value)}
            className="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          >
            {STATUSES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
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
        ) : companies.length === 0 ? (
          <p className="text-slate-500 dark:text-slate-400">No companies yet — add one above.</p>
        ) : (
          <ul className="space-y-3">
            {companies.map((company) => (
              <li
                key={company.id}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="font-medium text-slate-900 dark:text-white">{company.company_name}</span>

                  <div className="flex flex-wrap items-center gap-3">
                    <select
                      value={company.status}
                      onChange={(e) => handleStatusChange(company, e.target.value)}
                      className={`rounded-lg border-none px-3 py-1.5 text-sm font-medium outline-none ${STATUS_STYLES[company.status]}`}
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>

                    <button
                      onClick={() => handleDelete(company.id)}
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
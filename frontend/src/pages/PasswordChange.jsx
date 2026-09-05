// PasswordChange.jsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export default function PasswordChange() {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (newPassword !== confirmPassword) {
      setError('New password and confirmation do not match.')
      return
    }

    setSaving(true)
    try {
      await api.put('/profile/password', {
        current_password: currentPassword,
        new_password: newPassword,
      })
      setSuccess('Password updated successfully.')
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <nav className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-4">
        <span className="text-lg font-semibold text-slate-900 dark:text-white">Personal Learning Hub</span>
        <Link
          to="/profile"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
        >
          ← Profile
        </Link>
      </nav>

      <div className="max-w-lg mx-auto mt-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h1 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Change Password</h1>

        {error && (
          <p className="mb-4 text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
        {success && (
          <p className="mb-4 text-sm text-green-600 dark:text-green-400">{success}</p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Current Password
            </label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              New Password
            </label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              minLength={8}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Confirm New Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              minLength={8}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
              required
            />
          </div>

          <button
            type="submit"
            disabled={saving}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded"
          >
            {saving ? 'Updating...' : 'Update Password'}
          </button>
        </form>
      </div>
    </div>
  )
}
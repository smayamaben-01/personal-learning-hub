import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export default function Profile() {
  const [profile, setProfile] = useState({ full_name: '', email: '', bio: '' })
  const [username, setUsername] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    async function fetchProfile() {
      try {
        const res = await api.get('/profile')
        const { full_name, email, bio, username } = res.data
        setProfile({
            full_name: full_name || '',
            email: email || '',
            bio: bio || '',
        })
        setUsername(username)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchProfile()
  }, [])

  function handleChange(e) {
    setProfile({ ...profile, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const res = await api.put('/profile', profile)
      setProfile({
        full_name: res.data.full_name,
        email: res.data.email,
        bio: res.data.bio,
      })
      setSuccess('Profile updated.')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <p className="text-gray-500 dark:text-gray-400">Loading profile...</p>

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

      <div className="max-w-lg mx-auto mt-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h1 className="text-xl font-semibold mb-4 text-gray-900 dark:text-gray-100">Profile</h1>

        <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
          Username: <span className="font-medium">{username}</span>
        </p>

        {error && (
          <p className="mb-4 text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
        {success && (
          <p className="mb-4 text-sm text-green-600 dark:text-green-400">{success}</p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Full Name
            </label>
            <input
              type="text"
              name="full_name"
              value={profile.full_name || ''}
              onChange={handleChange}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={profile.email || ''}
              onChange={handleChange}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Bio
            </label>
            <textarea
              name="bio"
              value={profile.bio || ''}
              onChange={handleChange}
              rows={4}
              maxLength={300}
              className="mt-1 w-full rounded border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 px-3 py-2"
            />
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded"
            >
              {saving ? 'Saving...' : 'Save'}
            </button>

            <Link
              to="/profile/password"
              className="px-4 py-2 rounded border border-gray-300 dark:border-gray-600 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition"
            >
              Change Password
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
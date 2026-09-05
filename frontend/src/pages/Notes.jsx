import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export default function Notes() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [newTitle, setNewTitle] = useState('')
  const [newContent, setNewContent] = useState('')
  const [adding, setAdding] = useState(false)

  const [editingId, setEditingId] = useState(null)
  const [editTitle, setEditTitle] = useState('')
  const [editContent, setEditContent] = useState('')

  useEffect(() => {
    fetchNotes()
  }, [])

  async function fetchNotes() {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/notes')
      setNotes(res.data)
    } catch (err) {
      setError(err.message || 'Failed to load notes')
    } finally {
      setLoading(false)
    }
  }

  async function handleAddNote(e) {
    e.preventDefault()
    if (!newTitle.trim()) return
    setAdding(true)
    setError('')
    try {
      const res = await api.post('/notes', { title: newTitle.trim(), content: newContent })
      setNotes((prev) => [res.data, ...prev])
      setNewTitle('')
      setNewContent('')
    } catch (err) {
      setError(err.message || 'Failed to add note')
    } finally {
      setAdding(false)
    }
  }

  function startEdit(note) {
    setEditingId(note.id)
    setEditTitle(note.title)
    setEditContent(note.content)
  }

  function cancelEdit() {
    setEditingId(null)
    setEditTitle('')
    setEditContent('')
  }

  async function handleSaveEdit(noteId) {
    if (!editTitle.trim()) return
    try {
      const res = await api.put(`/notes/${noteId}`, { title: editTitle.trim(), content: editContent })
      setNotes((prev) => prev.map((n) => (n.id === noteId ? res.data : n)))
      cancelEdit()
    } catch (err) {
      setError(err.message || 'Failed to update note')
    }
  }

  async function handleDelete(noteId) {
    try {
      await api.delete(`/notes/${noteId}`)
      setNotes((prev) => prev.filter((n) => n.id !== noteId))
    } catch (err) {
      setError(err.message || 'Failed to delete note')
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
        <h1 className="mb-6 text-2xl font-semibold text-slate-900 dark:text-white">Notes</h1>

        <form onSubmit={handleAddNote} className="mb-8 space-y-3 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Note title"
            className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          />
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder="Write your note in Markdown…"
            rows={4}
            className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
          />
          <button
            type="submit"
            disabled={adding}
            className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:opacity-60 dark:bg-indigo-500 dark:hover:bg-indigo-400"
          >
            {adding ? 'Adding…' : 'Add Note'}
          </button>
        </form>

        {error && (
          <p className="mb-4 rounded-xl border border-red-200 dark:border-red-900/60 bg-red-50 dark:bg-red-950/50 px-3.5 py-2.5 text-sm text-red-700 dark:text-red-400">
            {error}
          </p>
        )}

        {loading ? (
          <p className="text-slate-500 dark:text-slate-400">Loading…</p>
        ) : notes.length === 0 ? (
          <p className="text-slate-500 dark:text-slate-400">No notes yet — add one above.</p>
        ) : (
          <ul className="space-y-4">
            {notes.map((note) => (
              <li
                key={note.id}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm"
              >
                {editingId === note.id ? (
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
                    />
                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      rows={4}
                      className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2.5 text-slate-900 dark:text-slate-100 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30"
                    />
                    <div className="flex gap-3">
                      <button
                        onClick={() => handleSaveEdit(note.id)}
                        className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="rounded-lg bg-slate-100 dark:bg-slate-800 px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="mb-2 flex items-center justify-between">
                      <h3 className="font-medium text-slate-900 dark:text-white">{note.title}</h3>
                      <div className="flex gap-3">
                        <button
                          onClick={() => startEdit(note)}
                          className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(note.id)}
                          className="text-sm font-medium text-red-600 hover:text-red-500 dark:text-red-400 dark:hover:text-red-300"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    <div
                      className="prose prose-sm dark:prose-invert max-w-none text-slate-700 dark:text-slate-300"
                      dangerouslySetInnerHTML={{ __html: note.rendered_content }}
                    />
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  )
}
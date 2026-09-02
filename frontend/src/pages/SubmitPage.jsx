import React, { useState } from 'react'
import client from '../api/client'

function SubmitPage() {
  const [form, setForm] = useState({
    student_name: '',
    project_name: '',
    language_stack: 'python',
    submission_type: 'github',
    source_url: '',
  })
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const params = new URLSearchParams(form).toString()
      const res = await client.post(`/submissions/?${params}`)
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Submission failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Submit a Project</h2>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <input
            name="student_name"
            placeholder="Student Name"
            value={form.student_name}
            onChange={handleChange}
            required
          />
          <input
            name="project_name"
            placeholder="Project Name"
            value={form.project_name}
            onChange={handleChange}
            required
          />
          <select name="language_stack" value={form.language_stack} onChange={handleChange}>
            <option value="python">Python</option>
            <option value="node">Node / MERN</option>
            <option value="laravel">Laravel</option>
            <option value="flutter">Flutter</option>
          </select>
          <select name="submission_type" value={form.submission_type} onChange={handleChange}>
            <option value="github">GitHub</option>
            <option value="gitlab">GitLab</option>
            <option value="zip">ZIP</option>
            <option value="docker_image">Docker Image</option>
          </select>
          <input
            name="source_url"
            placeholder="Repository URL"
            value={form.source_url}
            onChange={handleChange}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Project'}
          </button>
        </form>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && (
          <div>
            <p><b>Submitted!</b></p>
            <p>ID: {result.id}</p>
            <p>Status: <span className="status-badge">{result.status}</span></p>
          </div>
        )}
      </div>
    </div>
  )
}

export default SubmitPage

import React, { useState, useEffect } from 'react'
import client from '../api/client'

function StatusPage() {
  const [submissions, setSubmissions] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchSubmissions = async () => {
    try {
      const res = await client.get('/submissions/')
      setSubmissions(res.data)
      setError(null)
    } catch (err) {
      setError('Could not load submissions. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSubmissions()
    const interval = setInterval(fetchSubmissions, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h2>Submission Status</h2>
      <div className="card">
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {!loading && !error && submissions.length === 0 && <p>No submissions yet.</p>}
        {submissions.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Student</th>
                <th>Project</th>
                <th>Stack</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {submissions.map((s) => (
                <tr key={s.id}>
                  <td>{s.student_name}</td>
                  <td>{s.project_name}</td>
                  <td>{s.language_stack}</td>
                  <td><span className="status-badge">{s.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default StatusPage

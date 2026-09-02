import React, { useState, useEffect } from 'react'
import client from '../api/client'

function LeaderboardPage() {
  const [entries, setEntries] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    client.get('/leaderboard/')
      .then((res) => setEntries(res.data))
      .catch(() => setError('Could not load leaderboard.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <h2>Leaderboard</h2>
      <div className="card">
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {!loading && !error && entries.length === 0 && <p>No submissions evaluated yet.</p>}
        {entries.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Project</th>
                <th>Overall Score</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((e, i) => (
                <tr key={e.id}>
                  <td>{i + 1}</td>
                  <td>{e.student_name}</td>
                  <td>{e.project_name}</td>
                  <td>{e.overall_score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default LeaderboardPage

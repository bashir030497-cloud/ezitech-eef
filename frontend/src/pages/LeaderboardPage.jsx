import React, { useState, useEffect } from 'react'
import client from '../api/client'

const TABS = [
  { key: '', label: 'Overall' },
  { key: 'fastest-build', label: 'Fastest Build' },
  { key: 'best-architecture', label: 'Best Architecture' },
  { key: 'best-api-design', label: 'Best API Design' },
  { key: 'best-documentation', label: 'Best Documentation' },
  { key: 'best-performance', label: 'Best Performance' },
]

function LeaderboardPage() {
  const [activeTab, setActiveTab] = useState('')
  const [entries, setEntries] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const path = activeTab ? `/leaderboard/${activeTab}` : '/leaderboard/'
    client.get(path)
      .then((res) => setEntries(res.data))
      .catch(() => setError('Could not load leaderboard.'))
      .finally(() => setLoading(false))
  }, [activeTab])

  const metricFor = (tab) => {
    if (tab === 'fastest-build') return 'build_time_seconds'
    if (tab === 'best-architecture') return 'architecture_score'
    if (tab === 'best-api-design') return 'api_quality_score'
    if (tab === 'best-documentation') return 'documentation_score'
    if (tab === 'best-performance') return 'performance_score'
    return 'overall_score'
  }

  const metricLabel = (tab) => {
    if (tab === 'fastest-build') return 'Build Time (s)'
    if (tab === 'best-architecture') return 'Architecture Score'
    if (tab === 'best-api-design') return 'API Quality Score'
    if (tab === 'best-documentation') return 'Documentation Score'
    if (tab === 'best-performance') return 'Performance Score'
    return 'Overall Score'
  }

  const metric = metricFor(activeTab)

  return (
    <div>
      <h2>Leaderboard</h2>

      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              width: 'auto',
              background: activeTab === tab.key ? '#2563eb' : '#e2e8f0',
              color: activeTab === tab.key ? 'white' : '#334155',
              padding: '8px 14px',
              margin: 0,
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="card">
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {!loading && !error && entries.length === 0 && <p>No submissions yet in this category.</p>}
        {entries.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Project</th>
                <th>{metricLabel(activeTab)}</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((e, i) => (
                <tr key={e.id}>
                  <td>{i + 1}</td>
                  <td>{e.student_name}</td>
                  <td>{e.project_name}</td>
                  <td>{e[metric] ?? '—'}</td>
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

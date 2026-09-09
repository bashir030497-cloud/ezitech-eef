import React, { useState } from 'react'
import client from '../api/client'

function extractErrorMessage(err) {
  const detail = err.response?.data?.detail
  if (!detail) return 'Report not found yet.'
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
  }
  if (typeof detail === 'object') return detail.msg || JSON.stringify(detail)
  return 'Report not found yet.'
}

function ReportPage() {
  const [submissionId, setSubmissionId] = useState('')
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchReport = async () => {
    const cleanId = submissionId.trim()
    if (!cleanId) return
    setLoading(true)
    setError(null)
    setReport(null)
    try {
      const res = await client.get(`/evaluations/${cleanId}/report`)
      setReport(res.data)
    } catch (err) {
      setError(extractErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Evaluation Report</h2>
      <div className="card">
        <input
          placeholder="Paste Submission ID (e.g. d74d780e-aa73-...)"
          value={submissionId}
          onChange={(e) => setSubmissionId(e.target.value)}
        />
        <button onClick={fetchReport} disabled={loading}>
          {loading ? 'Loading...' : 'Get Report'}
        </button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>

      {report && (
        <>
          <div className="card">
            <h3>Scores</h3>
            <div className="score-grid">
              {Object.entries(report.scores).map(([key, value]) => (
                <div className="score-item" key={key}>
                  <div className="label">{key.replace(/_/g, ' ')}</div>
                  <div className="value">{String(value)}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>AI Feedback</h3>
            {Object.entries(report.feedback).map(([key, value]) => (
              <p key={key}>
                <b>{key.replace(/_/g, ' ')}:</b> {typeof value === 'string' ? value : JSON.stringify(value)}
              </p>
            ))}
          </div>

          <div className="card">
            <h3>Plagiarism</h3>
            <p>Score: {report.plagiarism.score} | Matches: {report.plagiarism.matches}</p>
          </div>
        </>
      )}
    </div>
  )
}

export default ReportPage

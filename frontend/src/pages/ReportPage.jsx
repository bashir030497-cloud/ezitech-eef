import React, { useState } from 'react'
import client from '../api/client'

function ReportPage() {
  const [submissionId, setSubmissionId] = useState('')
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchReport = async () => {
    if (!submissionId) return
    setLoading(true)
    setError(null)
    setReport(null)
    try {
      const res = await client.get(`/evaluations/${submissionId}/report`)
      setReport(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Report not found yet.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>Evaluation Report</h2>
      <div className="card">
        <input
          placeholder="Paste Submission ID"
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
                  <div className="value">{value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>AI Feedback</h3>
            {Object.entries(report.feedback).map(([key, value]) => (
              <p key={key}>
                <b>{key.replace(/_/g, ' ')}:</b> {value}
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

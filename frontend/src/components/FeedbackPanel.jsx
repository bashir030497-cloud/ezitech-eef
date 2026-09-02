import React from 'react'

function FeedbackPanel({ feedback }) {
  return (
    <div>
      <h3>AI Feedback</h3>
      <p>{feedback}</p>
    </div>
  )
}

export default FeedbackPanel

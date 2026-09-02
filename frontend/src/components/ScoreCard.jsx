import React from 'react'

function ScoreCard({ label, value }) {
  return (
    <div>
      <span>{label}: </span>
      <strong>{value}</strong>
    </div>
  )
}

export default ScoreCard

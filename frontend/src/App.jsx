import React from 'react'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import SubmitPage from './pages/SubmitPage'
import StatusPage from './pages/StatusPage'
import ReportPage from './pages/ReportPage'
import LeaderboardPage from './pages/LeaderboardPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="navbar">
          <h1>Ezitech EEF</h1>
          <nav>
            <NavLink to="/" end>Submit</NavLink>
            <NavLink to="/status">Status</NavLink>
            <NavLink to="/report">Report</NavLink>
            <NavLink to="/leaderboard">Leaderboard</NavLink>
          </nav>
        </header>

        <main className="content">
          <Routes>
            <Route path="/" element={<SubmitPage />} />
            <Route path="/status" element={<StatusPage />} />
            <Route path="/report" element={<ReportPage />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App

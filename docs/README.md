# Ezitech Enterprise AI Engineering Sandbox & Auto Evaluation Platform

An AI-powered platform that automatically executes, tests, and evaluates intern engineering submissions inside isolated sandbox environments — replacing manual mentor review with a consistent, secure, and scalable evaluation pipeline.

## Problem It Solves

Ezitech interns submit hundreds of projects across Laravel, MERN, AI/Python, Flutter, and DevOps stacks. Manually reviewing each one is slow, inconsistent across mentors, and risky (running unknown code directly). This platform automates the full lifecycle: submission → sandbox execution → validation → testing → AI scoring → feedback → reporting.

## Features

- **Multi-source submission**: GitHub, GitLab, ZIP, Docker image
- **Isolated sandbox execution**: Docker-based clone, build, run, and teardown per submission
- **Multi-language support**: Python, Node/MERN, Laravel, Flutter
- **Automated validation**: project structure, API availability, database connectivity, auth flow, security scan
- **Automated testing**: API tests, UI smoke tests, DB checks, performance checks
- **AI evaluation engine**: 7 engineering scores (feature completion, code quality, architecture, security, API quality, deployment readiness, engineering maturity)
- **AI feedback engine**: strengths, weaknesses, missing requirements, security risks, refactoring and improvement suggestions
- **Plagiarism detection** (bonus)
- **Leaderboard**: compares submissions by score, build time, architecture, API design
- **Auto-generated evaluation reports** (HTML)

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Docker SDK
- **Frontend**: React, Vite
- **Database**: PostgreSQL
- **Queue/Cache**: Redis
- **AI**: LLM API (Claude) for scoring and feedback generation
- **Testing**: Pytest-style API checks, Playwright (UI smoke tests)

## Project Structure

```
ezitech-eef/
├── backend/           # FastAPI app: sandbox, validation, testing, AI engine, reports
├── frontend/          # React dashboard: submit, status, report, leaderboard
├── docs/              # Architecture, API docs, DB schema, deployment guide
└── docker-compose.yml # Backend + frontend + Postgres + Redis
```

See `docs/architecture-diagram.md` for system architecture and `docs/sandbox-execution-workflow.md` for the execution pipeline.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Run with Docker Compose
```bash
docker-compose up --build
```

### Run backend locally (without Docker Compose)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run frontend locally
```bash
cd frontend
npm install
npm run dev
```

Backend runs at `http://localhost:8000`, frontend at `http://localhost:5173`.

### Environment Variables
Copy `backend/.env` and set your own values, especially:
- `DATABASE_URL`
- `LLM_API_KEY`

## API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/submissions/` | POST | Submit a new project for evaluation |
| `/submissions/{id}/status` | GET | Check pipeline status |
| `/evaluations/{id}/report` | GET | Get scores + AI feedback |
| `/leaderboard/` | GET | Top submissions |
| `/plagiarism/{id}` | GET | Plagiarism result for a submission |

Full API documentation: `docs/api-documentation.md`

## Team

2 AI Engineers — 4 week development cycle (Ezitech Case Study AI-022)

## License

Internal Ezitech project — for educational/internship evaluation purposes.

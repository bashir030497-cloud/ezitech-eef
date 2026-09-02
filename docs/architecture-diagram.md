# Architecture Diagram

## High-Level System Architecture

```
                              ┌─────────────────────┐
                              │   React Dashboard    │
                              │ (Submit / Status /   │
                              │ Report / Leaderboard)│
                              └──────────┬───────────┘
                                         │ REST API (HTTP)
                                         ▼
                              ┌─────────────────────┐
                              │   FastAPI Backend    │
                              │  (app/api/*.py)      │
                              └──────────┬───────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
┌───────────────┐              ┌─────────────────┐              ┌──────────────────┐
│ Sandbox Layer  │              │ Validation Layer │              │  Testing Layer    │
│ (docker_runner,│──run in──▶  │ (structure, api,  │              │ (api, ui, db,      │
│  repo_handler) │  container   │  db, auth, sec)   │              │  performance)      │
└───────┬────────┘              └─────────┬─────────┘              └─────────┬─────────┘
        │                                 │                                 │
        │        Docker Engine            │                                 │
        │   (isolated containers per      │                                 │
        │    submission, auto-destroyed)  │                                 │
        │                                 ▼                                 ▼
        │                         ┌──────────────────────────────────────────┐
        │                         │            AI Evaluation Engine           │
        │                         │  (scorer.py, feedback_generator.py,       │
        │                         │   plagiarism_check.py)                    │
        │                         └───────────────────┬────────────────────┘
        │                                              │
        │                                              ▼
        │                                    ┌──────────────────┐
        │                                    │  Report Generator │
        │                                    │ (report_builder)   │
        │                                    └─────────┬─────────┘
        │                                              │
        ▼                                              ▼
┌───────────────────────────────────────────────────────────────┐
│                        PostgreSQL Database                      │
│  submissions | evaluations | scores | test_results | leaderboard│
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│              Monitoring & Logging (app/core/logger.py)          │
│         Logs every stage: clone, build, run, test, evaluate     │
└───────────────────────────────────────────────────────────────┘
```

## Layers Explained

### 1. Presentation Layer (Frontend)
React + Vite dashboard. Lets users submit projects, track pipeline status, view evaluation reports, and browse the leaderboard.

### 2. API Layer (`app/api/`)
FastAPI REST endpoints exposing submissions, evaluations, leaderboard, and plagiarism results. Acts as the single entry point for the frontend.

### 3. Sandbox Execution Layer (`app/sandbox/`)
- `repo_handler.py`: clones GitHub/GitLab repos or extracts ZIP uploads
- `docker_runner.py`: orchestrates the full pipeline — builds and runs the project inside an isolated Docker container, then destroys it after evaluation
- `language_configs/`: per-language Docker base images and run commands (Python, Node, Laravel, Flutter)

### 4. Validation Layer (`app/validation/`)
Static checks against the cloned project: folder structure, dependency files, API reachability, database indicators, auth endpoint behavior, and hardcoded secret scanning.

### 5. Testing Layer (`app/testing/`)
Dynamic checks against the running container: API health tests, UI smoke tests (Playwright), DB migration checks, and response-time performance checks.

### 6. AI Evaluation Engine (`app/ai_engine/`)
- `scorer.py`: computes the 7 engineering scores from validation + test results
- `feedback_generator.py`: calls an LLM to generate strengths, weaknesses, and an improvement roadmap
- `plagiarism_check.py`: compares submitted code against prior submissions for similarity

### 7. Reporting Layer (`app/reports/`)
Generates a self-contained HTML evaluation report per submission.

### 8. Data Layer (PostgreSQL)
Stores submissions, evaluations, scores, test results, and leaderboard entries. See `db-schema.md` for full schema.

### 9. Monitoring & Logging
Every stage of the pipeline (clone, build, run, test, evaluate) is logged via `app/core/logger.py` to both console and `logs/eef.log`.

## Data Flow (Request Lifecycle)

1. User submits a project (GitHub URL, stack) via the dashboard → `POST /submissions/`
2. Backend creates a `Submission` record with status `PENDING`
3. `run_sandbox_pipeline()` is triggered:
   - Clone → Build → Run (Docker container spun up)
   - Validation checks run against the cloned code and running container
   - Automated tests run against the live container
   - AI engine scores the submission and generates feedback
   - Plagiarism check runs against stored submissions
   - Container is stopped and removed; local clone is deleted
4. Results are persisted (`Evaluation`, `Score`, `LeaderboardEntry`)
5. An HTML report is generated
6. Frontend polls `GET /submissions/{id}/status`, then fetches `GET /evaluations/{id}/report`

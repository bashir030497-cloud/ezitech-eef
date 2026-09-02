# Sandbox Execution Workflow

This document describes the step-by-step lifecycle a project submission goes through, from intake to final report, as implemented in `app/sandbox/docker_runner.py`.

## Workflow Steps

### 1. Submission Received
- Endpoint: `POST /submissions/`
- A `Submission` row is created with `status = PENDING`
- Fields captured: `student_name`, `project_name`, `language_stack`, `submission_type`, `source_url`

### 2. Clone
- `status → CLONING`
- `repo_handler.clone_repo()` shallow-clones the GitHub/GitLab repo into an isolated temp directory: `/tmp/eef_sandbox/{submission_id}/`
- On failure, the pipeline stops and `status → FAILED`

### 3. Build & Run (Sandbox)
- `status → BUILDING`
- The correct language config is loaded from `app/sandbox/language_configs/{stack}.yaml` (base Docker image + run command)
- A new Docker container is started via the Docker SDK:
  - Project folder mounted as a volume (`/app`)
  - Memory capped (512MB) to prevent resource abuse
  - Isolated bridge network
- `status → RUNNING`
- A short warm-up delay allows the app inside the container to boot

### 4. Validation Checks (Static + Live)
Run against the cloned code and the live container:
- **Structure check**: README, dependency file, folder presence
- **API check**: hits the configured health endpoint
- **Database check**: looks for models/migrations/schema indicators
- **Auth check**: posts to the auth endpoint, expects a sane response (not a crash)
- **Security check**: scans for hardcoded secrets/API keys/passwords

### 5. Automated Testing
- `status → TESTING`
- API tests run against the live health endpoint
- (Optional/extended) UI smoke tests via Playwright, DB migration tests, performance/response-time checks

### 6. AI Evaluation
- `status → EVALUATING`
- `scorer.calculate_scores()`: converts validation + test results into the 7 engineering scores
- `feedback_generator.generate_feedback()`: sends validation/test/score data to an LLM, receives structured feedback (strengths, weaknesses, missing requirements, security risks, suggestions, roadmap)
- `plagiarism_check.check_plagiarism()`: compares submitted code against prior submissions

### 7. Persist Results
- `Score` row saved (7 scores + overall)
- `Evaluation` row saved (feedback + plagiarism result)
- `LeaderboardEntry` row saved/updated
- `status → COMPLETED`

### 8. Report Generation
- `report_builder.build_report()` generates a self-contained HTML report to `reports_output/{submission_id}.html`

### 9. Cleanup (always runs, even on failure)
- Docker container is stopped and removed
- Cloned project folder is deleted from disk

## Status State Machine

```
PENDING → CLONING → BUILDING → RUNNING → TESTING → EVALUATING → COMPLETED
                                                              ↘
                                                              FAILED (from any stage on error)
```

## Failure Handling
If any stage raises an exception, the pipeline:
1. Logs the error with the submission ID
2. Sets `status → FAILED`
3. Still runs cleanup (container removal, folder deletion) via a `finally` block

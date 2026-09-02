# Database Schema

Database: **PostgreSQL**
ORM: SQLAlchemy (models in `backend/app/models/`)

## Entity Relationship Overview

```
submissions (1) ──< evaluations (1)
submissions (1) ──< scores (1)
submissions (1) ──< test_results (many)
submissions (1) ──< leaderboard (1)
```

All child tables reference `submissions.id` via a foreign key.

---

## Table: `submissions`
Stores each project submission and its pipeline status.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | auto-generated |
| student_name | String | required |
| project_name | String | required |
| language_stack | String | python / node / laravel / flutter |
| submission_type | Enum | github / gitlab / zip / docker_image |
| source_url | String | repo link or file path |
| status | Enum | pending / cloning / building / running / testing / evaluating / completed / failed |
| created_at | DateTime | default: now |
| updated_at | DateTime | auto-updated on change |

---

## Table: `evaluations`
Stores AI-generated feedback and plagiarism result for a submission.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | auto-generated |
| submission_id | UUID (FK → submissions.id) | required |
| strengths | Text | |
| weaknesses | Text | |
| missing_requirements | Text | |
| security_risks | Text | |
| performance_suggestions | Text | |
| refactoring_suggestions | Text | |
| improvement_roadmap | Text | |
| plagiarism_score | String | e.g. "12%" |
| plagiarism_matches | Text | comma-separated matched submission IDs |
| created_at | DateTime | default: now |

---

## Table: `scores`
Stores the 7 engineering scores per submission.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | auto-generated |
| submission_id | UUID (FK → submissions.id) | required |
| feature_completion_score | Float | default 0.0 |
| code_quality_score | Float | default 0.0 |
| architecture_score | Float | default 0.0 |
| security_score | Float | default 0.0 |
| api_quality_score | Float | default 0.0 |
| deployment_readiness_score | Float | default 0.0 |
| engineering_maturity_score | Float | default 0.0 |
| overall_score | Float | default 0.0 |
| created_at | DateTime | default: now |

---

## Table: `test_results`
Stores individual test outcomes (API, UI, DB, performance) per submission.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | auto-generated |
| submission_id | UUID (FK → submissions.id) | required |
| test_type | String | api / ui / db / performance |
| test_name | String | e.g. "health_check" |
| passed | Boolean | default False |
| details | Text | error message or status info |
| created_at | DateTime | default: now |

---

## Table: `leaderboard`
Denormalized table for fast leaderboard queries.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | auto-generated |
| submission_id | UUID (FK → submissions.id) | required |
| student_name | String | |
| project_name | String | |
| overall_score | Float | default 0.0 |
| build_time_seconds | Float | nullable |
| architecture_score | Float | nullable |
| api_quality_score | Float | nullable |
| updated_at | DateTime | auto-updated on change |

---

## Notes
- All primary keys use PostgreSQL `UUID` type for global uniqueness across distributed evaluation workers.
- Tables are created automatically on backend startup via `app/db/init_db.py` (`Base.metadata.create_all`).
- For production, replace `create_all` with a migration tool (e.g. Alembic) to support schema versioning.

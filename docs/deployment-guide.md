# Deployment Guide

## Prerequisites
- Docker & Docker Compose installed
- Git installed
- (For local/manual run) Python 3.11+, Node.js 20+
- An LLM API key (for the AI feedback engine)

---

## Option 1: Full Stack via Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ezitech-eef.git
   cd ezitech-eef
   ```

2. Set environment variables in `backend/.env`:
   ```
   DATABASE_URL=postgresql://eef_user:eef_pass@postgres:5432/eef_db
   REDIS_URL=redis://redis:6379/0
   LLM_API_KEY=your_actual_api_key
   LLM_MODEL=claude-sonnet-4-6
   SECRET_KEY=change_this_in_production
   ```
   > Note: when running via `docker-compose`, use the service names (`postgres`, `redis`) as hostnames, not `localhost`.

3. Build and start all services:
   ```bash
   docker-compose up --build
   ```

4. Services will be available at:
   - Backend API: `http://localhost:8000`
   - API docs (Swagger): `http://localhost:8000/docs`
   - Frontend dashboard: `http://localhost:5173`
   - PostgreSQL: `localhost:5432`
   - Redis: `localhost:6379`

5. Database tables are created automatically on backend startup (`init_db()` runs on FastAPI's `startup` event).

---

## Option 2: Manual/Local Setup (without Docker Compose)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Update `.env`:
```
DATABASE_URL=postgresql://eef_user:eef_pass@localhost:5432/eef_db
```

Ensure PostgreSQL is running locally, then start the API:
```bash
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

> Note: The sandbox execution feature (`docker_runner.py`) requires Docker to be running on the host machine, since it uses the Docker SDK to spin up containers for each submission — this is required in both deployment options.

---

## Environment Variables Reference

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` |
| `SANDBOX_TIMEOUT_SECONDS` | Max time allowed per sandbox run | `300` |
| `SANDBOX_WORKDIR` | Temp directory for cloned repos | `/tmp/eef_sandbox` |
| `LLM_API_KEY` | API key for the AI feedback engine | — |
| `LLM_MODEL` | LLM model identifier | `claude-sonnet-4-6` |
| `SECRET_KEY` | App secret key | change in production |

---

## Production Considerations
- Replace `Base.metadata.create_all()` with Alembic migrations for safe schema changes
- Move `run_sandbox_pipeline()` from synchronous execution to a background task queue (Celery + Redis) so submission requests don't block
- Set `DEBUG=False` and use a strong, unique `SECRET_KEY`
- Restrict Docker container resource limits and network access further for untrusted code execution
- Add HTTPS termination (reverse proxy e.g. Nginx) in front of the FastAPI service
- Store LLM API keys in a secrets manager rather than plain `.env` in production

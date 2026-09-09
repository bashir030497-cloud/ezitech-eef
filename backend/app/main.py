from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import submissions, evaluations, leaderboard, plagiarism
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submissions.router)
app.include_router(evaluations.router)
app.include_router(leaderboard.router)
app.include_router(plagiarism.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}

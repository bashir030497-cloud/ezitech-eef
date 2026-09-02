from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.models.submission import Submission, SubmissionStatus
from app.sandbox.docker_runner import run_sandbox_pipeline
from app.core.logger import get_logger

router = APIRouter(prefix="/submissions", tags=["Submissions"])
logger = get_logger("submissions_api")


@router.post("/")
def create_submission(
    student_name: str,
    project_name: str,
    language_stack: str,
    submission_type: str,
    source_url: str,
    db: Session = Depends(get_db),
):
    submission = Submission(
        student_name=student_name,
        project_name=project_name,
        language_stack=language_stack,
        submission_type=submission_type,
        source_url=source_url,
        status=SubmissionStatus.PENDING,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    logger.info(f"New submission created: {submission.id}")

    # Kick off sandbox pipeline (sync for MVP; move to background task/Celery later)
    run_sandbox_pipeline(submission.id, db)

    return {"id": str(submission.id), "status": submission.status}


@router.get("/{submission_id}/status")
def get_status(submission_id: UUID, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"id": str(submission.id), "status": submission.status}


@router.get("/")
def list_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).all()

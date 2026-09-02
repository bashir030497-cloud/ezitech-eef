from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.models.evaluation import Evaluation

router = APIRouter(prefix="/plagiarism", tags=["Plagiarism"])


@router.get("/{submission_id}")
def get_plagiarism_result(submission_id: UUID, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.submission_id == submission_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="No evaluation found")
    return {
        "plagiarism_score": evaluation.plagiarism_score,
        "matches": evaluation.plagiarism_matches,
    }

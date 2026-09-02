from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.models.evaluation import Evaluation
from app.models.score import Score

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@router.get("/{submission_id}/report")
def get_report(submission_id: UUID, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.submission_id == submission_id).first()
    score = db.query(Score).filter(Score.submission_id == submission_id).first()

    if not evaluation or not score:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "scores": {
            "feature_completion": score.feature_completion_score,
            "code_quality": score.code_quality_score,
            "architecture": score.architecture_score,
            "security": score.security_score,
            "api_quality": score.api_quality_score,
            "deployment_readiness": score.deployment_readiness_score,
            "engineering_maturity": score.engineering_maturity_score,
            "overall": score.overall_score,
        },
        "feedback": {
            "strengths": evaluation.strengths,
            "weaknesses": evaluation.weaknesses,
            "missing_requirements": evaluation.missing_requirements,
            "security_risks": evaluation.security_risks,
            "performance_suggestions": evaluation.performance_suggestions,
            "refactoring_suggestions": evaluation.refactoring_suggestions,
            "improvement_roadmap": evaluation.improvement_roadmap,
        },
        "plagiarism": {
            "score": evaluation.plagiarism_score,
            "matches": evaluation.plagiarism_matches,
        },
    }

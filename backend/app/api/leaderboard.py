from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.leaderboard import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .order_by(LeaderboardEntry.overall_score.desc())
        .limit(50)
        .all()
    )
    return entries

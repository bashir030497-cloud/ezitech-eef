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


@router.get("/fastest-build")
def fastest_build(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .filter(LeaderboardEntry.build_time_seconds.isnot(None))
        .order_by(LeaderboardEntry.build_time_seconds.asc())
        .limit(10)
        .all()
    )
    return entries


@router.get("/best-architecture")
def best_architecture(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .order_by(LeaderboardEntry.architecture_score.desc())
        .limit(10)
        .all()
    )
    return entries


@router.get("/best-api-design")
def best_api_design(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .order_by(LeaderboardEntry.api_quality_score.desc())
        .limit(10)
        .all()
    )
    return entries


@router.get("/best-documentation")
def best_documentation(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .order_by(LeaderboardEntry.documentation_score.desc())
        .limit(10)
        .all()
    )
    return entries


@router.get("/best-performance")
def best_performance(db: Session = Depends(get_db)):
    entries = (
        db.query(LeaderboardEntry)
        .filter(LeaderboardEntry.performance_score.isnot(None))
        .order_by(LeaderboardEntry.performance_score.desc())
        .limit(10)
        .all()
    )
    return entries

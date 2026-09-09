import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)

    student_name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)

    overall_score = Column(Float, default=0.0)
    build_time_seconds = Column(Float)
    architecture_score = Column(Float)
    api_quality_score = Column(Float)
    documentation_score = Column(Float)
    performance_score = Column(Float)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

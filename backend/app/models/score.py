import uuid
from datetime import datetime
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)

    feature_completion_score = Column(Float, default=0.0)
    code_quality_score = Column(Float, default=0.0)
    architecture_score = Column(Float, default=0.0)
    security_score = Column(Float, default=0.0)
    api_quality_score = Column(Float, default=0.0)
    deployment_readiness_score = Column(Float, default=0.0)
    engineering_maturity_score = Column(Float, default=0.0)

    overall_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

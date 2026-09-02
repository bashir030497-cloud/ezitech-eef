import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)

    strengths = Column(Text)
    weaknesses = Column(Text)
    missing_requirements = Column(Text)
    security_risks = Column(Text)
    performance_suggestions = Column(Text)
    refactoring_suggestions = Column(Text)
    improvement_roadmap = Column(Text)

    plagiarism_score = Column(String)      # e.g. "12%"
    plagiarism_matches = Column(Text)      # matched submission IDs, comma-separated

    created_at = Column(DateTime, default=datetime.utcnow)

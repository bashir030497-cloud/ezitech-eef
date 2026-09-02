import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)

    test_type = Column(String, nullable=False)  # api, ui, db, performance
    test_name = Column(String, nullable=False)
    passed = Column(Boolean, default=False)
    details = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

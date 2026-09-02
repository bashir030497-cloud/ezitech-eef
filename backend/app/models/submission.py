import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.database import Base


class SubmissionType(str, enum.Enum):
    GITHUB = "github"
    GITLAB = "gitlab"
    ZIP = "zip"
    DOCKER_IMAGE = "docker_image"


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    CLONING = "cloning"
    BUILDING = "building"
    RUNNING = "running"
    TESTING = "testing"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    FAILED = "failed"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    language_stack = Column(String, nullable=False)  # python, node, laravel, flutter
    submission_type = Column(Enum(SubmissionType), nullable=False)
    source_url = Column(String, nullable=False)  # repo link or file path
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

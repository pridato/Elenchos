"""Session and attempt models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Integer, Boolean, Float, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class ScaffoldLevel(str, enum.Enum):
    """Scaffold level enumeration"""
    LEVEL_1 = "LEVEL_1"  # Reflexión
    LEVEL_2 = "LEVEL_2"  # Pista con RAG
    LEVEL_3 = "LEVEL_3"  # Analogía simplificada


class ErrorType(str, enum.Enum):
    """Error type enumeration"""
    SYNTAX = "SYNTAX"
    PROCEDURE = "PROCEDURE"
    CONCEPT = "CONCEPT"


class Session(Base):
    """Session model - tracks student problem-solving session"""
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey(
        "students.id"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey(
        "problems.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    current_step = Column(Integer, default=0, nullable=False)
    scaffold_level = Column(SQLEnum(ScaffoldLevel), nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    # Sentiment tracking
    sentiment_scores = Column(JSON, default=list, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="sessions")
    problem = relationship("Problem", back_populates="sessions")
    step_attempts = relationship(
        "StepAttempt", back_populates="session", cascade="all, delete-orphan")


class StepAttempt(Base):
    """Step attempt model - tracks individual step attempts"""
    __tablename__ = "step_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey(
        "sessions.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    student_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    latency_seconds = Column(Float, nullable=False)

    # Scaffold information
    scaffold_provided = Column(JSON, nullable=True)

    # Relationships
    session = relationship("Session", back_populates="step_attempts")
    error_diagnosis = relationship(
        "ErrorDiagnosis", back_populates="step_attempt", uselist=False, cascade="all, delete-orphan")


class ErrorDiagnosis(Base):
    """Error diagnosis model"""
    __tablename__ = "error_diagnoses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    step_attempt_id = Column(UUID(as_uuid=True), ForeignKey(
        "step_attempts.id"), nullable=False, unique=True)
    error_type = Column(SQLEnum(ErrorType), nullable=False)
    error_details = Column(Text, nullable=False)
    affected_concept = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)  # 1-5

    # Relationships
    step_attempt = relationship(
        "StepAttempt", back_populates="error_diagnosis")

"""Problem models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Integer, Boolean, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class ProblemType(str, enum.Enum):
    """Problem type enumeration"""
    MATH = "MATH"
    CODE = "CODE"


class Language(str, enum.Enum):
    """Programming language enumeration"""
    PYTHON = "PYTHON"
    CPP = "CPP"
    JAVA = "JAVA"


class Problem(Base):
    """Problem model"""
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    skill_id = Column(String, nullable=False, index=True)
    type = Column(SQLEnum(ProblemType), nullable=False)
    difficulty = Column(Integer, nullable=False)  # 1-5
    solution_steps = Column(JSON, default=list, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey(
        "teachers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    created_by_teacher = relationship("Teacher", back_populates="problems")
    content = relationship("ProblemContent", back_populates="problem",
                           uselist=False, cascade="all, delete-orphan")
    test_cases = relationship(
        "TestCase", back_populates="problem", cascade="all, delete-orphan")
    sessions = relationship(
        "Session", back_populates="problem", cascade="all, delete-orphan")


class ProblemContent(Base):
    """Problem content model"""
    __tablename__ = "problem_contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey(
        "problems.id"), nullable=False, unique=True)
    text = Column(Text, nullable=True)
    latex = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    code_template = Column(Text, nullable=True)
    language = Column(SQLEnum(Language), nullable=True)

    # Relationships
    problem = relationship("Problem", back_populates="content")


class TestCase(Base):
    """Test case model for code problems"""
    __tablename__ = "test_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey(
        "problems.id"), nullable=False)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    description = Column(String, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)

    # Relationships
    problem = relationship("Problem", back_populates="test_cases")

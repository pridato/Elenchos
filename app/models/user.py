"""User models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class User(Base):
    """Base user model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": role,
    }


class Student(User):
    """Student user model"""
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey(
        "teachers.id"), nullable=True)
    total_problems_solved = Column(Integer, default=0, nullable=False)
    average_scaffold_level = Column(Float, default=0.0, nullable=False)

    # BKT parameters stored as JSON
    bkt_parameters = Column(JSON, default=dict, nullable=False)

    # Relationships
    teacher = relationship(
        "Teacher", back_populates="students", foreign_keys=[teacher_id])
    sessions = relationship(
        "Session", back_populates="student", cascade="all, delete-orphan")
    skill_states = relationship(
        "SkillState", back_populates="student", cascade="all, delete-orphan")
    class_memberships = relationship(
        "ClassStudent", back_populates="student", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": UserRole.STUDENT,
    }


class Teacher(User):
    """Teacher user model"""
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    notion_token = Column(String, nullable=True)
    notion_page_ids = Column(JSON, default=list, nullable=False)
    alert_preferences = Column(JSON, default=dict, nullable=False)

    # Relationships
    students = relationship(
        "Student", back_populates="teacher", foreign_keys=[Student.teacher_id])
    classes = relationship(
        "Class", back_populates="teacher", cascade="all, delete-orphan")
    problems = relationship(
        "Problem", back_populates="created_by_teacher", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": UserRole.TEACHER,
    }

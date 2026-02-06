"""Skill tree models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base


class SkillStatus(str, enum.Enum):
    """Skill status enumeration"""
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    IN_PROGRESS = "IN_PROGRESS"
    MASTERED = "MASTERED"


class Skill(Base):
    """Skill model - represents a node in the skill tree"""
    __tablename__ = "skills"

    id = Column(String, primary_key=True)  # skill_id like "algebra-1"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # e.g., "algebra", "calculus", "programming"
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    dependencies = relationship(
        "SkillDependency",
        foreign_keys="SkillDependency.skill_id",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
    dependent_on = relationship(
        "SkillDependency",
        foreign_keys="SkillDependency.depends_on_skill_id",
        back_populates="depends_on_skill",
        cascade="all, delete-orphan"
    )
    skill_states = relationship(
        "SkillState", back_populates="skill", cascade="all, delete-orphan")


class SkillDependency(Base):
    """Skill dependency model - represents edges in the skill tree"""
    __tablename__ = "skill_dependencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)
    depends_on_skill_id = Column(
        String, ForeignKey("skills.id"), nullable=False)

    # Relationships
    skill = relationship("Skill", foreign_keys=[
                         skill_id], back_populates="dependencies")
    depends_on_skill = relationship(
        "Skill", foreign_keys=[depends_on_skill_id], back_populates="dependent_on")


class SkillState(Base):
    """Skill state model - tracks student progress on a skill"""
    __tablename__ = "skill_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey(
        "students.id"), nullable=False)
    skill_id = Column(String, ForeignKey("skills.id"), nullable=False)

    # BKT probability
    domain_probability = Column(Float, default=0.1, nullable=False)  # L(t)

    # Status
    status = Column(SQLEnum(SkillStatus),
                    default=SkillStatus.LOCKED, nullable=False)

    # Activity tracking
    problems_attempted = Column(Integer, default=0, nullable=False)
    problems_solved = Column(Integer, default=0, nullable=False)
    last_activity = Column(DateTime, nullable=True)

    # BKT parameters for this skill (can be customized per skill)
    bkt_params = Column(JSON, default=dict, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="skill_states")
    skill = relationship("Skill", back_populates="skill_states")

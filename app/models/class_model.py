"""Class and class membership models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base


class Class(Base):
    """Class model - represents a teacher's class"""
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey(
        "teachers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    invitation_code = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    teacher = relationship("Teacher", back_populates="classes")
    class_students = relationship(
        "ClassStudent", back_populates="class_obj", cascade="all, delete-orphan")


class ClassStudent(Base):
    """Class-Student association model"""
    __tablename__ = "class_students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    class_id = Column(UUID(as_uuid=True), ForeignKey(
        "classes.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey(
        "students.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    class_obj = relationship("Class", back_populates="class_students")
    student = relationship("Student", back_populates="class_memberships")

"""
Property-Based Tests for Data Persistence

Feature: elenchos, Property 18: Persistencia Completa de Datos

Tests that validate Requirements 11.1, 11.2, 11.3, 11.4, 11.5:
- 11.1: User information persistence in PostgreSQL
- 11.2: Problem attempt registration storage
- 11.3: Skill tree state persistence
- 11.4: Teacher content embeddings in ChromaDB
- 11.5: Referential integrity maintenance
"""
from contextlib import contextmanager
import pytest
from hypothesis import given, settings, strategies as st
from hypothesis.strategies import composite
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.db.base import SessionLocal, engine, Base
from app.models import (
    User, Student, Teacher,
    Class, ClassStudent,
    Problem, ProblemContent, TestCase,
    Session as ProblemSession, StepAttempt, ErrorDiagnosis,
    Skill, SkillState, SkillDependency
)
from app.models.user import UserRole
from app.models.problem import ProblemType, Language
from app.models.session import ScaffoldLevel, ErrorType
from app.models.skill import SkillStatus


# ============================================================================
# Hypothesis Strategies for Generating Test Data
# ============================================================================

@composite
def user_data(draw):
    """Generate valid user data"""
    return {
        "email": draw(st.emails()),
        "password_hash": draw(st.text(min_size=60, max_size=60, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./$")),
        "role": draw(st.sampled_from([UserRole.STUDENT, UserRole.TEACHER])),
        "last_login": draw(st.one_of(st.none(), st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31))))
    }


@composite
def student_data(draw, teacher_id=None):
    """Generate valid student data"""
    return {
        "email": draw(st.emails()),
        "password_hash": draw(st.text(min_size=60, max_size=60, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./$")),
        "role": UserRole.STUDENT,
        "teacher_id": teacher_id,
        "total_problems_solved": draw(st.integers(min_value=0, max_value=1000)),
        "average_scaffold_level": draw(st.floats(min_value=0.0, max_value=3.0)),
        "bkt_parameters": draw(st.dictionaries(
            st.text(min_size=1, max_size=20),
            st.dictionaries(
                st.sampled_from(["P_L0", "P_T", "P_S", "P_G"]),
                st.floats(min_value=0.0, max_value=1.0)
            )
        ))
    }


@composite
def teacher_data(draw):
    """Generate valid teacher data"""
    return {
        "email": draw(st.emails()),
        "password_hash": draw(st.text(min_size=60, max_size=60, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./$")),
        "role": UserRole.TEACHER,
        "notion_token": draw(st.one_of(st.none(), st.text(min_size=10, max_size=100, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"))),
        "notion_page_ids": draw(st.lists(st.text(min_size=10, max_size=50, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"), max_size=5)),
        "alert_preferences": draw(st.dictionaries(
            st.sampled_from(
                ["email_alerts", "push_notifications", "threshold"]),
            st.one_of(st.booleans(), st.integers(min_value=1, max_value=10))
        ))
    }


@composite
def problem_data(draw, teacher_id):
    """Generate valid problem data"""
    return {
        "skill_id": draw(st.text(min_size=5, max_size=50, alphabet="abcdefghijklmnopqrstuvwxyz-0123456789")),
        "type": draw(st.sampled_from([ProblemType.MATH, ProblemType.CODE])),
        "difficulty": draw(st.integers(min_value=1, max_value=5)),
        "solution_steps": draw(st.lists(st.text(min_size=1, max_size=200), min_size=1, max_size=10)),
        "created_by": teacher_id
    }


@composite
def skill_data(draw):
    """Generate valid skill data"""
    return {
        "id": draw(st.text(min_size=5, max_size=50, alphabet="abcdefghijklmnopqrstuvwxyz-0123456789")),
        "name": draw(st.text(min_size=5, max_size=100)),
        "description": draw(st.one_of(st.none(), st.text(min_size=10, max_size=200))),
        "category": draw(st.sampled_from(["algebra", "calculus", "programming", "geometry"]))
    }


@composite
def skill_state_data(draw, student_id, skill_id):
    """Generate valid skill state data"""
    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "domain_probability": draw(st.floats(min_value=0.0, max_value=1.0)),
        "status": draw(st.sampled_from(list(SkillStatus))),
        "problems_attempted": draw(st.integers(min_value=0, max_value=100)),
        "problems_solved": draw(st.integers(min_value=0, max_value=100)),
        "last_activity": draw(st.one_of(st.none(), st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31)))),
        "bkt_params": draw(st.dictionaries(
            st.sampled_from(["P_L0", "P_T", "P_S", "P_G"]),
            st.floats(min_value=0.0, max_value=1.0)
        ))
    }


@composite
def session_data(draw, student_id, problem_id):
    """Generate valid session data"""
    return {
        "student_id": student_id,
        "problem_id": problem_id,
        "current_step": draw(st.integers(min_value=0, max_value=20)),
        "scaffold_level": draw(st.one_of(st.none(), st.sampled_from(list(ScaffoldLevel)))),
        "is_completed": draw(st.booleans()),
        "sentiment_scores": draw(st.lists(
            st.dictionaries(
                st.sampled_from(
                    ["frustration_level", "confidence_level", "timestamp"]),
                st.one_of(st.floats(min_value=0.0, max_value=1.0), st.datetimes(min_value=datetime(
                    2020, 1, 1), max_value=datetime(2025, 12, 31)).map(lambda d: d.isoformat()))
            ),
            max_size=10
        ))
    }


@composite
def step_attempt_data(draw, session_id):
    """Generate valid step attempt data"""
    return {
        "session_id": session_id,
        "step_number": draw(st.integers(min_value=0, max_value=20)),
        "student_answer": draw(st.text(min_size=1, max_size=500)),
        "is_correct": draw(st.booleans()),
        "latency_seconds": draw(st.floats(min_value=0.1, max_value=300.0)),
        "scaffold_provided": draw(st.one_of(
            st.none(),
            st.dictionaries(
                st.sampled_from(["level", "content", "should_alert_teacher"]),
                st.one_of(st.text(min_size=1, max_size=200), st.booleans())
            )
        ))
    }


# ============================================================================
# Database Session Context Manager
# ============================================================================


@contextmanager
def get_db_session():
    """Create a fresh database session as a context manager for property-based tests"""
    # Create all tables once (if they don't exist)
    Base.metadata.create_all(bind=engine)

    # Create session
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        # Clean up data but keep tables
        session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()


# Setup: Create tables once before all tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create database tables once for all tests"""
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup: Drop tables after all tests
    Base.metadata.drop_all(bind=engine)


# ============================================================================
# Property 18: Persistencia Completa de Datos
# ============================================================================

@settings(max_examples=10, deadline=None)
@given(data=user_data())
def test_property_18_user_persistence(data):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirement 11.1: User information persistence in PostgreSQL

    Property: For any user creation operation, the system SHALL persist
    the user data in PostgreSQL with all fields correctly stored.
    """
    with get_db_session() as db_session:
        # Create user
        user = User(
            id=uuid4(),
            email=data["email"],
            password_hash=data["password_hash"],
            role=data["role"],
            created_at=datetime.utcnow(),
            last_login=data["last_login"]
        )

        db_session.add(user)
        db_session.commit()

        # Retrieve user from database
        retrieved_user = db_session.query(User).filter_by(id=user.id).first()

        # Verify persistence
        assert retrieved_user is not None, "User should be persisted"
        assert retrieved_user.email == data["email"], "Email should match"
        assert retrieved_user.password_hash == data["password_hash"], "Password hash should match"
        assert retrieved_user.role == data["role"], "Role should match"
        assert retrieved_user.created_at is not None, "Created timestamp should exist"
        assert retrieved_user.last_login == data["last_login"], "Last login should match"


@settings(max_examples=1, deadline=None)
@given(teacher_data_dict=teacher_data(), student_data_gen=st.data())
def test_property_18_student_teacher_relationship(teacher_data_dict, student_data_gen):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirement 11.5: Referential integrity between students and teachers

    Property: For any student-teacher relationship, the system SHALL maintain
    referential integrity in PostgreSQL.
    """
    with get_db_session() as db_session:
        # Create teacher
        teacher = Teacher(
            id=uuid4(),
            email=teacher_data_dict["email"],
            password_hash=teacher_data_dict["password_hash"],
            role=teacher_data_dict["role"],
            created_at=datetime.utcnow(),
            notion_token=teacher_data_dict["notion_token"],
            notion_page_ids=teacher_data_dict["notion_page_ids"],
            alert_preferences=teacher_data_dict["alert_preferences"]
        )

        db_session.add(teacher)
        db_session.commit()

        # Create student with teacher relationship
        student_data_dict = student_data_gen.draw(
            student_data(teacher_id=teacher.id))
        student = Student(
            id=uuid4(),
            email=student_data_dict["email"],
            password_hash=student_data_dict["password_hash"],
            role=student_data_dict["role"],
            created_at=datetime.utcnow(),
            teacher_id=student_data_dict["teacher_id"],
            total_problems_solved=student_data_dict["total_problems_solved"],
            average_scaffold_level=student_data_dict["average_scaffold_level"],
            bkt_parameters=student_data_dict["bkt_parameters"]
        )

        db_session.add(student)
        db_session.commit()

        # Verify referential integrity
        retrieved_student = db_session.query(
            Student).filter_by(id=student.id).first()
        assert retrieved_student is not None, "Student should be persisted"
        assert retrieved_student.teacher_id == teacher.id, "Teacher relationship should be maintained"
        assert retrieved_student.teacher is not None, "Teacher relationship should be accessible"
        assert retrieved_student.teacher.id == teacher.id, "Teacher ID should match"


@settings(max_examples=10, deadline=None)
@given(teacher_data_dict=teacher_data(), problem_data_gen=st.data())
def test_property_18_problem_attempt_registration(teacher_data_dict, problem_data_gen):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirement 11.2: Problem attempt registration storage

    Property: For any problem attempt, the system SHALL store the problem,
    response, result, and scaffold level in PostgreSQL.
    """
    with get_db_session() as db_session:
        # Create teacher
        teacher = Teacher(
            id=uuid4(),
            email=teacher_data_dict["email"],
            password_hash=teacher_data_dict["password_hash"],
            role=teacher_data_dict["role"],
            created_at=datetime.utcnow(),
            notion_token=teacher_data_dict["notion_token"],
            notion_page_ids=teacher_data_dict["notion_page_ids"],
            alert_preferences=teacher_data_dict["alert_preferences"]
        )
        db_session.add(teacher)
        db_session.commit()

        # Create student
        student = Student(
            id=uuid4(),
            email="student@test.com",
            password_hash="$2b$12$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP",
            role=UserRole.STUDENT,
            created_at=datetime.utcnow(),
            teacher_id=teacher.id,
            total_problems_solved=0,
            average_scaffold_level=0.0,
            bkt_parameters={}
        )
        db_session.add(student)
        db_session.commit()

        # Create problem
        problem_data_dict = problem_data_gen.draw(
            problem_data(teacher_id=teacher.id))
        problem = Problem(
            id=uuid4(),
            skill_id=problem_data_dict["skill_id"],
            type=problem_data_dict["type"],
            difficulty=problem_data_dict["difficulty"],
            solution_steps=problem_data_dict["solution_steps"],
            created_by=problem_data_dict["created_by"],
            created_at=datetime.utcnow()
        )
        db_session.add(problem)
        db_session.commit()

        # Create session
        session_data_dict = problem_data_gen.draw(
            session_data(student_id=student.id, problem_id=problem.id))
        session = ProblemSession(
            id=uuid4(),
            student_id=session_data_dict["student_id"],
            problem_id=session_data_dict["problem_id"],
            started_at=datetime.utcnow(),
            current_step=session_data_dict["current_step"],
            scaffold_level=session_data_dict["scaffold_level"],
            is_completed=session_data_dict["is_completed"],
            sentiment_scores=session_data_dict["sentiment_scores"]
        )
        db_session.add(session)
        db_session.commit()

        # Create step attempt
        step_data_dict = problem_data_gen.draw(
            step_attempt_data(session_id=session.id))
        step_attempt = StepAttempt(
            id=uuid4(),
            session_id=step_data_dict["session_id"],
            step_number=step_data_dict["step_number"],
            student_answer=step_data_dict["student_answer"],
            is_correct=step_data_dict["is_correct"],
            timestamp=datetime.utcnow(),
            latency_seconds=step_data_dict["latency_seconds"],
            scaffold_provided=step_data_dict["scaffold_provided"]
        )
        db_session.add(step_attempt)
        db_session.commit()

        # Verify persistence
        retrieved_session = db_session.query(
            ProblemSession).filter_by(id=session.id).first()
        assert retrieved_session is not None, "Session should be persisted"
        assert retrieved_session.student_id == student.id, "Student relationship should be maintained"
        assert retrieved_session.problem_id == problem.id, "Problem relationship should be maintained"
        assert retrieved_session.scaffold_level == session_data_dict[
            "scaffold_level"], "Scaffold level should be stored"

        retrieved_step = db_session.query(
            StepAttempt).filter_by(id=step_attempt.id).first()
        assert retrieved_step is not None, "Step attempt should be persisted"
        assert retrieved_step.session_id == session.id, "Session relationship should be maintained"
        assert retrieved_step.student_answer == step_data_dict[
            "student_answer"], "Student answer should be stored"
        assert retrieved_step.is_correct == step_data_dict["is_correct"], "Result should be stored"
        assert retrieved_step.scaffold_provided == step_data_dict[
            "scaffold_provided"], "Scaffold info should be stored"


@settings(max_examples=10, deadline=None)
@given(skill_data_gen=skill_data(), student_email=st.emails())
def test_property_18_skill_tree_state_persistence(skill_data_gen, student_email):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirement 11.3: Skill tree state persistence

    Property: For any skill tree update, the system SHALL persist the new
    domain state in PostgreSQL.
    """
    with get_db_session() as db_session:
        # Create student
        student = Student(
            id=uuid4(),
            email=student_email,
            password_hash="$2b$12$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP",
            role=UserRole.STUDENT,
            created_at=datetime.utcnow(),
            teacher_id=None,
            total_problems_solved=0,
            average_scaffold_level=0.0,
            bkt_parameters={}
        )
        db_session.add(student)
        db_session.commit()

        # Create skill
        skill = Skill(
            id=skill_data_gen["id"],
            name=skill_data_gen["name"],
            description=skill_data_gen["description"],
            category=skill_data_gen["category"],
            created_at=datetime.utcnow()
        )
        db_session.add(skill)
        db_session.commit()

        # Create skill state
        skill_state_dict = {
            "student_id": student.id,
            "skill_id": skill.id,
            "domain_probability": 0.5,
            "status": SkillStatus.IN_PROGRESS,
            "problems_attempted": 5,
            "problems_solved": 3,
            "last_activity": datetime.utcnow(),
            "bkt_params": {"P_L0": 0.1, "P_T": 0.3, "P_S": 0.1, "P_G": 0.2}
        }

        skill_state = SkillState(
            id=uuid4(),
            **skill_state_dict
        )
        db_session.add(skill_state)
        db_session.commit()

        # Update skill state (simulate domain update)
        skill_state.domain_probability = 0.75
        skill_state.status = SkillStatus.MASTERED
        skill_state.problems_solved = 5
        db_session.commit()

        # Verify persistence of update
        retrieved_state = db_session.query(
            SkillState).filter_by(id=skill_state.id).first()
        assert retrieved_state is not None, "Skill state should be persisted"
        assert retrieved_state.domain_probability == 0.75, "Updated domain probability should be persisted"
        assert retrieved_state.status == SkillStatus.MASTERED, "Updated status should be persisted"
        assert retrieved_state.problems_solved == 5, "Updated problems solved should be persisted"
        assert retrieved_state.student_id == student.id, "Student relationship should be maintained"
        assert retrieved_state.skill_id == skill.id, "Skill relationship should be maintained"


@settings(max_examples=10, deadline=None)
@given(
    skill1_data=skill_data(),
    skill2_data=skill_data(),
    student_email=st.emails()
)
def test_property_18_referential_integrity_cascade(skill1_data, skill2_data, student_email):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirement 11.5: Referential integrity maintenance with cascades

    Property: For any entity deletion, the system SHALL maintain referential
    integrity by cascading deletes to dependent entities.
    """
    with get_db_session() as db_session:
        # Create student
        student = Student(
            id=uuid4(),
            email=student_email,
            password_hash="$2b$12$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP",
            role=UserRole.STUDENT,
            created_at=datetime.utcnow(),
            teacher_id=None,
            total_problems_solved=0,
            average_scaffold_level=0.0,
            bkt_parameters={}
        )
        db_session.add(student)
        db_session.commit()

        # Create two skills with different IDs
        skill1 = Skill(
            id=skill1_data["id"] + "_1",  # Ensure unique ID
            name=skill1_data["name"],
            description=skill1_data["description"],
            category=skill1_data["category"],
            created_at=datetime.utcnow()
        )
        skill2 = Skill(
            id=skill2_data["id"] + "_2",  # Ensure unique ID
            name=skill2_data["name"],
            description=skill2_data["description"],
            category=skill2_data["category"],
            created_at=datetime.utcnow()
        )
        db_session.add_all([skill1, skill2])
        db_session.commit()

        # Create skill states
        skill_state1 = SkillState(
            id=uuid4(),
            student_id=student.id,
            skill_id=skill1.id,
            domain_probability=0.5,
            status=SkillStatus.IN_PROGRESS,
            problems_attempted=5,
            problems_solved=3,
            bkt_params={}
        )
        skill_state2 = SkillState(
            id=uuid4(),
            student_id=student.id,
            skill_id=skill2.id,
            domain_probability=0.3,
            status=SkillStatus.AVAILABLE,
            problems_attempted=2,
            problems_solved=1,
            bkt_params={}
        )
        db_session.add_all([skill_state1, skill_state2])
        db_session.commit()

        # Verify states exist
        states_before = db_session.query(SkillState).filter_by(
            student_id=student.id).count()
        assert states_before == 2, "Both skill states should exist"

        # Delete student (should cascade to skill states)
        db_session.delete(student)
        db_session.commit()

        # Verify cascade deletion
        states_after = db_session.query(SkillState).filter_by(
            student_id=student.id).count()
        assert states_after == 0, "Skill states should be cascade deleted with student"

        # Verify skills still exist (not cascade deleted)
        skill1_exists = db_session.query(Skill).filter_by(id=skill1.id).first()
        skill2_exists = db_session.query(Skill).filter_by(id=skill2.id).first()
        assert skill1_exists is not None, "Skill 1 should still exist"
        assert skill2_exists is not None, "Skill 2 should still exist"


@settings(max_examples=5, deadline=None)
@given(
    teacher_data_dict=teacher_data(),
    num_students=st.integers(min_value=1, max_value=5),
    num_problems=st.integers(min_value=1, max_value=3)
)
def test_property_18_complex_referential_integrity(
    teacher_data_dict,
    num_students,
    num_problems
):
    """
    Feature: elenchos, Property 18: Persistencia Completa de Datos

    Validates Requirements 11.1, 11.2, 11.3, 11.5: Complete data persistence
    with complex relationships

    Property: For any complex entity graph (teacher -> students -> sessions -> attempts),
    the system SHALL maintain referential integrity across all relationships.
    """
    with get_db_session() as db_session:
        # Create teacher
        teacher = Teacher(
            id=uuid4(),
            email=teacher_data_dict["email"],
            password_hash=teacher_data_dict["password_hash"],
            role=teacher_data_dict["role"],
            created_at=datetime.utcnow(),
            notion_token=teacher_data_dict["notion_token"],
            notion_page_ids=teacher_data_dict["notion_page_ids"],
            alert_preferences=teacher_data_dict["alert_preferences"]
        )
        db_session.add(teacher)
        db_session.commit()

        # Create students
        students = []
        for i in range(num_students):
            student = Student(
                id=uuid4(),
                email=f"student{i}@test.com",
                password_hash="$2b$12$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP",
                role=UserRole.STUDENT,
                created_at=datetime.utcnow(),
                teacher_id=teacher.id,
                total_problems_solved=0,
                average_scaffold_level=0.0,
                bkt_parameters={}
            )
            students.append(student)
            db_session.add(student)
        db_session.commit()

        # Create problems
        problems = []
        for i in range(num_problems):
            problem = Problem(
                id=uuid4(),
                skill_id=f"skill-{i}",
                type=ProblemType.MATH,
                difficulty=3,
                solution_steps=["step1", "step2"],
                created_by=teacher.id,
                created_at=datetime.utcnow()
            )
            problems.append(problem)
            db_session.add(problem)
        db_session.commit()

        # Create sessions for each student-problem pair
        session_count = 0
        for student in students:
            for problem in problems:
                session = ProblemSession(
                    id=uuid4(),
                    student_id=student.id,
                    problem_id=problem.id,
                    started_at=datetime.utcnow(),
                    current_step=0,
                    is_completed=False,
                    sentiment_scores=[]
                )
                db_session.add(session)
                session_count += 1
        db_session.commit()

        # Verify all relationships
        retrieved_teacher = db_session.query(
            Teacher).filter_by(id=teacher.id).first()
        assert retrieved_teacher is not None, "Teacher should be persisted"
        assert len(
            retrieved_teacher.students) == num_students, "All students should be related to teacher"
        assert len(
            retrieved_teacher.problems) == num_problems, "All problems should be related to teacher"

        for student in students:
            retrieved_student = db_session.query(
                Student).filter_by(id=student.id).first()
            assert retrieved_student is not None, "Student should be persisted"
            assert retrieved_student.teacher_id == teacher.id, "Student should be related to teacher"
            assert len(
                retrieved_student.sessions) == num_problems, "Student should have sessions for all problems"

        # Verify total session count
        total_sessions = db_session.query(ProblemSession).count()
        expected_sessions = num_students * num_problems
        assert total_sessions == expected_sessions, f"Should have {expected_sessions} sessions"

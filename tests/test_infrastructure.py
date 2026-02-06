"""Test infrastructure setup"""
import pytest
from sqlalchemy import inspect
from app.db.base import engine, Base
from app.models import (
    User, Student, Teacher,
    Class, ClassStudent,
    Problem, ProblemContent, TestCase,
    Session, StepAttempt, ErrorDiagnosis,
    Skill, SkillState, SkillDependency
)


def test_all_models_imported():
    """Test that all models are properly imported"""
    assert User is not None
    assert Student is not None
    assert Teacher is not None
    assert Class is not None
    assert ClassStudent is not None
    assert Problem is not None
    assert ProblemContent is not None
    assert TestCase is not None
    assert Session is not None
    assert StepAttempt is not None
    assert ErrorDiagnosis is not None
    assert Skill is not None
    assert SkillState is not None
    assert SkillDependency is not None


def test_models_have_tablenames():
    """Test that all models have table names defined"""
    models = [
        User, Student, Teacher,
        Class, ClassStudent,
        Problem, ProblemContent, TestCase,
        Session, StepAttempt, ErrorDiagnosis,
        Skill, SkillState, SkillDependency
    ]

    for model in models:
        assert hasattr(model, '__tablename__')
        assert model.__tablename__ is not None


def test_base_metadata_has_tables():
    """Test that Base metadata contains all tables"""
    expected_tables = {
        'users', 'students', 'teachers',
        'classes', 'class_students',
        'problems', 'problem_contents', 'test_cases',
        'sessions', 'step_attempts', 'error_diagnoses',
        'skills', 'skill_states', 'skill_dependencies'
    }

    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables), \
        f"Missing tables: {expected_tables - actual_tables}"


def test_user_model_structure():
    """Test User model has required fields"""
    assert hasattr(User, 'id')
    assert hasattr(User, 'email')
    assert hasattr(User, 'password_hash')
    assert hasattr(User, 'role')
    assert hasattr(User, 'created_at')
    assert hasattr(User, 'last_login')


def test_student_model_structure():
    """Test Student model has required fields"""
    assert hasattr(Student, 'teacher_id')
    assert hasattr(Student, 'total_problems_solved')
    assert hasattr(Student, 'average_scaffold_level')
    assert hasattr(Student, 'bkt_parameters')


def test_problem_model_structure():
    """Test Problem model has required fields"""
    assert hasattr(Problem, 'skill_id')
    assert hasattr(Problem, 'type')
    assert hasattr(Problem, 'difficulty')
    assert hasattr(Problem, 'solution_steps')
    assert hasattr(Problem, 'created_by')


def test_session_model_structure():
    """Test Session model has required fields"""
    assert hasattr(Session, 'student_id')
    assert hasattr(Session, 'problem_id')
    assert hasattr(Session, 'started_at')
    assert hasattr(Session, 'current_step')
    assert hasattr(Session, 'scaffold_level')


def test_skill_model_structure():
    """Test Skill model has required fields"""
    assert hasattr(Skill, 'id')
    assert hasattr(Skill, 'name')
    assert hasattr(Skill, 'category')


def test_skill_state_model_structure():
    """Test SkillState model has required fields"""
    assert hasattr(SkillState, 'student_id')
    assert hasattr(SkillState, 'skill_id')
    assert hasattr(SkillState, 'domain_probability')
    assert hasattr(SkillState, 'status')
    assert hasattr(SkillState, 'problems_attempted')
    assert hasattr(SkillState, 'problems_solved')


def test_enums_defined():
    """Test that all enums are properly defined"""
    from app.models.user import UserRole
    from app.models.problem import ProblemType, Language
    from app.models.session import ScaffoldLevel, ErrorType
    from app.models.skill import SkillStatus

    # Test UserRole
    assert hasattr(UserRole, 'STUDENT')
    assert hasattr(UserRole, 'TEACHER')

    # Test ProblemType
    assert hasattr(ProblemType, 'MATH')
    assert hasattr(ProblemType, 'CODE')

    # Test Language
    assert hasattr(Language, 'PYTHON')
    assert hasattr(Language, 'CPP')
    assert hasattr(Language, 'JAVA')

    # Test ScaffoldLevel
    assert hasattr(ScaffoldLevel, 'LEVEL_1')
    assert hasattr(ScaffoldLevel, 'LEVEL_2')
    assert hasattr(ScaffoldLevel, 'LEVEL_3')

    # Test ErrorType
    assert hasattr(ErrorType, 'SYNTAX')
    assert hasattr(ErrorType, 'PROCEDURE')
    assert hasattr(ErrorType, 'CONCEPT')

    # Test SkillStatus
    assert hasattr(SkillStatus, 'LOCKED')
    assert hasattr(SkillStatus, 'AVAILABLE')
    assert hasattr(SkillStatus, 'IN_PROGRESS')
    assert hasattr(SkillStatus, 'MASTERED')

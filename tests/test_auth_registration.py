"""Tests for user registration functionality"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, get_db
from app.main import app
from app.models.user import User, Student, Teacher, UserRole
from app.core.security import verify_password
from app.core.config import settings

# Use PostgreSQL test database
TEST_DATABASE_URL = str(settings.DATABASE_URL).replace(
    "/elenchos", "/elenchos_test")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
        db.rollback()  # Rollback any uncommitted changes
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


class TestUserRegistration:
    """Test user registration functionality"""

    def test_register_student_success(self, client, db_session):
        """Test successful student registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "student@example.com",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "student@example.com"
        assert data["role"] == "STUDENT"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data

        # Verify user was created in database
        user = db_session.query(User).filter(
            User.email == "student@example.com").first()
        assert user is not None
        assert isinstance(user, Student)
        assert user.role == UserRole.STUDENT

    def test_register_teacher_success(self, client, db_session):
        """Test successful teacher registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "teacher@example.com",
                "password": "password123",
                "role": "TEACHER"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "teacher@example.com"
        assert data["role"] == "TEACHER"
        assert "id" in data

        # Verify user was created in database
        user = db_session.query(User).filter(
            User.email == "teacher@example.com").first()
        assert user is not None
        assert isinstance(user, Teacher)
        assert user.role == UserRole.TEACHER

    def test_password_is_hashed(self, client, db_session):
        """Test that password is hashed using bcrypt"""
        plain_password = "password123"
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": plain_password,
                "role": "STUDENT"
            }
        )

        assert response.status_code == 201

        # Verify password is hashed in database
        user = db_session.query(User).filter(
            User.email == "test@example.com").first()
        assert user.password_hash != plain_password
        assert user.password_hash.startswith("$2b$")  # bcrypt hash prefix

        # Verify password can be verified
        assert verify_password(plain_password, user.password_hash)

    def test_email_validation_invalid_format(self, client):
        """Test email validation rejects invalid formats"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_email_validation_missing_domain(self, client):
        """Test email validation rejects missing domain"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 422

    def test_email_normalized_to_lowercase(self, client, db_session):
        """Test that email is normalized to lowercase"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "User@Example.COM",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "user@example.com"

        # Verify in database
        user = db_session.query(User).filter(
            User.email == "user@example.com").first()
        assert user is not None

    def test_duplicate_email_rejected(self, client, db_session):
        """Test that duplicate email registration is rejected"""
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        # Try to register with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "different456",
                "role": "TEACHER"
            }
        )

        assert response.status_code == 400
        assert "ya está registrado" in response.json()["detail"].lower()

    def test_password_minimum_length(self, client):
        """Test password must be at least 8 characters"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 422

    def test_password_requires_letter(self, client):
        """Test password must contain at least one letter"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "12345678",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 422

    def test_password_requires_number(self, client):
        """Test password must contain at least one number"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "abcdefgh",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 422

    def test_role_assignment_student(self, client, db_session):
        """Test STUDENT role is correctly assigned"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "student@example.com",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 201
        user = db_session.query(User).filter(
            User.email == "student@example.com").first()
        assert user.role == UserRole.STUDENT
        assert isinstance(user, Student)
        assert user.total_problems_solved == 0
        assert user.average_scaffold_level == 0.0

    def test_role_assignment_teacher(self, client, db_session):
        """Test TEACHER role is correctly assigned"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "teacher@example.com",
                "password": "password123",
                "role": "TEACHER"
            }
        )

        assert response.status_code == 201
        user = db_session.query(User).filter(
            User.email == "teacher@example.com").first()
        assert user.role == UserRole.TEACHER
        assert isinstance(user, Teacher)

    def test_invalid_role_rejected(self, client):
        """Test invalid role is rejected"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "role": "ADMIN"
            }
        )

        assert response.status_code == 422

    def test_missing_required_fields(self, client):
        """Test registration fails with missing required fields"""
        # Missing password
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "role": "STUDENT"
            }
        )
        assert response.status_code == 422

        # Missing email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "password": "password123",
                "role": "STUDENT"
            }
        )
        assert response.status_code == 422

        # Missing role
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 422

    def test_student_initialized_with_defaults(self, client, db_session):
        """Test student is initialized with default values"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "student@example.com",
                "password": "password123",
                "role": "STUDENT"
            }
        )

        assert response.status_code == 201
        student = db_session.query(Student).filter(
            Student.email == "student@example.com").first()
        assert student.total_problems_solved == 0
        assert student.average_scaffold_level == 0.0
        assert student.bkt_parameters == {}
        assert student.teacher_id is None

    def test_teacher_initialized_with_defaults(self, client, db_session):
        """Test teacher is initialized with default values"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "teacher@example.com",
                "password": "password123",
                "role": "TEACHER"
            }
        )

        assert response.status_code == 201
        teacher = db_session.query(Teacher).filter(
            Teacher.email == "teacher@example.com").first()
        assert teacher.notion_page_ids == []
        assert teacher.alert_preferences == {}
        assert teacher.notion_token is None

"""Authentication service for user registration and login"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from uuid import UUID

from app.models.user import User, Student, Teacher, UserRole
from app.schemas.user import UserRegister
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user with password hashing

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Created user instance (Student or Teacher)

        Raises:
            HTTPException: If email already exists or registration fails
        """
        # Check if email already exists
        existing_user = db.query(User).filter(
            User.email == user_data.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya está registrado"
            )

        # Hash the password using bcrypt
        hashed_password = hash_password(user_data.password)

        try:
            # Create user based on role
            if user_data.role == UserRole.STUDENT:
                new_user = Student(
                    email=user_data.email.lower(),
                    password_hash=hashed_password,
                    role=UserRole.STUDENT,
                    total_problems_solved=0,
                    average_scaffold_level=0.0,
                    bkt_parameters={}
                )
            elif user_data.role == UserRole.TEACHER:
                new_user = Teacher(
                    email=user_data.email.lower(),
                    password_hash=hashed_password,
                    role=UserRole.TEACHER,
                    notion_page_ids=[],
                    alert_preferences={}
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rol de usuario inválido"
                )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al registrar usuario. El email puede estar ya en uso."
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno al registrar usuario: {str(e)}"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            User instance if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            User instance or None
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            db: Database session
            email: User email

        Returns:
            User instance or None
        """
        return db.query(User).filter(User.email == email.lower()).first()

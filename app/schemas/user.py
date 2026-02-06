"""User schemas for request/response validation"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import UserRole
import re


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr


class UserRegister(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """
        Validate email format

        Args:
            v: Email string to validate

        Returns:
            Validated email string

        Raises:
            ValueError: If email format is invalid
        """
        # EmailStr already validates basic format, but we can add additional checks
        if not v or len(v) < 3:
            raise ValueError("Email debe tener al menos 3 caracteres")

        # Check for valid domain
        if '@' not in v:
            raise ValueError("Email debe contener @")

        local, domain = v.rsplit('@', 1)
        if not local or not domain:
            raise ValueError(
                "Email debe tener formato válido: usuario@dominio.com")

        if '.' not in domain:
            raise ValueError("Dominio del email debe contener un punto")

        return v.lower()  # Normalize to lowercase

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength

        Args:
            v: Password string to validate

        Returns:
            Validated password string

        Raises:
            ValueError: If password doesn't meet requirements
        """
        if len(v) < 8:
            raise ValueError("Contraseña debe tener al menos 8 caracteres")

        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError("Contraseña debe contener al menos una letra")

        # Check for at least one number
        if not re.search(r'\d', v):
            raise ValueError("Contraseña debe contener al menos un número")

        return v


class UserResponse(UserBase):
    """Schema for user response"""
    id: UUID
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class StudentResponse(UserResponse):
    """Schema for student response"""
    teacher_id: Optional[UUID] = None
    total_problems_solved: int
    average_scaffold_level: float

    model_config = {
        "from_attributes": True
    }


class TeacherResponse(UserResponse):
    """Schema for teacher response"""
    notion_token: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

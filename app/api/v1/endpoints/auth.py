"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.user import UserRegister, UserResponse, StudentResponse, TeacherResponse
from app.services.auth_service import AuthService
from app.models.user import UserRole

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario (alumno o profesor)

    - **email**: Email válido del usuario
    - **password**: Contraseña (mínimo 8 caracteres, debe contener letras y números)
    - **role**: Rol del usuario (STUDENT o TEACHER)

    Retorna el usuario creado con su información básica.
    """
    user = AuthService.register_user(db, user_data)

    # Return appropriate response based on role
    if user.role == UserRole.STUDENT:
        return StudentResponse.model_validate(user)
    else:
        return TeacherResponse.model_validate(user)

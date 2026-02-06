"""Main API router"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Placeholder for future endpoint routers
# api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
# api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
# api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])


@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Elenchos API v1",
        "status": "operational"
    }

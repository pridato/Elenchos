"""Verify infrastructure setup"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def verify_imports():
    """Verify all models can be imported"""
    print("Verifying model imports...")
    try:
        from app.models import (
            User, Student, Teacher, UserRole,
            Class, ClassStudent,
            Problem, ProblemContent, TestCase, ProblemType, Language,
            Session, StepAttempt, ErrorDiagnosis, ScaffoldLevel, ErrorType,
            Skill, SkillState, SkillDependency, SkillStatus
        )
        print("✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error importing models: {e}")
        return False


def verify_database_config():
    """Verify database configuration"""
    print("\nVerifying database configuration...")
    try:
        from app.db.base import engine, Base, SessionLocal
        from app.core.config import settings

        print(f"✓ Database URL: {settings.DATABASE_URL}")
        print(f"✓ Engine created: {engine}")
        print(f"✓ SessionLocal factory: {SessionLocal}")
        print(f"✓ Base metadata tables: {len(Base.metadata.tables)}")

        # List all tables
        print("\nRegistered tables:")
        for table_name in sorted(Base.metadata.tables.keys()):
            print(f"  - {table_name}")

        return True
    except Exception as e:
        print(f"✗ Error with database config: {e}")
        return False


def verify_logging():
    """Verify logging configuration"""
    print("\nVerifying logging configuration...")
    try:
        from app.core.logging import setup_logging, get_logger

        logger = get_logger(__name__)
        logger.info("Test log message")
        print("✓ Logging configured successfully")
        return True
    except Exception as e:
        print(f"✗ Error with logging: {e}")
        return False


def verify_fastapi():
    """Verify FastAPI application"""
    print("\nVerifying FastAPI application...")
    try:
        from app.main import app
        from app.core.config import settings

        print(f"✓ FastAPI app created: {app.title}")
        print(f"✓ Version: {settings.VERSION}")
        print(f"✓ API prefix: {settings.API_V1_STR}")
        return True
    except Exception as e:
        print(f"✗ Error with FastAPI: {e}")
        return False


def verify_alembic():
    """Verify Alembic configuration"""
    print("\nVerifying Alembic configuration...")
    try:
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        print("✓ Alembic configuration loaded")
        return True
    except Exception as e:
        print(f"✗ Error with Alembic: {e}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Elenchos Infrastructure Verification")
    print("=" * 60)

    checks = [
        verify_imports,
        verify_database_config,
        verify_logging,
        verify_fastapi,
        verify_alembic,
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"✗ Unexpected error in {check.__name__}: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} checks passed")
    print("=" * 60)

    if all(results):
        print("\n✓ All infrastructure components verified successfully!")
        return 0
    else:
        print("\n✗ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""Complete database setup script"""
import sys
from pathlib import Path

# Add parent directory to path FIRST
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from sqlalchemy import text
    from alembic import command
    from alembic.config import Config
    from app.models import *  # Import all models
    from app.db.base import engine, Base
    from app.core.config import settings
    from app.core.logging import setup_logging, get_logger
except ImportError as e:
    print(f"❌ Error: Missing dependencies. Please install requirements first:")
    print(f"   pip install -r requirements.txt")
    print(f"\n📋 Details: {e}")
    sys.exit(1)

logger = get_logger(__name__)


def check_database_connection():
    """Check if database is accessible"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        return False


def run_migrations():
    """Run Alembic migrations"""
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}", exc_info=True)
        return False


def setup_database(use_migrations: bool = False):
    """
    Complete database setup

    Args:
        use_migrations: If True, use Alembic migrations. If False, create tables directly.
    """
    setup_logging()

    logger.info("Starting database setup...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")

    # Check connection
    if not check_database_connection():
        logger.error(
            "Cannot connect to database. Please check your configuration.")
        return False

    # Setup tables
    if use_migrations:
        success = run_migrations()
    else:
        success = create_tables()

    if success:
        logger.info("Database setup completed successfully!")
    else:
        logger.error("Database setup failed!")

    return success


if __name__ == "__main__":
    # Use migrations if --migrate flag is provided
    use_migrations = "--migrate" in sys.argv
    success = setup_database(use_migrations=use_migrations)
    sys.exit(0 if success else 1)

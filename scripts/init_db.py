"""Initialize database with initial migration"""
from app.core.logging import setup_logging, get_logger
from app.models import *  # Import all models
from app.db.base import Base, engine
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


logger = get_logger(__name__)


def init_db():
    """Initialize database tables"""
    try:
        setup_logging()
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)

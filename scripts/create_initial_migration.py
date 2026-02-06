"""Script to create initial Alembic migration"""
from alembic import command
from alembic.config import Config
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def create_initial_migration():
    """Create initial migration with all models"""
    alembic_cfg = Config("alembic.ini")

    print("Creating initial migration...")
    command.revision(
        alembic_cfg,
        autogenerate=True,
        message="initial_schema"
    )
    print("Initial migration created successfully!")


if __name__ == "__main__":
    create_initial_migration()

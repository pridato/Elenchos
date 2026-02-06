# Project Structure

## Directory Layout

```
elenchos/
├── app/                    # Main application code
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   ├── core/             # Core configuration and utilities
│   ├── db/               # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas (validation)
│   ├── services/         # Business logic layer
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── scripts/              # Utility scripts
├── tests/                # Test suite
├── docs/                 # Documentation
└── .kiro/                # Kiro AI assistant configuration
    ├── specs/            # Feature specifications
    └── steering/         # AI guidance rules
```

## Architecture Patterns

### Layered Architecture

1. **API Layer** (`app/api/`): FastAPI routers and endpoints
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Model Layer** (`app/models/`): SQLAlchemy ORM models
4. **Schema Layer** (`app/schemas/`): Pydantic models for validation

### Model Organization

All models inherit from base mixins:
- `TimestampMixin`: Adds `created_at` and `updated_at` fields
- `UUIDMixin`: Adds UUID primary key

Models are organized by domain:
- **User Management**: `User`, `Student`, `Teacher`
- **Class Management**: `Class`, `ClassStudent`
- **Problem Management**: `Problem`, `ProblemContent`, `TestCase`
- **Session Tracking**: `Session`, `StepAttempt`, `ErrorDiagnosis`
- **Skill Tree**: `Skill`, `SkillState`, `SkillDependency`

### Configuration Management

- Environment variables loaded via `.env` file
- Settings centralized in `app/core/config.py`
- Uses Pydantic Settings for validation and type safety
- Validators for complex configuration (CORS, database URL)

### Database Conventions

- Use Alembic for all schema changes
- UUID primary keys for all entities
- Timestamps on all tables (`created_at`, `updated_at`)
- Foreign keys with explicit naming
- Indexes on frequently queried fields

### API Conventions

- RESTful endpoint design
- Versioned API (`/api/v1/`)
- Consistent response formats
- OpenAPI/Swagger documentation auto-generated
- CORS middleware configured

### Logging

- Centralized logging setup in `app/core/logging.py`
- JSON format for structured logging
- Configurable log level via environment

## File Naming

- Python files: `snake_case.py`
- Models: Singular nouns (`user.py`, `problem.py`)
- Services: Domain-based (`auth_service.py`, `problem_service.py`)
- Tests: `test_*.py` prefix

## Import Conventions

- Absolute imports from `app` package
- Group imports: stdlib, third-party, local
- Use `from app.core.config import settings` for configuration

## Development Workflow

1. Create feature branch
2. Write/update models if needed
3. Create Alembic migration: `make db-migrate msg="description"`
4. Apply migration: `make db-upgrade`
5. Implement service layer logic
6. Create API endpoints
7. Write tests
8. Run tests: `make test`

## Docker Services

Services defined in `docker-compose.yml`:
- **postgres**: Port 5432, persistent volume
- **redis**: Port 6379, persistent volume
- **chromadb**: Port 8000, persistent volume

All services include health checks for reliability.

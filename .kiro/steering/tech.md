# Technology Stack

## Core Framework

- **FastAPI**: Web framework for building APIs
- **Python 3.11+**: Primary language
- **SQLAlchemy 2.0**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation and settings management

## Database & Storage

- **PostgreSQL 15**: Primary database
- **Redis 7**: Caching and session storage
- **ChromaDB**: Vector database for RAG (Retrieval-Augmented Generation)

## AI & ML

- **Anthropic API**: Claude LLM integration
- **Google Generative AI**: Gemini integration
- **Sentence Transformers**: Text embeddings
- **SymPy**: Symbolic mathematics and formal verification
- **scikit-learn**: ML models for clustering and prediction
- **pandas/numpy**: Data analysis

## Infrastructure

- **Docker**: Container runtime for code sandbox
- **Docker Compose**: Local development services
- **Celery**: Asynchronous task queue
- **Uvicorn**: ASGI server

## Authentication & Security

- **python-jose**: JWT token handling
- **passlib[bcrypt]**: Password hashing

## Testing

- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for API testing
- **hypothesis**: Property-based testing

## Common Commands

### Development Setup
```bash
make install          # Install dependencies
make db-up           # Start PostgreSQL, Redis, ChromaDB
make db-setup        # Create database tables
make run             # Start development server (localhost:8000)
```

### Database Operations
```bash
make db-migrate msg="description"  # Create new migration
make db-upgrade                    # Apply migrations
make db-downgrade                  # Revert last migration
```

### Testing & Quality
```bash
make test            # Run test suite
make test-cov        # Run tests with coverage report
make clean           # Remove temporary files and caches
```

### Manual Commands
```bash
# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest -v

# Database migrations
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Environment Configuration

Configuration via `.env` file (see `.env.example`). Key settings managed through `app/core/config.py` using Pydantic Settings.

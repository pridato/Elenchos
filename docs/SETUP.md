# Elenchos - Setup Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL client (optional, for manual database access)

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd elenchos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=elenchos
POSTGRES_PASSWORD=elenchos
POSTGRES_DB=elenchos
POSTGRES_PORT=5432

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI Models
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 3. Start Database Services

```bash
# Start PostgreSQL, Redis, and ChromaDB
make db-up

# Wait for services to be healthy (check with docker ps)
docker ps
```

### 4. Initialize Database

```bash
# Create database tables
make db-setup

# Or use Alembic migrations
make db-upgrade
```

### 5. Run the Application

```bash
# Start development server
make run

# Server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

## Database Management

### Creating Migrations

When you modify models, create a new migration:

```bash
make db-migrate msg="description of changes"
```

### Applying Migrations

```bash
make db-upgrade
```

### Rolling Back Migrations

```bash
make db-downgrade
```

### Manual Migration Creation

```bash
alembic revision -m "migration name"
```

## Project Structure

```
elenchos/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── logging.py    # Logging configuration
│   ├── db/               # Database configuration
│   │   └── base.py       # SQLAlchemy base
│   ├── models/           # Database models
│   │   ├── user.py       # User, Student, Teacher
│   │   ├── class_model.py # Class, ClassStudent
│   │   ├── problem.py    # Problem, ProblemContent, TestCase
│   │   ├── session.py    # Session, StepAttempt, ErrorDiagnosis
│   │   └── skill.py      # Skill, SkillState, SkillDependency
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── tests/                # Test suite
├── docker-compose.yml    # Docker services
├── Makefile              # Common commands
└── requirements.txt      # Python dependencies
```

## Data Models

### User Models
- **User**: Base user with email, password, role
- **Student**: Extends User with BKT parameters, skill states
- **Teacher**: Extends User with Notion integration, classes

### Problem Models
- **Problem**: Problem definition with type (MATH/CODE)
- **ProblemContent**: Problem content (text, LaTeX, code)
- **TestCase**: Unit tests for code problems

### Session Models
- **Session**: Student problem-solving session
- **StepAttempt**: Individual step attempts with timing
- **ErrorDiagnosis**: Error classification and details

### Skill Models
- **Skill**: Skill tree node with dependencies
- **SkillState**: Student progress on a skill (BKT)
- **SkillDependency**: Skill prerequisite relationships

### Class Models
- **Class**: Teacher's class with invitation code
- **ClassStudent**: Student-class membership

## Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_models.py -v
```

## Troubleshooting

### Database Connection Issues

1. Check if PostgreSQL is running:
   ```bash
   docker ps | grep postgres
   ```

2. Test connection:
   ```bash
   psql -h localhost -U elenchos -d elenchos
   ```

3. Check logs:
   ```bash
   docker logs elenchos_postgres
   ```

### ChromaDB Issues

1. Check if ChromaDB is running:
   ```bash
   curl http://localhost:8000/api/v1/heartbeat
   ```

2. Check logs:
   ```bash
   docker logs elenchos_chromadb
   ```

### Migration Issues

1. Check current migration status:
   ```bash
   alembic current
   ```

2. View migration history:
   ```bash
   alembic history
   ```

3. Reset database (WARNING: destroys all data):
   ```bash
   make db-down
   docker volume rm elenchos_postgres_data
   make db-up
   make db-setup
   ```

## Development Workflow

1. Create a feature branch
2. Modify models if needed
3. Create migration: `make db-migrate msg="add new field"`
4. Apply migration: `make db-upgrade`
5. Write tests
6. Run tests: `make test`
7. Commit and push

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

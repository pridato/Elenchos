# Elenchos

Plataforma educativa con enfoque neuro-simbólico para el aprendizaje de ciencias exactas y programación.

## Descripción

Elenchos combina la flexibilidad de los Large Language Models (LLMs) con la precisión de la verificación formal matemática y de código, utilizando el método socrático para guiar a los estudiantes hacia la comprensión profunda.

## Características Principales

- **Verificación Formal Matemática**: Validación rigurosa usando SymPy
- **Sandbox de Código Seguro**: Ejecución aislada en Docker
- **Andamiaje Socrático**: Ayuda gradual en 3 niveles
- **RAG Personalizado**: Integración con contenido del profesor desde Notion
- **BKT Engine**: Modelado probabilístico del conocimiento
- **Análisis ML**: Clustering de arquetipos y predicción de riesgo

## Requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker (para sandbox de código)
- ChromaDB (opcional, para RAG)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd elenchos
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Iniciar servicios con Docker Compose

```bash
docker-compose up -d
```

### 6. Ejecutar migraciones

```bash
alembic upgrade head
```

### 7. Iniciar servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Uso con Docker Compose

El proyecto incluye un `docker-compose.yml` que configura:
- PostgreSQL
- Redis
- ChromaDB (opcional)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## Estructura del Proyecto

```
elenchos/
├── app/
│   ├── api/              # Endpoints de la API
│   ├── core/             # Configuración y utilidades
│   ├── db/               # Configuración de base de datos
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Esquemas Pydantic
│   ├── services/         # Lógica de negocio
│   └── main.py           # Punto de entrada
├── alembic/              # Migraciones de base de datos
├── tests/                # Tests
├── .env.example          # Ejemplo de variables de entorno
├── docker-compose.yml    # Configuración de Docker
├── pyproject.toml        # Dependencias Poetry
└── requirements.txt      # Dependencias pip
```

## API Documentation

Una vez iniciado el servidor, la documentación interactiva está disponible en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=app

# Ejecutar tests específicos
pytest tests/test_models.py
```

## Migraciones de Base de Datos

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history
```

## Desarrollo

### Agregar nuevas dependencias

```bash
# Con pip
pip install <package>
pip freeze > requirements.txt

# Con poetry
poetry add <package>
```

### Formato de código

```bash
# Formatear con black
black app/

# Linting con ruff
ruff check app/
```

## Licencia

[Especificar licencia]

## Contribución

[Especificar guías de contribución]
# Elenchos

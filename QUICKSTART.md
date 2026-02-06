# Elenchos - Quick Start

## Task 1 Completed ✅

La infraestructura base ha sido configurada exitosamente. Todos los modelos de datos, configuración de base de datos, logging y sistema de migraciones están listos.

## Comenzar a Usar el Sistema

### 1. Instalar Dependencias

```bash
# Activar entorno virtual (si no está activo)
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Editar .env con tus configuraciones
# Mínimo requerido:
# - POSTGRES_* (ya configurado para desarrollo local)
# - SECRET_KEY (cambiar en producción)
```

### 3. Iniciar Servicios de Base de Datos

```bash
# Iniciar PostgreSQL, Redis y ChromaDB
make db-up

# Verificar que estén corriendo
docker ps
```

### 4. Crear Tablas de Base de Datos

```bash
# Opción 1: Crear tablas directamente
make db-setup

# Opción 2: Usar migraciones de Alembic
alembic revision --autogenerate -m "initial_schema"
make db-upgrade
```

### 5. Verificar Instalación

```bash
# Ejecutar script de verificación
python scripts/verify_setup.py
```

### 6. Iniciar Servidor de Desarrollo

```bash
# Iniciar FastAPI
make run

# El servidor estará disponible en:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

## Estructura del Proyecto

```
elenchos/
├── app/
│   ├── models/          # 14 modelos de datos completos
│   ├── core/            # Configuración y logging
│   ├── db/              # SQLAlchemy setup
│   ├── api/             # Endpoints (próximas tareas)
│   └── main.py          # FastAPI app
├── alembic/             # Migraciones de BD
├── scripts/             # Scripts de utilidad
├── tests/               # Tests
└── docs/                # Documentación
```

## Modelos Disponibles

- **User, Student, Teacher** - Gestión de usuarios
- **Class, ClassStudent** - Clases y membresías
- **Problem, ProblemContent, TestCase** - Problemas y tests
- **Session, StepAttempt, ErrorDiagnosis** - Sesiones de resolución
- **Skill, SkillState, SkillDependency** - Árbol de habilidades

## Comandos Útiles

```bash
# Base de datos
make db-up              # Iniciar servicios
make db-down            # Detener servicios
make db-setup           # Crear tablas
make db-migrate msg=""  # Nueva migración
make db-upgrade         # Aplicar migraciones

# Desarrollo
make run                # Iniciar servidor
make test               # Ejecutar tests
make clean              # Limpiar archivos temporales

# Verificación
python scripts/verify_setup.py  # Verificar setup
```

## Próximas Tareas

Según el plan de implementación (`.kiro/specs/elenchos/tasks.md`):

- **Task 2**: Sistema de autenticación y autorización
- **Task 3**: Gestión de clases e invitaciones
- **Task 4**: Checkpoint - Sistema de autenticación funcional

## Documentación Completa

- **docs/SETUP.md** - Guía detallada de configuración
- **docs/TASK_1_SUMMARY.md** - Resumen de Task 1
- **.kiro/specs/elenchos/** - Especificaciones completas
  - requirements.md - Requirements del sistema
  - design.md - Diseño arquitectónico
  - tasks.md - Plan de implementación

## Soporte

Si encuentras problemas:

1. Verifica que Docker esté corriendo: `docker ps`
2. Revisa logs de servicios: `docker logs elenchos_postgres`
3. Consulta docs/SETUP.md para troubleshooting
4. Ejecuta `python scripts/verify_setup.py` para diagnóstico

## Estado del Proyecto

✅ **Task 1 Completada**: Infraestructura base y modelos de datos
⏳ **Task 2 Pendiente**: Sistema de autenticación

¡El proyecto está listo para continuar con el desarrollo! 🚀

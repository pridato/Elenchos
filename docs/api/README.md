# API de Elenchos - Guía Rápida

## Índice

- [Registro de Usuarios](./registro-usuarios.md) - Documentación completa del endpoint de registro

## Endpoints Disponibles

### Autenticación

| Método | Endpoint | Descripción | Documentación |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Registrar nuevo usuario | [Ver docs](./registro-usuarios.md) |
| POST | `/api/v1/auth/login` | Iniciar sesión | _Próximamente_ |

## Quick Start

### 1. Iniciar el servidor

```bash
# Iniciar servicios de base de datos
make db-up

# Aplicar migraciones
make db-upgrade

# Iniciar servidor de desarrollo
make run
```

El servidor estará disponible en: http://localhost:8000

### 2. Ver documentación interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. Registrar tu primer usuario

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu-email@example.com",
    "password": "TuPassword123",
    "role": "STUDENT"
  }'
```

## Estructura de Respuestas

### Success Response

```json
{
  "id": "uuid",
  "email": "string",
  "role": "STUDENT | TEACHER",
  "created_at": "datetime",
  ...
}
```

### Error Response

```json
{
  "detail": "Mensaje de error descriptivo"
}
```

## Roles de Usuario

### STUDENT (Alumno)
- Resuelve problemas
- Recibe andamiaje socrático
- Tiene árbol de habilidades
- Se une a clases

### TEACHER (Profesor)
- Crea clases y problemas
- Sincroniza contenido desde Notion
- Monitorea progreso de alumnos
- Autoriza avances

## Validaciones Comunes

### Email
- ✅ Formato válido: `usuario@dominio.com`
- ✅ Se normaliza a minúsculas
- ❌ No puede estar duplicado

### Password
- ✅ Mínimo 8 caracteres
- ✅ Debe contener al menos una letra
- ✅ Debe contener al menos un número
- ❌ Se hashea con bcrypt (nunca se almacena en texto plano)

## Códigos de Estado HTTP

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Error en los datos (ej: email duplicado) |
| 401 | Unauthorized | No autenticado |
| 403 | Forbidden | No autorizado |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Error de validación |
| 500 | Internal Server Error | Error del servidor |

## Ejemplos Rápidos

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'Password123',
    role: 'STUDENT'
  })
});

const user = await response.json();
```

### Python

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/auth/register',
    json={
        'email': 'user@example.com',
        'password': 'Password123',
        'role': 'STUDENT'
    }
)

user = response.json()
```

### cURL

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Password123","role":"STUDENT"}'
```

## Recursos Adicionales

- [Documentación completa de Registro](./registro-usuarios.md)
- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [Health Check](http://localhost:8000/health)

## Próximos Endpoints

- [ ] Login de usuarios
- [ ] Refresh de tokens
- [ ] Gestión de clases
- [ ] Gestión de problemas
- [ ] Árbol de habilidades
- [ ] Panel del profesor

---

**Nota:** Esta API está en desarrollo activo. Consulta la documentación específica de cada endpoint para detalles completos.

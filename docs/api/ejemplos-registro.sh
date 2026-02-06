#!/bin/bash

# Ejemplos de uso del endpoint de registro de Elenchos
# Asegúrate de que el servidor esté corriendo: make run

BASE_URL="http://localhost:8000/api/v1"

echo "========================================="
echo "Ejemplos de Registro de Usuarios"
echo "========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para hacer requests con formato bonito
make_request() {
    local description=$1
    local data=$2
    
    echo -e "${YELLOW}📝 $description${NC}"
    echo "Request:"
    echo "$data" | python3 -m json.tool
    echo ""
    echo "Response:"
    
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/register" \
        -H "Content-Type: application/json" \
        -d "$data")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✓ Success (201 Created)${NC}"
        echo "$body" | python3 -m json.tool
    elif [ "$http_code" -eq 400 ]; then
        echo -e "${RED}✗ Error (400 Bad Request)${NC}"
        echo "$body" | python3 -m json.tool
    elif [ "$http_code" -eq 422 ]; then
        echo -e "${RED}✗ Error (422 Validation Error)${NC}"
        echo "$body" | python3 -m json.tool
    else
        echo -e "${RED}✗ Error ($http_code)${NC}"
        echo "$body"
    fi
    
    echo ""
    echo "========================================="
    echo ""
}

# Ejemplo 1: Registrar un alumno exitosamente
make_request "Ejemplo 1: Registrar un alumno" '{
  "email": "maria.garcia@example.com",
  "password": "MiPassword123",
  "role": "STUDENT"
}'

# Ejemplo 2: Registrar un profesor exitosamente
make_request "Ejemplo 2: Registrar un profesor" '{
  "email": "prof.rodriguez@university.edu",
  "password": "SecurePass456",
  "role": "TEACHER"
}'

# Ejemplo 3: Error - Email duplicado
make_request "Ejemplo 3: Intentar registrar email duplicado" '{
  "email": "maria.garcia@example.com",
  "password": "OtraPassword789",
  "role": "STUDENT"
}'

# Ejemplo 4: Error - Email inválido
make_request "Ejemplo 4: Email inválido" '{
  "email": "email-sin-arroba",
  "password": "Password123",
  "role": "STUDENT"
}'

# Ejemplo 5: Error - Contraseña muy corta
make_request "Ejemplo 5: Contraseña muy corta" '{
  "email": "nuevo1@example.com",
  "password": "abc",
  "role": "STUDENT"
}'

# Ejemplo 6: Error - Contraseña sin número
make_request "Ejemplo 6: Contraseña sin número" '{
  "email": "nuevo2@example.com",
  "password": "abcdefgh",
  "role": "STUDENT"
}'

# Ejemplo 7: Error - Contraseña sin letra
make_request "Ejemplo 7: Contraseña sin letra" '{
  "email": "nuevo3@example.com",
  "password": "12345678",
  "role": "STUDENT"
}'

# Ejemplo 8: Error - Rol inválido
make_request "Ejemplo 8: Rol inválido" '{
  "email": "nuevo4@example.com",
  "password": "Password123",
  "role": "ADMIN"
}'

# Ejemplo 9: Email con mayúsculas (se normaliza)
make_request "Ejemplo 9: Email con mayúsculas (se normaliza)" '{
  "email": "Usuario@EXAMPLE.COM",
  "password": "Password123",
  "role": "STUDENT"
}'

echo ""
echo -e "${GREEN}✓ Ejemplos completados${NC}"
echo ""
echo "Para limpiar la base de datos de prueba:"
echo "  PGPASSWORD=elenchos psql -U elenchos -h localhost -d elenchos_test -c 'TRUNCATE users, students, teachers CASCADE;'"

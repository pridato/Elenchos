# Documento de Diseño - Elenchos

## Overview

Elenchos es una plataforma educativa que implementa un enfoque neuro-simbólico para el aprendizaje de ciencias exactas y programación. El sistema combina la flexibilidad de los Large Language Models (LLMs) con la precisión de la verificación formal matemática y de código, utilizando el método socrático para guiar a los estudiantes hacia la comprensión profunda.

La arquitectura del sistema sigue un patrón de microservicios orquestados, donde cada componente tiene una responsabilidad específica:

- **Frontend (Next.js/React)**: Interfaces de usuario para alumnos y profesores
- **Backend (FastAPI/Python)**: Orquestación de servicios y lógica de negocio
- **Motor Matemático (SymPy)**: Verificación formal de equivalencia algebraica
- **Sandbox de Código (Docker)**: Ejecución aislada y validación de código
- **Orquestador de IA (Claude/Gemini)**: Generación de contenido pedagógico
- **RAG Engine (ChromaDB)**: Recuperación de contenido personalizado del profesor
- **BKT Engine**: Modelado probabilístico del conocimiento del alumno
- **Análisis ML**: Clustering de arquetipos y predicción de riesgo

El flujo principal del sistema sigue estos pasos:

1. **Ingesta**: El alumno envía un problema (texto, imagen, código)
2. **Clasificación**: El sistema determina si es Ciencias o Programación
3. **Verificación Formal**: SymPy o Docker Sandbox valida la respuesta
4. **Diagnóstico**: Se clasifica el error (Sintaxis, Procedimiento, Concepto)
5. **Andamiaje**: Se proporciona ayuda gradual (3 niveles)
6. **Actualización**: Se actualiza el perfil del alumno (BKT, Árbol de Habilidades)

## Architecture

### Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│  ┌──────────────────────┐      ┌──────────────────────────┐   │
│  │  Interfaz Alumno     │      │  Interfaz Profesor       │   │
│  │  - Chat Multimodal   │      │  - Panel de Control      │   │
│  │  - Árbol Habilidades │      │  - Semáforo de Riesgo    │   │
│  │  - Visualización     │      │  - Métricas en Tiempo    │   │
│  └──────────────────────┘      └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (FastAPI)                      │
│                    - Autenticación JWT                          │
│                    - Rate Limiting                              │
│                    - Request Routing                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Orquestador Principal                       │  │
│  │  - Clasificación de Problemas                            │  │
│  │  - Routing a Motores de Verificación                     │  │
│  │  - Gestión de Estado de Sesión                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Motor           │ │  Sandbox         │ │  Orquestador     │
│  Matemático      │ │  Código          │ │  IA              │
│  (SymPy)         │ │  (Docker)        │ │  (Claude/Gemini) │
└──────────────────┘ └──────────────────┘ └──────────────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INTELLIGENCE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Motor        │  │ RAG Engine   │  │ Análisis ML          │ │
│  │ Socrático    │  │ (ChromaDB)   │  │ - BKT Engine         │ │
│  │              │  │              │  │ - Clustering         │ │
│  │              │  │              │  │ - Sentiment Analysis │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
│  ┌──────────────────────┐      ┌──────────────────────────┐   │
│  │  PostgreSQL          │      │  ChromaDB                │   │
│  │  - Usuarios          │      │  - Embeddings            │   │
│  │  - Clases            │      │  - Contenido Profesor    │   │
│  │  │  - Problemas       │      │                          │   │
│  │  - Histórico         │      │                          │   │
│  │  - Árbol Habilidades │      │                          │   │
│  └──────────────────────┘      └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Patrones Arquitectónicos

**1. Microservicios Orquestados**
- Cada componente (Motor Matemático, Sandbox, IA) es independiente
- Comunicación mediante API REST interna
- Permite escalado horizontal de componentes individuales

**2. Event-Driven para Actualizaciones en Tiempo Real**
- WebSocket para comunicación bidireccional con frontend
- Eventos: `problem_submitted`, `verification_complete`, `help_requested`, `skill_updated`
- Permite notificaciones push al profesor sobre alertas de riesgo

**3. Strategy Pattern para Verificación**
- Interfaz común `Verifier` con implementaciones: `MathVerifier`, `CodeVerifier`
- Selección dinámica basada en clasificación del problema
- Facilita agregar nuevos tipos de verificación (ej: física, química)

**4. Chain of Responsibility para Andamiaje**
- Cada nivel de andamiaje es un handler en la cadena
- Nivel 1 → Nivel 2 → Nivel 3
- Permite agregar nuevos niveles sin modificar código existente

## Components and Interfaces

### 1. API Gateway

**Responsabilidad**: Punto de entrada único para todas las solicitudes del frontend.

**Endpoints Principales**:

```python
# Autenticación
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh

# Problemas
POST /api/v1/problems/submit
GET /api/v1/problems/{problem_id}/status
POST /api/v1/problems/{problem_id}/step

# Árbol de Habilidades
GET /api/v1/skills/tree
GET /api/v1/skills/{skill_id}/progress

# Profesor
GET /api/v1/teacher/dashboard
GET /api/v1/teacher/students/{student_id}/progress
POST /api/v1/teacher/students/{student_id}/authorize-advance
GET /api/v1/teacher/risk-alerts

# Sincronización Notion
POST /api/v1/teacher/sync-notion
GET /api/v1/teacher/sync-status
```

**Interfaz**:

```python
class APIGateway:
    def authenticate_request(self, token: str) -> User:
        """Valida JWT y retorna usuario autenticado"""
        
    def rate_limit_check(self, user_id: str, endpoint: str) -> bool:
        """Verifica límites de tasa para prevenir abuso"""
        
    def route_request(self, request: Request) -> Response:
        """Enruta solicitud al servicio apropiado"""
```

### 2. Orquestador Principal

**Responsabilidad**: Coordinar el flujo de procesamiento de problemas y gestionar el estado de sesión.

**Interfaz**:

```python
class ProblemOrchestrator:
    def classify_problem(self, content: ProblemContent) -> ProblemType:
        """
        Clasifica el problema como MATH o CODE
        
        Args:
            content: Contenido del problema (texto, imagen, código)
            
        Returns:
            ProblemType.MATH o ProblemType.CODE
        """
        
    def process_submission(self, problem: Problem, student: Student) -> VerificationResult:
        """
        Procesa una sumisión de problema completa
        
        Flujo:
        1. Clasificar problema
        2. Seleccionar verificador apropiado
        3. Ejecutar verificación
        4. Diagnosticar error si existe
        5. Generar respuesta (andamiaje o confirmación)
        6. Actualizar perfil del estudiante
        
        Returns:
            Resultado de verificación con feedback
        """
        
    def get_session_state(self, session_id: str) -> SessionState:
        """Recupera estado de sesión para continuidad"""
```

### 3. Motor Matemático (SymPy)

**Responsabilidad**: Verificación formal de equivalencia algebraica.

**Interfaz**:

```python
class MathVerifier:
    def verify_step(self, previous_expr: str, current_expr: str, 
                   context: MathContext) -> VerificationResult:
        """
        Verifica si current_expr es algebraicamente equivalente a previous_expr
        
        Args:
            previous_expr: Expresión matemática del paso anterior (LaTeX o texto)
            current_expr: Expresión propuesta por el alumno
            context: Contexto con variables, dominio, restricciones
            
        Returns:
            VerificationResult con:
            - is_correct: bool
            - error_type: ErrorType | None (SYNTAX, PROCEDURE, CONCEPT)
            - error_details: str
            
        Proceso:
        1. Parsear ambas expresiones a SymPy
        2. Simplificar ambas expresiones
        3. Verificar equivalencia usando simplify(expr1 - expr2) == 0
        4. Si no son equivalentes, diagnosticar tipo de error
        """
        
    def parse_latex(self, latex: str) -> sympy.Expr:
        """Convierte LaTeX a expresión SymPy"""
        
    def diagnose_error(self, expected: sympy.Expr, actual: sympy.Expr) -> ErrorDiagnosis:
        """
        Diagnostica el tipo de error cometido
        
        Heurísticas:
        - SYNTAX: Error de parsing o símbolos inválidos
        - PROCEDURE: Operación algebraica incorrecta (ej: distribución mal hecha)
        - CONCEPT: Malentendido fundamental (ej: confundir suma con producto)
        """
```

**Ejemplo de Uso**:

```python
# Paso anterior: 2x + 4 = 10
# Paso alumno: 2x = 6

verifier = MathVerifier()
result = verifier.verify_step(
    previous_expr="2*x + 4 = 10",
    current_expr="2*x = 6",
    context=MathContext(variables=["x"])
)

# result.is_correct = True
# (porque 2x = 6 es equivalente a 2x + 4 = 10 después de restar 4)
```

### 4. Sandbox de Código (Docker)

**Responsabilidad**: Ejecución aislada y segura de código con validación contra unit tests.

**Interfaz**:

```python
class CodeSandbox:
    def execute_code(self, code: str, language: Language, 
                    test_cases: List[TestCase], 
                    limits: ResourceLimits) -> ExecutionResult:
        """
        Ejecuta código en contenedor Docker aislado
        
        Args:
            code: Código fuente a ejecutar
            language: PYTHON | CPP | JAVA
            test_cases: Lista de casos de prueba con input/expected_output
            limits: Límites de CPU (1s), memoria (256MB), sin red
            
        Returns:
            ExecutionResult con:
            - passed: bool
            - failed_tests: List[TestCase]
            - error_type: ErrorType | None
            - execution_time: float
            - memory_used: int
            
        Proceso:
        1. Crear contenedor Docker efímero
        2. Copiar código al contenedor
        3. Ejecutar código con cada test case
        4. Capturar stdout/stderr
        5. Comparar output con expected
        6. Destruir contenedor
        """
        
    def build_docker_image(self, language: Language) -> str:
        """Construye imagen Docker base para el lenguaje"""
        
    def enforce_limits(self, container_id: str, limits: ResourceLimits):
        """Aplica límites de recursos al contenedor"""
```

**Configuración Docker**:

```dockerfile
# Imagen base para Python
FROM python:3.11-slim

# Sin privilegios
USER nobody

# Sin acceso a red
NETWORK none

# Límites de recursos
MEMORY 256m
CPU 1.0

# Timeout
TIMEOUT 1s
```

### 5. Orquestador de IA

**Responsabilidad**: Generar contenido pedagógico usando LLMs (Claude 3.5, Gemini Pro).

**Interfaz**:

```python
class AIOrchestrator:
    def generate_socratic_question(self, error: ErrorDiagnosis, 
                                   level: ScaffoldLevel,
                                   rag_context: Optional[str] = None) -> str:
        """
        Genera pregunta socrática basada en el error y nivel de andamiaje
        
        Args:
            error: Diagnóstico del error cometido
            level: LEVEL_1 (reflexión) | LEVEL_2 (pista) | LEVEL_3 (analogía)
            rag_context: Contenido relevante del profesor (opcional)
            
        Returns:
            Pregunta o pista generada
            
        Prompts por nivel:
        - Nivel 1: "¿Qué operación aplicaste aquí? ¿Es válida para ambos lados?"
        - Nivel 2: "Recuerda que [concepto del RAG]. ¿Cómo se aplica aquí?"
        - Nivel 3: "Piensa en esto como [analogía simple]. ¿Ves la conexión?"
        """
        
    def analyze_sentiment(self, text: str) -> SentimentScore:
        """
        Analiza el sentimiento del texto del alumno
        
        Returns:
            SentimentScore con:
            - frustration_level: float (0.0 - 1.0)
            - confidence_level: float (0.0 - 1.0)
            - needs_encouragement: bool
        """
        
    def select_model(self, task: AITask) -> LLMModel:
        """
        Selecciona el modelo apropiado para la tarea
        
        - Claude 3.5: Preguntas socráticas complejas, analogías
        - Gemini Pro: Análisis de sentimiento, clasificación rápida
        """
```

### 6. Motor Socrático

**Responsabilidad**: Gestionar el andamiaje gradual y decidir cuándo escalar niveles.

**Interfaz**:

```python
class SocraticEngine:
    def provide_help(self, student: Student, error: ErrorDiagnosis, 
                    attempt_count: int) -> ScaffoldResponse:
        """
        Proporciona ayuda gradual basada en intentos
        
        Lógica de escalamiento:
        - Intento 1: Nivel 1 (pregunta reflexiva)
        - Intento 2-3: Nivel 2 (pista con RAG)
        - Intento 4+: Nivel 3 (analogía simplificada)
        
        Returns:
            ScaffoldResponse con:
            - level: ScaffoldLevel
            - content: str (pregunta/pista/analogía)
            - should_alert_teacher: bool (si attempt_count > 5)
        """
        
    def block_solution_access(self, student: Student, problem: Problem) -> bool:
        """
        Determina si el alumno puede ver la solución completa
        
        Reglas:
        - Debe haber completado todos los pasos intermedios
        - O tener autorización explícita del profesor
        """
```

### 7. RAG Engine

**Responsabilidad**: Recuperar contenido relevante del profesor para personalización.

**Interfaz**:

```python
class RAGEngine:
    def sync_notion_content(self, notion_token: str, page_ids: List[str]) -> SyncResult:
        """
        Sincroniza contenido desde Notion
        
        Proceso:
        1. Conectar a Notion API
        2. Descargar páginas especificadas
        3. Extraer texto y estructura
        4. Generar embeddings con modelo de embeddings
        5. Almacenar en ChromaDB
        """
        
    def retrieve_relevant_content(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Recupera contenido relevante usando búsqueda vectorial
        
        Args:
            query: Descripción del concepto o error
            top_k: Número de documentos a recuperar
            
        Returns:
            Lista de documentos ordenados por relevancia
        """
        
    def generate_embeddings(self, text: str) -> np.ndarray:
        """Genera embeddings usando modelo (ej: sentence-transformers)"""
```

### 8. BKT Engine

**Responsabilidad**: Modelar probabilísticamente el conocimiento del alumno.

**Interfaz**:

```python
class BKTEngine:
    def update_knowledge_state(self, student: Student, skill: Skill, 
                              action: StudentAction) -> float:
        """
        Actualiza probabilidad de dominio usando Bayesian Knowledge Tracing
        
        Fórmula:
        L(t+1) = P(L(t)|Acción) + (1 - P(L(t)|Acción)) · P(T)
        
        Donde:
        - L(t): Probabilidad de dominio en tiempo t
        - P(T): Probabilidad de transición (aprender)
        - Acción: CORRECT | INCORRECT | HELP_REQUESTED
        
        Parámetros del modelo:
        - P(L0): Probabilidad inicial de conocimiento (0.1)
        - P(T): Probabilidad de aprender (0.3)
        - P(S): Probabilidad de slip (error por descuido) (0.1)
        - P(G): Probabilidad de guess (acierto por suerte) (0.2)
        
        Returns:
            Nueva probabilidad de dominio L(t+1)
        """
        
    def should_advance(self, student: Student, skill: Skill) -> bool:
        """
        Determina si el alumno puede avanzar
        
        Regla: L(t) >= 0.7 (70% de probabilidad de dominio)
        """
        
    def suggest_reinforcement(self, student: Student) -> List[Skill]:
        """
        Sugiere habilidades que necesitan refuerzo
        
        Retorna habilidades con L(t) < 0.7
        """
```

### 9. Análisis ML

**Responsabilidad**: Clustering de arquetipos y predicción de riesgo.

**Interfaz**:

```python
class MLAnalyzer:
    def cluster_students(self, students: List[Student], 
                        error_history: Dict[str, List[Error]]) -> ClusterResult:
        """
        Agrupa alumnos por patrones de error usando K-Means o DBSCAN
        
        Features para clustering:
        - Frecuencia de errores por tipo (sintaxis, procedimiento, concepto)
        - Latencia promedio de respuesta
        - Nivel de andamiaje promedio requerido
        - Tasa de éxito por categoría de problema
        
        Returns:
            ClusterResult con:
            - clusters: Dict[int, List[Student]]
            - archetypes: Dict[int, str] (ej: "Falla por base aritmética")
            - centroids: np.ndarray
        """
        
    def predict_failure_risk(self, student: Student, 
                            recent_activity: List[Activity]) -> RiskPrediction:
        """
        Predice riesgo de fracaso semanal usando Random Forest/XGBoost
        
        Features:
        - Latencia promedio últimos 7 días
        - Tasa de errores últimos 7 días
        - Nivel de andamiaje promedio
        - Días sin actividad
        - Sentimiento promedio (frustración)
        
        Returns:
            RiskPrediction con:
            - risk_score: float (0.0 - 1.0)
            - risk_level: LOW | MEDIUM | HIGH
            - contributing_factors: List[str]
        """
        
    def train_models(self, training_data: pd.DataFrame):
        """Entrena modelos de clustering y clasificación"""
```

### 10. Gestión de Árbol de Habilidades

**Responsabilidad**: Mantener y actualizar el grafo de dependencias de habilidades.

**Interfaz**:

```python
class SkillTreeManager:
    def get_student_tree(self, student: Student) -> SkillTree:
        """
        Retorna árbol de habilidades con estado actual del alumno
        
        Cada nodo contiene:
        - skill_id: str
        - name: str
        - domain_level: float (de BKT)
        - status: LOCKED | AVAILABLE | IN_PROGRESS | MASTERED
        - dependencies: List[str] (skill_ids requeridos)
        """
        
    def update_skill_status(self, student: Student, skill: Skill, 
                           new_domain: float):
        """
        Actualiza estado de habilidad y desbloquea dependientes si aplica
        
        Lógica:
        - Si new_domain >= 0.7: status = MASTERED
        - Si MASTERED: desbloquear habilidades que dependen de esta
        """
        
    def check_prerequisites(self, student: Student, skill: Skill) -> bool:
        """Verifica si el alumno cumple prerequisitos para una habilidad"""
```

## Data Models

### Modelos de Usuario

```python
class User(BaseModel):
    id: UUID
    email: EmailStr
    password_hash: str  # bcrypt
    role: UserRole  # STUDENT | TEACHER
    created_at: datetime
    last_login: datetime

class Student(User):
    teacher_id: UUID
    class_id: UUID
    skill_tree_state: Dict[str, SkillState]
    bkt_parameters: Dict[str, BKTParams]
    total_problems_solved: int
    average_scaffold_level: float
    
class Teacher(User):
    notion_token: Optional[str]
    notion_page_ids: List[str]
    classes: List[UUID]
    alert_preferences: AlertPreferences

class SkillState(BaseModel):
    skill_id: str
    domain_probability: float  # L(t) del BKT
    status: SkillStatus  # LOCKED | AVAILABLE | IN_PROGRESS | MASTERED
    problems_attempted: int
    problems_solved: int
    last_activity: datetime

class BKTParams(BaseModel):
    """Parámetros del modelo BKT por habilidad"""
    P_L0: float = 0.1  # Probabilidad inicial
    P_T: float = 0.3   # Probabilidad de aprender
    P_S: float = 0.1   # Probabilidad de slip
    P_G: float = 0.2   # Probabilidad de guess
```

### Modelos de Problema

```python
class Problem(BaseModel):
    id: UUID
    skill_id: str
    type: ProblemType  # MATH | CODE
    content: ProblemContent
    difficulty: int  # 1-5
    unit_tests: Optional[List[TestCase]]  # Para CODE
    solution_steps: List[str]  # Pasos esperados
    created_by: UUID  # teacher_id
    
class ProblemContent(BaseModel):
    text: Optional[str]
    latex: Optional[str]
    image_url: Optional[str]
    code_template: Optional[str]
    language: Optional[Language]  # PYTHON | CPP | JAVA

class TestCase(BaseModel):
    input: str
    expected_output: str
    description: str
    is_hidden: bool  # Tests ocultos para prevenir hardcoding
```

### Modelos de Sesión

```python
class Session(BaseModel):
    id: UUID
    student_id: UUID
    problem_id: UUID
    started_at: datetime
    current_step: int
    steps_history: List[StepAttempt]
    scaffold_level: ScaffoldLevel
    sentiment_scores: List[SentimentScore]
    
class StepAttempt(BaseModel):
    step_number: int
    student_answer: str
    is_correct: bool
    error_diagnosis: Optional[ErrorDiagnosis]
    scaffold_provided: Optional[ScaffoldResponse]
    timestamp: datetime
    latency_seconds: float  # Tiempo desde pregunta hasta respuesta

class ErrorDiagnosis(BaseModel):
    error_type: ErrorType  # SYNTAX | PROCEDURE | CONCEPT
    error_details: str
    affected_concept: str
    severity: int  # 1-5
```

### Modelos de Verificación

```python
class VerificationResult(BaseModel):
    is_correct: bool
    error_diagnosis: Optional[ErrorDiagnosis]
    execution_time: Optional[float]  # Para CODE
    memory_used: Optional[int]  # Para CODE
    feedback: str
    
class MathContext(BaseModel):
    variables: List[str]
    domain: str  # "real" | "complex" | "integer"
    constraints: List[str]  # ej: ["x > 0", "y != 0"]

class ExecutionResult(BaseModel):
    passed: bool
    failed_tests: List[TestCase]
    error_type: Optional[ErrorType]
    execution_time: float
    memory_used: int
    stdout: str
    stderr: str
```

### Modelos de Andamiaje

```python
class ScaffoldResponse(BaseModel):
    level: ScaffoldLevel  # LEVEL_1 | LEVEL_2 | LEVEL_3
    content: str
    should_alert_teacher: bool
    rag_sources: Optional[List[str]]  # URLs de Notion si aplica
    
class ScaffoldLevel(Enum):
    LEVEL_1 = "reflexion"  # Pregunta socrática
    LEVEL_2 = "pista"      # Pista con RAG
    LEVEL_3 = "analogia"   # Analogía simplificada
```

### Modelos de Análisis

```python
class ClusterResult(BaseModel):
    clusters: Dict[int, List[UUID]]  # cluster_id -> student_ids
    archetypes: Dict[int, str]  # cluster_id -> descripción
    centroids: List[List[float]]
    silhouette_score: float  # Métrica de calidad del clustering
    
class RiskPrediction(BaseModel):
    student_id: UUID
    risk_score: float  # 0.0 - 1.0
    risk_level: RiskLevel  # LOW | MEDIUM | HIGH
    contributing_factors: List[str]
    recommended_actions: List[str]
    
class SentimentScore(BaseModel):
    frustration_level: float  # 0.0 - 1.0
    confidence_level: float  # 0.0 - 1.0
    needs_encouragement: bool
    timestamp: datetime
```

### Modelos de RAG

```python
class Document(BaseModel):
    id: UUID
    content: str
    source: str  # URL de Notion
    embedding: List[float]
    metadata: Dict[str, Any]
    teacher_id: UUID
    
class SyncResult(BaseModel):
    success: bool
    documents_synced: int
    errors: List[str]
    last_sync: datetime
```

## Correctness Properties

*Una propiedad es una característica o comportamiento que debe mantenerse verdadero en todas las ejecuciones válidas de un sistema - esencialmente, una declaración formal sobre lo que el sistema debe hacer. Las propiedades sirven como puente entre las especificaciones legibles por humanos y las garantías de corrección verificables por máquinas.*

### Property 1: Clasificación Consistente de Problemas
*Para cualquier* contenido que contenga ecuaciones matemáticas (LaTeX, texto con símbolos matemáticos, o imágenes con OCR de ecuaciones), el sistema debe clasificarlo como tipo "Ciencias", y *para cualquier* contenido que contenga código fuente en Python, C++ o Java, el sistema debe clasificarlo como tipo "Programación".
**Validates: Requirements 1.1, 1.2, 1.3, 1.4**

### Property 2: Verificación de Equivalencia Algebraica y Avance
*Para cualquier* par de expresiones matemáticas algebraicamente equivalentes, el Motor Matemático debe verificar la equivalencia correctamente y permitir al alumno avanzar al siguiente paso.
**Validates: Requirements 2.1, 2.3**

### Property 3: Diagnóstico Completo de Errores Matemáticos
*Para cualquier* error matemático detectado, el sistema debe clasificarlo en exactamente una de tres categorías (Sintaxis, Procedimiento, o Concepto) e identificar la naturaleza específica del error según su tipo.
**Validates: Requirements 2.2, 4.1, 4.2, 4.3, 4.4**

### Property 4: Validación Simbólica de Variables
*Para cualquier* expresión matemática que contenga variables simbólicas, el Motor Matemático debe validar la equivalencia para todos los valores válidos del dominio, no solo para valores numéricos específicos.
**Validates: Requirements 2.4**

### Property 5: Validación de Código contra Unit Tests
*Para cualquier* código ejecutado en el Sandbox y conjunto de unit tests, si todos los tests pasan, el sistema debe marcar el paso como correcto; si algún test falla, debe proporcionar información del test fallido sin revelar la solución completa.
**Validates: Requirements 3.2, 3.4, 3.5**

### Property 6: Andamiaje Gradual Progresivo
*Para cualquier* alumno que comete un error, el Motor Socrático debe proporcionar ayuda comenzando en Nivel 1 (pregunta reflexiva), escalando a Nivel 2 (pista con RAG) si permanece bloqueado, y finalmente a Nivel 3 (analogía simplificada) si continúa bloqueado, registrando el nivel utilizado cuando se resuelve.
**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

### Property 7: Bloqueo de Soluciones Completas
*Para cualquier* problema con pasos intermedios, el sistema debe bloquear el acceso a la solución completa hasta que el alumno haya superado todos los pasos intermedios o tenga autorización explícita del profesor.
**Validates: Requirements 5.6**

### Property 8: Persistencia de Contenido RAG
*Para cualquier* contenido importado desde Notion, el RAG Engine debe vectorizarlo y almacenarlo en ChromaDB, y cuando el Motor Socrático necesite proporcionar una pista de Nivel 2, debe recuperar contenido relevante de los apuntes del profesor.
**Validates: Requirements 6.2, 6.3**

### Property 9: Actualización de Dominio en Árbol de Habilidades
*Para cualquier* alumno que completa exitosamente problemas de una habilidad, el sistema debe actualizar el nivel de Dominio de esa habilidad basándose en precisión, velocidad y nivel de andamiaje requerido.
**Validates: Requirements 7.2, 7.5**

### Property 10: Gestión de Dependencias de Habilidades
*Para cualquier* habilidad con dependencias no cumplidas, el sistema debe bloquear el acceso a esa habilidad, y cuando un alumno alcanza dominio suficiente (≥0.7) en una habilidad, debe desbloquear las habilidades dependientes.
**Validates: Requirements 7.3, 7.4**

### Property 11: Alertas de Riesgo por Frustración
*Para cualquier* alumno que muestra señales de frustración (múltiples errores consecutivos o bloqueado por más de un umbral configurable), el sistema debe generar una alerta en el Semáforo de Riesgo y notificar al profesor.
**Validates: Requirements 8.2, 8.3**

### Property 12: Autorización de Avance sin Requisitos
*Para cualquier* alumno que solicita avanzar sin cumplir requisitos de dominio, el sistema debe requerir autorización explícita del profesor antes de permitir el avance.
**Validates: Requirements 8.5**

### Property 13: Integración de Contexto en Contenido Pedagógico
*Para cualquier* contenido pedagógico generado por el Orquestador de IA, debe incluir el contexto del error diagnosticado y el nivel de andamiaje, y si el RAG Engine proporciona contenido del profesor, debe integrarlo en la respuesta sin revelar soluciones completas.
**Validates: Requirements 9.2, 9.3, 9.5**

### Property 14: Creación y Autenticación de Usuarios
*Para cualquier* usuario que se registra, el sistema debe crear una cuenta con rol de Alumno o Profesor, y cuando un usuario inicia sesión, debe autenticar credenciales y generar un token de sesión.
**Validates: Requirements 10.1, 10.2**

### Property 15: Gestión de Clases e Invitaciones
*Para cualquier* profesor que crea una clase, el sistema debe generar códigos de invitación únicos, y cuando un alumno usa un código de invitación válido, debe asociar al alumno con la clase del profesor correctamente.
**Validates: Requirements 10.3, 10.4**

### Property 16: Seguridad de Contraseñas
*Para cualquier* contraseña almacenada en el sistema, debe estar hasheada usando bcrypt o Argon2, nunca en texto plano.
**Validates: Requirements 10.5**

### Property 17: Rate Limiting de Autenticación
*Para cualquier* usuario que intenta autenticarse, el sistema debe implementar rate limiting para prevenir ataques de fuerza bruta, bloqueando intentos excesivos desde la misma IP o cuenta.
**Validates: Requirements 10.6**

### Property 18: Persistencia Completa de Datos
*Para cualquier* operación de creación o actualización (usuarios, intentos de resolución, árbol de habilidades, embeddings), el sistema debe persistir los datos en la base de datos apropiada (PostgreSQL o ChromaDB) manteniendo integridad referencial.
**Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**

### Property 19: Formato JSON Estandarizado en API
*Para cualquier* solicitud del frontend, el sistema debe responder usando formato JSON estandarizado, y cuando ocurre un error, debe retornar códigos HTTP apropiados (4xx para errores de cliente, 5xx para errores de servidor) con mensajes descriptivos.
**Validates: Requirements 12.1, 12.2**

### Property 20: Procesamiento Asíncrono de Operaciones Largas
*Para cualquier* problema enviado para verificación que excede 2 segundos de procesamiento, el sistema debe procesar la solicitud de forma asíncrona y notificar al cliente cuando esté completa.
**Validates: Requirements 12.3**

### Property 21: Estructura Completa del Árbol de Habilidades
*Para cualquier* solicitud del estado del Árbol de Habilidades, el sistema debe retornar la estructura completa con todos los nodos y sus estados actualizados (skill_id, name, domain_level, status, dependencies).
**Validates: Requirements 12.4**

### Property 22: Manejo Graceful de Errores del Motor Matemático
*Para cualquier* fallo del Motor Matemático al procesar una expresión, el sistema debe notificar al alumno con un mensaje descriptivo y registrar el error para revisión sin interrumpir la sesión.
**Validates: Requirements 14.1**

### Property 23: Manejo de Errores del Sandbox
*Para cualquier* fallo del Sandbox de Código al ejecutar código, el sistema debe proporcionar un mensaje de error descriptivo indicando la naturaleza del problema (timeout, límite de memoria, error de compilación, etc.).
**Validates: Requirements 14.2**

### Property 24: Fallback para Timeout de IA
*Para cualquier* solicitud al Orquestador de IA que no responde en 30 segundos, el sistema debe usar una respuesta de fallback predefinida apropiada al contexto para no bloquear al alumno.
**Validates: Requirements 14.3**

### Property 25: Resiliencia de Conexión a PostgreSQL
*Para cualquier* pérdida de conexión a PostgreSQL, el sistema debe reintentar la conexión con backoff exponencial (1s, 2s, 4s, 8s, ...) hasta un máximo de intentos antes de fallar.
**Validates: Requirements 14.4**

### Property 26: Degradación Graceful sin RAG
*Para cualquier* situación donde ChromaDB no está disponible, el sistema debe funcionar sin RAG usando solo el Orquestador de IA, proporcionando ayuda de Nivel 1 y 3 pero omitiendo Nivel 2.
**Validates: Requirements 14.5**

### Property 27: Logging Centralizado de Errores
*Para cualquier* error que ocurra en el sistema (verificación, ejecución, IA, base de datos), debe registrarse en un sistema de logging centralizado con timestamp, contexto, y stack trace.
**Validates: Requirements 14.6**

### Property 28: Almacenamiento de Histórico de Errores
*Para cualquier* error cometido por un alumno, el sistema debe almacenar el error en el histórico del alumno con información completa (tipo, detalles, concepto afectado, timestamp) para análisis de patrones.
**Validates: Requirements 4.5**

### Property 29: Actualización BKT tras Interacción
*Para cualquier* interacción del alumno con un problema (correcto, incorrecto, ayuda solicitada), el motor BKT debe actualizar la probabilidad de dominio L(t+1) usando la fórmula: L(t+1) = P(L(t)|Acción) + (1 - P(L(t)|Acción)) · P(T).
**Validates: Requirements 16.1, 16.2**

### Property 30: Sugerencia de Refuerzo por Dominio Bajo
*Para cualquier* habilidad donde la probabilidad de dominio del alumno sea inferior al 70%, el sistema debe sugerir actividades de refuerzo de conceptos base antes de permitir el avance a habilidades dependientes.
**Validates: Requirements 16.3**

### Property 31: Predicción de Riesgo de Fracaso
*Para cualquier* alumno, el sistema debe ejecutar un modelo de Clasificación Binaria (Random Forest o XGBoost) para predecir el riesgo de fracaso semanal basado en latencia, errores, nivel de andamiaje y días sin actividad, retornando un score de riesgo (0.0-1.0) y nivel (LOW/MEDIUM/HIGH).
**Validates: Requirements 16.4**

### Property 32: Clustering Semanal de Arquetipos
*Para cualquier* conjunto de alumnos, el sistema debe ejecutar semanalmente un algoritmo de Clustering (K-Means o DBSCAN) sobre el histórico de errores y clasificar a los alumnos en arquetipos identificables (ej: "Falla por base aritmética" vs "Falla por lógica procedimental").
**Validates: Requirements 17.1, 17.2**

### Property 33: Análisis de Sentimiento en Chat
*Para cualquier* texto introducido por un alumno en el chat, el Orquestador de IA debe realizar un Análisis de Sentimiento, y si se detecta "Frustración Alta", el Motor Socrático debe priorizar el refuerzo positivo y analogías simplificadas.
**Validates: Requirements 18.1, 18.2**


## Error Handling

### Estrategia General de Manejo de Errores

El sistema implementa una estrategia de manejo de errores en capas que garantiza resiliencia y proporciona feedback útil a los usuarios:

1. **Validación en el Frontend**: Validación básica de entrada antes de enviar al backend
2. **Validación en API Gateway**: Validación de esquema y autenticación
3. **Manejo en Servicios**: Cada servicio maneja sus propios errores específicos
4. **Logging Centralizado**: Todos los errores se registran para análisis
5. **Respuestas Descriptivas**: Mensajes de error claros para usuarios y desarrolladores

### Categorías de Errores

**Errores de Usuario (4xx)**:
- 400: Entrada inválida, expresiones mal formadas
- 401: Token JWT inválido, credenciales incorrectas
- 403: Acceso no autorizado a recursos
- 404: Recurso no encontrado
- 429: Rate limiting activado

**Errores de Sistema (5xx)**:
- 500: Error inesperado del servidor
- 503: Servicio no disponible (BD, ChromaDB, Docker)
- 504: Timeout de operación

### Manejo Específico por Componente

**Motor Matemático**: Maneja errores de parsing identificando problemas específicos (paréntesis desbalanceados, símbolos inválidos) y proporciona mensajes descriptivos sin interrumpir la sesión.

**Sandbox de Código**: Maneja timeouts (>1s), límites de memoria (>256MB), errores de runtime y compilación con mensajes específicos y hints de optimización.

**Orquestador de IA**: Implementa fallbacks para timeouts (respuestas predefinidas por nivel de andamiaje) y errores de API (cambio a modelo alternativo o respuestas genéricas).

**Base de Datos**: Implementa retry con backoff exponencial (1s, 2s, 4s, 8s, 16s) para PostgreSQL y degradación graceful para ChromaDB (continuar sin RAG).

### Logging y Monitoreo

Todos los errores se registran con:
- Timestamp, tipo de error, stack trace
- Usuario afectado, operación que falló
- Estado del sistema
- Envío a sistema centralizado (ELK Stack, CloudWatch)
- Alertas para errores críticos

Métricas trackeadas:
- Tasa de errores por endpoint y componente
- Tiempo de recuperación
- Errores por usuario
- Timeouts de IA
- Fallos de conexión a BD

## Testing Strategy

### Enfoque Dual: Unit Tests + Property-Based Tests

El sistema utiliza un enfoque complementario:

1. **Unit Tests**: Validan ejemplos específicos, casos edge y condiciones de error
2. **Property-Based Tests**: Validan propiedades universales a través de muchos inputs generados

Ambos son necesarios para cobertura completa:
- Unit tests capturan bugs concretos y casos específicos
- Property tests verifican corrección general y descubren casos edge inesperados

### Configuración de Property-Based Testing

**Biblioteca**: `hypothesis` (Python)

**Configuración Estándar**:
```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)  # Mínimo 100 iteraciones
@given(...)
def test_property_X(...):
    """
    Feature: elenchos, Property X: [descripción]
    """
    pass
```

**Requisitos**:
- Mínimo 100 iteraciones por propiedad (debido a randomización)
- Tag con referencia a propiedad del diseño
- Formato: `Feature: elenchos, Property {número}: {texto}`

### Property Tests Clave

**Motor Matemático**:
- Property 2: Verificación de equivalencia algebraica
- Property 3: Diagnóstico completo de errores (Sintaxis/Procedimiento/Concepto)
- Property 4: Validación simbólica de variables

**Sandbox de Código**:
- Property 5: Validación contra unit tests sin revelar solución

**Motor Socrático**:
- Property 6: Andamiaje gradual (Nivel 1 → 2 → 3)
- Property 7: Bloqueo de soluciones completas

**BKT Engine**:
- Property 29: Actualización correcta de L(t+1) usando fórmula BKT
- Property 30: Sugerencia de refuerzo cuando L < 0.7

**Árbol de Habilidades**:
- Property 10: Bloqueo/desbloqueo basado en dependencias

**Seguridad**:
- Property 16: Contraseñas hasheadas (bcrypt/Argon2)
- Property 17: Rate limiting de autenticación

### Unit Tests Complementarios

Los unit tests se enfocan en:
- **Ejemplos Específicos**: Casos concretos conocidos
- **Casos Edge**: División por cero, límites, valores extremos
- **Integración**: Interacción entre componentes
- **Seguridad**: Aislamiento de red del sandbox, inyección SQL

### Cobertura de Testing

**Objetivos**:
- Cobertura de código: >= 80%
- Cobertura de propiedades: 100% (todas las 33 propiedades del diseño)
- Casos edge: Identificados y testeados explícitamente

**Métricas**:
- Propiedades implementadas vs diseñadas
- Iteraciones por property test (mínimo 100)
- Tasa de fallos en property tests
- Tiempo de ejecución de test suite

### CI/CD Integration

```yaml
test:
  unit_tests:
    command: pytest tests/unit -v --cov=src --cov-report=html
    coverage_threshold: 80%

  property_tests:
    command: pytest tests/properties -v --hypothesis-show-statistics
    min_examples: 100

  integration_tests:
    command: pytest tests/integration -v
    requires: [postgres, chromadb, docker]
```


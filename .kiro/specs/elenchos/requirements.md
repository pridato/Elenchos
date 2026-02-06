# Documento de Requirements - Elenchos

## Introducción

Elenchos es una plataforma educativa que transforma el aprendizaje pasivo de ciencias exactas y programación en un proceso de pensamiento crítico guiado. El sistema combina la creatividad de la IA con el rigor de la validación formal matemática y de código, utilizando el método socrático para guiar a los estudiantes hacia la comprensión profunda en lugar de la simple copia de soluciones.

El problema central que resuelve Elenchos es el "Efecto Photomath": estudiantes que copian soluciones sin procesar los conceptos subyacentes. La plataforma implementa un enfoque neuro-simbólico que bloquea el acceso a soluciones completas hasta que el estudiante demuestre comprensión de los pasos intermedios.

## Glosario

- **Sistema**: La plataforma completa Elenchos
- **Motor_Socrático**: Componente que genera preguntas reflexivas y gestiona el andamiaje pedagógico
- **Motor_Matemático**: Componente basado en SymPy que valida equivalencia algebraica
- **Sandbox_Código**: Entorno Docker aislado para ejecución y validación de código
- **Orquestador_IA**: Componente que coordina los LLMs (Claude/Gemini) para pedagogía
- **RAG_Engine**: Sistema de recuperación aumentada con vectores para contenido del profesor
- **Alumno**: Usuario estudiante que interactúa con el sistema
- **Profesor**: Usuario docente que supervisa y configura el aprendizaje
- **Árbol_Habilidades**: Estructura de conocimientos y dependencias del plan de estudios
- **Nivel_Andamiaje**: Grado de ayuda proporcionada (1=reflexión, 2=pista, 3=analogía)
- **Dominio**: Métrica de comprensión del alumno en una habilidad específica
- **Paso_Intermedio**: Etapa de resolución que debe validarse antes de avanzar
- **Verificación_Formal**: Proceso de validación rigurosa (matemática o código)
- **BKT_Engine**: Motor de Bayesian Knowledge Tracing para modelado probabilístico del conocimiento
- **Probabilidad_Dominio**: Métrica L que representa la probabilidad de que el alumno domine una habilidad
- **Arquetipo**: Patrón de error identificado mediante clustering de alumnos con problemas similares
- **Análisis_Sentimiento**: Proceso de NLP para detectar el estado emocional del alumno

## Requirements

### Requirement 1: Ingesta y Clasificación de Problemas

**User Story:** Como alumno, quiero enviar problemas de ciencias exactas o programación en múltiples formatos, para que el sistema pueda ayudarme a resolverlos paso a paso.

#### Acceptance Criteria

1. WHEN un alumno envía texto con ecuaciones matemáticas, THEN EL Sistema SHALL clasificar el problema como tipo "Ciencias"
2. WHEN un alumno envía código fuente en Python, C++ o Java, THEN EL Sistema SHALL clasificar el problema como tipo "Programación"
3. WHEN un alumno envía una imagen con contenido matemático, THEN EL Sistema SHALL extraer el texto mediante OCR y clasificar el problema
4. WHEN un alumno envía contenido mixto (texto y código), THEN EL Sistema SHALL identificar ambos componentes y clasificarlos apropiadamente
5. THE Sistema SHALL soportar entrada multimodal incluyendo texto plano, LaTeX, imágenes y código fuente

### Requirement 2: Verificación Formal Matemática

**User Story:** Como alumno, quiero que mis pasos matemáticos sean validados rigurosamente, para asegurarme de que mi razonamiento es correcto sin depender de respuestas ambiguas.

#### Acceptance Criteria

1. WHEN un alumno propone un paso matemático, THEN EL Motor_Matemático SHALL verificar la equivalencia algebraica con el paso anterior usando SymPy
2. WHEN la verificación detecta un error algebraico, THEN EL Motor_Matemático SHALL identificar la naturaleza del error (sintaxis, procedimiento o concepto)
3. WHEN un paso es algebraicamente equivalente, THEN EL Sistema SHALL permitir al alumno avanzar al siguiente paso
4. WHEN un paso contiene variables simbólicas, THEN EL Motor_Matemático SHALL validar la equivalencia para todos los valores válidos del dominio
5. THE Motor_Matemático SHALL manejar expresiones en álgebra, cálculo, trigonometría y ecuaciones diferenciales

### Requirement 3: Verificación Formal de Código

**User Story:** Como alumno, quiero que mi código sea validado contra casos de prueba reales, para confirmar que mi solución funciona correctamente antes de avanzar.

#### Acceptance Criteria

1. WHEN un alumno envía código Python, C++ o Java, THEN EL Sandbox_Código SHALL ejecutar el código en un entorno Docker aislado
2. WHEN el código se ejecuta, THEN EL Sandbox_Código SHALL validar la salida contra unit tests predefinidos
3. IF el código excede límites de tiempo o memoria, THEN EL Sandbox_Código SHALL terminar la ejecución y reportar el error
4. WHEN todos los unit tests pasan, THEN EL Sistema SHALL marcar el paso como correcto
5. WHEN algún unit test falla, THEN EL Sistema SHALL proporcionar información sobre el caso de prueba fallido sin revelar la solución completa
6. THE Sandbox_Código SHALL prevenir acceso a red, sistema de archivos y recursos del host

### Requirement 4: Diagnóstico Inteligente de Errores

**User Story:** Como alumno, quiero recibir retroalimentación específica sobre mis errores, para entender qué tipo de problema tengo y cómo abordarlo.

#### Acceptance Criteria

1. WHEN la verificación formal detecta un error, THEN EL Sistema SHALL clasificar el error en una de tres categorías: Sintaxis, Procedimiento o Concepto
2. WHEN un error es de sintaxis, THEN EL Sistema SHALL identificar la regla sintáctica violada
3. WHEN un error es de procedimiento, THEN EL Sistema SHALL identificar el paso algorítmico incorrecto
4. WHEN un error es de concepto, THEN EL Sistema SHALL identificar el concepto fundamental malentendido
5. THE Sistema SHALL almacenar el histórico de errores del alumno para análisis de patrones

### Requirement 5: Andamiaje Socrático Gradual

**User Story:** Como alumno, quiero recibir ayuda progresiva cuando estoy bloqueado, para desarrollar mi pensamiento crítico sin recibir la respuesta directamente.

#### Acceptance Criteria

1. WHEN un alumno comete un error, THEN EL Motor_Socrático SHALL proporcionar ayuda en Nivel_Andamiaje 1 (pregunta reflexiva)
2. WHEN un alumno permanece bloqueado después del Nivel 1, THEN EL Motor_Socrático SHALL escalar a Nivel_Andamiaje 2 (pista contextual del RAG)
3. WHEN un alumno permanece bloqueado después del Nivel 2, THEN EL Motor_Socrático SHALL escalar a Nivel_Andamiaje 3 (analogía simplificada)
4. WHEN un alumno resuelve el problema después de recibir ayuda, THEN EL Sistema SHALL registrar el nivel de andamiaje utilizado
5. THE Motor_Socrático SHALL generar preguntas contextuales basadas en el tipo de error diagnosticado
6. THE Sistema SHALL bloquear el acceso a la solución completa hasta que se superen todos los pasos intermedios

### Requirement 6: Personalización con Contenido del Profesor

**User Story:** Como profesor, quiero que el sistema utilice mis apuntes y materiales, para que los alumnos reciban ayuda alineada con mi metodología de enseñanza.

#### Acceptance Criteria

1. WHEN un profesor sincroniza contenido desde Notion, THEN EL Sistema SHALL importar y procesar los apuntes
2. WHEN el contenido es importado, THEN EL RAG_Engine SHALL vectorizar el contenido y almacenarlo en ChromaDB
3. WHEN el Motor_Socrático necesita proporcionar una pista de Nivel 2, THEN EL RAG_Engine SHALL recuperar contenido relevante de los apuntes del profesor
4. WHEN se actualiza contenido en Notion, THEN EL Sistema SHALL sincronizar automáticamente los cambios
5. THE RAG_Engine SHALL mantener la coherencia terminológica con el material del profesor

### Requirement 7: Gestión del Árbol de Habilidades

**User Story:** Como alumno, quiero visualizar mi progreso en un árbol de habilidades interactivo, para entender qué conceptos domino y cuáles necesito reforzar.

#### Acceptance Criteria

1. WHEN un alumno accede a su perfil, THEN EL Sistema SHALL mostrar el Árbol_Habilidades con el estado de cada nodo
2. WHEN un alumno completa exitosamente problemas de una habilidad, THEN EL Sistema SHALL actualizar el nivel de Dominio de esa habilidad
3. WHEN una habilidad tiene dependencias no cumplidas, THEN EL Sistema SHALL bloquear el acceso a esa habilidad
4. WHEN un alumno alcanza dominio suficiente en una habilidad, THEN EL Sistema SHALL desbloquear habilidades dependientes
5. THE Sistema SHALL calcular el Dominio basándose en precisión, velocidad y nivel de andamiaje requerido

### Requirement 8: Panel de Control del Profesor

**User Story:** Como profesor, quiero monitorear el progreso de mis alumnos en tiempo real, para identificar quiénes necesitan intervención y autorizar avances cuando sea apropiado.

#### Acceptance Criteria

1. WHEN un profesor accede al panel de control, THEN EL Sistema SHALL mostrar métricas en tiempo real de todos los alumnos
2. WHEN un alumno muestra señales de frustración (múltiples errores consecutivos), THEN EL Sistema SHALL generar una alerta en el Semáforo de Riesgo
3. WHEN un alumno está bloqueado por más de un umbral configurable, THEN EL Sistema SHALL notificar al profesor
4. WHEN un profesor revisa el progreso de un alumno, THEN EL Sistema SHALL mostrar el histórico de errores y patrones identificados
5. WHEN un alumno solicita avanzar sin cumplir requisitos, THEN EL Sistema SHALL requerir autorización explícita del profesor
6. THE Sistema SHALL permitir al profesor configurar umbrales de dominio para avance automático

### Requirement 9: Orquestación de IA para Pedagogía

**User Story:** Como sistema, necesito coordinar múltiples modelos de IA, para generar contenido pedagógico de alta calidad mientras mantengo la verificación formal.

#### Acceptance Criteria

1. WHEN se requiere generar una pregunta socrática, THEN EL Orquestador_IA SHALL utilizar Claude 3.5 o Gemini Pro
2. WHEN se genera contenido pedagógico, THEN EL Orquestador_IA SHALL incluir contexto del error diagnosticado y el nivel de andamiaje
3. WHEN el RAG_Engine proporciona contenido del profesor, THEN EL Orquestador_IA SHALL integrar ese contenido en la respuesta
4. WHEN se genera una analogía (Nivel 3), THEN EL Orquestador_IA SHALL simplificar el concepto manteniendo rigor conceptual
5. THE Orquestador_IA SHALL nunca revelar soluciones completas, solo guiar el razonamiento

### Requirement 10: Gestión de Usuarios y Autenticación

**User Story:** Como usuario, quiero acceder de forma segura a la plataforma, para proteger mi progreso y datos personales.

#### Acceptance Criteria

1. WHEN un usuario se registra, THEN EL Sistema SHALL crear una cuenta con rol de Alumno o Profesor
2. WHEN un usuario inicia sesión, THEN EL Sistema SHALL autenticar credenciales y generar un token de sesión
3. WHEN un profesor crea una clase, THEN EL Sistema SHALL generar códigos de invitación para alumnos
4. WHEN un alumno usa un código de invitación, THEN EL Sistema SHALL asociar al alumno con la clase del profesor
5. THE Sistema SHALL almacenar contraseñas usando hashing seguro (bcrypt o Argon2)
6. THE Sistema SHALL implementar rate limiting para prevenir ataques de fuerza bruta

### Requirement 11: Persistencia y Gestión de Datos

**User Story:** Como sistema, necesito almacenar y recuperar datos de forma eficiente, para mantener el estado del aprendizaje y permitir análisis histórico.

#### Acceptance Criteria

1. WHEN se crea o actualiza información de usuario, THEN EL Sistema SHALL persistir los datos en PostgreSQL
2. WHEN se registra un intento de resolución, THEN EL Sistema SHALL almacenar el problema, respuesta, resultado y nivel de andamiaje
3. WHEN se actualiza el Árbol_Habilidades, THEN EL Sistema SHALL persistir el nuevo estado de dominio
4. WHEN se vectoriza contenido del profesor, THEN EL Sistema SHALL almacenar los embeddings en ChromaDB
5. THE Sistema SHALL mantener integridad referencial entre usuarios, clases, problemas y progreso
6. THE Sistema SHALL implementar backups automáticos diarios de PostgreSQL

### Requirement 12: API y Comunicación Frontend-Backend

**User Story:** Como desarrollador, necesito una API bien definida, para que el frontend pueda comunicarse eficientemente con los servicios backend.

#### Acceptance Criteria

1. WHEN el frontend envía una solicitud, THEN EL Sistema SHALL responder usando formato JSON estandarizado
2. WHEN ocurre un error, THEN EL Sistema SHALL retornar códigos HTTP apropiados y mensajes descriptivos
3. WHEN se envía un problema para verificación, THEN EL Sistema SHALL procesar la solicitud de forma asíncrona si excede 2 segundos
4. WHEN se solicita el estado del Árbol_Habilidades, THEN EL Sistema SHALL retornar la estructura completa con estados actualizados
5. THE Sistema SHALL implementar versionado de API (v1, v2) para compatibilidad futura
6. THE Sistema SHALL documentar todos los endpoints usando OpenAPI/Swagger

### Requirement 13: Interfaz de Usuario Alumno

**User Story:** Como alumno, quiero una interfaz intuitiva y responsiva, para interactuar fácilmente con el sistema desde cualquier dispositivo.

#### Acceptance Criteria

1. WHEN un alumno accede a la plataforma, THEN EL Sistema SHALL mostrar un chat multimodal para enviar problemas
2. WHEN un alumno envía un problema, THEN EL Sistema SHALL mostrar retroalimentación en tiempo real durante la verificación
3. WHEN el sistema proporciona una pregunta socrática, THEN EL Sistema SHALL mostrarla de forma destacada en el chat
4. WHEN un alumno visualiza el Árbol_Habilidades, THEN EL Sistema SHALL renderizar un grafo interactivo con zoom y navegación
5. WHEN un alumno está en dispositivo móvil, THEN EL Sistema SHALL adaptar la interfaz para pantallas pequeñas
6. THE Sistema SHALL soportar renderizado de LaTeX para ecuaciones matemáticas
7. THE Sistema SHALL soportar syntax highlighting para código fuente

### Requirement 14: Manejo de Errores y Resiliencia

**User Story:** Como sistema, necesito manejar errores gracefully, para proporcionar una experiencia confiable incluso cuando ocurren fallos.

#### Acceptance Criteria

1. IF el Motor_Matemático falla al procesar una expresión, THEN EL Sistema SHALL notificar al alumno y registrar el error para revisión
2. IF el Sandbox_Código no puede ejecutar código, THEN EL Sistema SHALL proporcionar un mensaje de error descriptivo
3. IF el Orquestador_IA no responde en 30 segundos, THEN EL Sistema SHALL usar una respuesta de fallback predefinida
4. IF la conexión a PostgreSQL se pierde, THEN EL Sistema SHALL reintentar la conexión con backoff exponencial
5. IF ChromaDB no está disponible, THEN EL Sistema SHALL funcionar sin RAG usando solo el Orquestador_IA
6. THE Sistema SHALL registrar todos los errores en un sistema de logging centralizado

### Requirement 15: Seguridad del Sandbox de Código

**User Story:** Como administrador del sistema, necesito que la ejecución de código sea segura, para prevenir que código malicioso comprometa la infraestructura.

#### Acceptance Criteria

1. WHEN se ejecuta código en el Sandbox_Código, THEN EL Sistema SHALL usar contenedores Docker con privilegios mínimos
2. THE Sandbox_Código SHALL bloquear acceso a red externa
3. THE Sandbox_Código SHALL limitar uso de CPU a 1 segundo de tiempo de ejecución
4. THE Sandbox_Código SHALL limitar uso de memoria a 256MB por ejecución
5. THE Sandbox_Código SHALL bloquear acceso al sistema de archivos del host
6. WHEN se detecta intento de violación de seguridad, THEN EL Sistema SHALL terminar la ejecución y registrar el incidente

### Requirement 16: Inteligencia Predictiva y BKT

**User Story:** Como sistema, quiero modelar el estado mental del alumno probabilísticamente, para personalizar el ritmo de aprendizaje de forma científica.

#### Acceptance Criteria

1. THE Sistema SHALL implementar un motor de Bayesian Knowledge Tracing (BKT) para calcular la probabilidad de dominio (L) tras cada interacción
2. THE Sistema SHALL actualizar L mediante la fórmula: L(t+1) = P(L(t)|Acción) + (1 - P(L(t)|Acción)) · P(T)
3. WHEN la probabilidad de dominio sea inferior al umbral del 70%, THEN EL Sistema SHALL sugerir actividades de refuerzo de conceptos base antes de permitir el avance
4. THE Sistema SHALL ejecutar un modelo de Clasificación Binaria (Random Forest o XGBoost) para predecir el riesgo de fracaso semanal basado en latencia y errores

### Requirement 17: Análisis No Supervisado de Arquetipos

**User Story:** Como profesor, quiero identificar grupos de alumnos con problemas similares, para optimizar mis explicaciones grupales en la academia.

#### Acceptance Criteria

1. THE Sistema SHALL ejecutar semanalmente un algoritmo de Clustering (K-Means o DBSCAN) sobre el histórico de errores
2. THE Sistema SHALL clasificar a los alumnos en arquetipos (ej: "Falla por base aritmética" vs "Falla por lógica procedimental")
3. THE Sistema SHALL visualizar estos clusters en el Panel de Control del Profesor para facilitar la toma de decisiones pedagógicas

### Requirement 18: Detección de Frustración (NLP Sentiment)

**User Story:** Como alumno, quiero que el sistema detecte mi estado emocional, para que el tutor ajuste su tono cuando me siento bloqueado.

#### Acceptance Criteria

1. WHEN un alumno introduce texto en el chat, THEN EL Orquestador_IA SHALL realizar un Análisis de Sentimiento
2. IF se detecta un sentimiento de "Frustración Alta", THEN EL Motor_Socrático SHALL priorizar el refuerzo positivo y analogías simplificadas del RAG_Engine

# Plan de Implementación: Elenchos

## Overview

Este plan de implementación descompone el sistema Elenchos en tareas incrementales y ejecutables. El enfoque es construir el sistema en capas, comenzando con la infraestructura base, luego los motores de verificación, seguido por la inteligencia (IA, BKT, ML), y finalmente las interfaces de usuario.

Cada tarea está diseñada para ser autocontenida y construir sobre las tareas anteriores, asegurando que no haya código huérfano y que el sistema sea funcional en cada checkpoint.

## Tasks

- [x] 1. Configurar infraestructura base y modelos de datos
  - Configurar proyecto Python con FastAPI
  - Configurar PostgreSQL y ChromaDB
  - Definir modelos de datos base (User, Student, Teacher, Problem, Session)
  - Configurar sistema de migraciones (Alembic)
  - Configurar logging centralizado
  - _Requirements: 10.1, 11.1, 11.5_

- [ ]* 1.1 Escribir tests de propiedad para modelos de datos
  - **Property 18: Persistencia Completa de Datos**
  - **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5**

- [ ] 2. Implementar sistema de autenticación y autorización
  - [ ] 2.1 Implementar registro de usuarios con hashing de contraseñas
    - Usar bcrypt para hashing
    - Validar formato de email
    - Asignar roles (STUDENT, TEACHER)
    - _Requirements: 10.1, 10.5_

  - [ ]* 2.2 Escribir test de propiedad para seguridad de contraseñas
    - **Property 16: Seguridad de Contraseñas**
    - **Validates: Requirements 10.5**

  - [ ] 2.3 Implementar login y generación de tokens JWT
    - Validar credenciales
    - Generar token JWT con expiración
    - _Requirements: 10.2_

  - [ ]* 2.4 Escribir test de propiedad para autenticación
    - **Property 14: Creación y Autenticación de Usuarios**
    - **Validates: Requirements 10.1, 10.2**

  - [ ] 2.5 Implementar rate limiting para prevenir fuerza bruta
    - Usar Redis para tracking de intentos
    - Bloquear después de 5 intentos fallidos
    - _Requirements: 10.6_

  - [ ]* 2.6 Escribir test de propiedad para rate limiting
    - **Property 17: Rate Limiting de Autenticación**
    - **Validates: Requirements 10.6**

- [ ] 3. Implementar gestión de clases e invitaciones
  - [ ] 3.1 Implementar creación de clases por profesores
    - Generar códigos de invitación únicos
    - Almacenar en PostgreSQL
    - _Requirements: 10.3_

  - [ ] 3.2 Implementar uso de códigos de invitación por alumnos
    - Validar código
    - Asociar alumno con clase
    - _Requirements: 10.4_

  - [ ]* 3.3 Escribir test de propiedad para gestión de clases
    - **Property 15: Gestión de Clases e Invitaciones**
    - **Validates: Requirements 10.3, 10.4**

- [ ] 4. Checkpoint - Sistema de autenticación funcional
  - Verificar que todos los tests pasen
  - Confirmar que usuarios pueden registrarse, iniciar sesión y unirse a clases
  - Preguntar al usuario si hay dudas o ajustes necesarios

- [ ] 5. Implementar API Gateway y routing
  - [ ] 5.1 Crear API Gateway con FastAPI
    - Definir endpoints principales
    - Implementar middleware de autenticación
    - Configurar CORS
    - _Requirements: 12.1, 12.2_

  - [ ] 5.2 Implementar manejo de errores estandarizado
    - Retornar códigos HTTP apropiados
    - Mensajes descriptivos en JSON
    - _Requirements: 12.2, 14.6_

  - [ ]* 5.3 Escribir test de propiedad para formato JSON
    - **Property 19: Formato JSON Estandarizado en API**
    - **Validates: Requirements 12.1, 12.2**

  - [ ] 5.4 Implementar procesamiento asíncrono para operaciones largas
    - Usar Celery con Redis
    - Notificar cliente cuando complete
    - _Requirements: 12.3_

  - [ ]* 5.5 Escribir test de propiedad para procesamiento asíncrono
    - **Property 20: Procesamiento Asíncrono de Operaciones Largas**
    - **Validates: Requirements 12.3**

- [ ] 6. Implementar Orquestador Principal
  - [ ] 6.1 Crear clasificador de problemas
    - Detectar ecuaciones matemáticas (regex, LaTeX)
    - Detectar código fuente (Python, C++, Java)
    - Manejar contenido mixto
    - _Requirements: 1.1, 1.2, 1.4_

  - [ ]* 6.2 Escribir test de propiedad para clasificación
    - **Property 1: Clasificación Consistente de Problemas**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**

  - [ ] 6.3 Implementar OCR para imágenes con ecuaciones
    - Integrar Tesseract o servicio cloud
    - Extraer texto matemático
    - _Requirements: 1.3_

  - [ ] 6.4 Implementar orquestador de flujo de verificación
    - Routing a verificadores apropiados
    - Gestión de estado de sesión
    - Coordinación de respuestas
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 7. Implementar Motor Matemático (SymPy)
  - [ ] 7.1 Crear parser de expresiones matemáticas
    - Parsear LaTeX a SymPy
    - Parsear texto plano a SymPy
    - Manejar errores de parsing
    - _Requirements: 2.1_

  - [ ] 7.2 Implementar verificador de equivalencia algebraica
    - Simplificar expresiones
    - Verificar equivalencia usando simplify(expr1 - expr2) == 0
    - Manejar variables simbólicas
    - _Requirements: 2.1, 2.3, 2.4_

  - [ ]* 7.3 Escribir test de propiedad para equivalencia algebraica
    - **Property 2: Verificación de Equivalencia Algebraica y Avance**
    - **Validates: Requirements 2.1, 2.3**

  - [ ]* 7.4 Escribir test de propiedad para validación simbólica
    - **Property 4: Validación Simbólica de Variables**
    - **Validates: Requirements 2.4**

  - [ ] 7.5 Implementar diagnóstico de errores matemáticos
    - Clasificar en SYNTAX, PROCEDURE, CONCEPT
    - Identificar naturaleza específica del error
    - _Requirements: 2.2, 4.1, 4.2, 4.3, 4.4_

  - [ ]* 7.6 Escribir test de propiedad para diagnóstico de errores
    - **Property 3: Diagnóstico Completo de Errores Matemáticos**
    - **Validates: Requirements 2.2, 4.1, 4.2, 4.3, 4.4**

  - [ ] 7.7 Implementar manejo de errores del Motor Matemático
    - Notificar alumno con mensaje descriptivo
    - Registrar error para revisión
    - No interrumpir sesión
    - _Requirements: 14.1_

  - [ ]* 7.8 Escribir test de propiedad para manejo de errores
    - **Property 22: Manejo Graceful de Errores del Motor Matemático**
    - **Validates: Requirements 14.1**

- [ ] 8. Checkpoint - Motor Matemático funcional
  - Verificar que todos los tests pasen
  - Confirmar que el motor puede verificar expresiones algebraicas
  - Preguntar al usuario si hay dudas o ajustes necesarios

- [ ] 9. Implementar Sandbox de Código (Docker)
  - [ ] 9.1 Crear imágenes Docker base para Python, C++, Java
    - Configurar sin privilegios (USER nobody)
    - Sin acceso a red (NETWORK none)
    - Límites de recursos (256MB, 1s CPU)
    - _Requirements: 3.1, 15.1, 15.2, 15.3, 15.4, 15.5_

  - [ ] 9.2 Implementar ejecutor de código en contenedores
    - Crear contenedor efímero
    - Copiar código al contenedor
    - Ejecutar con límites
    - Capturar stdout/stderr
    - Destruir contenedor
    - _Requirements: 3.1, 3.2_

  - [ ] 9.3 Implementar validación contra unit tests
    - Ejecutar código con cada test case
    - Comparar output con expected
    - Marcar como correcto si todos pasan
    - Proporcionar info de tests fallidos sin revelar solución
    - _Requirements: 3.2, 3.4, 3.5_

  - [ ]* 9.4 Escribir test de propiedad para validación de código
    - **Property 5: Validación de Código contra Unit Tests**
    - **Validates: Requirements 3.2, 3.4, 3.5**

  - [ ] 9.5 Implementar manejo de límites y errores del sandbox
    - Timeout (>1s)
    - Límite de memoria (>256MB)
    - Errores de runtime y compilación
    - Mensajes descriptivos con hints
    - _Requirements: 3.3, 14.2_

  - [ ]* 9.6 Escribir test de propiedad para manejo de errores del sandbox
    - **Property 23: Manejo de Errores del Sandbox**
    - **Validates: Requirements 14.2**

  - [ ] 9.7 Implementar detección de violaciones de seguridad
    - Detectar intentos de acceso a red
    - Detectar intentos de acceso a filesystem
    - Terminar ejecución y registrar incidente
    - _Requirements: 15.6_

- [ ] 10. Checkpoint - Sandbox de Código funcional
  - Verificar que todos los tests pasen
  - Confirmar que el sandbox puede ejecutar código de forma segura
  - Preguntar al usuario si hay dudas o ajustes necesarios

- [ ] 11. Implementar RAG Engine (ChromaDB)
  - [ ] 11.1 Configurar ChromaDB y modelo de embeddings
    - Usar sentence-transformers
    - Configurar colección para contenido del profesor
    - _Requirements: 6.2, 11.4_

  - [ ] 11.2 Implementar sincronización con Notion
    - Conectar a Notion API
    - Descargar páginas especificadas
    - Extraer texto y estructura
    - _Requirements: 6.1, 6.4_

  - [ ] 11.3 Implementar vectorización y almacenamiento
    - Generar embeddings del contenido
    - Almacenar en ChromaDB con metadata
    - _Requirements: 6.2, 11.4_

  - [ ]* 11.4 Escribir test de propiedad para persistencia RAG
    - **Property 8: Persistencia de Contenido RAG** (primera parte)
    - **Validates: Requirements 6.2**

  - [ ] 11.5 Implementar recuperación de contenido relevante
    - Búsqueda vectorial por similitud
    - Retornar top-k documentos
    - _Requirements: 6.3_

  - [ ]* 11.6 Escribir test de propiedad para recuperación RAG
    - **Property 8: Persistencia de Contenido RAG** (segunda parte)
    - **Validates: Requirements 6.3**

  - [ ] 11.7 Implementar degradación graceful sin ChromaDB
    - Detectar indisponibilidad
    - Continuar sin RAG (omitir Nivel 2)
    - _Requirements: 14.5_

  - [ ]* 11.8 Escribir test de propiedad para degradación graceful
    - **Property 26: Degradación Graceful sin RAG**
    - **Validates: Requirements 14.5**

- [ ] 12. Implementar Orquestador de IA
  - [ ] 12.1 Configurar clientes para Claude 3.5 y Gemini Pro
    - Configurar API keys
    - Implementar selección de modelo por tarea
    - _Requirements: 9.1_

  - [ ] 12.2 Implementar generación de preguntas socráticas
    - Prompts por nivel de andamiaje
    - Incluir contexto del error
    - Integrar contenido del RAG si disponible
    - _Requirements: 9.2, 9.3_

  - [ ]* 12.3 Escribir test de propiedad para integración de contexto
    - **Property 13: Integración de Contexto en Contenido Pedagógico**
    - **Validates: Requirements 9.2, 9.3, 9.5**

  - [ ] 12.4 Implementar análisis de sentimiento
    - Detectar frustración en texto del alumno
    - Retornar score de frustración y confianza
    - _Requirements: 18.1_

  - [ ]* 12.5 Escribir test de propiedad para análisis de sentimiento
    - **Property 33: Análisis de Sentimiento en Chat**
    - **Validates: Requirements 18.1, 18.2**

  - [ ] 12.6 Implementar manejo de timeouts y fallbacks
    - Timeout de 30 segundos
    - Respuestas de fallback por nivel
    - Cambio a modelo alternativo en rate limit
    - _Requirements: 14.3_

  - [ ]* 12.7 Escribir test de propiedad para fallback de timeout
    - **Property 24: Fallback para Timeout de IA**
    - **Validates: Requirements 14.3**

  - [ ] 12.8 Implementar verificación de no revelar soluciones
    - Filtrar respuestas que contengan soluciones completas
    - _Requirements: 9.5_

- [ ] 13. Implementar Motor Socrático
  - [ ] 13.1 Implementar lógica de andamiaje gradual
    - Intento 1: Nivel 1 (pregunta reflexiva)
    - Intentos 2-3: Nivel 2 (pista con RAG)
    - Intentos 4+: Nivel 3 (analogía simplificada)
    - Registrar nivel utilizado
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ]* 13.2 Escribir test de propiedad para andamiaje gradual
    - **Property 6: Andamiaje Gradual Progresivo**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

  - [ ] 13.3 Implementar ajuste basado en sentimiento
    - Si frustración alta, priorizar refuerzo positivo
    - Escalar más rápido a analogías simplificadas
    - _Requirements: 18.2_

  - [ ] 13.4 Implementar bloqueo de soluciones completas
    - Verificar que se completaron todos los pasos intermedios
    - O que hay autorización del profesor
    - _Requirements: 5.6_

  - [ ]* 13.5 Escribir test de propiedad para bloqueo de soluciones
    - **Property 7: Bloqueo de Soluciones Completas**
    - **Validates: Requirements 5.6**

  - [ ] 13.6 Implementar alertas al profesor
    - Generar alerta si attempt_count > 5
    - _Requirements: 5.1, 5.2, 5.3_

- [ ] 14. Checkpoint - Sistema de andamiaje funcional
  - Verificar que todos los tests pasen
  - Confirmar que el andamiaje escala correctamente
  - Preguntar al usuario si hay dudas o ajustes necesarios

- [ ] 15. Implementar BKT Engine
  - [ ] 15.1 Implementar modelo de Bayesian Knowledge Tracing
    - Definir parámetros BKT (P_L0, P_T, P_S, P_G)
    - Implementar fórmula de actualización de L(t+1)
    - _Requirements: 16.1, 16.2_

  - [ ]* 15.2 Escribir test de propiedad para actualización BKT
    - **Property 29: Actualización BKT tras Interacción**
    - **Validates: Requirements 16.1, 16.2**

  - [ ] 15.3 Implementar verificación de umbral de dominio
    - Verificar si L(t) >= 0.7 para avance
    - _Requirements: 16.3_

  - [ ] 15.4 Implementar sugerencia de refuerzo
    - Identificar habilidades con L(t) < 0.7
    - Sugerir actividades de refuerzo
    - _Requirements: 16.3_

  - [ ]* 15.5 Escribir test de propiedad para sugerencia de refuerzo
    - **Property 30: Sugerencia de Refuerzo por Dominio Bajo**
    - **Validates: Requirements 16.3**

- [ ] 16. Implementar Gestión de Árbol de Habilidades
  - [ ] 16.1 Crear estructura de árbol de habilidades
    - Definir nodos con skill_id, name, dependencies
    - Almacenar en PostgreSQL
    - _Requirements: 7.1_

  - [ ] 16.2 Implementar actualización de dominio
    - Calcular dominio basado en precisión, velocidad, andamiaje
    - Actualizar estado de habilidad
    - _Requirements: 7.2, 7.5_

  - [ ]* 16.3 Escribir test de propiedad para actualización de dominio
    - **Property 9: Actualización de Dominio en Árbol de Habilidades**
    - **Validates: Requirements 7.2, 7.5**

  - [ ] 16.4 Implementar gestión de dependencias
    - Bloquear habilidades con dependencias no cumplidas
    - Desbloquear cuando se alcanza dominio >= 0.7
    - _Requirements: 7.3, 7.4_

  - [ ]* 16.5 Escribir test de propiedad para gestión de dependencias
    - **Property 10: Gestión de Dependencias de Habilidades**
    - **Validates: Requirements 7.3, 7.4**

  - [ ] 16.6 Implementar endpoint para retornar árbol completo
    - Incluir todos los nodos con estados actualizados
    - _Requirements: 12.4_

  - [ ]* 16.7 Escribir test de propiedad para estructura del árbol
    - **Property 21: Estructura Completa del Árbol de Habilidades**
    - **Validates: Requirements 12.4**

- [ ] 17. Implementar Análisis ML
  - [ ] 17.1 Implementar predicción de riesgo de fracaso
    - Entrenar modelo Random Forest o XGBoost
    - Features: latencia, errores, andamiaje, días sin actividad
    - Retornar risk_score (0.0-1.0) y risk_level (LOW/MEDIUM/HIGH)
    - _Requirements: 16.4_

  - [ ]* 17.2 Escribir test de propiedad para predicción de riesgo
    - **Property 31: Predicción de Riesgo de Fracaso**
    - **Validates: Requirements 16.4**

  - [ ] 17.3 Implementar clustering de arquetipos
    - Ejecutar K-Means o DBSCAN semanalmente
    - Features: frecuencia de errores por tipo, latencia, andamiaje
    - Clasificar en arquetipos identificables
    - _Requirements: 17.1, 17.2_

  - [ ]* 17.4 Escribir test de propiedad para clustering
    - **Property 32: Clustering Semanal de Arquetipos**
    - **Validates: Requirements 17.1, 17.2**

  - [ ] 17.5 Implementar job semanal para actualizar clusters
    - Usar Celery Beat para scheduling
    - Actualizar clusters y arquetipos
    - _Requirements: 17.1_

- [ ] 18. Implementar Panel de Control del Profesor
  - [ ] 18.1 Crear endpoint para dashboard con métricas en tiempo real
    - Métricas de todos los alumnos
    - Progreso por habilidad
    - _Requirements: 8.1_

  - [ ] 18.2 Implementar Semáforo de Riesgo
    - Detectar múltiples errores consecutivos
    - Detectar bloqueo por más de umbral configurable
    - Generar alertas
    - _Requirements: 8.2, 8.3_

  - [ ]* 18.3 Escribir test de propiedad para alertas de riesgo
    - **Property 11: Alertas de Riesgo por Frustración**
    - **Validates: Requirements 8.2, 8.3**

  - [ ] 18.4 Implementar visualización de histórico de errores
    - Mostrar errores y patrones identificados
    - _Requirements: 8.4_

  - [ ] 18.5 Implementar autorización de avance
    - Permitir al profesor autorizar avance sin cumplir requisitos
    - _Requirements: 8.5_

  - [ ]* 18.6 Escribir test de propiedad para autorización de avance
    - **Property 12: Autorización de Avance sin Requisitos**
    - **Validates: Requirements 8.5**

  - [ ] 18.7 Implementar configuración de umbrales
    - Permitir configurar umbral de dominio para avance
    - _Requirements: 8.6_

  - [ ] 18.8 Implementar visualización de clusters de arquetipos
    - Mostrar clusters en el panel
    - _Requirements: 17.3_

- [ ] 19. Checkpoint - Backend completo funcional
  - Verificar que todos los tests pasen
  - Confirmar que todos los componentes backend están integrados
  - Preguntar al usuario si hay dudas o ajustes necesarios

- [ ] 20. Implementar Frontend - Interfaz Alumno
  - [ ] 20.1 Configurar proyecto Next.js con React
    - Configurar TypeScript
    - Configurar Tailwind CSS
    - Configurar cliente API
    - _Requirements: 13.1_

  - [ ] 20.2 Implementar chat multimodal
    - Input de texto
    - Upload de imágenes
    - Input de código con syntax highlighting
    - _Requirements: 13.1, 13.6, 13.7_

  - [ ] 20.3 Implementar visualización de retroalimentación en tiempo real
    - WebSocket para actualizaciones
    - Mostrar estado de verificación
    - _Requirements: 13.2_

  - [ ] 20.4 Implementar visualización de preguntas socráticas
    - Mostrar de forma destacada
    - Diferenciar por nivel de andamiaje
    - _Requirements: 13.3_

  - [ ] 20.5 Implementar visualización de Árbol de Habilidades
    - Grafo interactivo con D3.js o React Flow
    - Zoom y navegación
    - Estados visuales (LOCKED, AVAILABLE, IN_PROGRESS, MASTERED)
    - _Requirements: 13.4_

  - [ ] 20.6 Implementar renderizado de LaTeX
    - Usar KaTeX o MathJax
    - _Requirements: 13.6_

  - [ ] 20.7 Implementar responsive design
    - Adaptar para móviles
    - _Requirements: 13.5_

- [ ] 21. Implementar Frontend - Interfaz Profesor
  - [ ] 21.1 Implementar panel de control con métricas
    - Visualización de métricas en tiempo real
    - Gráficos con Chart.js o Recharts
    - _Requirements: 8.1_

  - [ ] 21.2 Implementar Semáforo de Riesgo visual
    - Alertas destacadas
    - Filtros por nivel de riesgo
    - _Requirements: 8.2, 8.3_

  - [ ] 21.3 Implementar visualización de progreso de alumnos
    - Vista detallada por alumno
    - Histórico de errores
    - Patrones identificados
    - _Requirements: 8.4_

  - [ ] 21.4 Implementar controles de autorización de avance
    - Botón para autorizar avance
    - Confirmación
    - _Requirements: 8.5_

  - [ ] 21.5 Implementar configuración de umbrales
    - Formulario para configurar umbrales
    - _Requirements: 8.6_

  - [ ] 21.6 Implementar sincronización con Notion
    - Formulario para token y page IDs
    - Estado de sincronización
    - _Requirements: 6.1, 6.4_

  - [ ] 21.7 Implementar visualización de clusters de arquetipos
    - Gráfico de clusters
    - Descripción de arquetipos
    - _Requirements: 17.3_

- [ ] 22. Implementar manejo de errores y resiliencia
  - [ ] 22.1 Implementar retry con backoff exponencial para PostgreSQL
    - Máximo 5 intentos
    - Delays: 1s, 2s, 4s, 8s, 16s
    - _Requirements: 14.4_

  - [ ]* 22.2 Escribir test de propiedad para resiliencia de PostgreSQL
    - **Property 25: Resiliencia de Conexión a PostgreSQL**
    - **Validates: Requirements 14.4**

  - [ ] 22.3 Implementar logging centralizado de errores
    - Registrar todos los errores con contexto completo
    - Enviar a sistema centralizado (ELK Stack o CloudWatch)
    - _Requirements: 14.6_

  - [ ]* 22.4 Escribir test de propiedad para logging de errores
    - **Property 27: Logging Centralizado de Errores**
    - **Validates: Requirements 14.6**

  - [ ] 22.5 Implementar almacenamiento de histórico de errores
    - Almacenar errores del alumno con información completa
    - _Requirements: 4.5_

  - [ ]* 22.6 Escribir test de propiedad para histórico de errores
    - **Property 28: Almacenamiento de Histórico de Errores**
    - **Validates: Requirements 4.5**

- [ ] 23. Checkpoint final - Sistema completo integrado
  - Verificar que todos los tests pasen (unit y property)
  - Confirmar que frontend y backend están completamente integrados
  - Realizar pruebas end-to-end manuales
  - Verificar que todas las 33 propiedades tienen tests implementados
  - Preguntar al usuario si hay ajustes finales necesarios

## Notes

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia los requirements específicos que implementa
- Los checkpoints aseguran validación incremental
- Los property tests validan propiedades universales con mínimo 100 iteraciones
- Los unit tests complementan con casos específicos y edge cases
- El sistema está diseñado para ser construido incrementalmente sin código huérfano

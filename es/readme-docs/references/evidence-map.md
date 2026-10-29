# Mapa de evidencias

Relaciona lo que se encuentra en un proyecto con los apartados de `standard.md` que activa o afecta.

- En el **modo crear**, sirve para decidir qué apartados `[C]` aplican.
- En el **modo actualizar**, sirve para saber qué apartados revisar cuando cambia un archivo.

Los ejemplos de archivos no son exhaustivos. Aplica la misma lógica al equivalente en cualquier lenguaje o tecnología.

| Evidencia en el proyecto | Ejemplos | Apartados |
|---|---|---|
| Manifiestos de dependencias y versiones de runtime | `package.json`, `pom.xml`, `build.gradle`, `go.mod`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `pubspec.yaml`, `Gemfile`, `*.csproj`, `.nvmrc`, `.tool-versions` | Stack tecnológico, Prerrequisitos, Instalación |
| Scripts y automatización de tareas | `scripts` de `package.json`, `Makefile`, `justfile`, `Taskfile`, carpeta `scripts/` | Ejecución de la aplicación, Ejecución de pruebas, Compilación, Comandos frecuentes |
| Variables de entorno y configuración | `.env.example`, `application.yml`, `appsettings.json`, `config/`, lecturas de variables en el código | Variables de entorno, Configuración por ambientes |
| Varios perfiles o ambientes | `application-prod.yml`, `.env.staging`, `config/environments/` | Configuración por ambientes, Despliegue |
| Rutas, controladores o especificaciones de API | Definiciones de rutas, controladores, resolvers de GraphQL, archivos `.proto`, `openapi.yaml` | APIs y endpoints, Contratos de integración, Ejemplos de consumo, Documentación interactiva |
| Autenticación | Middlewares de autenticación, guards, JWT, OAuth, gestión de roles | Autenticación y autorización, Consideraciones de seguridad |
| Mensajería | Productores o consumidores de Kafka, RabbitMQ, SQS, Pub/Sub; manejo de eventos o webhooks | Mensajería y eventos, Contratos de integración |
| Clientes de servicios externos | SDKs de terceros, clientes HTTP hacia otros servicios, servicios cloud | Integraciones con servicios externos, Dependencias e integraciones externas |
| Base de datos | Migraciones, modelos de ORM, esquemas, archivos `.sql`, seeds | Modelo de datos, Base de datos y migraciones, Preparación de dependencias locales |
| Contenedores y servicios locales | `Dockerfile`, `docker-compose.yml`, devcontainers | Preparación de dependencias locales, Compilación y empaquetado, Despliegue |
| Infraestructura | Terraform, Kubernetes, Helm, CloudFormation, `serverless.yml`, configuración de la plataforma de hosting | Infraestructura y recursos, Despliegue, Configuración por ambientes |
| CI/CD | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` | CI/CD, Despliegue |
| Pruebas | Carpetas de pruebas, configuración del framework de pruebas, configuración de cobertura | Ejecución de pruebas, Estrategia de pruebas, Cobertura |
| Calidad de código | Configuración de linters y formateadores, `.editorconfig`, hooks de pre-commit | Estándares de código |
| Contribución | `CONTRIBUTING.md`, plantillas de issues o pull requests, convenciones de commits | Guía de contribución, Estrategia de ramas y commits |
| Estructura del código | Carpetas de primer nivel, módulos, paquetes, capas | Estructura de carpetas, Componentes y módulos, Arquitectura |
| Varios servicios o aplicaciones | Monorepo, `docker-compose` con varios servicios, workspaces | Arquitectura, Diagramas, Dependencias e integraciones externas |
| Manejo de errores | Manejadores globales de errores, excepciones personalizadas, códigos de error | Manejo de errores y excepciones |
| Resiliencia | Reintentos, timeouts, circuit breakers, colas de reintento | Disponibilidad y recuperación ante fallos |
| Observabilidad | Librerías de logging, métricas, trazas, health checks | Logs y observabilidad, Monitoreo y alertas |
| Caché, límites de peticiones o colas de trabajos | Redis, rate limiters, workers en segundo plano | Rendimiento y escalabilidad |
| Validaciones de dominio | Validadores, esquemas de entrada, reglas en la capa de dominio | Reglas de negocio y validaciones |
| Versión y releases | Campo `version`, tags de git, `CHANGELOG.md`, configuración de releases | Versionado y compatibilidad, Historial de cambios |
| Licencia | `LICENSE`, campo `license` del manifiesto | Licencia y condiciones de uso |
| Documentación existente | Carpeta `docs/`, wikis enlazadas, ADRs | Documentación complementaria, Decisiones arquitectónicas |
| Configuración de depuración | `.vscode/launch.json`, configuraciones de ejecución del IDE | Entorno de depuración |

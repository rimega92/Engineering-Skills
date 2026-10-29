# Estándar de documentación para README.md

## Clasificación

- `[M]` Obligatorio para todos los proyectos.
- `[C]` Obligatorio cuando aplique a la naturaleza del proyecto.
- `[O]` Opcional, según la complejidad y las necesidades del proyecto.

## 1. Identificación y descripción del proyecto

- [ ] `[M]` **Nombre del proyecto:** Nombre oficial del sistema, servicio, componente o librería.
- [ ] `[M]` **Descripción general:** Propósito del proyecto, problema que resuelve y valor que aporta.
- [ ] `[M]` **Estado del proyecto:** Estado actual, como en desarrollo, activo, en mantenimiento, deprecado o archivado.
- [ ] `[M]` **Responsables y canales de soporte:** Equipo o persona propietaria y canales para resolver dudas o reportar problemas (por ejemplo, el issue tracker en un proyecto open source).
- [ ] `[C]` **Alcance funcional:** Capacidades, responsabilidades y límites del sistema.
- [ ] `[O]` **Audiencia objetivo:** Usuarios, desarrolladores o sistemas consumidores a los que está dirigido.
- [ ] `[O]` **Tabla de contenido:** Índice navegable para facilitar la consulta de documentos extensos.

## 2. Inicio rápido y ejecución local

- [ ] `[M]` **Prerrequisitos:** Herramientas, versiones, runtimes, permisos y dependencias necesarias para ejecutar el proyecto.
- [ ] `[M]` **Instalación y configuración local:** Pasos para preparar el entorno desde un repositorio recién clonado.
- [ ] `[M]` **Variables de entorno y configuración:** Variables requeridas, valores esperados, perfiles y archivos de configuración. Nunca incluir secretos reales. Si el proyecto no usa variables de entorno ni configuración, indicarlo en una línea.
- [ ] `[M]` **Ejecución de la aplicación:** Comandos para iniciar el proyecto y verificar su funcionamiento. En una librería, cómo importarla o usarla desde otro proyecto.
- [ ] `[M]` **Ejecución de pruebas:** Comandos básicos para ejecutar las pruebas y validar que el proyecto funciona correctamente. Si no hay pruebas automatizadas, indicarlo.
- [ ] `[C]` **Compilación y empaquetado:** Procedimiento para generar artefactos ejecutables, paquetes o imágenes de contenedor.
- [ ] `[C]` **Preparación de dependencias locales:** Instrucciones para levantar bases de datos, servicios auxiliares, contenedores o datos iniciales.
- [ ] `[O]` **Ejemplo de uso rápido:** Ejemplo mínimo que demuestre la funcionalidad principal del proyecto.
- [ ] `[O]` **Comandos frecuentes:** Referencia rápida de comandos habituales de desarrollo y diagnóstico.

## 3. Funcionalidades y comportamiento

- [ ] `[M]` **Funcionalidad principal:** Resumen de las capacidades y el comportamiento esperado del proyecto.
- [ ] `[C]` **Reglas de negocio y validaciones:** Restricciones, condiciones, invariantes y validaciones relevantes.
- [ ] `[C]` **Flujos funcionales principales:** Descripción de los procesos más importantes y sus etapas.
- [ ] `[C]` **Limitaciones conocidas:** Restricciones técnicas o funcionales, escenarios no soportados y funcionalidades pendientes.
- [ ] `[O]` **Casos de uso:** Ejemplos de escenarios habituales de utilización.
- [ ] `[O]` **Glosario de términos:** Definición de siglas y conceptos específicos del negocio o del dominio.

## 4. Stack tecnológico y arquitectura

- [ ] `[M]` **Stack tecnológico:** Lenguajes, frameworks, librerías, runtimes y herramientas principales, incluyendo versiones relevantes.
- [ ] `[C]` **Arquitectura del sistema:** Descripción de la arquitectura, componentes principales, responsabilidades y relaciones.
- [ ] `[C]` **Estructura de carpetas y archivos:** Scaffold del repositorio con una explicación de los directorios y archivos relevantes.
- [ ] `[C]` **Componentes y módulos principales:** Responsabilidades de los módulos y forma en que interactúan.
- [ ] `[C]` **Dependencias e integraciones externas:** Sistemas, servicios y plataformas requeridos para el funcionamiento.
- [ ] `[C]` **Modelo de datos:** Entidades, relaciones y estructuras relevantes para comprender la información gestionada.
- [ ] `[C]` **Configuración por ambientes:** Diferencias de configuración entre desarrollo, pruebas y producción.
- [ ] `[O]` **Diagramas de arquitectura:** Representación visual de componentes, capas, servicios y dependencias, preferiblemente con Mermaid.
- [ ] `[O]` **Diagramas de contexto:** Relación del sistema con usuarios, actores y sistemas externos.
- [ ] `[O]` **Diagramas de módulos:** Organización interna y dependencias entre módulos.
- [ ] `[O]` **Diagramas de flujo y secuencia:** Representación de procesos, flujos de datos e interacciones.
- [ ] `[O]` **Decisiones arquitectónicas:** Justificación de decisiones relevantes, alternativas evaluadas y principales ventajas y desventajas.

## 5. Interfaces y contratos de integración

- [ ] `[C]` **APIs y endpoints expuestos:** Métodos, rutas, parámetros, headers, cuerpos de solicitud, respuestas, códigos HTTP y errores posibles.
- [ ] `[C]` **Contratos de integración:** Formatos de intercambio, esquemas, protocolos y reglas de comunicación entre componentes.
- [ ] `[C]` **Autenticación y autorización:** Mecanismos de acceso, roles, permisos y requisitos de autenticación.
- [ ] `[C]` **Mensajería y eventos:** Colas, tópicos, eventos publicados y consumidos, contratos de mensajes y políticas de procesamiento.
- [ ] `[C]` **Integraciones con servicios externos:** Configuración necesaria para conectar con proveedores, servicios cloud y otros sistemas.
- [ ] `[O]` **Ejemplos de consumo:** Solicitudes y respuestas de ejemplo, fragmentos de código o comandos `curl`.
- [ ] `[O]` **Documentación interactiva de APIs:** Enlaces a Swagger UI, OpenAPI, Postman u otras herramientas de consulta.
- [ ] `[O]` **Diagramas de integración:** Secuencias de llamadas e interacciones entre servicios.

## 6. Calidad, pruebas y desarrollo

- [ ] `[C]` **Estrategia de pruebas:** Tipos de pruebas utilizadas, como unitarias, integración, contrato, aceptación o end-to-end, y cómo ejecutar cada tipo.
- [ ] `[C]` **Estándares de código:** Convenciones de nomenclatura, formato, análisis estático y criterios de calidad.
- [ ] `[C]` **Guía de contribución:** Procedimiento para modificar el proyecto, validar cambios y proponer contribuciones.
- [ ] `[C]` **CI/CD:** Descripción o referencia a los pipelines de integración, validación y entrega continua.
- [ ] `[O]` **Cobertura y métricas de calidad:** Objetivos de cobertura, umbrales y métricas relevantes.
- [ ] `[O]` **Estrategia de ramas y commits:** Convenciones de branching, nomenclatura de ramas y mensajes de commit.
- [ ] `[O]` **Entorno de depuración:** Configuración para depurar la aplicación y ejecutar pruebas desde el IDE.

## 7. Seguridad, operación y mantenimiento

- [ ] `[C]` **Consideraciones de seguridad:** Gestión de secretos, protección de datos, permisos y prácticas de desarrollo seguro.
- [ ] `[C]` **Manejo de errores y excepciones:** Estrategia de errores, excepciones relevantes y comportamiento ante fallos.
- [ ] `[C]` **Logs y observabilidad:** Formato y ubicación de logs, métricas, trazas, identificadores de correlación y herramientas de diagnóstico.
- [ ] `[C]` **Despliegue:** Procedimientos o referencias para desplegar el proyecto en los ambientes correspondientes.
- [ ] `[C]` **Infraestructura y recursos asociados:** Recursos necesarios, configuración declarativa y dependencias operativas.
- [ ] `[C]` **Disponibilidad y recuperación ante fallos:** Timeouts, reintentos, recuperación y tolerancia a fallos.
- [ ] `[C]` **Base de datos y migraciones:** Configuración de conexión, preparación del esquema y ejecución de migraciones.
- [ ] `[C]` **Rendimiento y escalabilidad:** Límites conocidos, requisitos de capacidad y consideraciones de rendimiento.
- [ ] `[C]` **Posibles errores y solución de problemas:** Problemas frecuentes, causas conocidas, síntomas y soluciones.
- [ ] `[O]` **Procedimientos operativos:** Tareas de mantenimiento, reinicio, recuperación y validaciones posteriores al despliegue.
- [ ] `[O]` **Monitoreo y alertas:** Indicadores operativos, umbrales y referencias a tableros de monitoreo.
- [ ] `[O]` **Costos y consumo de recursos:** Consideraciones de costo, límites de consumo y recomendaciones de optimización.

## 8. Versionado, referencias y aspectos legales

- [ ] `[M]` **Documentación complementaria:** Enlaces a manuales, especificaciones, diagramas, contratos y recursos relacionados. Si no existe documentación adicional, este apartado se omite.
- [ ] `[C]` **Versionado y compatibilidad:** Versión actual, estrategia de versionado y compatibilidad con otros componentes.
- [ ] `[C]` **Historial de cambios:** Referencia al changelog o a las notas de versión cuando exista una gestión formal de releases.
- [ ] `[C]` **Licencia y condiciones de uso:** Licencia aplicable o referencia al archivo correspondiente, según el modelo de distribución.
- [ ] `[O]` **Alternativas y comparaciones:** Soluciones alternativas y diferencias relevantes para entender el propósito del proyecto.
- [ ] `[O]` **Reconocimientos y referencias externas:** Créditos, fuentes y recursos que contribuyeron al desarrollo.

## 9. Reglas generales del estándar

- La documentación debe mantenerse actualizada junto con el código.
- Los apartados `[C]` y `[O]` que no apliquen se omiten, sin marcarlos como "No aplica".
- La documentación extensa debe mantenerse en archivos especializados (por ejemplo, dentro de `docs/`) y enlazarse desde el README.
- Los contratos técnicos deben tener una fuente de verdad. Por ejemplo, utilizar OpenAPI como contrato de una API y referenciarlo desde el README.
- Los diagramas deben utilizarse cuando ayuden a comprender la arquitectura, los módulos o los flujos relevantes.
- Nunca documentar credenciales, tokens, contraseñas ni secretos reales.
- Los comandos y ejemplos deben ser reproducibles y corresponder a la versión actual del proyecto.
- La profundidad de la documentación debe ser proporcional a la complejidad, criticidad y público objetivo del proyecto.

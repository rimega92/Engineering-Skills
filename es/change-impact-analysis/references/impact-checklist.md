# Checklist de impacto

Las dimensiones que un cambio puede afectar y qué buscar en cada una. Los puntos no dependen de la tecnología: aplica cada uno con las costumbres del lenguaje, el framework y la arquitectura del proyecto.

No todos los puntos aplican a todos los cambios. Úsalos como guía, no como un formulario que rellenar. En modo Rápido, recorre Código y Pruebas a fondo y dedica una línea a cada una de las demás, diciendo si aplica.

## Cómo buscar

El compilador o el IDE encuentran las referencias directas. Muchos impactos se esconden donde ellos no ven:

- **Referencias en el código:** llamadas, imports, herencia e implementaciones de interfaces, configuración de inyección de dependencias, genéricos y sobrecargas.
- **Nombres como texto:** reflexión, serialización (JSON, XML, mapeos del ORM), rutas, nombres de eventos y colas, SQL en cadenas, plantillas, claves de traducción, archivos de configuración, scripts, archivos de infraestructura.
- **Código generado:** clientes y modelos generados desde OpenAPI, `.proto` o esquemas. Cambia la fuente, no el archivo generado, y cuenta la regeneración.
- **Otros lenguajes en el mismo repositorio:** el frontend que consume el backend, scripts, infraestructura, pruebas en otro lenguaje.
- **Historial:** `git log` sobre los archivos afectados muestra con qué frecuencia cambian, qué cambios suelen ir juntos y qué zonas son frágiles.

## 1. Código: módulos y unidades

- Unidades que tienen que cambiar: clases, módulos, componentes, funciones, modelos.
- Llamadores de las unidades cambiadas y cómo las usan (un parámetro obligatorio nuevo los rompe a todos; uno opcional, a ninguno).
- Implementaciones y subclases de las interfaces o clases base que cambian.
- Límites de módulos o de capas que el cambio cruza, y si respeta las reglas de dependencias del proyecto.
- Código compartido (utilidades, librerías comunes, componentes base) cuyo cambio llega a partes que no tienen nada que ver.
- Lógica duplicada: la misma regla implementada en varios sitios que tienen que cambiar juntos.

## 2. Procesos y flujos

- Flujos de negocio que pasan por el código cambiado, de principio a fin.
- Trabajos en segundo plano, tareas programadas, procesos por lotes, consumidores de colas y eventos, webhooks.
- Flujos cuyo orden importa: máquinas de estados, procesos de varios pasos, reintentos, compensaciones.
- Procesos en curso durante el despliegue: mensajes ya encolados, trabajos a medias, sesiones abiertas.

## 3. Contratos

- APIs expuestas (REST, GraphQL, gRPC, WebSocket): rutas, campos, tipos, campos obligatorios, códigos de estado, errores.
- Eventos y mensajes publicados o consumidos: nombres, esquemas, versiones.
- API pública de una librería o SDK, comandos y opciones de una CLI, formatos de archivo que se importan o exportan.
- El esquema de la base de datos, cuando otros sistemas la leen directamente.
- **Compatibilidad:** si los consumidores actuales siguen funcionando sin cambios (añadir un campo opcional) o se rompen (renombrar, quitar, cambiar un tipo o hacer obligatorio un campo). Si se rompen, cómo se versiona y cuánto tiempo tienen que convivir las dos versiones.

## 4. Datos

- Cambios de esquema: tablas, columnas, índices, restricciones, tipos, nulabilidad, valores por defecto.
- Registros existentes: qué valor reciben, si hace falta un backfill y cuántas filas toca.
- Migraciones: si bloquean tablas o tardan mucho con volúmenes grandes, si se pueden aplicar sin parar el servicio, si son reversibles.
- Datos derivados de los que cambian: cachés, índices de búsqueda, vistas materializadas, informes, exportaciones, analítica.
- Datos personales o sensibles: clasificación, retención, cifrado, auditoría.

## 5. Pruebas

- Pruebas existentes que cubren el código cambiado y que habrá que modificar (aserciones, fixtures, mocks, snapshots, datos de prueba).
- Pruebas que faltan: comportamiento que el cambio añade o modifica sin prueba, y casos límite.
- Pruebas de contrato, de integración y de extremo a extremo que cubren flujos o consumidores afectados.
- El estado actual de la zona: si tiene poca cobertura, escribir pruebas primero forma parte del cambio y del estimado.
- Infraestructura de pruebas que el cambio necesita: fixtures nuevos, factorías, contenedores, dobles de prueba.

## 6. Consumidores

- **Internos, visibles en el repositorio:** otros módulos, apps o servicios del mismo repositorio (frontend, móvil, workers).
- **Externos, no visibles:** otros repositorios o servicios, otros equipos, apps móviles en versiones ya instaladas, socios y terceros, informes o BI que leen los datos. Lístalos como "por confirmar" y di cómo encontrarlos (logs del API gateway, registro de clientes, catálogo de servicios, preguntar al equipo responsable).
- Qué necesita cada consumidor: nada, una actualización o un despliegue coordinado.

## 7. Configuración e infraestructura

- Variables de entorno, archivos de configuración, feature flags, secretos.
- Infraestructura como código, contenedores, permisos, reglas de red, colas y topics que crear.
- Dependencias: librerías nuevas o actualizaciones de versión, y su propio impacto.
- Build y CI/CD: pipelines, scripts, comprobaciones obligatorias.

## 8. Seguridad y cumplimiento

- Autenticación y autorización: endpoints o datos nuevos que necesitan comprobar permisos, roles que cambian.
- Validación de entrada para los campos o parámetros nuevos.
- Exposición de datos sensibles en respuestas, logs, eventos o errores.
- Requisitos de auditoría, legales o normativos que el cambio toca.

## 9. Operación y observabilidad

- Logs, métricas, trazas, alertas y dashboards que hay que cambiar o añadir.
- Rendimiento: consultas nuevas, bucles sobre colecciones grandes, llamadas externas, comportamiento de la caché.
- Despliegue: orden entre servicios, base de datos antes que el código, feature flags, necesidad de una ventana de mantenimiento.
- Vuelta atrás: si el cambio se puede revertir y qué pasa con los datos escritos mientras tanto.

## 10. Documentación y experiencia de usuario

- README, documentación técnica, documentación de la API, registros de decisiones de arquitectura.
- Textos y pantallas que ven los usuarios, traducciones, correos y notificaciones.
- Guías de usuario, contenido de ayuda, notas de versión.

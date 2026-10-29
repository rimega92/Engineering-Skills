# Lista de comprobación

Las áreas que hay que revisar antes de que una historia esté lista para desarrollo. Para cada área: qué debería dejar claro la historia, qué buscar en el código y preguntas típicas. Usa las preguntas como inspiración, no como una lista para copiar: pregunta solo lo que la historia y el código dejan abierto, y formúlalo con lo que encontraste.

Da a cada área un estado: ✅ Clara, ⚠️ Ambigua, ❌ Falta o ➖ No aplica. Un área en ⚠️ o ❌ se convierte en una pregunta, un supuesto o una pregunta abierta.

## 1. Valor y usuario

- **La historia debería decir:** quién lo necesita (rol o tipo de usuario), qué quiere hacer y para qué. El "para qué" decide qué elegir cuando algo no está especificado.
- **En el código:** los roles y tipos de usuario que existen.
- **Preguntas típicas:** ¿qué tipos de usuario entran? ¿Qué problema resuelve y cómo sabremos que está resuelto?

## 2. Alcance y tamaño

- **La historia debería decir:** qué incluye y qué deja fuera de forma explícita, y en qué plataformas o canales (web, móvil, backoffice, API pública).
- **En el código:** todos los sitios donde vive el mismo comportamiento (por ejemplo, la misma pantalla en web y en móvil, o la misma regla en dos servicios).
- **Preguntas típicas:** ¿aplica también a la app móvil? ¿Cubre los registros existentes o solo los nuevos?
- **Tamaño:** si la historia mezcla varios comportamientos, tipos de usuario o entregas independientes, propón dividirla. Cada parte debería aportar valor por sí sola y poder probarse.

## 3. Criterios de aceptación

- **La historia debería decir:** condiciones observables y verificables para el flujo principal, las alternativas y los errores. "Funciona correctamente" o "es rápido" no son criterios.
- **En el código:** las pruebas existentes del área, que muestran cómo se verifica hoy su comportamiento.
- **Preguntas típicas:** ¿qué ve el usuario cuando funciona, y cuando falla? ¿Qué resultado demuestra que la historia está terminada?

## 4. Reglas de negocio y validaciones

- **La historia debería decir:** reglas, cálculos, límites, formatos, campos obligatorios, estados y transiciones.
- **En el código:** validaciones, máquinas de estados, cálculos y constantes existentes. Aquí aparecen la mayoría de las contradicciones: un campo obligatorio en el API pero opcional en la historia, un estado que la entidad no tiene, un límite distinto.
- **Preguntas típicas:** el código rechaza X (`ruta:línea`); ¿eso debe cambiar? ¿Qué pasa en el límite (cero, máximo, vacío)? ¿Cuál manda si dos reglas chocan?

## 5. Casos límite y errores

- **La historia debería decir:** qué pasa con entradas vacías o inválidas, duplicados, acciones simultáneas, timeouts, fallos parciales y dependencias caídas.
- **En el código:** cómo maneja hoy el área los errores (mensajes, reintentos, códigos de error, rollback).
- **Preguntas típicas:** ¿y si el servicio externo no responde? ¿Puede el usuario hacerlo dos veces? ¿Y si falla la mitad de los registros?

## 6. Datos

- **La historia debería decir:** datos nuevos o cambiados, qué pasa con los registros existentes, de dónde salen los datos, cuánto tiempo se guardan y si incluyen datos personales o sensibles.
- **En el código:** entidades, tablas, columnas, migraciones y quién más lee esos datos.
- **Preguntas típicas:** ¿qué valor toman los registros existentes? ¿Se calcula o se guarda? ¿Es un dato personal y quién puede verlo?

## 7. Contratos e integraciones

- **La historia debería decir:** qué APIs, eventos, archivos o integraciones con terceros cambian, y si los consumidores actuales deben seguir funcionando.
- **En el código:** endpoints, modelos de petición y respuesta, eventos, clientes de otros servicios, especificaciones de API (OpenAPI, esquemas GraphQL, Protobuf) y los consumidores que se ven.
- **Preguntas típicas:** ¿el campo nuevo debe aparecer en todos los endpoints que devuelven esta entidad? ¿Se acepta un cambio incompatible o debe ser compatible? ¿Quién consume este evento fuera de este repositorio?

## 8. Diseño, textos y experiencia de usuario

- **La historia debería decir:** las pantallas o el enlace a los diseños, los textos y sus traducciones, y los estados: cargando, vacío, error, éxito y sin permiso.
- **En el código:** componentes existentes que se pueden reutilizar, archivos de traducción, convenciones de accesibilidad.
- **Preguntas típicas:** ¿hay diseño? ¿Qué ve el usuario mientras carga, o cuando no hay nada que mostrar? ¿Los textos necesitan traducción?

## 9. Permisos y seguridad

- **La historia debería decir:** quién puede ver y hacer qué, y qué pasa cuando lo intenta alguien sin permiso.
- **En el código:** roles, comprobaciones de permisos, guards y políticas en las pantallas y endpoints implicados.
- **Preguntas típicas:** ¿puede hacerlo cualquier rol o solo los administradores? ¿Puede un usuario actuar sobre datos de otro? ¿Necesita registro de auditoría?

## 10. Requisitos no funcionales

- **La historia debería decir:** volumen, tiempo de respuesta, disponibilidad, auditoría, cumplimiento normativo y analítica o tracking, solo cuando importan para esta historia.
- **En el código:** paginación, límites, cachés, eventos de analítica y métricas existentes.
- **Preguntas típicas:** ¿cuántos registros como máximo (exportar 100 filas no es lo mismo que un millón)? ¿Necesita un evento de analítica? ¿Hay algún requisito legal o normativo?

## 11. Dependencias y despliegue

- **La historia debería decir:** de qué depende (otros equipos, otras historias, terceros, datos) y cómo se libera (de una vez, detrás de un feature flag, de forma gradual).
- **En el código:** feature flags, configuración por entorno, clientes de servicios externos.
- **Preguntas típicas:** ¿otro equipo tiene que cambiar algo antes? ¿Debe ir detrás de un feature flag? ¿Se necesita en todos los entornos y países?

## 12. Facilidad de prueba

- **La historia debería decir:** lo suficiente para saber cómo se va a probar: datos de prueba, entornos y las dependencias que hay que simular.
- **En el código:** tipos de prueba y herramientas en uso, fixtures, mocks de servicios externos.
- **Preguntas típicas:** ¿hay datos de prueba para este caso en el entorno de pruebas? ¿Se puede usar el tercero en las pruebas o hace falta un mock?

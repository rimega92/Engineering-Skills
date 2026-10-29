# Checklist de revisión

Qué buscar en un cambio, con qué profundidad y cómo priorizar cada hallazgo. Los puntos no dependen de ninguna tecnología: aplica cada uno con las convenciones del lenguaje, el framework y la arquitectura del proyecto.

No todos los puntos aplican a todos los cambios. Úsalos como guía, no como un formulario que rellenar.

## Prioridad

Prioriza cada hallazgo según su impacto, alcance, probabilidad y contexto. Si el proyecto tiene su propia escala, usa esa en lugar de esta.

| Prioridad | Significado | Ejemplo |
|---|---|---|
| 🔴 **P0, Crítica** | Riesgo crítico e inmediato, como una vulnerabilidad explotable o una corrupción grave de datos. | Exposición de información financiera de muchos clientes |
| 🟠 **P1, Alta** | Defecto importante que puede afectar a una operación central o provocar un fallo grave. | Una transacción queda aplicada a medias |
| 🟡 **P2, Media** | Defecto de alcance limitado, o riesgo relevante bajo ciertas condiciones. | Un caso límite produce un resultado incorrecto |
| 🔵 **P3, Baja** | Problema menor y concreto que vale la pena corregir. | Un escenario poco frecuente se comporta mal con poco efecto |
| 💡 **Info** | Mejora no bloqueante o recomendación que no es un defecto confirmado. | Simplificar una función que funciona correctamente |

Reglas:

- La prioridad refleja el impacto real o razonablemente esperado.
- Incumplir un principio de diseño no hace crítico un hallazgo por sí solo.
- Ten en cuenta el alcance del problema, las condiciones necesarias para que ocurra y las salvaguardas que ya existen.
- Si el proyecto usa a la vez severidad técnica y prioridad de corrección, mantenlas separadas.
- No dupliques hallazgos que comparten causa raíz.
- No presentes preferencias de estilo como defectos funcionales.
- Si la evidencia no es suficiente, reporta la incertidumbre (riesgo potencial) en lugar de un defecto confirmado.

**Veredicto** de la revisión:

- ✅ **Listo:** ningún hallazgo P0, P1 ni P2.
- ⚠️ **Listo con cambios:** ningún hallazgo P0, pero hay P1 o P2 que corregir antes.
- ❌ **Necesita trabajo:** al menos un hallazgo P0, o hay que replantear el enfoque.

## Niveles de profundidad

Cada modo de revisión usa algunos de estos niveles: Rápida usa el nivel 1; Estándar, los niveles 1 y 2; Profunda, los tres.

### Nivel 1, básica: todos los modos

- Correctitud funcional y casos límite relevantes.
- Posibles regresiones.
- Cumplimiento de los estándares y del scaffold del proyecto.
- Alcance y coherencia del cambio.
- Pruebas y verificabilidad.
- Manejo básico de errores.
- Problemas de seguridad evidentes.
- Coherencia con la arquitectura existente.

### Nivel 2, especializada: modos Estándar y Profunda

Profundiza con los apartados 1 a 12 de abajo, pero solo los de las áreas que toque el cambio: arquitectura y SOLID, seguridad y autorización, persistencia e integridad de datos, APIs, eventos e integraciones, rendimiento y complejidad, concurrencia, resiliencia, configuración y observabilidad, migraciones y compatibilidad, dependencias e infraestructura.

### Nivel 3, profunda: modo Profunda

Cuando el cambio afecte a sistemas críticos, datos sensibles, operaciones financieras, seguridad o componentes de alta disponibilidad, considera además:

- Modelado de amenazas y escenarios de abuso.
- Integridad financiera y consistencia transaccional.
- Idempotencia y operaciones duplicadas.
- Concurrencia compleja y condiciones de carrera.
- Fallos parciales en sistemas distribuidos; reintentos, compensaciones y recuperación.
- Compatibilidad durante despliegues graduales; migraciones de datos y reversibilidad.
- Resiliencia cuando las dependencias no están disponibles.
- Impacto operativo, alertas y capacidad de diagnóstico; riesgos de rollback y recuperación ante incidentes.

## 1. Diseño y calidad del código

- **Clean code:** legibilidad, nombres descriptivos, intención clara, funciones cohesionadas, poco ruido.
- **SOLID:** responsabilidad única, abierto/cerrado, sustitución de Liskov, segregación de interfaces e inversión de dependencias, donde aporten valor.
- **KISS:** sin complejidad innecesaria; la solución más simple que cumple los requisitos.
- **DRY:** lógica o conocimiento duplicados que pueden volverse inconsistentes.
- **YAGNI:** sin funcionalidades, abstracciones ni puntos de extensión que no se necesitan.
- **Separación de responsabilidades:** responsabilidades bien separadas (por ejemplo, validación, reglas de negocio y acceso a datos no mezclados en una función).
- **Alta cohesión y bajo acoplamiento:** responsabilidades relacionadas juntas, sin dependencias innecesarias ni accesos a los detalles internos de otros módulos.
- **Menor sorpresa:** los componentes se comportan de forma predecible; los nombres no mienten sobre lo que hace el código.
- **Complejidad accidental:** anidamiento profundo, funciones demasiado largas, condiciones difíciles de leer, abstracciones innecesarias.
- **Encapsulamiento:** los detalles internos y el estado se exponen solo cuando hace falta.
- **Coherencia del diseño:** el cambio mantiene los criterios de diseño que ya sigue el proyecto.

## 2. Arquitectura y estructura del proyecto

- **Cumplimiento del scaffold:** la estructura de directorios, módulos, paquetes y archivos que define el proyecto.
- **Arquitectura definida:** capas, módulos, límites de contexto y responsabilidades arquitectónicas.
- **Reglas de dependencia:** sin dependencias prohibidas, ciclos ni dependencias en la dirección equivocada.
- **Patrones de diseño:** se usan cuando resuelven un problema concreto, no de forma artificial.
- **DDD, cuando aplique:** entidades, objetos de valor, agregados, repositorios, servicios de dominio y límites de contexto.
- **Separación entre dominio e infraestructura:** las reglas de negocio no dependen de detalles técnicos sin necesidad.
- **Configuración y convenciones:** las reglas documentadas en el `README`, `AGENTS.md`, `CLAUDE.md`, archivos de instrucciones, linters y demás estándares.
- **Reutilización de componentes:** se aprovechan los componentes existentes cuando conviene, sin añadir abstracciones genéricas que nadie necesita.
- **Responsabilidad de los módulos:** ningún módulo asume responsabilidades ajenas a su propósito.
- **Coherencia arquitectónica:** no se introduce una arquitectura distinta sin justificación o, cuando haga falta, sin aprobación.

## 3. Correctitud funcional y lógica

- **Requisitos:** el cambio cumple los requisitos y criterios de aceptación conocidos.
- **Lógica de negocio:** reglas incorrectas, omitidas, contradictorias o en la capa equivocada.
- **Casos límite:** valores nulos o vacíos, límites numéricos, colecciones vacías, duplicados, entradas inesperadas.
- **Condiciones y ramas:** condiciones invertidas, errores de uno (off-by-one), ramas inalcanzables, escenarios no contemplados, casos de `switch` o `match` incompletos.
- **Estado y ciclo de vida:** inicialización, actualizaciones, transiciones de estado y limpieza de recursos.
- **Idempotencia:** las operaciones repetidas no causan efectos secundarios incorrectos cuando la idempotencia es necesaria.
- **Compatibilidad hacia atrás:** cambios que pueden romper comportamientos existentes, consumidores, integraciones o datos.
- **Fechas y zonas horarias:** formatos, conversiones, límites de fechas y zonas horarias.
- **Precisión numérica:** redondeos, overflow, conversiones y precisión decimal según el dominio.
- **Invariantes:** las condiciones que siempre deben cumplirse se siguen cumpliendo.
- **Efectos secundarios:** cambios de estado inesperados, escrituras adicionales o llamadas externas sin justificar.

## 4. Seguridad

- **Validación de entradas:** datos de usuarios, sistemas externos y otras fuentes no confiables.
- **Autenticación:** las operaciones protegidas validan bien la identidad.
- **Autorización:** permisos, roles y control de acceso a recursos y operaciones; controles que no se hacen solo en el cliente.
- **Inyección:** SQL, comandos, XSS, LDAP, rutas, plantillas y cualquier otro tipo que aplique.
- **Secretos:** sin credenciales, tokens, claves privadas ni secretos en el código, el repositorio o los logs. Reporta la ubicación, nunca el valor.
- **Protección de datos:** exposición mínima de información personal, financiera, confidencial o sensible.
- **Criptografía:** algoritmos, protocolos y librerías aprobados; nada de criptografía propia.
- **Dependencias vulnerables:** vulnerabilidades conocidas en dependencias nuevas o actualizadas.
- **Consumo abusivo de recursos:** límites de peticiones, tamaños de entrada, operaciones costosas y posibilidades de abuso.
- **Configuración insegura:** permisos excesivos, valores por defecto inseguros, servicios expuestos sin necesidad.
- **Mensajes de error:** los errores no revelan secretos, detalles internos ni información útil para un atacante.
- **Mínimo privilegio:** cada componente tiene solo los permisos que necesita.

## 5. Manejo de errores y resiliencia

- **Manejo de errores:** sin errores ignorados, excepciones ocultas ni seguir adelante en un estado inválido.
- **Excepciones específicas:** sin capturas demasiado amplias; se conserva la causa original cuando importa.
- **Contratos de error:** respuestas, códigos de error y mensajes coherentes con los contratos existentes.
- **Timeouts:** límites razonables en las llamadas externas y en las operaciones que pueden bloquearse.
- **Reintentos:** sin reintentos ilimitados, tormentas de peticiones ni efectos secundarios duplicados.
- **Circuit breakers:** valorados para dependencias cuya indisponibilidad puede afectar a servicios críticos.
- **Degradación controlada:** el comportamiento cuando una dependencia no está disponible.
- **Liberación de recursos:** conexiones, archivos, transacciones y otros recursos se cierran bien.
- **Consistencia ante fallos:** qué pasa cuando una operación falla en parte o del todo.
- **Recuperación:** el sistema se recupera sin intervención manual cuando eso es un requisito.
- **Propagación de errores:** los errores se propagan o transforman bien entre capas.
- **Cancelación:** sin trabajo innecesario después de una cancelación o de un timeout.

## 6. Rendimiento y concurrencia

- **Complejidad algorítmica:** algoritmos costosos o que no escalan con el volumen esperado.
- **Acceso a datos:** consultas redundantes, consultas N+1, falta de paginación, operaciones innecesarias.
- **Memoria y recursos:** acumulaciones innecesarias, copias excesivas, fugas, consumo sin límite.
- **Operaciones bloqueantes:** I/O bloqueante o trabajo pesado en el contexto de ejecución equivocado (por ejemplo, el hilo principal o de la interfaz).
- **Concurrencia:** acceso compartido, sincronización, atomicidad, seguridad entre hilos, condiciones de carrera, llamadas asíncronas sin esperar.
- **Deadlocks:** orden de adquisición de bloqueos, transacciones y esperas mutuas.
- **Caché:** expiración, invalidación, consistencia y riesgo de servir datos obsoletos.
- **Escalabilidad:** volúmenes, concurrencia y patrones de carga razonablemente esperados.
- **Llamadas externas:** llamadas repetidas, serialización innecesaria, falta de límites.
- **CPU:** cálculos repetidos o procesamiento innecesario en flujos relevantes.
- **Pools y colas:** capacidad y políticas de espera.
- **Evidencia:** no afirmes que hay un problema de rendimiento sin evidencia suficiente; distingue los riesgos teóricos de los problemas medidos.

## 7. Persistencia e integridad de datos

- **Transacciones:** límites transaccionales, rollback y atomicidad.
- **Integridad de datos:** restricciones, relaciones, invariantes y reglas de negocio.
- **Escrituras concurrentes:** sin actualizaciones perdidas, duplicados ni conflictos entre operaciones simultáneas.
- **Migraciones de esquema:** compatibilidad, orden de ejecución, reversibilidad y seguridad del despliegue.
- **Consultas y ORM:** consultas ineficientes, efectos secundarios inesperados del mapeo o del lazy loading.
- **Datos existentes:** registros históricos, campos nulos, formatos anteriores y datos inconsistentes.
- **Precisión financiera:** decimales, moneda, redondeo, idempotencia y trazabilidad.
- **Restricciones de base de datos:** índices, claves, restricciones y relaciones adecuados para el cambio.
- **Consistencia entre sistemas:** riesgo de que bases de datos, servicios y otros sistemas se desincronicen.
- **Operaciones destructivas:** eliminaciones, actualizaciones masivas o cambios irreversibles.
- **Datos sensibles:** cómo se tratan, guardan y eliminan los datos confidenciales.
- **Compatibilidad durante los despliegues:** las versiones antigua y nueva pueden funcionar a la vez durante una migración.

## 8. APIs e integraciones

- **Contratos de API:** esquemas, códigos de estado, formatos, nombres y semántica acordada.
- **Compatibilidad con los consumidores:** impacto en clientes y sistemas dependientes.
- **Validación y serialización:** formatos, campos obligatorios, límites y conversiones.
- **Integraciones externas:** errores, latencia, indisponibilidad, límites y cambios del proveedor.
- **Eventos y mensajería:** contratos, duplicados, orden, reentrega, colas de mensajes fallidos (DLQ) y evolución de esquemas.
- **Consistencia distribuida:** idempotencia, compensaciones y consistencia eventual.
- **Versionado:** los cambios de contrato siguen la estrategia de versionado del proyecto.
- **Paginación y filtros:** límites, ordenamiento y comportamiento con conjuntos grandes de resultados.
- **Compatibilidad de formatos:** sin cambios involuntarios en nombres de campos, tipos, valores por defecto o formatos de fecha.
- **Respuestas inesperadas:** comportamiento ante respuestas incompletas, inválidas o incompatibles.
- **Límites del proveedor:** cuotas, rate limits y restricciones de los sistemas integrados.

## 9. Pruebas y verificabilidad

- **Cobertura de escenarios:** las pruebas cubren el comportamiento importante, no solo las líneas ejecutadas. La lógica nueva tiene pruebas; una corrección de un error idealmente trae una prueba que lo habría detectado.
- **Pruebas unitarias:** reglas de negocio, límites, errores y escenarios relevantes.
- **Pruebas de integración:** interacciones reales entre componentes, donde aplique.
- **Pruebas de regresión:** comportamientos anteriores que el cambio podría romper.
- **Aserciones:** sin pruebas que pasan sin comprobar el resultado correcto.
- **Aislamiento y determinismo:** sin dependencias accidentales del orden, el reloj, la red o datos externos sin control.
- **Mocks:** sin simulaciones excesivas que impidan probar el comportamiento real.
- **Pruebas negativas:** entradas inválidas, permisos insuficientes y fallos externos.
- **Pruebas de límites:** valores extremos, colecciones vacías y condiciones excepcionales.
- **Pruebas de concurrencia:** operaciones simultáneas cuando el cambio puede generar conflictos.
- **Pruebas de contrato:** compatibilidad con los consumidores y proveedores de APIs o eventos.
- **Pruebas de migración:** transformaciones, integridad y compatibilidad de los datos.
- **Datos de prueba:** sin fixtures inconsistentes ni datos que oculten defectos.
- **Comportamiento cambiado:** se refleja en las pruebas existentes, en lugar de esquivarlo borrándolas o debilitándolas.

## 10. Mantenibilidad y coherencia

- **Nombres:** coherentes con el dominio y las convenciones existentes. Evita nombres vagos (`data`, `info`, `manager`) y abreviaturas desconocidas.
- **Duplicación:** lógica duplicada que puede divergir y encarecer el mantenimiento.
- **Comentarios y documentación:** se corrige la documentación desactualizada; los comentarios explican el porqué cuando el código no basta. Sin `TODO` sin contexto.
- **Código muerto:** imports, variables, funciones, ramas y archivos sin usar; código comentado; restos de depuración.
- **Estilo:** el formateador, el linter y las reglas del proyecto, sin convertir preferencias personales en defectos.
- **APIs internas:** sin interfaces innecesarias, demasiados parámetros, flags booleanos que esconden dos funciones ni contratos difíciles de usar bien.
- **Valores mágicos:** números o textos sin explicar que deberían ser constantes con nombre o configuración.
- **Deuda técnica:** atajos que crean riesgos concretos y relevantes.
- **Flujo legible:** el comportamiento se sigue con facilidad, sin saltos ni indirecciones innecesarios.
- **Responsabilidad de las funciones:** funciones y métodos centrados en una responsabilidad comprensible.
- **Mutabilidad:** sin cambios de estado difíciles de rastrear o que causen efectos secundarios innecesarios.
- **Configuración duplicada:** sin valores repetidos que puedan divergir con el tiempo.
- **Facilidad de cambio:** el diseño cumple los requisitos actuales sin complejidad innecesaria.

## 11. Configuración, despliegue y observabilidad

- **Configuración por entorno:** sin valores propios de un entorno escritos directamente en el código.
- **Variables y valores por defecto:** valores obligatorios validados, valores por defecto seguros, fallo claro si falta configuración.
- **Logs:** contexto útil, sin secretos ni datos sensibles.
- **Métricas y trazas:** instrumentación cuando el cambio altera flujos críticos o puntos de fallo importantes.
- **Health checks:** reflejan el estado real de la aplicación y de sus dependencias relevantes.
- **CI/CD:** compatible con la compilación, las validaciones, el empaquetado y el despliegue.
- **Compatibilidad operativa:** feature flags, rollback, despliegue gradual y cambios incompatibles.
- **Recursos:** límites, cuotas, conexiones y recursos que necesita el cambio.
- **Infraestructura como código:** permisos, exposición, configuración y efectos colaterales de los cambios de infraestructura.
- **Alertas:** si el cambio necesita nuevas señales para detectar fallos importantes.
- **Trazabilidad:** las operaciones críticas se pueden seguir a través de los componentes relevantes.
- **Despliegues parciales:** comportamiento mientras conviven versiones distintas del sistema.
- **Rollback:** si el cambio se puede revertir, y qué efectos persistentes podrían impedir una reversión segura.

## 12. Alcance y calidad del cambio

- **Alcance:** sin cambios sin relación, refactorizaciones oportunistas ni modificaciones innecesarias.
- **Trazabilidad:** el cambio está ligado al requisito, la incidencia o la decisión que lo justifica.
- **Tamaño y cohesión:** el cambio es comprensible, revisable y está bien dividido; no agrupa cambios funcionales independientes.
- **Archivos generados y artefactos:** sin binarios, archivos temporales ni artefactos accidentales.
- **Dependencias nuevas:** justificadas, teniendo en cuenta el mantenimiento, la licencia, la seguridad y el coste operativo.
- **Archivos de configuración:** sin cambios accidentales ni valores locales.
- **Cambios de contrato:** se señalan los que necesitan coordinación con otros equipos o consumidores.
- **Documentación:** si el cambio requiere actualizar el `README`, diagramas, contratos o instrucciones.
- **Coherencia del conjunto:** código, pruebas, configuración, migraciones y documentación describen el mismo comportamiento.
- **Desviaciones justificadas:** incumplimientos de los estándares que necesitan una excepción documentada.

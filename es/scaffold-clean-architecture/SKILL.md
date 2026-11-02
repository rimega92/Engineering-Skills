---
name: scaffold-clean-architecture
description: Crea aplicaciones Java nuevas con Clean Architecture usando el plugin de Gradle scaffold-clean-architecture de Bancolombia (co.com.bancolombia.cleanArchitecture), y añade modelos, casos de uso, driven adapters, entry points, helpers, pipelines y pruebas a proyectos generados con él. Comprueba Java y Gradle, pregunta las decisiones del proyecto, ejecuta las tareas del plugin, aplica las correcciones a problemas conocidos del proyecto generado, implementa el flujo de negocio respetando la regla de dependencias y verifica el resultado con validateStructure, la compilación, los tests y un arranque real de la aplicación. Úsala cuando el usuario pida crear un microservicio o aplicación Java con Clean Architecture o con el scaffold de Bancolombia, o añadir un módulo, adaptador o entry point a un proyecto que use este plugin. No sirve para migrar proyectos de Scaffold 4 ni para aplicar Clean Architecture a proyectos no generados con el plugin.
compatibility: Requiere Java 17 o superior, Gradle 9.2.1 o superior y acceso de red al Gradle Plugin Portal y a Maven Central. Escrita y probada con la versión 5.1.0 del plugin.
---

# scaffold-clean-architecture

Crea y hace crecer aplicaciones Java con el plugin de Gradle [scaffold-clean-architecture](https://github.com/bancolombia/scaffold-clean-architecture). El plugin genera un proyecto Spring Boot multimódulo en el que cada capa es un módulo de Gradle y la regla de dependencias se comprueba en cada compilación.

El resultado es un proyecto que compila, cuyos tests se ejecutan de verdad y que arranca. Generar los archivos no basta: varios proyectos generados no compilan o no ejecutan sus tests hasta aplicar las correcciones de `references/known-issues.md`.

## Principios

- **Usa el plugin, no lo imites.** Crea los módulos con sus tareas en lugar de escribir su estructura a mano. Escribe a mano solo el código de negocio que va dentro.
- **Regenerar sobrescribe.** `gm`, `guc`, `gda` y `gep` sobrescriben sin avisar los archivos de un módulo o clase que ya existe, incluidas tus ediciones, y no comprueban git. `ca` reemplaza los archivos de la raíz. Nunca ejecutes un generador sobre algo que ya existe sin la confirmación explícita del usuario.
- **No te fíes del silencio de una tarea.** Algunas terminan bien sin haber hecho nada útil: `gep --type=restmvc` y `gda --type=jpa` generan sin protestar en un proyecto reactivo, `u` con cambios pendientes no hace nada y aun así termina en `BUILD SUCCESSFUL`, y `test` pasa sin ejecutar tests. Comprueba el resultado, no solo el código de salida.
- **Informa de lo verificado.** Di qué comprobaciones se hicieron y cuáles no se pudieron hacer (por ejemplo, un arranque que necesita una base de datos). Nunca presentes una compilación como prueba de que los tests pasaron sin haberlos visto ejecutarse.
- **Nunca secretos.** No escribas credenciales en `application.yaml` ni en ningún otro archivo. Usa variables de entorno o las opciones de secretos del plugin.

## Decide qué hacer

Mira la carpeta de trabajo:

| Qué hay | Qué hacer |
| ------- | --------- |
| Carpeta vacía, o el usuario pide un proyecto nuevo | **Crear** un proyecto (pasos 1 a 6) |
| `gradle.properties` con `package=` y `reactive=`, y el plugin en `settings.gradle` | **Hacer crecer** el proyecto (pasos 4 a 6) |
| Un archivo `main.gradle` en la raíz | Es un proyecto de Scaffold 4. Detente: el plugin se niega a ejecutarse ahí. Indica al usuario la [guía de migración](https://bancolombia.github.io/scaffold-clean-architecture/docs/migrations/v4-v5). Esta skill no migra |
| Cualquier otro proyecto con código | Detente. `ca` reemplazaría sus archivos de la raíz. Crea el proyecto nuevo en otra carpeta |

## 1. Comprueba el entorno

1. **Java:** ejecuta `java -version` y lista los JDK instalados (en macOS, `/usr/libexec/java_home -V`). La versión de Java del proyecto debe estar instalada: el proyecto generado usa un toolchain de Gradle sin descarga automática, así que compilar para una versión que no está instalada falla con `Cannot find a Java installation`. La versión por defecto del plugin es la 25.
2. **Gradle:** ejecuta `gradle --version`. Necesita 9.2.1 o superior. Si falta, pide al usuario que lo instale. Después, el proyecto generado usa su propio wrapper.
3. **Versión del plugin:** lee la última de `https://plugins.gradle.org/m2/co/com/bancolombia/cleanArchitecture/co.com.bancolombia.cleanArchitecture.gradle.plugin/maven-metadata.xml`. No la tomes de la guía oficial, cuyos ejemplos pueden ir atrasados. Si la última es más nueva que la 5.1.0, úsala y avisa al usuario de que esta skill se probó con la 5.1.0, así que hay que volver a comprobar sus problemas conocidos. Si no está disponible la misma versión mayor, usa la 5.1.0.

## 2. Pregunta las decisiones

Pregúntalo todo en un solo mensaje, con una recomendación para cada punto. No preguntes lo que el usuario ya dijo.

| Decisión | Opción | Recomendación |
| -------- | ------ | -------------- |
| Nombre del proyecto | `--name` | Obligatorio, el valor por defecto no sirve |
| Paquete base | `--package` | Obligatorio. Nunca dejes el valor por defecto: `co.com.bancolombia` pertenece a esa empresa |
| Tipo | `--type=reactive` o `imperative` | `reactive` si el servicio hace mucha E/S y el equipo conoce Reactor; `imperative` para un stack más simple o para JPA. Explica la diferencia si el usuario no tiene preferencia: condiciona qué módulos están disponibles |
| Java | `--java-version=17`, `21` o `25` | La más alta de estas que esté instalada |
| Lombok | `--lombok` | `true`. Con `false`, algunos adaptadores no compilan (ver problemas conocidos) |
| Métricas | `--metrics` | `true` |
| Pruebas de mutación | `--mutation` | `true`. Hacen más lenta la compilación; `false` quita Pitest, y entonces `-x pitest` falla porque la tarea no existe |
| OpenTelemetry | `--otel` | `false`, salvo que haya un colector. Con `true`, el agente registra errores de exportación continuamente si nada escucha en `localhost:4318` |
| Entry points y adaptadores | Ver `references/tasks.md` | Lo que necesite el servicio: cómo recibe peticiones y con qué sistemas habla |
| Primer modelo y caso de uso | Nombres de negocio | Opcional, se pueden añadir después |

**La analítica debe ir en este mensaje.** El plugin envía por defecto datos de uso a un servidor externo: nombre de usuario del sistema operativo, país, versiones de Java y del plugin, tarea y tipo, y los nombres que se den a modelos, casos de uso, helpers y módulos eliminados. Cuenta dos cosas al usuario:

- `ca` siempre envía un evento, aunque `analytics=false` ya esté en el archivo, porque reescribe `gradle.properties`. Si esto no es aceptable (por ejemplo, en un proyecto interno con un nombre confidencial), deja que el usuario decida antes de ejecutarlo.
- Esta skill desactiva la analítica justo después de `ca`, antes de que se envíe ningún nombre, salvo que el usuario prefiera mantenerla.

## 3. Genera el proyecto

1. Crea la carpeta y haz `git init`, si aún no es un repositorio.
2. Escribe el `build.gradle` mínimo, con la versión del paso 1:

   ```groovy
   plugins {
       id 'co.com.bancolombia.cleanArchitecture' version '<version>'
   }
   ```

3. Ejecuta el generador. También crea el wrapper de Gradle:

   ```shell
   gradle ca --name=<Nombre> --package=<paquete> --type=<tipo> --java-version=<version>
   ```

4. Desactiva la analítica, lo primero después de `ca`:

   ```shell
   ./gradlew analytics --enabled false
   ```

5. **Haz que los tests se ejecuten.** Consulta `references/known-issues.md`, problema 1. En la versión 5.1.0 la tarea `test` no ejecuta ningún test, así que un test que falla no rompe la compilación. Aplica la corrección al `build.gradle` de la raíz, avisa al usuario y confirma que aparecen archivos `build/test-results/test/*.xml`.
6. Propón un primer commit y espera la respuesta. A partir de aquí, un repositorio limpio es la única protección frente a un generador que sobrescriba algo.

## 4. Añade módulos

Lee `references/tasks.md` para las tareas y sus opciones. Antes de cada generador:

1. **Comprueba que encaja con el tipo de proyecto,** con la tabla de compatibilidad: lee `reactive=` en `gradle.properties`. No confíes en que el plugin lo rechace, porque no siempre lo hace.
2. **Comprueba que aún no existe,** mirando en `domain/` e `infrastructure/`. Si existe, pregunta antes de sobrescribir y sugiere hacer commit primero.
3. **Usa nombres de negocio** para modelos y casos de uso, sin palabras de tecnología. El plugin rechaza nombres que terminan en `dto`, `request` o `response` y nombres que contienen `kafka`, `redis`, `s3`, `http` y otros.

Orden habitual: `gm`, `guc`, `gda`, `gep`. Después de los generadores:

1. Busca `co.com.bancolombia` en los módulos nuevos y aplica las correcciones de `references/known-issues.md`, problema 2. El plugin deja fijo su propio paquete en algunas plantillas.
2. Aplica las demás correcciones de ese archivo que correspondan a los módulos generados.
3. Ejecuta `./gradlew validateStructure compileJava compileTestJava`, para que un problema aparezca ahora y no cuando ya hayas construido encima.

## 5. Implementa el flujo

Lee `references/architecture.md`. Lo esencial:

- **El flujo va** entry point → caso de uso → gateway (una interfaz en `model`) ← driven adapter.
- **No conectes módulos a mano.** Los módulos nuevos se descubren por su `build.gradle`, y `app-service` los recibe automáticamente. Las clases de caso de uso se convierten en beans si terminan en `UseCase` y están bajo `<paquete>.usecase`.
- **Reemplaza los marcadores del generador:** los tipos `Object` en los adaptadores (`/* change for domain model */`), las clases de ejemplo `My*` y las rutas de ejemplo en `Handler` y `RouterRest`.
- **Actualiza los tests generados** cuando cambies el código que cubren. Inyectar un caso de uso en `Handler` o quitar una ruta de ejemplo rompe `RouterRestTest` y `ConfigTest`.
- **Escribe tests del código de negocio,** sobre todo de los casos de uso, con los gateways simulados.

## 6. Verifica

Ejecuta esto en orden e informa de cada resultado:

1. `./gradlew validateStructure`: la regla de dependencias.
2. `./gradlew build jacocoMergedReport`: compilación, tests, Pitest si está activo y cobertura unificada en `build/reports/jacocoMergedReport/`.
3. **Comprueba que los tests se ejecutaron:** debe haber archivos `build/test-results/test/*.xml` con más de cero tests en los módulos que tienen tests.
4. `./gradlew bootRun` y una petición a un endpoint real y a `/actuator/health`; después, detén el proceso. Si necesita una base de datos o un broker que no está disponible, dilo y di qué queda sin verificar, en vez de saltártelo en silencio.
5. Lee `build/issues.json`, si existe: la mayoría de las reglas de ArchUnit solo informan ahí, sin romper la compilación.

Cierra con un resumen: qué se generó, las correcciones aplicadas, qué se verificó, qué le queda al usuario (valores de entorno, credenciales, reglas de negocio reales) y los comandos para ejecutar el proyecto. Pregunta antes de hacer commit.

## Archivos de referencia

- `references/tasks.md`: todas las tareas, sus opciones y qué está disponible para cada tipo de proyecto.
- `references/architecture.md`: capas, reglas de dependencias, conexión automática, reglas de ArchUnit y configuración del proyecto generado.
- `references/known-issues.md`: problemas verificados del plugin y del código generado, con sus correcciones, y diferencias con la documentación oficial.

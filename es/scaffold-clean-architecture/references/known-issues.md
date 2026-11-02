# Problemas conocidos

Problemas encontrados al ejecutar la versión 5.1.0 del plugin con Gradle 9.8.2 en macOS. Son hechos de esa versión: en una más nueva, comprueba si cada uno sigue ocurriendo antes de aplicar su corrección.

## 1. La tarea `test` no ejecuta ningún test

**Síntoma:** un test que falla no rompe `./gradlew test` ni `:modulo:test`. Hay una carpeta `build/test-results/test/binary`, pero ningún archivo XML.

**Causa:** las convenciones del plugin no llaman a `useJUnitPlatform()` y ponen `failOnNoDiscoveredTests` en `false`, así que Gradle no encuentra tests de JUnit 5 y no protesta. Pitest sí ejecuta los tests, así que con `--mutation=true` un test que falla detiene la compilación más tarde, en `:pitest`, con `tests did not pass without mutation`. Con `--mutation=false` los tests nunca se ejecutan.

**Corrección en proyectos imperativos,** en el bloque `subprojects` existente del `build.gradle` de la raíz:

```groovy
subprojects {
    tasks.withType(Test).configureEach {
        useJUnitPlatform()
    }
    // ... contenido existente
}
```

**Corrección en proyectos reactivos.** Con JUnit Platform activo, el listener de BlockHound rompe la JVM de los tests (`BlockHoundTestExecutionListener could not be instantiated`, `The instrumentation have failed`). Ocurrió con el proyecto en Java 17, 21 y 25, y con Gradle ejecutándose en 21 y 25. No se identificó la causa raíz, así que exclúyelo también:

```groovy
subprojects {
    tasks.withType(Test).configureEach {
        useJUnitPlatform()
    }
    configurations.matching { it.name.startsWith('test') }.configureEach {
        exclude group: 'io.projectreactor.tools', module: 'blockhound-junit-platform'
    }
    // ... contenido existente
}
```

Avisa al usuario de la exclusión: sin ella los tests no se ejecutan, pero con ella nada detecta llamadas bloqueantes dentro de flujos reactivos durante los tests.

**Comprobación:** `./gradlew test --rerun-tasks`, y busca `build/test-results/test/*.xml` con más de cero tests. Añade `-x pitest` para omitir la mutación solo si Pitest está declarado: con `--mutation=false` esa tarea no existe y Gradle se detiene con `Task 'pitest' not found`.

## 2. Plantillas con el paquete del plugin fijo

Parte del código generado usa `co.com.bancolombia` en lugar de tu paquete, así que falla con cualquier otro:

| Módulo | Síntoma | Corrección |
| ------ | ------- | ---------- |
| `restmvc` | `package co.com.bancolombia.api.config does not exist` en `TestConfig.java` | Cambia el import a `<paquete>.api.config` |
| `asynceventhandler` | `package co.com.bancolombia.events.handlers does not exist` en `HandlerRegistryConfigurationTest.java` | Cambia los imports a `<paquete>.events.handlers` |
| `mcp` | `cannot find symbol: McpSecurityConfig` en los tests de `app-service` | Ver abajo |

**`mcp`** escribe `McpSecurityConfig` y su test en `applications/app-service/src/{main,test}/java/co/com/bancolombia/config/`, incluso con `--enable-security=false`. Mueve ambos a `<paquete>/config/`, actualiza sus líneas `package` y borra las carpetas `co/` vacías. Moverlos también importa en ejecución: `MainApplication` solo escanea tu paquete base, así que en la ubicación original la configuración de seguridad no se cargaría. Con `--enable-security=false`, borra los dos archivos en su lugar y comprueba que el módulo compila.

**Después de generar cualquier módulo,** busca `co.com.bancolombia` en él. Los imports de librerías de esa empresa (`co.com.bancolombia.secretsmanager`, `co.com.bancolombia.commons.jms`, Bin Stash) son correctos. Una referencia a un paquete de tu propio proyecto es este problema.

## 3. El adaptador `jpa` generado no arranca hasta fijar sus tipos

**Síntoma:** la aplicación no arranca, con `Not a managed type: class java.lang.Object`.

**Causa:** `JPARepository` y `JPARepositoryAdapter` usan `Object` como marcador (`/* change for adapter model */`).

**Corrección:** crea la clase `@Entity` en el adaptador y reemplaza los marcadores por los tipos de la entidad y del dominio. Revisa otros adaptadores por si tienen el mismo comentario. Revisa también `application.yaml`: el adaptador añade un datasource H2 de ejemplo, que hay que reemplazar por la base de datos real.

## 4. `jpa` con `--lombok=false` no compila

**Síntoma:** `cannot find symbol: method builder()` en `DBSecret`, en `jpa/config/`.

**Corrección:** usa `--lombok=true`, o escribe a mano el builder que falta. Otros adaptadores pueden tener el mismo problema: compila justo después de generarlos cuando Lombok está desactivado.

## 5. Los tests generados del entry point se rompen al implementar el flujo

**Síntoma:** `RouterRestTest` y `ConfigTest` fallan después de inyectar un caso de uso en `Handler` (no existe ese bean) o de quitar las rutas de ejemplo (404).

**Corrección:** añade el caso de uso a esos tests con `@MockitoBean` y apúntalos a las rutas reales, o reemplázalos por tests del flujo real. No borres `ConfigTest` sin conservar una comprobación equivalente de las cabeceras de seguridad.

```java
@MockitoBean
private CreateOrderUseCase createOrderUseCase;
```

## 6. `secretskafkastrimzi` no funciona

**Síntomas:** `--secret-name` detiene la tarea con `Cannot invoke ... ModuleBuilder.addParam ... because "this.builder" is null`. Sin esa opción genera un módulo llamado `secrets`, y la compilación falla con `Could not find software.amazon.awssdk:sts:.`, una dependencia sin versión.

**Qué hacer:** avisa al usuario antes de usarlo. Añadir el BOM del SDK de AWS al módulo debería aportar la versión, pero esta corrección no se probó.

## 7. `ca` sobrescribe `gradle.properties`

**Síntoma:** un `analytics=false` escrito antes de `ca` se pierde, y `ca` envía igualmente su evento de analítica.

**Corrección:** no hay ajuste para el primer evento. Ejecuta `./gradlew analytics --enabled false` justo después de `ca`, antes de cualquier tarea que envíe nombres de negocio.

## Diferencias con la documentación oficial

| La documentación dice | Lo que ocurre en realidad |
| --------------------- | ------------------------- |
| Versión de ejemplo del plugin `5.0.2` | Desactualizada. Lee la última de los metadatos del Plugin Portal |
| `arch.unit.ski=true` | La propiedad es `arch.unit.skip` |
| Dos reglas numeradas 2.7, una sobre campos | La regla de campos es la 2.6 |
| Las reglas de ArchUnit se "imponen" | Solo la 2.5 hace fallar. Las demás solo escriben avisos en `build/issues.json` |
| `gpt` genera en `./performance-test/` | Genera en `deployment/performance-test/` |
| `gpl` genera en `./deployment/` | El pipeline de GitHub va en `.github/workflows/` |
| Las tablas listan `restmvc`, `jpa` y `grpc` sin tipo de proyecto | No se rechazan en proyectos reactivos, pero ahí no corresponden |
| `secretskafkastrimzi` acepta `--secret-name` | La opción hace fallar la tarea |

## Qué se verificó y qué no

- **De la generación a una petición real:** reactivo con `ca`, `gm`, `guc`, adaptador `generic` y `webflux`. Imperativo con `--lombok=false` y `restmvc` con Jetty y Swagger.
- **Versiones de Java:** los tests del proyecto reactivo se ejecutaron en 17, 21 y 25. El proyecto imperativo y la matriz de módulos de abajo, solo en 21.
- **Generados, compilados y con sus tests generados en verde, con un paquete propio, en Java 21:**
  - Adaptadores reactivos: `mongodb`, `redis`, `sqs`, `restconsumer`, `dynamodb`, `s3`, `kms`, `secrets`, `mq`, `asynceventbus`, `rsocket`, `binstash`, `cognitotokenprovider`, `r2dbc`.
  - Entry points reactivos: `webflux`, `kafka`, `sqs`, `mq`, `graphql`, `rsocket`, `kafkastrimzi`, `agent`, y `asynceventhandler` y `mcp` después de las correcciones de arriba.
  - Adaptadores imperativos: `mongodb`, `redis`, `sqs`, `restconsumer`, `dynamodb`, `s3`, `kms`, `secrets`, `mq`, `jpa`.
  - Entry points imperativos: `sqs`, `mq`, `graphql`, `grpc`, y `restmvc` después de la corrección de arriba.
- **ArchUnit:** la regla 2.5 hace fallar el test y la 2.6 solo escribe en `build/issues.json`, ambas vistas en ejecución. Las demás se leyeron del código generado.
- **Solo generados:** `gpl --type=github`, `gat`, `gpt --type=jmeter`.
- **Sin probar:** conexiones a infraestructura real (bases de datos, brokers, AWS), opciones no predeterminadas de la mayoría de los módulos y otros sistemas operativos. Pasar aquí significa que el código compila y sus tests generados pasan, no que el módulo funcione contra el servicio real. Los adaptadores imperativos `mongodb`, `redis`, `sqs`, `dynamodb`, `s3`, `kms`, `secrets` y `mq` no generan tests propios, así que para ellos solo significa que compilan.

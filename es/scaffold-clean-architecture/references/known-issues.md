# Problemas conocidos

Problemas encontrados al ejecutar la versión 5.1.0 del plugin con Gradle 9.8.2 y Java 21. Son hechos de esa versión: en una más nueva, comprueba si cada uno sigue ocurriendo antes de aplicar su corrección.

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

**Corrección en proyectos reactivos.** Con JUnit Platform activo, el listener de BlockHound puede romper la JVM de los tests (`BlockHoundTestExecutionListener could not be instantiated`, `The instrumentation have failed`, visto en módulos con Spring, en Java 21). Si ocurre, exclúyelo también:

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

Avisa al usuario de la exclusión: sin ella los tests no corren en ese entorno, pero con ella nada detecta llamadas bloqueantes dentro de flujos reactivos durante los tests.

**Comprobación:** `./gradlew test --rerun-tasks -x pitest`, y busca `build/test-results/test/*.xml` con más de cero tests.

## 2. `restmvc`: los tests no compilan con un paquete propio

**Síntoma:** `package co.com.bancolombia.api.config does not exist` en `api-rest/src/test/java/.../TestConfig.java`.

**Causa:** la plantilla tiene fijo el paquete del propio plugin en ese import.

**Corrección:** cambia el import a `<paquete>.api.config`.

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

## 6. `ca` sobrescribe `gradle.properties`

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

## Qué se verificó y qué no

- **Ejecutado desde la generación hasta una petición real, reactivo:** `ca`, `gm`, `guc`, adaptador `generic`, `webflux`, tests, compilación, `bootRun`.
- **Ejecutado, imperativo, con `--lombok=false`:** `ca`, `restmvc` con Jetty y Swagger, tests, compilación, `bootRun`.
- **Generado y compilado:** `r2dbc`, `restconsumer`, `webflux --from-swagger`, `gh`.
- **Solo generado:** `jpa`, `gpl --type=github`, `gat`, `gpt --type=jmeter`.
- **Leído del código generado, no ejecutado:** que la regla 2.5 haga fallar el test.
- **Sin probar:** los demás adaptadores y entry points, conexiones reales a bases de datos y Java 17 o 25. Sus opciones vienen de la documentación y del código fuente. Compila justo después de generarlos.

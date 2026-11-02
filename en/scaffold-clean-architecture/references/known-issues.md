# Known issues

Problems found by running plugin version 5.1.0 with Gradle 9.8.2 and Java 21. They're facts about that version: on a newer one, check whether each still happens before applying its fix.

## 1. The `test` task runs no tests

**Symptom:** a failing test doesn't break `./gradlew test` or `:module:test`. There's a `build/test-results/test/binary` folder, but no XML files.

**Cause:** the plugin's conventions don't call `useJUnitPlatform()` and set `failOnNoDiscoveredTests` to `false`, so Gradle finds no JUnit 5 tests and doesn't complain. Pitest does run the tests, so with `--mutation=true` a failing test stops the build later, at `:pitest`, with `tests did not pass without mutation`. With `--mutation=false` the tests never run.

**Fix in imperative projects,** in the existing `subprojects` block of the root `build.gradle`:

```groovy
subprojects {
    tasks.withType(Test).configureEach {
        useJUnitPlatform()
    }
    // ... existing content
}
```

**Fix in reactive projects.** With JUnit Platform active, the BlockHound listener can break the test JVM (`BlockHoundTestExecutionListener could not be instantiated`, `The instrumentation have failed`, seen in modules with Spring, on Java 21). If that happens, also exclude it:

```groovy
subprojects {
    tasks.withType(Test).configureEach {
        useJUnitPlatform()
    }
    configurations.matching { it.name.startsWith('test') }.configureEach {
        exclude group: 'io.projectreactor.tools', module: 'blockhound-junit-platform'
    }
    // ... existing content
}
```

Tell the user about the exclusion: without it the tests don't run on that setup, but with it nothing detects blocking calls inside reactive flows during tests.

**Check:** `./gradlew test --rerun-tasks -x pitest`, and look for `build/test-results/test/*.xml` with tests above zero.

## 2. `restmvc`: tests don't compile with a custom package

**Symptom:** `package co.com.bancolombia.api.config does not exist` in `api-rest/src/test/java/.../TestConfig.java`.

**Cause:** the template has the plugin's own package hardcoded in that import.

**Fix:** change the import to `<package>.api.config`.

## 3. Generated `jpa` adapter doesn't start until its types are set

**Symptom:** the app fails to start with `Not a managed type: class java.lang.Object`.

**Cause:** `JPARepository` and `JPARepositoryAdapter` use `Object` as a placeholder (`/* change for adapter model */`).

**Fix:** create the `@Entity` class in the adapter, and replace the placeholders with the entity and domain types. Review other adapters for the same comment. Also review `application.yaml`: the adapter adds an H2 datasource as an example, and H2 must be replaced with the real database.

## 4. `jpa` with `--lombok=false` doesn't compile

**Symptom:** `cannot find symbol: method builder()` on `DBSecret`, in `jpa/config/`.

**Fix:** use `--lombok=true`, or write the missing builder by hand. Other adapters may have the same problem: compile right after generating them when Lombok is off.

## 5. Generated entry point tests break when you implement the flow

**Symptom:** `RouterRestTest` and `ConfigTest` fail after injecting a use case into `Handler` (no such bean), or after removing the sample routes (404).

**Fix:** add the use case to those tests with `@MockitoBean` and point them to the real routes, or replace them with tests of the real flow. Don't delete `ConfigTest` without keeping an equivalent check of the security headers.

```java
@MockitoBean
private CreateOrderUseCase createOrderUseCase;
```

## 6. `ca` overwrites `gradle.properties`

**Symptom:** `analytics=false` written before `ca` is lost, and `ca` sends its analytics event anyway.

**Fix:** there's no setting for the first event. Run `./gradlew analytics --enabled false` right after `ca`, before any task that sends business names.

## Differences from the official documentation

| The documentation says | What actually happens |
| ---------------------- | ---------------------- |
| Example plugin version `5.0.2` | Outdated. Read the latest from the Plugin Portal metadata |
| `arch.unit.ski=true` | The property is `arch.unit.skip` |
| Two rules numbered 2.7, one about fields | The field rule is 2.6 |
| ArchUnit rules are "enforced" | Only rule 2.5 fails. The others only write warnings to `build/issues.json` |
| `gpt` generates in `./performance-test/` | It generates in `deployment/performance-test/` |
| `gpl` generates in `./deployment/` | GitHub's pipeline goes in `.github/workflows/` |
| The tables list `restmvc`, `jpa` and `grpc` with no project type | They aren't rejected in reactive projects, but they don't belong there |

## What was verified, and what wasn't

- **Run from generation to a real request, reactive:** `ca`, `gm`, `guc`, `generic` adapter, `webflux`, tests, build, `bootRun`.
- **Run, imperative, with `--lombok=false`:** `ca`, `restmvc` with Jetty and Swagger, tests, build, `bootRun`.
- **Generated and compiled:** `r2dbc`, `restconsumer`, `webflux --from-swagger`, `gh`.
- **Generated only:** `jpa`, `gpl --type=github`, `gat`, `gpt --type=jmeter`.
- **Read from the generated code, not run:** that rule 2.5 fails the test.
- **Not tried:** the other adapters and entry points, real database connections, and Java 17 or 25. Their options come from the documentation and source code. Compile right after generating them.

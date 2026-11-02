# Known issues

Problems found by running plugin version 5.1.0 with Gradle 9.8.2 on macOS. They're facts about that version: on a newer one, check whether each still happens before applying its fix.

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

**Fix in reactive projects.** With JUnit Platform active, the BlockHound listener breaks the test JVM (`BlockHoundTestExecutionListener could not be instantiated`, `The instrumentation have failed`). This happened with the project on Java 17, 21 and 25, and with Gradle running on 21 and 25. The root cause wasn't identified, so also exclude it:

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

Tell the user about the exclusion: without it the tests don't run, but with it nothing detects blocking calls inside reactive flows during tests.

**Check:** `./gradlew test --rerun-tasks`, and look for `build/test-results/test/*.xml` with tests above zero. Add `-x pitest` to skip mutation only if Pitest is declared: with `--mutation=false` that task doesn't exist and Gradle stops with `Task 'pitest' not found`.

## 2. Templates with the plugin's package hardcoded

Some generated code uses `co.com.bancolombia` instead of your package, so it fails with any other one:

| Module | Symptom | Fix |
| ------ | ------- | --- |
| `restmvc` | `package co.com.bancolombia.api.config does not exist` in `TestConfig.java` | Change the import to `<package>.api.config` |
| `asynceventhandler` | `package co.com.bancolombia.events.handlers does not exist` in `HandlerRegistryConfigurationTest.java` | Change the imports to `<package>.events.handlers` |
| `mcp` | `cannot find symbol: McpSecurityConfig` in `app-service` tests | See below |

**`mcp`** writes `McpSecurityConfig` and its test in `applications/app-service/src/{main,test}/java/co/com/bancolombia/config/`, even with `--enable-security=false`. Move both to `<package>/config/`, update their `package` lines, and delete the empty `co/` folders. The move also matters at runtime: `MainApplication` only scans your base package, so in the original location the security configuration wouldn't be loaded. With `--enable-security=false`, delete both files instead, and check that the module compiles.

**After generating any module,** search it for `co.com.bancolombia`. Imports of that company's libraries (`co.com.bancolombia.secretsmanager`, `co.com.bancolombia.commons.jms`, Bin Stash) are correct. A reference to a package of your own project is this problem.

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

## 6. `secretskafkastrimzi` is broken

**Symptoms:** `--secret-name` stops the task with `Cannot invoke ... ModuleBuilder.addParam ... because "this.builder" is null`. Without that option it generates a module called `secrets`, and the build fails with `Could not find software.amazon.awssdk:sts:.`, a dependency with no version.

**What to do:** tell the user before using it. Adding the AWS SDK BOM to the module should supply the version, but this fix wasn't tried.

## 7. `ca` overwrites `gradle.properties`

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
| `secretskafkastrimzi` accepts `--secret-name` | The option makes the task fail |

## What was verified, and what wasn't

- **From generation to a real request:** reactive with `ca`, `gm`, `guc`, `generic` adapter and `webflux`. Imperative with `--lombok=false` and `restmvc` with Jetty and Swagger.
- **Java versions:** the reactive project's tests ran on 17, 21 and 25. The imperative project and the module matrix below ran on 21 only.
- **Generated, compiled and generated tests passing, with a custom package, on Java 21:**
  - Reactive adapters: `mongodb`, `redis`, `sqs`, `restconsumer`, `dynamodb`, `s3`, `kms`, `secrets`, `mq`, `asynceventbus`, `rsocket`, `binstash`, `cognitotokenprovider`, `r2dbc`.
  - Reactive entry points: `webflux`, `kafka`, `sqs`, `mq`, `graphql`, `rsocket`, `kafkastrimzi`, `agent`, and `asynceventhandler` and `mcp` after the fixes above.
  - Imperative adapters: `mongodb`, `redis`, `sqs`, `restconsumer`, `dynamodb`, `s3`, `kms`, `secrets`, `mq`, `jpa`.
  - Imperative entry points: `sqs`, `mq`, `graphql`, `grpc`, and `restmvc` after the fix above.
- **ArchUnit:** rule 2.5 fails the test and rule 2.6 only writes to `build/issues.json`, both seen running. The other rules were read from the generated code.
- **Generated only:** `gpl --type=github`, `gat`, `gpt --type=jmeter`.
- **Not tried:** connections to real infrastructure (databases, brokers, AWS), non-default options of most modules, and other operating systems. Passing here means the code compiles and its generated tests pass, not that the module works against the real service. Imperative `mongodb`, `redis`, `sqs`, `dynamodb`, `s3`, `kms`, `secrets` and `mq` adapters generate no tests of their own, so for them it only means they compile.

---
name: scaffold-clean-architecture
description: Creates new Java applications with Clean Architecture using the Bancolombia Gradle plugin scaffold-clean-architecture (co.com.bancolombia.cleanArchitecture), and adds models, use cases, driven adapters, entry points, helpers, pipelines and tests to projects generated with it. It checks Java and Gradle, asks for the project's decisions, runs the plugin's tasks, applies fixes for known problems in the generated project, implements the business flow respecting the dependency rule, and verifies the result with validateStructure, the build, the tests and a real start of the application. Use it when the user asks to create a Java microservice or application with Clean Architecture or with the Bancolombia scaffold, or to add a module, adapter or entry point to a project that uses this plugin. Not for migrating Scaffold 4 projects or for applying Clean Architecture to projects not generated with the plugin.
compatibility: Requires Java 17 or later, Gradle 9.2.1 or later and network access to the Gradle Plugin Portal and Maven Central. Written and tested against plugin version 5.1.0.
---

# scaffold-clean-architecture

Creates and grows Java applications with the [scaffold-clean-architecture](https://github.com/bancolombia/scaffold-clean-architecture) Gradle plugin. The plugin generates a multi-module Spring Boot project in which each layer is a Gradle module and the dependency rule is checked on every build.

The result of a run is a project that compiles, whose tests really run, and that starts. Generating files isn't enough: several generated projects don't compile or don't run their tests until the fixes in `references/known-issues.md` are applied.

## Principles

- **Use the plugin, don't imitate it.** Create modules with its tasks instead of writing their structure by hand. Write by hand only the business code that goes inside them.
- **Regenerating overwrites.** `gm`, `guc`, `gda` and `gep` silently overwrite the files of a module or class that already exists, including your edits, and they don't check git. `ca` replaces the root files. Never run a generator on something that already exists without the user's explicit confirmation.
- **Don't trust the task's silence.** Some tasks succeed when they did nothing useful: `gep --type=restmvc` and `gda --type=jpa` generate without complaint in a reactive project, `u` with pending changes does nothing and still ends in `BUILD SUCCESSFUL`, and `test` passes without running tests. Check the result, not only the exit code.
- **Report what was verified.** Say which checks ran and which couldn't run (for example, a start that needs a database). Never present a build as proof that the tests passed until you've seen them run.
- **Never secrets.** Don't write credentials into `application.yaml` or any other file. Use environment variables or the plugin's secrets options.

## Decide what to do

Look at the working folder:

| What's there | What to do |
| ------------ | ---------- |
| Empty folder, or the user asks for a new project | **Create** a project (steps 1 to 6) |
| `gradle.properties` with `package=` and `reactive=`, and the plugin in `settings.gradle` | **Grow** the project (steps 4 to 6) |
| A `main.gradle` file in the root | It's a Scaffold 4 project. Stop: the plugin refuses to run there. Point the user to the [migration guide](https://bancolombia.github.io/scaffold-clean-architecture/docs/migrations/v4-v5). This skill doesn't migrate |
| Any other project with code | Stop. `ca` would replace its root files. Create the new project in another folder |

## 1. Check the environment

1. **Java:** run `java -version` and list the installed JDKs (on macOS, `/usr/libexec/java_home -V`). The project's Java version must be installed: the generated project uses a Gradle toolchain with no auto-provisioning, so compiling for a version that isn't installed fails with `Cannot find a Java installation`. The plugin's default is 25.
2. **Gradle:** run `gradle --version`. It needs 9.2.1 or later. If it's missing, ask the user to install it. The generated project then uses its own wrapper.
3. **Plugin version:** read the latest one from `https://plugins.gradle.org/m2/co/com/bancolombia/cleanArchitecture/co.com.bancolombia.cleanArchitecture.gradle.plugin/maven-metadata.xml`. Don't take it from the official guide, whose examples can lag behind. If the latest is newer than 5.1.0, use it and tell the user that this skill was tested on 5.1.0, so its known issues need checking again. If the same major version isn't available, use 5.1.0.

## 2. Ask for the decisions

Ask everything in a single message, with a recommendation for each. Don't ask what the user already said.

| Decision | Option | Recommendation |
| -------- | ------ | -------------- |
| Project name | `--name` | Required, no default worth keeping |
| Base package | `--package` | Required. Never leave the default: `co.com.bancolombia` belongs to that company |
| Type | `--type=reactive` or `imperative` | `reactive` if the service is I/O-heavy and the team knows Reactor; `imperative` for a simpler stack or for JPA. Explain the difference if the user doesn't state a preference: it conditions which modules are available |
| Java | `--java-version=17`, `21` or `25` | The highest of these that's installed |
| Lombok | `--lombok` | `true`. With `false`, some adapters don't compile (see known issues) |
| Metrics | `--metrics` | `true` |
| Mutation tests | `--mutation` | `true`. They slow down the build; `false` removes Pitest, and then `-x pitest` fails because the task doesn't exist |
| OpenTelemetry | `--otel` | `false`, unless there's a collector. With `true`, the agent keeps logging export errors if nothing listens on `localhost:4318` |
| Entry points and adapters | See `references/tasks.md` | What the service needs: how it receives requests and which systems it talks to |
| First model and use case | Business names | Optional, they can be added later |

**Analytics must be part of this message.** The plugin sends usage data to an external server by default: operating system user name, country, Java and plugin versions, task and type, and the names given to models, use cases, helpers and deleted modules. Tell the user two things:

- `ca` always sends one event, even with `analytics=false` already in the file, because it rewrites `gradle.properties`. If this isn't acceptable (for example, for an internal project with a confidential name), let the user decide before running it.
- This skill turns analytics off right after `ca`, before any name is sent, unless the user prefers to keep it on.

## 3. Generate the project

1. Create the folder and `git init`, if it isn't a repository yet.
2. Write the minimal `build.gradle`, with the version from step 1:

   ```groovy
   plugins {
       id 'co.com.bancolombia.cleanArchitecture' version '<version>'
   }
   ```

3. Run the generator. It also creates the Gradle wrapper:

   ```shell
   gradle ca --name=<Name> --package=<package> --type=<type> --java-version=<version>
   ```

4. Turn off analytics, as the first thing after `ca`:

   ```shell
   ./gradlew analytics --enabled false
   ```

5. **Make the tests run.** Check `references/known-issues.md`, issue 1. In version 5.1.0 the `test` task runs no tests, so a failing test doesn't break the build. Apply the fix to the root `build.gradle`, tell the user, and confirm that `build/test-results/test/*.xml` files appear.
6. Propose a first commit and wait for the answer. From here on, a clean repository is the only protection against a generator overwriting something.

## 4. Add modules

Read `references/tasks.md` for the tasks and their options. Before each generator:

1. **Check it fits the project's type,** using the compatibility table: read `reactive=` in `gradle.properties`. Don't rely on the plugin to reject it, since it doesn't always do so.
2. **Check it doesn't exist yet,** looking in `domain/` and `infrastructure/`. If it exists, ask before overwriting and suggest committing first.
3. **Use business names** for models and use cases, without technology words. The plugin rejects names ending in `dto`, `request` or `response` and names containing `kafka`, `redis`, `s3`, `http` and others.

Usual order: `gm`, `guc`, `gda`, `gep`. After the generators:

1. Search the new modules for `co.com.bancolombia` and apply the fixes in `references/known-issues.md`, issue 2. The plugin hardcodes its own package in some templates.
2. Apply the other fixes in that file that match the modules you generated.
3. Run `./gradlew validateStructure compileJava compileTestJava`, so a problem shows up now and not after you've built on top of it.

## 5. Implement the flow

Read `references/architecture.md`. The essentials:

- **The flow goes** entry point → use case → gateway (an interface in `model`) ← driven adapter.
- **Don't wire modules by hand.** New modules are discovered from their `build.gradle`, and `app-service` receives them automatically. Use case classes become beans if they end in `UseCase` and live under `<package>.usecase`.
- **Replace the generator's placeholders:** `Object` types in adapters (`/* change for domain model */`), the example `My*` classes and the sample routes in `Handler` and `RouterRest`.
- **Update the generated tests** when you change the code they cover. Injecting a use case into `Handler` or removing a sample route breaks `RouterRestTest` and `ConfigTest`.
- **Write tests for the business code,** especially for use cases, mocking the gateways.

## 6. Verify

Run these in order and report each result:

1. `./gradlew validateStructure`: the dependency rule.
2. `./gradlew build jacocoMergedReport`: compilation, tests, Pitest if enabled, and merged coverage in `build/reports/jacocoMergedReport/`.
3. **Check that the tests ran:** there must be `build/test-results/test/*.xml` files with a test count above zero in the modules that have tests.
4. `./gradlew bootRun` and a request to a real endpoint and to `/actuator/health`, then stop the process. If it needs a database or a broker that isn't available, say so and say what's left unverified, instead of skipping it silently.
5. Read `build/issues.json`, if it exists: most ArchUnit rules only report there, without failing the build.

Close with a summary: what was generated, the fixes applied, what was verified, what's left to the user (environment values, credentials, real business rules) and the commands to run the project. Ask before committing.

## Reference files

- `references/tasks.md`: every task, its options, and what's available for each project type.
- `references/architecture.md`: layers, dependency rules, automatic wiring, ArchUnit rules, and configuration of the generated project.
- `references/known-issues.md`: verified problems in the plugin and generated code, with their fixes, and differences from the official documentation.

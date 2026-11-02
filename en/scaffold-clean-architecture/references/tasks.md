# Plugin tasks

Reference for version 5.1.0. To check an option in another version, run `./gradlew help --task <task>`. Options accept both `--type=webflux` and `--type webflux`.

## Summary

| Task | Short | Required | What it does |
| ---- | ----- | -------- | ------------ |
| `cleanArchitecture` | `ca` | - | Generates the project. Replaces the root files if they exist |
| `generateModel` | `gm` | `--name` | Model and gateway in `domain/model` |
| `generateUseCase` | `guc` | `--name` | Use case in `domain/usecase`. Adds the `UseCase` suffix if missing |
| `generateDrivenAdapter` | `gda` | `--type` | Module in `infrastructure/driven-adapters` |
| `generateEntryPoint` | `gep` | `--type` | Module in `infrastructure/entry-points` |
| `generateHelper` | `gh` | `--name` | Module in `infrastructure/helpers` |
| `generatePipeline` | `gpl` | `--type` | `azure`, `circleci`, `github` or `jenkins`. Option `--mono-repo`. GitHub's goes in `.github/workflows/` |
| `generateAcceptanceTest` | `gat` | - | Karate project in `deployment/acceptanceTest`, or another folder with `--name` |
| `generatePerformanceTest` | `gpt` | `--type` | `jmeter`, in `deployment/performance-test` |
| `validateStructure` | `vs` | - | Checks dependencies between layers. Also runs on every compilation |
| `deleteModule` | `dm` | `--module` | Deletes the module folder. Confirm first, and commit before |
| `updateCleanArchitecture` | `u` | - | Updates plugin and dependencies. Options `--dependencies` and `--git`. With pending changes it does nothing and ends successfully; commit first |
| `analytics` | `a` | `--enabled` | Turns usage analytics on or off |
| `jacocoMergedReport` | - | - | Merged coverage in `build/reports/jacocoMergedReport/` |

## `ca` options

| Option | Values | Default |
| ------ | ------ | ------- |
| `--name` | Text | `cleanArchitecture` |
| `--package` | Java package | `co.com.bancolombia` |
| `--type` | `reactive`, `imperative` | `reactive` |
| `--java-version` | `17`, `21`, `25` | `25` |
| `--lombok` | `true`, `false` | `true` |
| `--metrics` | `true`, `false` | `true` |
| `--mutation` | `true`, `false` | `true` |
| `--otel` | `true`, `false` | `false` |

## Driven adapters (`gda --type=...`)

| Type | What it is | Project | Options |
| ---- | ---------- | ------- | ------- |
| `generic` | Empty module | Both | `--name` (required) |
| `dynamodb` | DynamoDB | Both | - |
| `kms` | AWS KMS | Both | - |
| `mongodb` | MongoDB | Both | `--secret` |
| `mq` | JMS message sender | Both | - |
| `redis` | Redis | Both | `--mode=template\|repository`, `--secret`. `repository` is imperative only |
| `restconsumer` | REST client | Both | `--url`, `--from-swagger=<file>` |
| `s3` | AWS S3 | Both | - |
| `secrets` | Secrets manager | Both | `--secrets-backend=aws_secrets_manager\|vault` |
| `sqs` | SQS sender | Both | - |
| `jpa` | JPA repository | Imperative\* | `--secret` |
| `asynceventbus` | Async event bus | Reactive | `--eda`, `--tech=rabbitmq\|kafka\|rabbitmq,kafka` |
| `binstash` | Bin Stash cache | Reactive | `--cache-mode=LOCAL\|CENTRALIZED\|HYBRID` |
| `cognitotokenprovider` | Cognito tokens | Reactive | - |
| `r2dbc` | R2DBC PostgreSQL | Reactive | - |
| `rsocket` | RSocket requester | Reactive | - |
| `secretskafkastrimzi` | Secrets for Kafka Strimzi | Reactive\* | `--secret-name` |

## Entry points (`gep --type=...`)

| Type | What it is | Project | Options |
| ---- | ---------- | ------- | ------- |
| `generic` | Empty module | Both | `--name` (required) |
| `graphql` | GraphQL API | Both | `--pathgql` |
| `mq` | JMS listener | Both | - |
| `sqs` | SQS listener | Both | - |
| `restmvc` | REST with Spring MVC | Imperative\* | `--server=tomcat\|jetty`, `--authorization`, `--versioning=HEADER\|PATH\|NONE`, `--from-swagger=<file>`, `--swagger` |
| `grpc` | gRPC server | Imperative\* | - |
| `webflux` | REST with WebFlux | Reactive | `--router`, `--authorization`, `--versioning`, `--from-swagger=<file>`, `--swagger` |
| `asynceventhandler` | Async event handler | Reactive | `--eda`, `--tech` |
| `kafka` | Kafka consumer | Reactive | - |
| `kafkastrimzi` | Kafka Strimzi consumer | Reactive | `--name`, `--topic-consumer` |
| `rsocket` | RSocket controller | Reactive | - |
| `mcp` | MCP server | Reactive | `--name`, `--enable-tools`, `--enable-resources`, `--enable-prompts`, `--enable-security`, `--enable-audit` |
| `agent` | Spring AI A2A agent | Reactive | `--name`, `--agent-role=collaborative\|supervisor\|hybrid`, `--agent-enable-kafka`, `--agent-enable-mcp-client` |

**Reactive** means that the plugin rejects it in an imperative project, with `This module is only available for reactive projects`.

**\*** means that the plugin doesn't enforce it: the module gets generated in the other project type without any error, even though it doesn't belong there. The plugin's own generation script only uses these types with the project type shown. Check this yourself before running the task.

`RESTMVCSERVER` appears in the plugin's list of types, but it's an internal part of `restmvc`. Don't use it directly.

## Generating from OpenAPI

With `--from-swagger=<file>`, the file must already exist. `gep --type=webflux --from-swagger=swagger.yaml --router=false` generates a controller and models for each API tag, in addition to the sample `ApiRest`, and compiles without changes.

## Project properties (`gradle.properties`)

| Property | What it's for |
| -------- | ------------- |
| `package`, `reactive`, `lombok`, `metrics`, `javaVersion` | Set by `ca`, and read by later tasks |
| `analytics` | `false` turns analytics off |
| `excludeModule` | Modules excluded from the Gradle build, comma separated |
| `excludeModuleFromApp` | Modules not injected into `app-service`, comma separated |
| `arch.unit.skip` | `true` skips the ArchUnit test. Not recommended |
| `arch.unit.forbiddenDomainSuffixes` | Replaces the forbidden suffixes (default `dto,request,response`) |
| `arch.unit.forbiddenDomainClassNames` | Replaces the forbidden technology words |

## Blocks in the root `build.gradle`

```groovy
// Allows domain libraries that validateStructure would reject. Platforms (BOMs) are already allowed
cleanPlugin {
    modelProps {
        whitelistedDependencies = "allowed-library, another-library"
    }
}

// Forces versions to address vulnerabilities. Two-part coordinates apply to a whole group
dependenciesOverride {
    ensure 'com.fasterxml.jackson.core:jackson-core:2.22.4'
    ensure 'tools.jackson.core:3.2.4'
}
```

Plugin versions for Spring Boot, Sonar and Pitest can be set in the root `plugins {}` block. Keep `apply false` on Spring Boot.

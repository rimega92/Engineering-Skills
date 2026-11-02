# Tareas del plugin

Referencia para la versión 5.1.0. Para comprobar una opción en otra versión, ejecuta `./gradlew help --task <tarea>`. Las opciones aceptan tanto `--type=webflux` como `--type webflux`.

## Resumen

| Tarea | Corta | Obligatorio | Qué hace |
| ----- | ----- | ----------- | -------- |
| `cleanArchitecture` | `ca` | - | Genera el proyecto. Reemplaza los archivos de la raíz si existen |
| `generateModel` | `gm` | `--name` | Modelo y gateway en `domain/model` |
| `generateUseCase` | `guc` | `--name` | Caso de uso en `domain/usecase`. Añade el sufijo `UseCase` si falta |
| `generateDrivenAdapter` | `gda` | `--type` | Módulo en `infrastructure/driven-adapters` |
| `generateEntryPoint` | `gep` | `--type` | Módulo en `infrastructure/entry-points` |
| `generateHelper` | `gh` | `--name` | Módulo en `infrastructure/helpers` |
| `generatePipeline` | `gpl` | `--type` | `azure`, `circleci`, `github` o `jenkins`. Opción `--mono-repo`. El de GitHub va en `.github/workflows/` |
| `generateAcceptanceTest` | `gat` | - | Proyecto Karate en `deployment/acceptanceTest`, o en otra carpeta con `--name` |
| `generatePerformanceTest` | `gpt` | `--type` | `jmeter`, en `deployment/performance-test` |
| `validateStructure` | `vs` | - | Comprueba las dependencias entre capas. También corre en cada compilación |
| `deleteModule` | `dm` | `--module` | Borra la carpeta del módulo. Confirma antes y haz commit primero |
| `updateCleanArchitecture` | `u` | - | Actualiza el plugin y las dependencias. Opciones `--dependencies` y `--git`. Con cambios pendientes no hace nada y termina bien; haz commit primero |
| `analytics` | `a` | `--enabled` | Activa o desactiva la analítica de uso |
| `jacocoMergedReport` | - | - | Cobertura unificada en `build/reports/jacocoMergedReport/` |

## Opciones de `ca`

| Opción | Valores | Por defecto |
| ------ | ------- | ----------- |
| `--name` | Texto | `cleanArchitecture` |
| `--package` | Paquete Java | `co.com.bancolombia` |
| `--type` | `reactive`, `imperative` | `reactive` |
| `--java-version` | `17`, `21`, `25` | `25` |
| `--lombok` | `true`, `false` | `true` |
| `--metrics` | `true`, `false` | `true` |
| `--mutation` | `true`, `false` | `true` |
| `--otel` | `true`, `false` | `false` |

## Driven adapters (`gda --type=...`)

| Tipo | Qué es | Proyecto | Opciones |
| ---- | ------ | -------- | -------- |
| `generic` | Módulo vacío | Ambos | `--name` (obligatorio) |
| `dynamodb` | DynamoDB | Ambos | - |
| `kms` | AWS KMS | Ambos | - |
| `mongodb` | MongoDB | Ambos | `--secret` |
| `mq` | Emisor de mensajes JMS | Ambos | - |
| `redis` | Redis | Ambos | `--mode=template\|repository`, `--secret`. `repository` solo en imperativo |
| `restconsumer` | Cliente REST | Ambos | `--url`, `--from-swagger=<archivo>` |
| `s3` | AWS S3 | Ambos | - |
| `secrets` | Gestor de secretos | Ambos | `--secrets-backend=aws_secrets_manager\|vault` |
| `sqs` | Emisor SQS | Ambos | - |
| `jpa` | Repositorio JPA | Imperativo\* | `--secret` |
| `asynceventbus` | Bus de eventos asíncrono | Reactivo | `--eda`, `--tech=rabbitmq\|kafka\|rabbitmq,kafka` |
| `binstash` | Caché Bin Stash | Reactivo | `--cache-mode=LOCAL\|CENTRALIZED\|HYBRID` |
| `cognitotokenprovider` | Tokens de Cognito | Reactivo | - |
| `r2dbc` | R2DBC PostgreSQL | Reactivo | - |
| `rsocket` | Requester RSocket | Reactivo | - |
| `secretskafkastrimzi` | Secretos para Kafka Strimzi | Reactivo\* | `--secret-name` |

## Entry points (`gep --type=...`)

| Tipo | Qué es | Proyecto | Opciones |
| ---- | ------ | -------- | -------- |
| `generic` | Módulo vacío | Ambos | `--name` (obligatorio) |
| `graphql` | API GraphQL | Ambos | `--pathgql` |
| `mq` | Listener JMS | Ambos | - |
| `sqs` | Listener SQS | Ambos | - |
| `restmvc` | REST con Spring MVC | Imperativo\* | `--server=tomcat\|jetty`, `--authorization`, `--versioning=HEADER\|PATH\|NONE`, `--from-swagger=<archivo>`, `--swagger` |
| `grpc` | Servidor gRPC | Imperativo\* | - |
| `webflux` | REST con WebFlux | Reactivo | `--router`, `--authorization`, `--versioning`, `--from-swagger=<archivo>`, `--swagger` |
| `asynceventhandler` | Manejador de eventos asíncrono | Reactivo | `--eda`, `--tech` |
| `kafka` | Consumidor Kafka | Reactivo | - |
| `kafkastrimzi` | Consumidor Kafka Strimzi | Reactivo | `--name`, `--topic-consumer` |
| `rsocket` | Controlador RSocket | Reactivo | - |
| `mcp` | Servidor MCP | Reactivo | `--name`, `--enable-tools`, `--enable-resources`, `--enable-prompts`, `--enable-security`, `--enable-audit` |
| `agent` | Agente A2A con Spring AI | Reactivo | `--name`, `--agent-role=collaborative\|supervisor\|hybrid`, `--agent-enable-kafka`, `--agent-enable-mcp-client` |

**Reactivo** significa que el plugin lo rechaza en un proyecto imperativo, con `This module is only available for reactive projects`.

**\*** significa que el plugin no lo impone: el módulo se genera en el otro tipo de proyecto sin ningún error, aunque ahí no corresponde. El script de generación del propio plugin solo usa estos tipos con el tipo de proyecto indicado. Compruébalo tú antes de ejecutar la tarea.

`RESTMVCSERVER` aparece en la lista de tipos del plugin, pero es una parte interna de `restmvc`. No lo uses directamente.

## Generar desde OpenAPI

Con `--from-swagger=<archivo>`, el archivo ya debe existir. `gep --type=webflux --from-swagger=swagger.yaml --router=false` genera un controlador y modelos por cada etiqueta de la API, además del `ApiRest` de ejemplo, y compila sin cambios.

## Propiedades del proyecto (`gradle.properties`)

| Propiedad | Para qué sirve |
| --------- | --------------- |
| `package`, `reactive`, `lombok`, `metrics`, `javaVersion` | Las fija `ca` y las leen las tareas posteriores |
| `analytics` | `false` desactiva la analítica |
| `excludeModule` | Módulos excluidos de la compilación de Gradle, separados por comas |
| `excludeModuleFromApp` | Módulos que no se inyectan en `app-service`, separados por comas |
| `arch.unit.skip` | `true` omite el test de ArchUnit. No recomendado |
| `arch.unit.forbiddenDomainSuffixes` | Reemplaza los sufijos prohibidos (por defecto `dto,request,response`) |
| `arch.unit.forbiddenDomainClassNames` | Reemplaza las palabras de tecnología prohibidas |

## Bloques en el `build.gradle` de la raíz

```groovy
// Permite librerías en el dominio que validateStructure rechazaría. Las plataformas (BOM) ya están permitidas
cleanPlugin {
    modelProps {
        whitelistedDependencies = "allowed-library, another-library"
    }
}

// Fuerza versiones para corregir vulnerabilidades. Las coordenadas de dos partes se aplican a todo un grupo
dependenciesOverride {
    ensure 'com.fasterxml.jackson.core:jackson-core:2.22.4'
    ensure 'tools.jackson.core:3.2.4'
}
```

Las versiones de los plugins de Spring Boot, Sonar y Pitest se pueden fijar en el bloque `plugins {}` de la raíz. Mantén `apply false` en Spring Boot.

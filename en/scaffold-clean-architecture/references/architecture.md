# Architecture of the generated project

## Layers and modules

| Layer | Folder | What it holds | Can depend on |
| ----- | ------ | ------------- | ------------- |
| Domain | `domain/model` | Entities and gateways (ports, as interfaces) | Nothing. In reactive projects, Reactor is allowed |
| Domain | `domain/usecase` | Application logic, orchestrating gateways | `model` only |
| Infrastructure | `infrastructure/driven-adapters/*` | Implementations of gateways: databases, REST clients, queues | `model`, external libraries |
| Infrastructure | `infrastructure/entry-points/*` | Start of the flows: REST, consumers | `model`, `usecase`, external libraries |
| Infrastructure | `infrastructure/helpers/*` | Utilities shared by adapters and entry points | `model`, external libraries |
| Application | `applications/app-service` | `MainApplication`, bean configuration, `application.yaml` | Assembles all modules |

Infrastructure modules must never depend on `app-service`. An adapter never calls an entry point, and a use case never names a technology.

## A flow, step by step

1. **Model:** `gm --name=Order` creates `model/order/Order.java` and `model/order/gateways/OrderRepository.java`. Add fields to the entity and methods to the gateway.
2. **Use case:** `guc --name=CreateOrder` creates `usecase/createorder/CreateOrderUseCase.java`. Inject the gateway through a `final` field.
3. **Adapter:** generate it with `gda`, implement the gateway and annotate the class with `@Repository` or `@Component`. Map between the adapter's persistence models and the domain model here, never in the domain.
4. **Entry point:** generate it with `gep`, inject the use case, and call it.

Example of a reactive use case:

```java
@RequiredArgsConstructor
public class CreateOrderUseCase {
    private final OrderRepository orderRepository;

    public Mono<Order> create(String product) {
        return orderRepository.save(Order.builder().product(product).build());
    }
}
```

In imperative projects the same code returns `Order` directly. In reactive projects, don't block inside a flow (`.block()`, synchronous clients).

## Automatic wiring

The plugin's conventions do this. Don't do it by hand:

- **Module discovery:** any folder with a `build.gradle` under `applications`, `domain` or `infrastructure` is a module. `settings.gradle` has no `include` lines.
- **Dependencies:** `usecase` receives `model`; adapters and helpers receive `model` and `spring-context`; entry points receive `model`, `usecase` and `spring-context`; `app-service` receives all modules.
- **Dependencies between infrastructure modules aren't automatic:** add them yourself in the module's `build.gradle`.
- **Libraries in every module:** Spring Boot's BOM (so versions of Spring libraries are optional), `spring-boot-starter-test`, Lombok if enabled, and Reactor if reactive.
- **Use case beans:** `UseCasesConfig` scans `<package>.usecase` with the pattern `^.+UseCase$`. A class that doesn't end in `UseCase` or lives elsewhere won't be a bean.
- **Component scan:** `MainApplication` scans the base package, so adapters and entry points must live under it. For a `generic` module, which is generated with no source files, create the package yourself, without hyphens (`in-memory-orders` → `<package>.inmemory`).

## Dependency rule (`validateStructure`)

It runs on every `compileJava`, so a violation stops the build:

| Violation | Message |
| --------- | ------- |
| A library in `model` | `Model module is invalid` |
| A library other than `model` in `usecase` | `Use case module is invalid` |
| `app-service` as a dependency of infrastructure | `Infrastructure layer is invalid` |

The right response to a violation is to move the code to the layer it belongs to, usually behind a gateway. Use `whitelistedDependencies` only for a library the user has decided to allow in the domain.

## ArchUnit rules

`validateStructure` writes `ArchitectureTest.java` and `Utils.java` into the tests of `app-service`. They're ignored by git because they contain absolute paths. Don't edit or commit them.

| Rule | What it checks | Effect |
| ---- | -------------- | ------ |
| 1.5 | Reactive flows use AWS async clients | Warning |
| 2.2 | Domain classes without technology suffixes (`Dto`, `Request`, `Response`) | Warning |
| 2.4 | Domain classes without technology names | Warning |
| 2.5 | Use cases with only `final` fields | **Fails the test** |
| 2.6 | Domain fields without technology names | Warning |
| 2.7 | Beans with only `final` fields, injected by constructor | Warning |

A warning doesn't break the build: it's written to `build/issues.json`, for Sonar. Read that file and fix what it reports, rather than assuming that a green build means no violations.

The rule behind 2.5 and 2.7 matters for correctness, not only style: a bean is shared between concurrent requests, so request data kept in a field gets mixed up between users.

## Quality and packaging

- **Coverage:** `build/reports/jacocoMergedReport/`.
- **Mutation:** with Pitest declared, `pitest` runs in each module as part of `jacocoTestReport`, and the aggregate lands in `build/reports/pitest/`. It requires all tests to pass. To skip it in a run: `-x pitest`.
- **Sonar:** configured at the root, reading the reports above and `build/issues.json`. Project values go in a `sonar {}` block in the root `build.gradle`.
- **Packaging:** `bootJar` produces `<project>.jar` in `applications/app-service/build/libs/`. `deployment/Dockerfile` is a starting point: review it before relying on it.
- **Build cache:** in `build-cache/` at the root, already ignored by git.
- **Generated README:** generic and in Spanish. Replace it with one describing the real project.

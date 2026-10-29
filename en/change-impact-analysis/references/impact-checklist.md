# Impact checklist

The dimensions a change can affect, and what to look for in each one. The items are technology-agnostic: apply each one with the idioms of the project's language, framework and architecture.

Not every item applies to every change. Use them as a guide, not as a form to fill in. In Quick mode, go through Code and Tests in depth and give the others one line each, saying whether they apply.

## How to search

The compiler or the IDE finds direct references. Many impacts hide in places they can't see:

- **References in code:** calls, imports, inheritance and interface implementations, dependency injection wiring, generics and overloads.
- **Names as text:** reflection, serialization (JSON, XML, ORM mappings), routes, event and queue names, SQL in strings, templates, translation keys, configuration files, scripts, infrastructure files.
- **Generated code:** clients and models generated from OpenAPI, `.proto` or schemas. Change the source, not the generated file, and count the regeneration.
- **Other languages in the same repository:** frontend that consumes the backend, scripts, infrastructure, tests in another language.
- **History:** `git log` on the affected files shows how often they change, which changes usually go together and which areas are fragile.

## 1. Code: modules and units

- Units that must change: classes, modules, components, functions, models.
- Callers of the changed units and how they use them (a new required parameter breaks all of them; an optional one, none).
- Implementations and subclasses of changed interfaces or base classes.
- Module or layer boundaries the change crosses, and whether it respects the project's dependency rules.
- Shared code (utilities, common libraries, base components) whose change reaches unrelated parts.
- Duplicated logic: the same rule implemented in several places that must change together.

## 2. Processes and flows

- Business flows that pass through the changed code, from start to end.
- Background jobs, scheduled tasks, batch processes, queue and event consumers, webhooks.
- Flows that run in an order that matters: state machines, multi-step processes, retries, compensations.
- Processes in flight during the deploy: messages already queued, jobs half done, sessions open.

## 3. Contracts

- APIs exposed (REST, GraphQL, gRPC, WebSocket): paths, fields, types, required fields, status codes, errors.
- Events and messages published or consumed: names, schemas, versions.
- Public API of a library or SDK, CLI commands and options, file formats imported or exported.
- The database schema, when other systems read it directly.
- **Compatibility:** whether current consumers keep working without changes (adding an optional field) or break (renaming, removing, changing a type or making a field required). If it breaks, how it's versioned and how long both versions must coexist.

## 4. Data

- Schema changes: tables, columns, indexes, constraints, types, nullability, default values.
- Existing records: what value they get, whether a backfill is needed, and how many rows it touches.
- Migrations: whether they lock tables or take long on large volumes, whether they can be applied without downtime, whether they're reversible.
- Data derived from the changed data: caches, search indexes, materialized views, reports, exports, analytics.
- Personal or sensitive data: classification, retention, encryption, audit.

## 5. Tests

- Existing tests that cover the changed code and will need to change (assertions, fixtures, mocks, snapshots, test data).
- Tests that are missing: behavior the change adds or modifies with no test, and edge cases.
- Contract, integration and end-to-end tests that cover affected flows or consumers.
- The current state of the area: if it has little coverage, writing tests first is part of the change and of the estimate.
- Test infrastructure the change needs: new fixtures, factories, containers, test doubles.

## 6. Consumers

- **Internal, visible in the repository:** other modules, apps or services in the same repository (frontend, mobile, workers).
- **External, not visible:** other repositories or services, other teams, mobile apps in versions already installed, partners and third parties, reports or BI that read the data. List them as "to confirm" and say how to find them (API gateway logs, client registry, service catalog, asking the owning team).
- What each consumer needs: nothing, an update, or a coordinated deploy.

## 7. Configuration and infrastructure

- Environment variables, configuration files, feature flags, secrets.
- Infrastructure as code, containers, permissions, network rules, queues and topics to create.
- Dependencies: new libraries or version upgrades, and their own impact.
- Build and CI/CD: pipelines, scripts, required checks.

## 8. Security and compliance

- Authentication and authorization: new endpoints or data that need permission checks, roles that change.
- Input validation for new fields or parameters.
- Exposure of sensitive data in responses, logs, events or errors.
- Audit, legal or regulatory requirements the change touches.

## 9. Operations and observability

- Logs, metrics, traces, alerts and dashboards that must change or be added.
- Performance: new queries, loops over large collections, external calls, cache behavior.
- Deploy: order between services, database before code, feature flags, need for a maintenance window.
- Rollback: whether the change can be reverted, and what happens to data written in the meantime.

## 10. Documentation and user experience

- README, technical documentation, API documentation, architecture decision records.
- Texts and screens users see, translations, emails and notifications.
- User guides, help content, release notes.

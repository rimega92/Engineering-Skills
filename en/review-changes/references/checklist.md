# Review checklist

What to look for in a change, how deep to go and how to prioritize each finding. The items are technology-agnostic: apply each one with the idioms of the project's language, framework and architecture.

Not every item applies to every change. Use them as a guide, not as a form to fill in.

## Priority

Prioritize each finding by its impact, reach, likelihood and context. If the project has its own scale, use it instead of this one.

| Priority | Meaning | Example |
|---|---|---|
| 🔴 **P0, Critical** | Critical, immediate risk, such as an exploitable vulnerability or serious data corruption. | Financial data from many customers exposed |
| 🟠 **P1, High** | Major defect that can affect a core operation or cause a serious failure. | A transaction is left partially applied |
| 🟡 **P2, Medium** | Defect of limited reach, or a relevant risk under certain conditions. | An edge case produces a wrong result |
| 🔵 **P3, Low** | Minor, concrete problem worth fixing. | A rare scenario behaves wrongly with little effect |
| 💡 **Info** | Non-blocking improvement or recommendation that isn't a confirmed defect. | Simplify a function that works correctly |

Rules:

- The priority reflects the real or reasonably expected impact.
- Breaking a design principle doesn't make a finding critical on its own.
- Consider the reach of the problem, the conditions needed to trigger it and the safeguards that already exist.
- If the project uses both technical severity and fix priority, keep them apart.
- Don't duplicate findings that share a root cause.
- Don't present style preferences as functional defects.
- If the evidence isn't enough, report the uncertainty (potential risk) instead of a confirmed defect.

**Verdict** of the review:

- ✅ **Ready:** no P0, P1 or P2 findings.
- ⚠️ **Ready with changes:** no P0 findings, but there are P1 or P2 findings to fix first.
- ❌ **Needs work:** at least one P0 finding, or the approach itself needs rethinking.

## Depth levels

Each review mode uses some of these levels: Quick uses Level 1; Standard, Levels 1 and 2; Deep, all three.

### Level 1, basic: every mode

- Functional correctness and relevant edge cases.
- Possible regressions.
- Compliance with the project's standards and scaffold.
- Scope and coherence of the change.
- Tests and verifiability.
- Basic error handling.
- Obvious security problems.
- Consistency with the existing architecture.

### Level 2, specialized: Standard and Deep modes

Go deeper using sections 1 to 12 below, but only the ones for the areas the change touches: architecture and SOLID, security and authorization, persistence and data integrity, APIs, events and integrations, performance and complexity, concurrency, resilience, configuration and observability, migrations and compatibility, dependencies and infrastructure.

### Level 3, deep: Deep mode

When the change affects critical systems, sensitive data, financial operations, security or high-availability components, also consider:

- Threat modeling and abuse scenarios.
- Financial integrity and transactional consistency.
- Idempotency and duplicated operations.
- Complex concurrency and race conditions.
- Partial failures in distributed systems; retries, compensations and recovery.
- Compatibility during gradual deployments; data migrations and reversibility.
- Resilience when dependencies are unavailable.
- Operational impact, alerts and diagnosability; rollback risks and incident recovery.

## 1. Design and code quality

- **Clean code:** readability, descriptive names, clear intent, cohesive functions, little noise.
- **SOLID:** single responsibility, open/closed, Liskov substitution, interface segregation and dependency inversion, where they add value.
- **KISS:** no unnecessary complexity; the simplest solution that meets the requirements.
- **DRY:** duplicated logic or knowledge that can become inconsistent.
- **YAGNI:** no features, abstractions or extension points that aren't needed.
- **Separation of concerns:** responsibilities properly separated (for example, validation, business rules and data access not mixed in one function).
- **High cohesion, low coupling:** related responsibilities together, no unnecessary dependencies, no reaching into other modules' internals.
- **Least surprise:** components behave predictably; names don't lie about what the code does.
- **Accidental complexity:** deep nesting, very long functions, hard-to-read conditions, unnecessary abstractions.
- **Encapsulation:** internal details and state exposed only when needed.
- **Design consistency:** the change keeps the design criteria the project already follows.

## 2. Architecture and project structure

- **Scaffold compliance:** the directory, module, package and file structure the project defines.
- **Defined architecture:** layers, modules, bounded contexts and architectural responsibilities.
- **Dependency rules:** no forbidden dependencies, cycles or dependencies pointing the wrong way.
- **Design patterns:** used when they solve a concrete problem, not applied artificially.
- **DDD, when it applies:** entities, value objects, aggregates, repositories, domain services and context boundaries.
- **Domain and infrastructure separation:** business rules don't depend on technical details without need.
- **Configuration and conventions:** the rules documented in `README`, `AGENTS.md`, `CLAUDE.md`, instruction files, linters and other standards.
- **Component reuse:** existing components reused where appropriate, without adding generic abstractions nobody needs.
- **Module responsibility:** no module takes on responsibilities outside its purpose.
- **Architectural consistency:** no different architecture introduced without justification or, when needed, approval.

## 3. Functional correctness and logic

- **Requirements:** the change meets the known requirements and acceptance criteria.
- **Business logic:** rules that are wrong, missing, contradictory or in the wrong layer.
- **Edge cases:** null or empty values, numeric limits, empty collections, duplicates, unexpected input.
- **Conditions and branches:** inverted conditions, off-by-one errors, unreachable branches, unhandled scenarios, incomplete `switch` or `match` cases.
- **State and lifecycle:** initialization, updates, state transitions and resource cleanup.
- **Idempotency:** repeated operations don't cause wrong side effects when idempotency is needed.
- **Backward compatibility:** changes that can break existing behavior, consumers, integrations or data.
- **Dates and time zones:** formats, conversions, date boundaries and time zones.
- **Numeric precision:** rounding, overflow, conversions and decimal precision for the domain.
- **Invariants:** conditions that must always hold still hold.
- **Side effects:** unexpected state changes, extra writes or unjustified external calls.

## 4. Security

- **Input validation:** data from users, external systems and other untrusted sources.
- **Authentication:** protected operations verify identity correctly.
- **Authorization:** permissions, roles and access control on resources and operations; checks not done only on the client.
- **Injection:** SQL, commands, XSS, LDAP, paths, templates and any other kind that applies.
- **Secrets:** no credentials, tokens, private keys or secrets in the code, the repository or the logs. Report the location, never the value.
- **Data protection:** minimal exposure of personal, financial, confidential or sensitive data.
- **Cryptography:** approved algorithms, protocols and libraries; no home-made cryptography.
- **Vulnerable dependencies:** known vulnerabilities in new or updated dependencies.
- **Resource abuse:** request limits, input sizes, expensive operations and abuse possibilities.
- **Insecure configuration:** excessive permissions, insecure defaults, needlessly exposed services.
- **Error messages:** errors don't reveal secrets, internal details or information useful to an attacker.
- **Least privilege:** each component has only the permissions it needs.

## 5. Error handling and resilience

- **Error handling:** no ignored errors, swallowed exceptions or carrying on in an invalid state.
- **Specific exceptions:** no overly broad catches; the original cause is kept when it matters.
- **Error contracts:** responses, error codes and messages consistent with existing contracts.
- **Timeouts:** reasonable limits on external calls and potentially blocking operations.
- **Retries:** no unlimited retries, request storms or duplicated side effects.
- **Circuit breakers:** considered for dependencies whose unavailability can affect critical services.
- **Graceful degradation:** behavior when a dependency is unavailable.
- **Resource release:** connections, files, transactions and other resources are closed properly.
- **Consistency on failure:** what happens when an operation fails partially or completely.
- **Recovery:** the system recovers without manual intervention when that's a requirement.
- **Error propagation:** errors are propagated or transformed correctly between layers.
- **Cancellation:** no unnecessary work after a cancellation or a timeout.

## 6. Performance and concurrency

- **Algorithmic complexity:** algorithms that are expensive or don't scale with the expected volume.
- **Data access:** redundant queries, N+1 queries, missing pagination, unnecessary operations.
- **Memory and resources:** unnecessary accumulation, excessive copies, leaks, unbounded consumption.
- **Blocking operations:** blocking I/O or heavy work on the wrong execution context (for example, the main or UI thread).
- **Concurrency:** shared access, synchronization, atomicity, thread safety, race conditions, unawaited async calls.
- **Deadlocks:** lock acquisition order, transactions and mutual waits.
- **Caching:** expiration, invalidation, consistency and the risk of serving stale data.
- **Scalability:** reasonably expected volumes, concurrency and load patterns.
- **External calls:** repeated calls, unnecessary serialization, missing limits.
- **CPU:** repeated computation or unnecessary processing in relevant flows.
- **Pools and queues:** capacity and waiting policies.
- **Evidence:** don't claim a performance problem without enough evidence; distinguish theoretical risks from measured problems.

## 7. Persistence and data integrity

- **Transactions:** transaction boundaries, rollback and atomicity.
- **Data integrity:** constraints, relationships, invariants and business rules.
- **Concurrent writes:** no lost updates, duplicates or conflicts between simultaneous operations.
- **Schema migrations:** compatibility, execution order, reversibility and deployment safety.
- **Queries and ORM:** inefficient queries, unexpected side effects of mapping or lazy loading.
- **Existing data:** historical records, null fields, earlier formats and inconsistent data.
- **Financial precision:** decimals, currency, rounding, idempotency and traceability.
- **Database constraints:** indexes, keys, constraints and relationships suited to the change.
- **Cross-system consistency:** risk of databases, services and other systems getting out of sync.
- **Destructive operations:** deletions, bulk updates or irreversible changes.
- **Sensitive data:** how confidential data is handled, stored and deleted.
- **Compatibility during deployments:** old and new versions can run side by side during a migration.

## 8. APIs and integrations

- **API contracts:** schemas, status codes, formats, names and agreed semantics.
- **Consumer compatibility:** impact on clients and dependent systems.
- **Validation and serialization:** formats, required fields, limits and conversions.
- **External integrations:** errors, latency, unavailability, limits and provider changes.
- **Events and messaging:** contracts, duplicates, ordering, redelivery, dead-letter queues and schema evolution.
- **Distributed consistency:** idempotency, compensations and eventual consistency.
- **Versioning:** contract changes follow the project's versioning strategy.
- **Pagination and filters:** limits, ordering and behavior with large result sets.
- **Format compatibility:** no unintended changes to field names, types, defaults or date formats.
- **Unexpected responses:** behavior with incomplete, invalid or incompatible responses.
- **Provider limits:** quotas, rate limits and restrictions of integrated systems.

## 9. Tests and verifiability

- **Scenario coverage:** tests cover the important behavior, not just executed lines. New logic has tests; a bug fix ideally has a test that would have caught it.
- **Unit tests:** business rules, limits, errors and relevant scenarios.
- **Integration tests:** real interactions between components, where it applies.
- **Regression tests:** earlier behavior the change could break.
- **Assertions:** no tests that pass without checking the right result.
- **Isolation and determinism:** no accidental dependence on order, clock, network or uncontrolled external data.
- **Mocks:** no excessive mocking that stops the real behavior from being tested.
- **Negative tests:** invalid input, insufficient permissions and external failures.
- **Boundary tests:** extreme values, empty collections and exceptional conditions.
- **Concurrency tests:** simultaneous operations when the change can cause conflicts.
- **Contract tests:** compatibility with API or event consumers and providers.
- **Migration tests:** transformations, integrity and data compatibility.
- **Test data:** no inconsistent fixtures or data that hides defects.
- **Changed behavior:** reflected in the existing tests, not worked around by deleting or weakening them.

## 10. Maintainability and consistency

- **Naming:** consistent with the domain and the existing conventions. Avoid vague names (`data`, `info`, `manager`) and unknown abbreviations.
- **Duplication:** duplicated logic that can drift and raise maintenance cost.
- **Comments and documentation:** outdated documentation fixed; comments explain why when the code isn't enough. No `TODO` without context.
- **Dead code:** unused imports, variables, functions, branches and files; commented-out code; leftover debugging.
- **Style:** the project's formatter, linter and rules, without turning personal preferences into defects.
- **Internal APIs:** no unnecessary interfaces, too many parameters, boolean flags that hide two functions, or contracts that are hard to use correctly.
- **Magic values:** unexplained numbers or strings that should be named constants or configuration.
- **Technical debt:** shortcuts that create concrete, relevant risks.
- **Readable flow:** behavior easy to follow, without unnecessary jumps or indirection.
- **Function responsibility:** functions and methods focused on one understandable responsibility.
- **Mutability:** no state changes that are hard to trace or cause unnecessary side effects.
- **Duplicated configuration:** no repeated values that can drift over time.
- **Ease of change:** the design meets the current requirements without unnecessary complexity.

## 11. Configuration, deployment and observability

- **Per-environment configuration:** no environment-specific values hard-coded.
- **Variables and defaults:** required values validated, safe defaults, clear failure when configuration is missing.
- **Logs:** useful context, without secrets or sensitive data.
- **Metrics and traces:** instrumentation when the change alters critical flows or important failure points.
- **Health checks:** reflect the real state of the application and its relevant dependencies.
- **CI/CD:** compatible with the build, validations, packaging and deployment.
- **Operational compatibility:** feature flags, rollback, gradual deployment and breaking changes.
- **Resources:** limits, quotas, connections and resources the change needs.
- **Infrastructure as code:** permissions, exposure, configuration and side effects of infrastructure changes.
- **Alerts:** whether the change needs new signals to detect important failures.
- **Traceability:** critical operations can be followed across the relevant components.
- **Partial deployments:** behavior while different versions of the system coexist.
- **Rollback:** whether the change can be reverted, and what persistent effects could prevent a safe revert.

## 12. Scope and quality of the change

- **Scope:** no unrelated changes, opportunistic refactors or unnecessary modifications.
- **Traceability:** the change is linked to the requirement, issue or decision that justifies it.
- **Size and cohesion:** the change is understandable, reviewable and properly split; independent functional changes aren't bundled together.
- **Generated files and artifacts:** no binaries, temporary files or accidental artifacts.
- **New dependencies:** justified, considering maintenance, license, security and operational cost.
- **Configuration files:** no accidental changes or local values.
- **Contract changes:** changes that need coordination with other teams or consumers are flagged.
- **Documentation:** whether the change needs updates to the `README`, diagrams, contracts or instructions.
- **Overall consistency:** code, tests, configuration, migrations and documentation describe the same behavior.
- **Justified deviations:** departures from the standards that need a documented exception.

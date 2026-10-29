# README.md documentation standard

## Classification

- `[M]` Mandatory for every project.
- `[C]` Mandatory when it applies to the nature of the project.
- `[O]` Optional, depending on the project's complexity and needs.

## 1. Project identification and description

- [ ] `[M]` **Project name:** Official name of the system, service, component or library.
- [ ] `[M]` **Overview:** The project's purpose, the problem it solves and the value it provides.
- [ ] `[M]` **Project status:** Current status, such as in development, active, in maintenance, deprecated or archived.
- [ ] `[M]` **Owners and support channels:** Owning team or person, and the channels for asking questions or reporting problems (for example, the issue tracker in an open source project).
- [ ] `[C]` **Functional scope:** The system's capabilities, responsibilities and boundaries.
- [ ] `[O]` **Target audience:** The users, developers or consuming systems it's intended for.
- [ ] `[O]` **Table of contents:** Navigable index that makes long documents easier to browse.

## 2. Quick start and local execution

- [ ] `[M]` **Prerequisites:** Tools, versions, runtimes, permissions and dependencies needed to run the project.
- [ ] `[M]` **Local installation and setup:** Steps to prepare the environment from a freshly cloned repository.
- [ ] `[M]` **Environment variables and configuration:** Required variables, expected values, profiles and configuration files. Never include real secrets. If the project uses no environment variables or configuration, say so in one line.
- [ ] `[M]` **Running the application:** Commands to start the project and check that it works. For a library, how to import or use it from another project.
- [ ] `[M]` **Running tests:** Basic commands to run the tests and confirm the project works correctly. If there are no automated tests, say so.
- [ ] `[C]` **Build and packaging:** Procedure for producing executables, packages or container images.
- [ ] `[C]` **Local dependency setup:** Instructions for starting databases, auxiliary services, containers or seed data.
- [ ] `[O]` **Quick usage example:** Minimal example demonstrating the project's main functionality.
- [ ] `[O]` **Common commands:** Quick reference of everyday development and troubleshooting commands.

## 3. Features and behavior

- [ ] `[M]` **Main functionality:** Summary of the project's capabilities and expected behavior.
- [ ] `[C]` **Business rules and validations:** Relevant constraints, conditions, invariants and validations.
- [ ] `[C]` **Main functional flows:** Description of the most important processes and their stages.
- [ ] `[C]` **Known limitations:** Technical or functional constraints, unsupported scenarios and pending features.
- [ ] `[O]` **Use cases:** Examples of common usage scenarios.
- [ ] `[O]` **Glossary:** Definitions of acronyms and business- or domain-specific concepts.

## 4. Tech stack and architecture

- [ ] `[M]` **Tech stack:** Main languages, frameworks, libraries, runtimes and tools, including relevant versions.
- [ ] `[C]` **System architecture:** Description of the architecture, main components, responsibilities and relationships.
- [ ] `[C]` **Folder and file structure:** Repository layout with an explanation of the relevant directories and files.
- [ ] `[C]` **Main components and modules:** What each module is responsible for and how they interact.
- [ ] `[C]` **External dependencies and integrations:** Systems, services and platforms required for it to work.
- [ ] `[C]` **Data model:** Entities, relationships and structures needed to understand the data being managed.
- [ ] `[C]` **Per-environment configuration:** Configuration differences between development, testing and production.
- [ ] `[O]` **Architecture diagrams:** Visual representation of components, layers, services and dependencies, preferably in Mermaid.
- [ ] `[O]` **Context diagrams:** How the system relates to users, actors and external systems.
- [ ] `[O]` **Module diagrams:** Internal organization and dependencies between modules.
- [ ] `[O]` **Flow and sequence diagrams:** Representation of processes, data flows and interactions.
- [ ] `[O]` **Architecture decisions:** Rationale for relevant decisions, alternatives considered and main trade-offs.

## 5. Interfaces and integration contracts

- [ ] `[C]` **Exposed APIs and endpoints:** Methods, routes, parameters, headers, request bodies, responses, HTTP status codes and possible errors.
- [ ] `[C]` **Integration contracts:** Exchange formats, schemas, protocols and communication rules between components.
- [ ] `[C]` **Authentication and authorization:** Access mechanisms, roles, permissions and authentication requirements.
- [ ] `[C]` **Messaging and events:** Queues, topics, published and consumed events, message contracts and processing policies.
- [ ] `[C]` **External service integrations:** Configuration needed to connect to providers, cloud services and other systems.
- [ ] `[O]` **Usage examples:** Sample requests and responses, code snippets or `curl` commands.
- [ ] `[O]` **Interactive API documentation:** Links to Swagger UI, OpenAPI, Postman or other exploration tools.
- [ ] `[O]` **Integration diagrams:** Call sequences and interactions between services.

## 6. Quality, testing and development

- [ ] `[C]` **Testing strategy:** Types of tests used, such as unit, integration, contract, acceptance or end-to-end, and how to run each type.
- [ ] `[C]` **Coding standards:** Naming conventions, formatting, static analysis and quality criteria.
- [ ] `[C]` **Contribution guide:** Procedure for changing the project, validating changes and proposing contributions.
- [ ] `[C]` **CI/CD:** Description of, or reference to, the integration, validation and delivery pipelines.
- [ ] `[O]` **Coverage and quality metrics:** Coverage targets, thresholds and relevant metrics.
- [ ] `[O]` **Branching and commit strategy:** Branching conventions, branch naming and commit messages.
- [ ] `[O]` **Debugging setup:** Configuration for debugging the application and running tests from the IDE.

## 7. Security, operations and maintenance

- [ ] `[C]` **Security considerations:** Secret management, data protection, permissions and secure development practices.
- [ ] `[C]` **Error and exception handling:** Error strategy, relevant exceptions and behavior on failure.
- [ ] `[C]` **Logging and observability:** Log format and location, metrics, traces, correlation IDs and diagnostic tools.
- [ ] `[C]` **Deployment:** Procedures for, or references to, deploying the project to the relevant environments.
- [ ] `[C]` **Infrastructure and associated resources:** Required resources, declarative configuration and operational dependencies.
- [ ] `[C]` **Availability and failure recovery:** Timeouts, retries, recovery and fault tolerance.
- [ ] `[C]` **Database and migrations:** Connection configuration, schema setup and running migrations.
- [ ] `[C]` **Performance and scalability:** Known limits, capacity requirements and performance considerations.
- [ ] `[C]` **Common errors and troubleshooting:** Frequent problems, known causes, symptoms and fixes.
- [ ] `[O]` **Operational procedures:** Maintenance, restart and recovery tasks, and post-deployment checks.
- [ ] `[O]` **Monitoring and alerting:** Operational indicators, thresholds and links to monitoring dashboards.
- [ ] `[O]` **Costs and resource usage:** Cost considerations, usage limits and optimization recommendations.

## 8. Versioning, references and legal

- [ ] `[M]` **Additional documentation:** Links to manuals, specifications, diagrams, contracts and related resources. If there's no additional documentation, this section is left out.
- [ ] `[C]` **Versioning and compatibility:** Current version, versioning strategy and compatibility with other components.
- [ ] `[C]` **Change history:** Link to the changelog or release notes when releases are managed formally.
- [ ] `[C]` **License and terms of use:** Applicable license, or a link to the license file, depending on the distribution model.
- [ ] `[O]` **Alternatives and comparisons:** Alternative solutions and differences that help explain the project's purpose.
- [ ] `[O]` **Acknowledgements and external references:** Credits, sources and resources that contributed to the project.

## 9. General rules of the standard

- Documentation must be kept up to date alongside the code.
- `[C]` and `[O]` sections that don't apply are left out, without marking them "Not applicable".
- Long documentation should live in dedicated files (for example, under `docs/`) and be linked from the README.
- Technical contracts must have a single source of truth. For example, use OpenAPI as an API's contract and link to it from the README.
- Use diagrams when they help explain the architecture, modules or relevant flows.
- Never document real credentials, tokens, passwords or secrets.
- Commands and examples must be reproducible and match the current version of the project.
- The depth of the documentation should be proportional to the project's complexity, criticality and audience.

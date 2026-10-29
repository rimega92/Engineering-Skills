# Evidence map

Maps what you find in a project to the sections of `standard.md` it triggers or affects.

- In **create mode**, use it to decide which `[C]` sections apply.
- In **update mode**, use it to know which sections to review when a file changes.

The example files are not exhaustive. Apply the same logic to the equivalent in any language or technology.

| Evidence in the project | Examples | Sections |
|---|---|---|
| Dependency manifests and runtime versions | `package.json`, `pom.xml`, `build.gradle`, `go.mod`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `pubspec.yaml`, `Gemfile`, `*.csproj`, `.nvmrc`, `.tool-versions` | Tech stack, Prerequisites, Installation |
| Scripts and task automation | `package.json` `scripts`, `Makefile`, `justfile`, `Taskfile`, `scripts/` folder | Running the application, Running tests, Build, Common commands |
| Environment variables and configuration | `.env.example`, `application.yml`, `appsettings.json`, `config/`, environment variable reads in the code | Environment variables, Per-environment configuration |
| Several profiles or environments | `application-prod.yml`, `.env.staging`, `config/environments/` | Per-environment configuration, Deployment |
| Routes, controllers or API specs | Route definitions, controllers, GraphQL resolvers, `.proto` files, `openapi.yaml` | APIs and endpoints, Integration contracts, Usage examples, Interactive API documentation |
| Authentication | Auth middleware, guards, JWT, OAuth, role management | Authentication and authorization, Security considerations |
| Messaging | Kafka, RabbitMQ, SQS or Pub/Sub producers and consumers; event or webhook handlers | Messaging and events, Integration contracts |
| External service clients | Third-party SDKs, HTTP clients for other services, cloud services | External service integrations, External dependencies and integrations |
| Database | Migrations, ORM models, schemas, `.sql` files, seeds | Data model, Database and migrations, Local dependency setup |
| Containers and local services | `Dockerfile`, `docker-compose.yml`, devcontainers | Local dependency setup, Build and packaging, Deployment |
| Infrastructure | Terraform, Kubernetes, Helm, CloudFormation, `serverless.yml`, hosting platform config | Infrastructure and resources, Deployment, Per-environment configuration |
| CI/CD | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` | CI/CD, Deployment |
| Tests | Test folders, test framework configuration, coverage configuration | Running tests, Testing strategy, Coverage |
| Code quality | Linter and formatter configuration, `.editorconfig`, pre-commit hooks | Coding standards |
| Contribution | `CONTRIBUTING.md`, issue or pull request templates, commit conventions | Contribution guide, Branching and commit strategy |
| Code structure | Top-level folders, modules, packages, layers | Folder structure, Components and modules, Architecture |
| Several services or apps | Monorepo, `docker-compose` with several services, workspaces | Architecture, Diagrams, External dependencies and integrations |
| Error handling | Global error handlers, custom exceptions, error codes | Error and exception handling |
| Resilience | Retries, timeouts, circuit breakers, retry queues | Availability and failure recovery |
| Observability | Logging libraries, metrics, traces, health checks | Logging and observability, Monitoring and alerting |
| Caching, rate limiting or job queues | Redis, rate limiters, background workers | Performance and scalability |
| Domain validations | Validators, input schemas, rules in the domain layer | Business rules and validations |
| Version and releases | `version` field, git tags, `CHANGELOG.md`, release configuration | Versioning and compatibility, Change history |
| License | `LICENSE`, manifest `license` field | License and terms of use |
| Existing documentation | `docs/` folder, linked wikis, ADRs | Additional documentation, Architecture decisions |
| Debugging configuration | `.vscode/launch.json`, IDE run configurations | Debugging setup |

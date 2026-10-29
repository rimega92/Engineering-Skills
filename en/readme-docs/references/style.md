# Style guide

How to write the README so it's easy to read: wording, Markdown formatting and Mermaid diagrams.

## Writing

### Tone and technical level

- **Plain language by default.** Write the way you'd explain the project to someone new on the team: short sentences, active voice, second person ("run", "configure").
- **Technical where it's needed.** The level depends on the section:
  - **For any reader** (overview, main functionality, scope, status): no jargon. Someone who doesn't code should understand what the project does and what it's for.
  - **For people who will run or change the project** (quick start, architecture, APIs, data model, operations, security): use the correct technical terminology, without oversimplifying. Explain terms specific to the project or its domain, not industry-standard ones.
- **Lead with what matters.** Each section opens with a sentence saying what it covers or what it's for. Details come after.
- **Concrete before abstract.** An example, a command or a table explains more than a generic paragraph.
- **Acronyms.** Define them the first time they appear, except very well-known ones (API, URL, HTTP).
- **Consistent terminology.** Always use the same name for the same thing. If the code says `order`, don't alternate between "order", "purchase" and "request".
- **No filler.** Avoid words like "simply", "easily" or "obviously", and sentences that carry no information ("This section describes...").

### Paragraphs and lists

- Paragraphs of three or four sentences at most.
- Numbered lists for steps that are followed in order. One step is one action, with its command if it has one.
- Bulleted lists for items with no order.
- Tables for information with the same repeated structure (environment variables, endpoints, commands).

## Markdown

Follow the [markdownlint](https://github.com/DavidAnson/markdownlint) rules and GitHub Flavored Markdown.

### Structure

- A single `#` heading (the project name), at the top of the file.
- Don't skip heading levels (`##` → `####`).
- Headings with `#` (ATX style), with no trailing period, and no two headings with the same text.
- A blank line before and after headings, lists, tables and code blocks.
- Add a table of contents when the README has more than five `##` sections.

### Code and commands

- Every code block declares its language: `bash`, `json`, `yaml`, `http`, `sql`, `typescript`, etc. Use `text` when there's no language.
- Commands are written without the prompt (`$`), so they can be copied and pasted.
- One command per line. If a step needs several commands, explain what each one does when it isn't obvious.
- File names, variables, commands and values go in backticks: `` `.env` ``, `` `PORT` ``.

### Tables

- Short headers and one idea per cell.
- Recommended format for environment variables:

  ```markdown
  | Variable | Required | Description | Example |
  |----------|----------|-------------|---------|
  | `DATABASE_URL` | Yes | PostgreSQL connection string | `postgres://user:pass@localhost:5432/app` |
  ```

- Recommended format for endpoints:

  ```markdown
  | Method | Path | Description | Authentication |
  |--------|------|-------------|----------------|
  | `GET` | `/api/orders/{id}` | Gets an order | Bearer token |
  ```

### Links and images

- Relative links for files in the repository: `[deployment guide](docs/deployment.md)`.
- Descriptive link text. Never "here" or "this link".
- Every image has alt text describing its content.

### GitHub elements

- **Alerts** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`): use them only for information the reader must not miss, one or two per section at most. If the project isn't on GitHub, use plain blockquotes, because other platforms show the `[!NOTE]` text as is.
- **Collapsible blocks** (`<details>` and `<summary>`): for long, secondary content, such as a long sample output or the full list of options.
- **Badges:** only if they carry real information (CI status, published version, license). Never more than one line of badges.

## Mermaid diagrams

GitHub, GitLab and most editors render Mermaid inside a ` ```mermaid ` block.

### When to use a diagram

- When it explains something better than text: several connected services, a flow with decisions, a sequence of calls between components, a data model with relationships.
- Never for something a sentence or a list can explain.
- Every diagram is preceded by a sentence saying what it shows.

### Which type to use

| To show | Type |
|---|---|
| Architecture, components, context, dependencies between modules | `flowchart` |
| Interactions between components over time | `sequenceDiagram` |
| Data entities and their relationships | `erDiagram` |
| States an entity goes through | `stateDiagram-v2` |
| Class or type structure | `classDiagram` |

Use only these types. Newer ones (`architecture-beta`, `C4Context`, etc.) are experimental and don't always render on GitHub.

### Readability

- **About 15 nodes per diagram at most.** If there are more, split it: one overview diagram and others for detail.
- **Direction to match the shape:** `LR` (left to right) for flows and chains of services, `TD` (top down) for hierarchies and layers.
- **Short IDs and clear labels:** `api["Orders API"]`. Put labels in quotes if they contain spaces, accents, parentheses or other special characters.
- **Group with `subgraph`** the components that belong to the same layer, service or boundary (for example, "Cloud" versus "External").
- **Label arrows** when the relationship isn't obvious: `api -->|"REST"| db`.
- **Shapes with meaning:** `[(...)]` for databases, `([...])` for start and end, `{...}` for decisions, `[[...]]` for subprocesses.
- **In sequence diagrams,** use `autonumber` and `participant` with short aliases.
- **No theme directives** (`%%{init: ...}%%`): they force a theme that may not look right in light or dark mode.

### Colors

Use color when it helps tell component types apart, not as decoration. Define colors with `classDef` and apply them with `:::class` or `class`.

This palette reads well in both GitHub's light and dark modes: light fills, a saturated border and dark text.

```text
classDef frontend fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
classDef backend  fill:#dcfce7,stroke:#16a34a,color:#14532d
classDef data     fill:#fef3c7,stroke:#d97706,color:#78350f
classDef external fill:#f3e8ff,stroke:#9333ea,color:#581c87
classDef async    fill:#ffe4e6,stroke:#e11d48,color:#881337
classDef infra    fill:#f1f5f9,stroke:#64748b,color:#0f172a
```

| Class | Color | For |
|---|---|---|
| `frontend` | Blue | User interfaces: web, mobile, desktop |
| `backend` | Green | Your own services, APIs, workers |
| `data` | Amber | Databases, caches, storage |
| `external` | Purple | External systems and providers |
| `async` | Rose | Queues, topics, events |
| `infra` | Gray | Infrastructure, gateways, load balancers |

Rules:

- Five or six colors per diagram at most, always with the same meaning throughout the README.
- If you use color, add a legend below the diagram (one line of text is enough), because color alone shouldn't be the only way information is conveyed.
- Don't use dark fills or light text.

Example:

```mermaid
flowchart LR
    user(["User"])

    subgraph app["Application"]
        web["Web (React)"]:::frontend
        api["Orders API"]:::backend
        worker["Notifications worker"]:::backend
    end

    db[("PostgreSQL")]:::data
    queue["Event queue"]:::async
    pay["Payment gateway"]:::external

    user --> web
    web -->|"REST"| api
    api --> db
    api -->|"order.created"| queue
    queue --> worker
    api -->|"HTTPS"| pay

    classDef frontend fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef backend  fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef data     fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef external fill:#f3e8ff,stroke:#9333ea,color:#581c87
    classDef async    fill:#ffe4e6,stroke:#e11d48,color:#881337
```

Legend: blue, user interface; green, own services; amber, data; rose, messaging; purple, external systems.

### Validation

- If `mmdc` (Mermaid CLI) is installed, validate each diagram with it.
- If not, check the syntax carefully: labels with special characters in quotes, every `subgraph` closed with `end`, and no reserved word (`end`, `graph`, `class`) used as a node ID.

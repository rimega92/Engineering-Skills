# Rimega Skills

🇬🇧 English · [🇪🇸 Español](README.es.md)

A collection of agent skills for [Claude Code](https://claude.com/claude-code), [OpenAI Codex](https://developers.openai.com/codex) and [GitHub Copilot](https://github.com/features/copilot) that you can reuse across projects. The skills follow the open [Agent Skills](https://agentskills.io/) format, so the same skill works in all three tools. Most skills don't depend on a particular technology or programming language, so they work for frontend, backend, mobile and other kinds of work. When a skill does target a specific language or stack, its entry below says so.

Every skill comes in two languages:

- [`en/`](en/): English
- [`es/`](es/): Spanish

Both versions of a skill have the same folder name and the same content.

## Contents

- [Skills](#skills)
  - [readme-docs](#readme-docs)
- [Installation](#installation)
- [Usage](#usage)

## Skills

| Skill | What it's for | Stack |
|-------|---------------|-------|
| [`readme-docs`](#readme-docs) | Create a project's README.md, or update it after code changes | Agnostic |

### readme-docs

Creates and maintains a project's `README.md` following a documentation standard. Each section of the standard is classified as mandatory (`[M]`), conditional (`[C]`, required when it applies to the project) or optional (`[O]`). The standard covers identification, quick start, features, architecture, APIs and integrations, quality, operations and versioning.

**When to use it**
- To document a project that has no README, or only a minimal one.
- To update the README after changing the code: new dependencies, endpoints, environment variables, services, and so on.

**How to use it**
- Ask for it: _"Document this project"_, _"Update the README with the latest changes"_.
- It picks the mode on its own: create mode if there's no README with real content, update mode otherwise. To force a mode, say so: _"Create the README from scratch"_, _"Update the README"_.

**How it works**
- It infers everything it can from the project (manifests, scripts, configuration, Docker, CI, tests, code). For facts only the team knows, such as status, owners or the reasons behind decisions, it asks you all its questions in a single message. Anything you leave unanswered becomes a visible `Pending` marker.
- In update mode it reads a sync marker at the end of the README, `<!-- readme-docs:sync commit=... date=... -->`, reviews the changes since that commit and edits only the affected sections. It keeps text written by people, and it asks before removing a whole section.
- It moves long content (full API reference, data model, and so on) into files under `docs/` with standard names (`architecture.md`, `api.md`, `data-model.md`, ...) and links them from the README. Update mode keeps those files current too. `docs/` files written by people are linked but never modified.
- It never copies secrets, and it checks that the commands and paths it documents actually exist.
- It writes READMEs that are easy to read. Sections meant for any reader use plain language, and sections that need it (architecture, APIs, operations) use technical language. Markdown follows markdownlint and GitHub Flavored Markdown. Mermaid diagrams are kept small and use a color palette that reads well in both light and dark mode, with a legend.
- It keeps the existing README's language. A new README is written in the language you use to talk to it.

**Files**
- `SKILL.md`: the workflow for both modes.
- `references/standard.md`: the documentation standard, with each section's classification.
- `references/evidence-map.md`: which files in a project trigger or affect each section.
- `references/style.md`: style guide for wording, Markdown and Mermaid diagrams, including the color palette.

## Installation

A skill is a folder that contains a `SKILL.md` file. To install one, copy its folder from the language you want into your tool's skills folder:

| Tool | One project | Every project (personal) |
|------|-------------|--------------------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

First, clone the repository:

```bash
git clone https://github.com/rimega92/Rimega-Skills.git
```

Then copy the skill for your tool.

### Claude Code

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.claude/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.claude/skills/
```

### OpenAI Codex

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.codex/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.agents/skills/
```

### GitHub Copilot

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.copilot/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.github/skills/
```

If the destination folder doesn't exist yet, create it first with `mkdir -p`. For the Spanish version, replace `en/` with `es/`.

Install only one language version of each skill. Both versions share the same `name`, so installing both causes a conflict.

## Usage

The agent triggers a skill on its own when your request matches the skill's `description`, so in most cases you just ask for what you need. Each tool also has its own way to invoke a skill explicitly; in Claude Code, for example, you type `/<skill-name>`.

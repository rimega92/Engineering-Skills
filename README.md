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
- [Contributing](#contributing)

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

### Install in Claude Code

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.claude/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.claude/skills/
```

### Install in OpenAI Codex

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.codex/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.agents/skills/
```

### Install in GitHub Copilot

```bash
# Personal install
cp -r Rimega-Skills/en/<skill-name> ~/.copilot/skills/

# Single-project install
cp -r Rimega-Skills/en/<skill-name> /path/to/project/.github/skills/
```

If the destination folder doesn't exist yet, create it first with `mkdir -p`. For the Spanish version, replace `en/` with `es/`.

Install only one language version of each skill. Both versions share the same `name`, so installing both causes a conflict.

## Usage

There are two ways to use a skill:

- **Automatically:** the agent triggers the skill on its own when your request matches the skill's `description`. In most cases you just ask for what you need.
- **Explicitly:** you name the skill, using your tool's syntax. Useful when the agent doesn't pick the skill on its own, or when you want to be sure it uses it.

The examples below use the `readme-docs` skill.

### Use in Claude Code

```text
# Automatically
Update the README with the latest changes

# Explicitly
/readme-docs
/readme-docs update the README with the latest changes
```

### Use in OpenAI Codex

```text
# Automatically
Update the README with the latest changes

# Explicitly
$readme-docs update the README with the latest changes
```

In the Codex CLI and IDE extension, you can also run `/skills` to pick a skill from a list.

### Use in GitHub Copilot

```text
# Automatically
Update the README with the latest changes

# Explicitly
/readme-docs update the README with the latest changes
Use the /readme-docs skill to update the README with the latest changes
```

In VS Code, type `/` in the chat to see the available skills. In Copilot CLI, include `/<skill-name>` in your prompt, as in the second example.

## Contributing

Contributions are welcome: fixes, improvements to existing skills and new skills.

### Before you start

- **New skill:** open an [issue](https://github.com/rimega92/Rimega-Skills/issues) first describing what it's for, so we can agree on it before you put work into it.
- **Fix or improvement:** you can open the pull request directly. For bigger changes, an issue first is still a good idea.

### Workflow

1. Fork the repository on GitHub (you don't have write access to the original, so your changes go to your copy).
2. Clone your fork and add the original repository as `upstream`:

   ```bash
   git clone https://github.com/<your-user>/Rimega-Skills.git
   cd Rimega-Skills
   git remote add upstream https://github.com/rimega92/Rimega-Skills.git
   ```

3. Create a branch from an up-to-date `main`. Use a short name with a prefix that says what kind of change it is: `feat/` (new skill or feature), `fix/` (bug fix) or `docs/` (documentation only).

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feat/<skill-name>
   ```

4. Make your changes following the [rules](#rules) below.
5. Commit with clear messages: in English, in the imperative mood, and with a short first line (for example, `Add commit-message skill` or `Fix typo in readme-docs`). Prefer small commits that each do one thing.

   ```bash
   git add .
   git commit -m "Add <skill-name> skill"
   ```

6. Push the branch to your fork:

   ```bash
   git push -u origin feat/<skill-name>
   ```

7. Open a pull request on GitHub against `main` of this repository. In the description, explain what changes and why, and link the issue if there is one.
8. Respond to review comments by pushing new commits to the same branch; the pull request updates on its own.

### Rules

- **Both languages:** every skill exists in `en/` and `es/` with the same folder name, in English and kebab-case. Any change to one version goes to the other in the same pull request. Translate the text, but keep code, commands and file names identical.
- **Frontmatter:** each `SKILL.md` starts with `name` (identical to the folder name, lowercase letters, numbers and hyphens, at most 64 characters) and `description` (at most 1024 characters, written in that folder's language, saying what the skill does and when to use it).
- **Tool-neutral:** write for "the agent". Don't mention a specific tool or rely on its syntax or frontmatter fields, so the skill works in Claude Code, Codex and Copilot alike.
- **READMEs:** if you add, change or remove a skill, update `README.md` and `README.es.md`: table of contents, skills table and the skill's own section.
- **Test it:** before opening the pull request, install the skill in at least one tool and check that it triggers and does what it says.

[`AGENTS.md`](AGENTS.md) has the full conventions. If you work with an AI agent, it reads them on its own.

# Rimega Skills

🇬🇧 English · [🇪🇸 Español](README.es.md)

A collection of [Claude Code](https://claude.com/claude-code) skills that you can reuse across projects. Most skills don't depend on a particular technology or programming language, so they work for frontend, backend, mobile and other kinds of work. When a skill does target a specific language or stack, its entry below says so.

Every skill comes in two languages:

- [`en/`](en/): English
- [`es/`](es/): Spanish

Both versions of a skill have the same folder name and the same content.

## Skills

| Skill | What it's for | Stack |
|-------|---------------|-------|
| _No skills yet_ | | |

## Installation

A skill is a folder that contains a `SKILL.md` file. To install one, copy its folder from the language you want into one of these locations:

- **Every project (personal):** `~/.claude/skills/`
- **One project:** `.claude/skills/` inside that project

```bash
git clone https://github.com/<user>/Rimega-Skills.git

# Personal install (English version)
cp -r Rimega-Skills/en/<skill-name> ~/.claude/skills/

# Single-project install (Spanish version)
cp -r Rimega-Skills/es/<skill-name> /path/to/project/.claude/skills/
```

Install only one language version of each skill. Both versions share the same `name`, so installing both causes a conflict.

## Usage

Claude Code triggers a skill on its own when your request matches the skill's `description`. You can also invoke a skill directly by typing `/<skill-name>`.

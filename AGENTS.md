# AGENTS.md

Guidance for AI coding agents (Claude Code, OpenAI Codex, GitHub Copilot and others) working in this repository.

## Purpose

A personal library of agent skills, reused across many projects and published on GitHub. Skills follow the open [Agent Skills](https://agentskills.io/) format, so the same skill works in Claude Code, OpenAI Codex and GitHub Copilot. Skills are technology- and language-agnostic by default (frontend, backend, mobile, etc.). A skill is tied to a specific language or stack only when the owner explicitly says so.

Skills are built one at a time, and the owner chooses which one to work on next. Don't create skills nobody asked for.

## Structure

```text
es/<skill-name>/SKILL.md   # Spanish version
en/<skill-name>/SKILL.md   # English version
```

- Every skill exists in **both** `es/` and `en/`, with the same folder name (kebab-case, in English) so the two versions map 1:1.
- When creating or changing a skill, update both language versions in the same change. They should match in content and structure. Translate the text, but keep code, commands and file names identical.
- A skill folder can hold supporting files beside `SKILL.md` (scripts, reference docs, templates). Mirror them in both languages. Translate the text files; don't duplicate scripts that contain no language-specific text unless they need translating.
- Don't create per-tool folders or copies. One skill folder serves every tool; only the install path differs.

## Skill format

Each `SKILL.md` starts with YAML frontmatter:

```markdown
---
name: <skill-name>
description: <what the skill does and when to use it; this is what triggers it>
---
```

- `name`: 1 to 64 characters, lowercase letters, numbers and hyphens, and identical to the skill's folder name.
- `description`: at most 1024 characters. It decides when the skill gets triggered, so be specific about when to use it, and write it in that folder's language.
- **Tool-neutral content.** Write skills for "the agent", not for a specific tool. Don't mention Claude, Codex or Copilot, don't rely on one tool's invocation syntax (such as `/skill-name` arguments), and don't use tool-specific frontmatter fields. If a skill truly needs a specific tool, say so in the optional `compatibility` field.

## README

There are two READMEs: `README.md` (English) and `README.es.md` (Spanish). Whenever a skill is added, changed or removed, update **both** READMEs in the same change:

- Keep the table of contents current: each skill has an entry nested under "Skills".
- Keep the skills table current. For each skill, list what it's for and its stack ("Agnostic" or the specific language/technology).
- Under the table, give each skill its own section covering when to use it, how to invoke it (including example prompts), and other relevant details such as requirements, supporting files and limitations.
- Keep the installation table current with the skill paths for each supported tool.

## Pending work

`TODO.local.md` holds the project's pending work. It's git-ignored (`*.local.md`), so it stays local. Check it when deciding what to work on, and keep it updated.

## Conversation

The owner usually writes in Spanish. Reply in Spanish.

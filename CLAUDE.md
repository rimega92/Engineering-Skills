# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

A personal library of Claude Code skills, reused across many projects and published on GitHub. Skills are technology- and language-agnostic by default (frontend, backend, mobile, etc.). A skill is tied to a specific language or stack only when the owner explicitly says so.

Skills are built one at a time, and the owner chooses which one to work on next. Don't create skills nobody asked for.

## Structure

```
es/<skill-name>/SKILL.md   # Spanish version
en/<skill-name>/SKILL.md   # English version
```

- Every skill exists in **both** `es/` and `en/`, with the same folder name (kebab-case, in English) so the two versions map 1:1.
- When creating or changing a skill, update both language versions in the same change. They should match in content and structure. Translate the text, but keep code, commands and file names identical.
- A skill folder can hold supporting files beside `SKILL.md` (scripts, reference docs, templates). Mirror them in both languages. Translate the text files; don't duplicate scripts that contain no language-specific text unless they need translating.

## README

There are two READMEs: `README.md` (English) and `README.es.md` (Spanish). Whenever a skill is added, changed or removed, update **both** READMEs in the same change:
- Keep the table of contents current: each skill has an entry nested under "Skills".
- Keep the skills table current. For each skill, list what it's for and its stack ("Agnostic" or the specific language/technology).
- Under the table, give each skill its own section covering when to use it, how to invoke it (including example prompts and any arguments), and other relevant details such as requirements, supporting files and limitations.

## Skill format

Each `SKILL.md` starts with YAML frontmatter:

```markdown
---
name: <skill-name>
description: <what the skill does and when to use it; this is what triggers it>
---
```

The `description` decides when the skill gets triggered. Make it specific about when to use the skill, and write it in that folder's language.

## Conversation

The owner usually writes in Spanish. Reply in Spanish.

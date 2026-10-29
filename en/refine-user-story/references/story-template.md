# Refined story template

Structure of the file saved to `.stories/<story>.md`. The conversation shows the verdict, the functional part, the open questions and a summary of the technical notes; the file has everything. Write it in the language of the original story. Leave out sections with no content, except the refined story, the readiness table and the original story.

## Rules

- **Functional part** (section "Refined story"): plain language, for the whole team, without code paths or internal names. It must make sense pasted alone into the issue tracker.
- **Acceptance criteria:** in the Given / When / Then format, with the keywords in the language of the story (for example, in Spanish: Dado / Cuando / Entonces). One scenario per behavior, including alternatives and errors. Each one observable: what the user sees, what the system returns or stores.
- **Technical notes:** every item with a location (`path:line` or `path`) and the repository or component it belongs to.
- **Assumptions:** any decision nobody confirmed. A reader must be able to tell confirmed decisions from assumptions at a glance.
- Never copy the value of a secret.

## Template

````markdown
# <ID>: <title>

| | |
|---|---|
| **Version** | <1, 2, ...> |
| **Date** | <YYYY-MM-DD> |
| **Verdict** | <✅ Ready | ⚠️ Ready with assumptions | ❌ Not ready>: <reason in one sentence> |
| **Components** | <frontends, services and APIs involved> |
| **Analyzed code** | <repository or component>: `<short sha>` on `<branch>` <one line per repository> |
| **Not visible** | <components that couldn't be read, or "—"> |

## Refined story

**As** <role>, **I want** <action> **so that** <benefit>.

### Context

<Why this story exists and the current situation, in a few sentences.>

### Acceptance criteria

**Scenario 1: <name>**

- **Given** <initial state>
- **When** <action>
- **Then** <observable result>

**Scenario 2: <name>**

- ...

### Business rules

- <Rule, limit, calculation or validation.>

### Out of scope

- <What this story doesn't include, and where it goes if it's known (another story, a later phase).>

### Proposed split

<Only if the story is too big. One line per part: title and goal.>

## Technical notes

| Component | Location | What changes or what to check |
|---|---|---|
| <web-app> | `<path:line>` | <short description> |

- **Contracts:** <endpoints, events or schemas that change, and their known consumers.>
- **Data:** <new or changed data, existing records.>
- **Contradictions with the current code:** <what the story asks versus what the code does, with location, and how it was settled.>
- **To confirm:** <what couldn't be verified, and how to confirm it.>

## Readiness

| Area | Status | Note |
|---|---|---|
| Value and user | <✅ ⚠️ ❌ ➖> | <one line> |
| Scope and size | | |
| Acceptance criteria | | |
| Business rules and validations | | |
| Edge cases and errors | | |
| Data | | |
| Contracts and integrations | | |
| Design, texts and user experience | | |
| Permissions and security | | |
| Non-functional requirements | | |
| Dependencies and rollout | | |
| Testability | | |

## Decisions and assumptions

| Topic | Decision | Source |
|---|---|---|
| <Existing records> | <They keep their current value> | <Answer, round 1 | Assumption> |

## Open questions

| # | Question | For | Blocking | Proposed answer |
|---|---|---|---|---|
| Q1 | <question> | <Product | Design | Technical | Team X> | <Yes | No> | <answer> |

## Original story

<The text exactly as the user gave it, in this version.>

## History

| Version | Date | Changes |
|---|---|---|
| 1 | <YYYY-MM-DD> | First refinement. |
| 2 | <YYYY-MM-DD> | <What changed: new text, answers to Q1 and Q3, new verdict.> |

<details>
<summary>Original story, version 1</summary>

<The previous original text, when a new version replaced it.>

</details>
````

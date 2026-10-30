# Engineering Skills

🇬🇧 English · [🇪🇸 Español](README.es.md)

A collection of agent skills for [Claude Code](https://claude.com/claude-code), [OpenAI Codex](https://developers.openai.com/codex) and [GitHub Copilot](https://github.com/features/copilot) that you can reuse across projects. The skills follow the open [Agent Skills](https://agentskills.io/) format, so the same skill works in all three tools. Most skills don't depend on a particular technology or programming language, so they work for frontend, backend, mobile and other kinds of work. When a skill does target a specific language or stack, its entry below says so.

Every skill comes in two languages:

- [`en/`](en/): English
- [`es/`](es/): Spanish

Both versions of a skill have the same folder name and the same content.

- **Status:** active. New skills are added one at a time.
- **Maintainer:** Ricardo Mesa Gallego ([@rimega92](https://github.com/rimega92)).
- **Support:** for questions, ideas or bugs, open an [issue](https://github.com/rimega92/Engineering-Skills/issues).

## Contents

- [Skills](#skills)
  - [readme-docs](#readme-docs)
  - [review-changes](#review-changes)
  - [change-impact-analysis](#change-impact-analysis)
  - [refine-user-story](#refine-user-story)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [More information](#more-information)
- [License](#license)

## Skills

| Skill | What it's for | Stack |
| ----- | ------------- | ----- |
| [`readme-docs`](#readme-docs) | Create a project's README.md, or update it after code changes | Agnostic |
| [`review-changes`](#review-changes) | Review code changes before a commit or a pull request, with a prioritized report and recommendations | Agnostic |
| [`change-impact-analysis`](#change-impact-analysis) | Analyze what a planned change affects before implementing it, with an assessment, a count of what to modify and an effort estimate | Agnostic |
| [`refine-user-story`](#refine-user-story) | Check whether a user story is ready to implement, against the code it affects, and turn it into a refined story with testable acceptance criteria | Agnostic |

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

**Tested**

- Claude Code: tested on an iOS app project (Xcode) and on a Java microservice, where it produced complete documentation.
- GitHub Copilot: tested, with good results.
- OpenAI Codex: not tested yet.

### review-changes

Reviews code changes before a commit or a pull request to catch the problems that matter before they reach production: functional defects, regressions, security risks, data integrity issues, design and structural problems, and departures from the project's standards. It aims for relevant findings backed by evidence, not for the longest list. It writes a prioritized report with a recommendation for each finding, can apply the fixes you approve, and can re-review the branch to check them.

**When to use it**

- Before committing, to review what you haven't committed yet.
- Before opening a pull request, to review the whole branch.
- To review someone else's pull request.
- After fixing the findings, to check that they're fixed and that nothing new came up.

**How to use it**

- Ask for it: _"Review my changes"_, _"Review this branch before the PR"_, _"Review PR 42"_.
- To narrow the scope: _"Review only what I haven't committed"_, _"Review the last commit"_.
- To force a mode: _"Do a quick review"_, _"Do a deep review"_.
- After the report: _"Fix F1 and F3"_, _"Apply the P0 and P1 fixes"_.
- To check the fixes: _"Review again"_.

**How it works**

- By default it reviews everything that would go into the pull request: the branch's commits since it left its base branch, plus uncommitted changes. For pull requests it uses `gh` or `glab` if they're installed; otherwise it fetches the branch with `git`.
- First it discovers the project's standards (`README`, `AGENTS.md`, `CLAUDE.md`, scaffold, architecture rules, linters, contracts), so it judges the change against them and not against outside conventions. It applies SOLID, DDD and patterns only where they add value.
- The size and risk of the change decide how much it does, so a small fix before a commit stays fast:
  - **Quick** (small change, no sensitive area): basic checklist, fast checks (lint, format, types) and a short report.
  - **Standard** (larger change, or one that touches a sensitive area such as authentication, data, public contracts or configuration): it adds the checklist sections for the areas the change touches and the related tests.
  - **Deep** (critical systems, sensitive data, financial operations, security): all of the above plus threat and failure analysis, the full test suite and the build.
- The checklist has 12 areas, from design and architecture to deployment and the scope of the change. It reads only the sections for the areas the change touches.
- It runs the project's own validations, without anything that modifies files, installs dependencies or touches data, and asks first if they're slow or need external services. The report says what ran, what failed and what couldn't run.
- It checks each finding against seven questions before reporting it, to avoid false positives. Each one has a priority (🔴 P0, 🟠 P1, 🟡 P2, 🔵 P3 or 💡 Info, or the project's own scale), a type (confirmed defect or potential risk), an origin (introduced or pre-existing), and the conditions, impact, evidence and recommendation. P3 and Info findings take a single line. The review gets a verdict: ✅ Ready, ⚠️ Ready with changes or ❌ Needs work. It never claims the code is bug-free.
- It saves the report to `.reviews/<branch>/review-<n>.md` in the folder of the component the changes belong to (in a monorepo, the root of the microservice, app or package they modify, or the root of the repository if they touch several), one file per round (`review-1.md`, `review-2.md`, ...). The header records the date, the branch, the base and the reviewed commit. It keeps reports out of commits and pushes: the first time, it adds `.reviews/` to a `.gitignore` and reminds you to commit that change.
- It never changes code during the review. At the end it offers to apply the fixes, and applies only the ones you approve, without committing.
- A re-review reads the previous round's report, marks each earlier finding as fixed, partially fixed, still open or no longer applicable, and reviews the fixes and any new changes. It reuses the standards the previous round found instead of searching for them again.

**Files**

- `SKILL.md`: the workflow: scope, context, review mode, review, validations, verification, report, fixes and re-review.
- `references/checklist.md`: the priority scale, the verdicts, the depth levels used by each mode and what to look for in each of the 12 areas.
- `references/report-template.md`: the report's structure, its size in each mode, and the full and compact finding formats.

**Requirements and limitations**

- The project must use `git`.
- Reviewing a pull request by number works best with `gh` (GitHub) or `glab` (GitLab) installed and signed in.
- It can only run the validations the project already defines and the environment supports. What it couldn't run is listed in the report as not verified.

**Tested**

- Claude Code: tested on an iOS app project (Xcode, about 11,000 lines of Swift), reviewing the whole project in Deep mode. It ran the tests and the Release build, applied the project's own rules and reported relevant findings with evidence, without noise. Also tested on a Java microservice, with the same results.
- GitHub Copilot: tested, with good results.
- OpenAI Codex: not tested yet.

### change-impact-analysis

Analyzes a change before you write it: which modules, units, processes, contracts, data, tests, configuration and consumers it can affect, directly or indirectly. It explores the code, asks you the questions that decide what really needs to change, and gives you an assessment, a count of what to modify and an effort estimate. It never changes the code.

**When to use it**

- Before starting a feature, refactor, fix or upgrade, to know what it involves and how big it is.
- To compare a minimal version of a change with the full one.
- To prepare a ticket or a story: scope, risks, estimate and what to settle first.

**How to use it**

- Describe the change and ask: _"What would it take to add a currency field to orders?"_, _"Analyze the impact of moving payment notifications from REST to events"_, _"How hard is it to upgrade to Spring Boot 3?"_.
- To force a mode: _"Do a quick impact analysis"_, _"Do a deep impact analysis"_.
- After the analysis: _"Save the analysis"_, _"Go ahead and implement the minimal scope"_.

**How it works**

- It restates the change and separates the goal from the proposed solution. If a smaller change meets the goal, it says so.
- It explores the code to find where the change lands, and then asks you up to six questions in a single message, based on what it found (for example, which endpoints should expose a new field, or what happens to existing records). Each question comes with a proposed default; anything you don't answer becomes a visible assumption.
- The size and risk of the change decide how deep it goes:
  - **Quick** (local change, no contracts, data or sensitive areas): code and tests in depth, one line for each other dimension, few or no questions.
  - **Deep** (several modules, public contracts, data or migrations, sensitive areas, or high uncertainty): all ten dimensions in depth.
- The ten dimensions are code, processes and flows, contracts, data, tests, consumers, configuration and infrastructure, security, operations, and documentation. It also searches for uses the compiler can't see: names in strings, serialization, routes, SQL, configuration and scripts.
- Every affected item has a location (`path:line`), the kind of impact (direct or indirect) and the evidence that links it to the change. Consumers outside the repository (other services, old app versions, third parties) are listed as "to confirm", with how to confirm them.
- The result comes in the conversation, starting with a summary: size (XS to XL), an estimate as a range for a developer who knows the code, and three separate ratings for complexity, risk and confidence. Then it gives the impact by area, the count of files and tests to modify, create or delete, the estimate broken down by activity with what makes it grow, what to check before starting, risks, minimal versus full scope and a suggested implementation order.
- It only runs commands that change nothing (searches, `git log`). It doesn't run the tests: it describes them.
- If you ask, it saves the analysis to `.impact/<change>.md` in the folder of the project the change targets (in a monorepo, the root of the microservice, app or package it modifies, or the root of the repository if it touches several) and tells you the path, both relative to the repository and absolute. It keeps analyses out of commits and pushes: the first time, it adds `.impact/` to a `.gitignore` and reminds you to commit that change.

**Files**

- `SKILL.md`: the workflow: understand, explore, mode, questions, analysis, verification, delivery and saving.
- `references/impact-checklist.md`: how to search and what to look for in each of the ten dimensions.
- `references/estimation.md`: the complexity, risk and confidence scales, the sizes and how to build the estimate.
- `references/report-template.md`: the structure of the analysis and its size in each mode.

**Requirements and limitations**

- It only sees what's in the repository. Consumers and systems outside it are marked as "to confirm", which lowers the confidence.
- The estimate is a reasoned range, not a commitment, and it doesn't include waiting time, coordination, QA or deploy.
- Saving the analysis works best in a `git` repository; without git, the file goes in the project's root folder and isn't ignored automatically.

**Tested**

- Claude Code: tested on an iOS app project (Xcode) and on a Java project, with good results.
- GitHub Copilot: tested, with good results.
- OpenAI Codex: not tested yet.

### refine-user-story

Checks whether a user story is clear and complete enough to implement, comparing it with the code of the frontends, services and APIs it affects. It asks the questions that close the gaps and delivers the refined story: testable acceptance criteria, business rules, out of scope, technical notes, assumptions and open questions. It never changes the code and doesn't estimate effort.

**When to use it**

- Before a refinement session or sprint planning, to bring a story with its gaps and questions already found.
- When you pick up a story to implement, to check that you can build it without guessing.
- When the story changes or the open questions get answered, to update the refinement.

**How to use it**

- Share the story and ask: _"Refine this user story: …"_, _"Is PROJ-123 ready for development?"_, _"What's missing from this story?"_.
- If the story touches components in other repositories, give their local paths: _"The API is in ~/projects/orders-api"_.
- To update it: _"The PO changed the story, here's the new text: …"_, _"Answers to the open questions of PROJ-123: …"_.

**How it works**

- It restates the story (who, what and why) and separates the need from any solution the story imposes.
- It explores the code of each affected component to learn what exists today: screens, endpoints, models, validations, permissions, texts and data. It flags where the story contradicts the code (for example, a field the story makes optional but the API requires).
- It checks twelve areas, from value and scope to acceptance criteria, business rules, edge cases, data, contracts, design, permissions, non-functional requirements, dependencies and testability, and marks each one ✅ clear, ⚠️ ambiguous, ❌ missing or ➖ not applicable. If the story is too big, it proposes how to split it.
- It asks at most two rounds of questions: up to eight in the first and up to four in a second one, only if the answers raise new doubts. The questions are based on the code, grouped by who should answer them (product, design, technical, another team), marked as blocking or not, and each one comes with a proposed answer. Whatever stays unanswered becomes an assumption or an open question for you to take to the people who decide.
- It gives a verdict: ✅ Ready, ⚠️ Ready with assumptions or ❌ Not ready. In the conversation it shows the functional part of the refined story, ready to paste into your issue tracker, plus the open questions and a summary of the technical notes.
- It always saves the result to `.stories/<ID>-<title>.md` in the folder of the project the story targets (in a monorepo, the root of the component it affects, or the root of the repository if it affects several) and tells you the path, both relative to the repository and absolute. The file also keeps the original text and a version history. It keeps stories out of commits and pushes: the first time, it adds `.stories/` to a `.gitignore` and reminds you to commit that change.
- When you bring a new version of the story or answers to its open questions, it updates the same file: it compares the texts, keeps the decisions that still hold, asks only what's new and bumps the version.
- If the project has its own story template or Definition of Ready, it uses that as the base.
- At the end it offers to analyze the story's impact and effort with `change-impact-analysis`, if it's installed.

**Files**

- `SKILL.md`: the workflow: read, explore, diagnose, ask, write, save and update.
- `references/readiness-checklist.md`: what to check in the story and in the code for each of the twelve areas, with typical questions.
- `references/story-template.md`: the structure of the refined story and of the saved file.

**Requirements and limitations**

- It only sees the code you can give it access to. Components in repositories it can't read are marked as "to confirm".
- Business decisions belong to the people who own the story: its proposed answers are assumptions until someone confirms them.
- Saving works best in a `git` repository; without git, the file goes in the project's root folder and isn't ignored automatically.

**Tested**

- Not tested yet in Claude Code, OpenAI Codex or GitHub Copilot.

## Repository structure

A skill is plain Markdown: a `SKILL.md` file with YAML frontmatter (`name` and `description`), following the [Agent Skills](https://agentskills.io/) format, plus optional supporting files. There's no code to build, no dependencies to install and no configuration or environment variables.

```text
Engineering-Skills/
├── en/                    # English versions of the skills
│   └── <skill-name>/
│       ├── SKILL.md       # Instructions the agent follows, with frontmatter
│       └── references/    # Supporting files the skill reads when needed
├── es/                    # Spanish versions, same folders as en/
├── AGENTS.md              # Repository conventions for AI agents
├── CLAUDE.md              # Imports AGENTS.md for Claude Code
├── LICENSE
├── README.md              # This file
└── README.es.md           # Spanish README
```

There are no automated tests. Each skill is tested by hand in the tools (see the **Tested** list in each skill's section).

## Installation

A skill is a folder that contains a `SKILL.md` file. To install one, copy its folder from the language you want into your tool's skills folder:

| Tool | One project | Every project (personal) |
| ---- | ----------- | ------------------------ |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

You need `git` and at least one of the tools in the table.

First, clone the repository:

```bash
git clone https://github.com/rimega92/Engineering-Skills.git
```

Then copy the skill for your tool.

### Install in Claude Code

```bash
# Personal install
cp -r Engineering-Skills/en/<skill-name> ~/.claude/skills/

# Single-project install
cp -r Engineering-Skills/en/<skill-name> /path/to/project/.claude/skills/
```

### Install in OpenAI Codex

```bash
# Personal install
cp -r Engineering-Skills/en/<skill-name> ~/.codex/skills/

# Single-project install
cp -r Engineering-Skills/en/<skill-name> /path/to/project/.agents/skills/
```

### Install in GitHub Copilot

```bash
# Personal install
cp -r Engineering-Skills/en/<skill-name> ~/.copilot/skills/

# Single-project install
cp -r Engineering-Skills/en/<skill-name> /path/to/project/.github/skills/
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

- **New skill:** open an [issue](https://github.com/rimega92/Engineering-Skills/issues) first describing what it's for, so we can agree on it before you put work into it.
- **Fix or improvement:** you can open the pull request directly. For bigger changes, an issue first is still a good idea.

### Workflow

1. Fork the repository on GitHub (you don't have write access to the original, so your changes go to your copy).
2. Clone your fork and add the original repository as `upstream`:

   ```bash
   git clone https://github.com/<your-user>/Engineering-Skills.git
   cd Engineering-Skills
   git remote add upstream https://github.com/rimega92/Engineering-Skills.git
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

## More information

- [Agent Skills](https://agentskills.io/): the open format these skills follow.
- [`AGENTS.md`](AGENTS.md): the repository's conventions for skills, languages and READMEs.

## License

Released under the [MIT License](LICENSE). You can use, copy, modify and share the skills, including in commercial projects, as long as you keep the copyright notice.

<!-- readme-docs:sync commit=22b20d0 date=2026-10-29 -->

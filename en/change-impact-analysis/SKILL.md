---
name: change-impact-analysis
description: Analyzes the impact of a planned code change before it's implemented, to find which modules, units, processes, contracts, data, tests, configuration and consumers it can affect, directly or indirectly. It explores the code, asks questions to pin down what really needs to change, and delivers in the conversation an assessment of complexity, risk and confidence, a count of the files and tests to modify or create, an effort estimate with a size and a range, what to check before starting, a minimal scope versus the full one and a suggested implementation order. It doesn't modify code. It can save the analysis to a file in the project, kept out of git. Use it when the user describes a change, feature, refactor or fix they plan to make and asks what it involves, what it affects, how hard it is, how long it will take or how to approach it.
---

# change-impact-analysis

Analyzes a change before it's written: what it touches, what can break, how big it is and what to settle before starting. Works with any language, framework and architecture. The result is an impact analysis in the conversation, with evidence from the code, an assessment and an effort estimate.

The goal isn't the longest list of files, but a reliable picture of the change: what really has to change, what has to be checked, and how sure the analysis is.

The flow has five steps:

1. **Understand** the request.
2. **Explore** the code to find where the change lands.
3. **Ask** the questions that decide the scope.
4. **Analyze** the impact in depth, with the answers.
5. **Deliver** the analysis in the conversation and, if the user wants it, save it to a file.

## Principles

- **Read only.** The analysis never modifies code, data or configuration. It only reads, searches and runs commands that change nothing.
- **Evidence from the code.** Every affected item points to a location (`path:line`) and says why it's affected. Don't list a file because its name sounds related.
- **Direct and indirect.** Separate what the change edits from what is affected through it: callers, implementations, serialization, consumers.
- **Visible and not visible.** The repository doesn't show everything. Consumers in other repositories, other teams, old app versions, reports or third parties are listed as "to confirm", never left out or presented as certain.
- **The goal before the solution.** Separate what the user wants to achieve from the solution they propose. If a smaller change meets the goal, say so.
- **Don't invent requirements.** Ask when a decision belongs to the user. If they don't answer, use the default you proposed and mark it as an assumption.
- **Honest estimates.** Give ranges, not exact figures, and say what makes them grow. Never hide uncertainty to make the estimate look precise.
- **Don't inflate.** A change isn't risky just because it's large, and a dimension with no impact gets one line, not a section.
- **Never secrets.** If you find a credential or token, mention its location without copying its value.
- **The user's language.** Write the analysis in the language the user is writing in.

## 1. Understand the request

1. **Restate the change in one sentence**, the way you understood it.
2. **Separate the goal from the solution.** For example: goal "show prices in the customer's currency"; proposed solution "add a `currency` field to `Order`".
3. **Identify the type of change:** new feature, change of behavior, refactor, bug fix, dependency or platform upgrade, data change, contract change. The type guides where to look first.
4. If the request is too vague to search the code (for example, "improve orders"), ask what the user wants to achieve before exploring.

## 2. Explore the code

A quick, targeted pass to find where the change lands, not the full analysis yet:

1. **Read the project's context:** `README`, agent instruction files (`AGENTS.md`, `CLAUDE.md` and similar), architecture documentation and the directory structure.
2. **Find the entry points:** the units (classes, modules, components, functions), models, endpoints, events, tables and configuration that the change names or implies. Search by identifiers, routes, event names, table and column names, and texts shown to users.
3. **Follow the first level of dependencies:** who uses those entry points and what they depend on.
4. **Choose the mode** (step 3 below explains when).

## 3. Choose the mode

| Mode | When | Dimensions | Questions | Result |
|---|---|---|---|---|
| **Quick** | Local change: one module, a few files, no contract, data or sensitive area involved | Code and Tests in depth; one line for each of the others, saying whether it applies | 0 to 2 | Short: summary, decisions, impact, count, estimate, before you start |
| **Deep** | Several modules, a public contract, data or migrations, a sensitive area, or high uncertainty | All, in depth | 3 to 6 | Full |

**Sensitive areas:** authentication and authorization, secrets and cryptography, personal or financial data, persistence and migrations, public API or event contracts, concurrency, configuration and infrastructure. A change that touches any of them is Deep.

Rules:

- The user can force a mode ("quick analysis", "deep analysis"). Respect it, but if a quick analysis finds a sensitive area, say so and suggest the Deep one.
- If the change turns out bigger than it looked, move to Deep and say so.

## 4. Ask

Ask **once, in a single message**, the questions whose answer changes the scope, the effort or the risk. Base them on what you found in the code, not on generic templates. For example: "`Order` is serialized in 3 public endpoints and in the `OrderCreated` event; should the new field appear in all of them, or only in the internal endpoint?".

For each question:

- Say why it matters (what changes depending on the answer).
- Propose a default answer, the one you'd choose.

Typical topics, only when they apply:

- **Scope:** which screens, endpoints, consumers or kinds of users the change covers.
- **Existing data:** what happens to records created before the change (default value, backfill, leave them as they are).
- **Compatibility:** whether current consumers must keep working without changes, or a breaking version is acceptable.
- **Rollout:** all at once, behind a feature flag, or gradually.
- **Minimal version:** whether a smaller change is enough for now (propose it if you see one).
- **Non-functional requirements:** volume, performance, security or compliance requirements that change the solution.

In Quick mode, if nothing is ambiguous, skip the questions and state your assumptions in the result. If the user answers only some questions, use your defaults for the rest and mark them as assumptions.

## 5. Analyze

With the answers, go through the dimensions in `references/impact-checklist.md` according to the mode. For each affected item, record:

- **Location:** `path:line` or `path`.
- **What changes**, briefly.
- **Kind of impact:** direct (it's edited) or indirect (it's affected through something else).
- **Evidence:** the call, import, serialization, query, configuration or contract that links it to the change.
- **Visibility:** confirmed in the code, or to confirm (outside the repository or not verifiable).

Then:

1. **Count** the files and units to modify, create and delete, separating production code, tests, migrations and scripts, configuration and infrastructure, and documentation.
2. **Assess** complexity, risk and confidence, and **estimate** the effort, with `references/estimation.md`.
3. **Define the scope:** the minimal change that meets the goal and the full one, if they differ, with what each includes and its estimate.
4. **List what to check before starting:** decisions pending, coordination with other teams or consumers, data to inspect, tests missing in the area that should be written first.
5. **Propose an implementation order**, in steps that can be merged and, when possible, deployed separately (for example: compatible migration, then code that writes the new field, then consumers, then cleanup).

You can run commands that change nothing to back the analysis: searches, `git log` to see how often an area changes, test listings, dependency trees. Don't run anything that modifies files, installs dependencies or touches data, and don't run the test suite: the analysis describes the tests, it doesn't run them.

## 6. Verify

Before delivering, check that:

1. Every affected item has evidence. Drop the ones without it, or move them to "to confirm" and say what would confirm them.
2. Indirect impacts follow a real chain (A calls B, B serializes C), not just a similar name.
3. You searched for uses the compiler can't see: strings, reflection, configuration files, templates, SQL, serialized names, routes, scripts.
4. The count matches the listed items.
5. The estimate and the assessment are consistent with the impact found, and the confidence reflects what couldn't be verified.

## 7. Deliver

Write the analysis in the conversation with the structure in `references/report-template.md` (short version in Quick mode, full in Deep). Start with the summary: size, estimate, complexity, risk and confidence, so the user gets the answer at a glance.

At the end, offer the next steps:

- **Save the analysis** to a file (see below).
- **Implement the change**, following the suggested order. Don't start without the user's approval.
- After implementing, review the changes (for example, with the `review-changes` skill, if it's installed).

## 8. Save the analysis (if the user wants it)

**Location:** `.impact/<change>.md` in the folder of the project the change targets:

- **Single-project repository:** the root of the repository.
- **Monorepo:** the folder of the microservice, app or package the change modifies (for example, `services/orders/.impact/`), not the root of the repository. If the change spans several of them, use the folder of the main one and mention the others in the analysis; if none is clearly the main one, ask.
- **Without git:** the project's root folder.

From here on, `<folder>` is that folder.

- `<change>` is a short kebab-case name for the change, in English (`add-order-currency`).
- If a file with that name already exists (an earlier analysis of the same change), ask whether to replace it or create `<change>-2.md`.
- The file's header records the date and the analyzed commit.

**Keep analyses out of git.** They're personal working files and must never be committed or pushed. Before writing the file:

1. Check whether the folder is ignored: `git check-ignore -q <folder>/.impact/`.
2. If it isn't, add `.impact/` to a `.gitignore`: the one in `<folder>` if it has one, otherwise the one at the root of the repository (create it if it doesn't exist). Put it on its own line with a comment: `# Change impact analyses (change-impact-analysis)` followed by `.impact/`. In the root `.gitignore`, the pattern has no leading `/`, so it also covers the `.impact/` folders of the other services in a monorepo. Don't change anything else in the file.
3. Tell the user which `.gitignore` changed and that they need to commit it. Don't commit it yourself.
4. If `.impact/` was already committed (`git ls-files <folder>/.impact` lists files), ignoring it isn't enough: warn the user and suggest `git rm -r --cached <folder>/.impact` to stop tracking it without deleting the files.

**Tell the user where the file is.** When it's written, give its path relative to the root of the repository and its absolute path, for example: "The analysis is in `services/orders/.impact/add-order-currency.md` (`/home/user/projects/shop/services/orders/.impact/add-order-currency.md`)".

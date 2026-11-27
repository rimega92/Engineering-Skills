# Classifying the contribution

How to classify each commit and file, what counts as one's own work depending on the role, and which quality problems to look for.

## Commit classes

Give each commit a main class. If a commit mixes classes, state the main one and break down the lines, for example: "🟥 Copy (2,100 lines) + 🟩 Own code (40 lines)".

| Class | What it is | How to recognize it |
|---|---|---|
| 🟥 **Template or generated** | Files created by a tool: scaffold, `init`, generators, wrappers, lockfiles, generated code | Template markers (`TODO`, `sample`, `my-operation`, `Change this`), empty classes, a structure identical to what the tool produces, category `boilerplate` or `test_assets` |
| 🟥 **Copy** | Content that already existed in the repository, written by other people, duplicated elsewhere | Copy percentage ≥ 80% in `summary.md`, confirmed with `git diff -w` against the source |
| 🟧 **Adaptation** | A copy with real changes: names, values or logic adjusted to the new case | Copy between 50% and 80%, and the diff shows meaningful changes, not just renames |
| 🟧 **Configuration tweak** | Small changes to versions, properties, paths, flags, manifests | 1 to ~20 lines in `config`, `build` or `deploy_ci` files, with no new logic |
| 🟦 **Own infrastructure** | Deployment, CI, build or platform work that is new to the repository and solves a real problem | Copy < 50%, more than a version bump: pipelines, infrastructure modules, deployment scripts with logic |
| 🟩 **Own code** | New logic, written by the person, that works | Copy < 50% in production or test code, no defects found |
| 🟨 **Own code with problems** | New logic with defects | Same as above, with at least one problem from the quality list |
| ⬛ **Junk or accidental** | Files that should never have been committed | Category `junk`: logs, compiled binaries, `.env`, build folders, local IDE settings |
| ⬜ **No content** | Renames, moves, empty merges | 0 lines added and deleted, or renames only |

Rules:

- **A copy isn't one's own work, even when it's useful.** Creating a microservice by copying another may be exactly what was asked, but in the report those lines count as a copy, not as written code. Acknowledge the task ("set up the service structure") without counting it as development.
- **A template isn't a copy of a teammate's work.** If both files come from the same tool, say "generated from a template", not "copied from John".
- **You don't know who copied whom** when two nearly identical files appear a few days apart, or when the similarity is with a later file. Say they share a source.
- **Changes repeated across several modules** (the same line in three services) count once as work and are noted as replication.

## What counts as one's own work by role

| Role | Counts as main own work | Counts as support |
|---|---|---|
| Developer (backend, frontend, mobile, fullstack) | 🟩 and 🟨 in production and test code | 🟦 and 🟧 |
| DevOps or platform | 🟦 (deployment, CI, build, infrastructure) and scripts | 🟧 and production code |
| QA or automation | New test code, test data and test scenarios (< 50% copy) | Production code and configuration |
| Tech lead | Own code, plus PR reviews, design and technical decisions (outside git: query them in step 4) | Configuration |
| Intern or junior | Same as developer; the report may comment on what the level is expected to deliver, but the figures don't change | Same as developer |

The script applies this table with `--role`. It flags a file as **own** when it's in the role's main categories, has less than 50% copy and isn't template-like, and as a **template** when it has template markers or is small and has only empty types. It measures everyone on the team the same way. These are rules, not a reading of the code: confirm them with the diff and correct them in the analysis when they're wrong.

## Quality problems to look for

Review their own code (🟩, 🟨, 🟦) against this list. Every problem you find goes into the report with the commit, the path and, where it applies, the line.

**Bugs**

- Hard-coded values where a parameter or configuration should be used, especially timeouts, URLs, credentials or limits.
- Wrong units (seconds vs. milliseconds, bytes vs. KB).
- Injected or received parameters that are never used.
- Error handling that swallows the exception, returns empty or loses information.
- Unimplemented template logic that reaches the main branch (`return Mono.empty()`, `pass`, `TODO`).
- Changes to other people's code that break or remove their functionality without coordination.

**Security and data**

- Secrets, tokens or passwords in code or configuration. Report only the location, never the value.
- Files that shouldn't be in git: logs, `.env`, certificates, binaries, build folders.

**Maintainability**

- Commented-out code instead of deleted code.
- Duplicated or contradictory configuration (the same dependency forced to two different versions).
- Copied modules or dependencies the component doesn't need.
- Models or classes with fields that don't belong to the case (copied from another context).

**Tests**

- Tests that don't verify behavior: they only check that something doesn't throw, or that a template returns empty.
- New logic without any test.

**Way of working**

- Trial and error on the main branch: several commits or PRs on the same day for the same line.
- Commits that fix the same person's previous commit.
- Very large commits with messages that don't describe the content.
- Commit messages that don't say what changed or why.

## Fate of the code

For each important part of their own code, note what happened next:

| Fate | What it means |
|---|---|
| **Present** | Still on the analyzed branch, with most of its lines |
| **Modified by others** | Still there, but other people changed a significant part |
| **Rewritten by others** | The file exists, but almost all its lines now belong to other people |
| **Deleted** | The file no longer exists. Note who deleted it, when, and the reason the commit gives |

Read the commits of whoever modified or deleted their code. Separate replacements due to defects from replacements due to a requirements change or a general refactor.

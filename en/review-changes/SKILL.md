---
name: review-changes
description: Reviews code changes before a commit or a pull request (uncommitted changes, a branch's commits or an open pull request) for defects, regressions, security risks, design and structural problems and departures from the project's standards, and writes a prioritized report with evidence and a recommendation for each finding. It runs the project's tests and linters when available, can apply the fixes the user approves, and can re-review the changes later to check the fixes and catch anything new. Use it when the user asks to review their changes, review code before committing or opening a pull request, review a pull request, or check whether earlier review findings were fixed.
---

# review-changes

Reviews code changes to catch the problems that matter before they reach production: functional defects, regressions, security risks, data integrity issues, design and structural problems and departures from the project's standards. Works with any language, framework and architecture. The result is a prioritized report saved in the project, with evidence and a recommendation for each finding.

The goal isn't to find as many remarks as possible, but to find the relevant problems, with enough evidence and actionable recommendations, and without false positives or noise.

The flow has three steps:

1. **Review:** analyze the changes, run the available validations and write the report. The size and risk of the change decide how much it does: a quick review for small changes, a deeper one for large or sensitive ones.
2. **Fix (optional):** apply the fixes the user approves.
3. **Re-review:** run again on the same branch to check what was fixed and whether anything new appeared.

## Principles

- **The change first, then its context.** Judge the lines that changed, then the related code, consumers and integrations they affect. Don't turn the review into an audit of the whole repository.
- **The project's standards, not yours.** Find out the project's conventions before judging compliance. Don't impose outside conventions that contradict them without a solid reason.
- **Real defects over preferences.** Prioritize functional problems, vulnerabilities, data corruption, regressions and architectural violations with concrete consequences. Style preferences aren't defects.
- **Principles in context.** Apply SOLID, DDD, design patterns and similar principles only where they add value. Don't demand layers, interfaces or abstractions the code doesn't need.
- **Don't invent requirements.** Base every finding on code, contracts, requirements, documentation or verifiable behavior. Code isn't wrong just because it could be written another way. When context is missing, say what information you need.
- **Facts, risks and suggestions are different things.** Separate confirmed defects from potential risks and from optional improvements. Never present an assumption as a fact.
- **Introduced or pre-existing.** Distinguish problems the change introduces from ones that were already there. Report pre-existing problems only when they matter for the change, and label them.
- **Honest about validation.** Never claim a test, linter or analysis ran if it didn't, and never declare the code bug-free. State what was reviewed and the limits of the review.
- **Don't touch the code without approval.** The review only reads and reports. Fixes are applied only to the findings the user approves.
- **Never secrets.** If the changes contain a credential or token, report its location without copying its value.
- **The user's language.** Write the report in the language the user is writing in.

## 1. Choose what to review

The default scope is **everything that would go into the pull request**: the branch's commits since it diverged from its base, plus uncommitted changes (staged, unstaged and new untracked files).

The user can narrow it:

| The user asks for | Scope |
|---|---|
| "Review my changes" / no detail | Branch commits against the base + uncommitted changes |
| "Review what I haven't committed" | Only uncommitted changes: `git diff HEAD` plus untracked files |
| "Review this branch" / "before the PR" | Branch commits against the base, plus uncommitted changes if there are any |
| "Review PR 42" / a pull request URL | The pull request's changes against its base branch |
| "Review the last commit" / a commit range | That commit or range |

**Find the base branch.** For a pull request, use its base branch. Otherwise use the repository's default branch (`git symbolic-ref refs/remotes/origin/HEAD`, or `main` / `master` if that fails). Compare against the merge base (`git merge-base <base> HEAD`), not against the tip of the base branch. If the base is ambiguous, ask.

**Pull requests.** If the platform's CLI is installed and authenticated (`gh` for GitHub, `glab` for GitLab), use it to get the pull request's base, title, description, linked issues and diff. If not, fetch the pull request's branch (`git fetch origin pull/<n>/head:<local-branch>` on GitHub) and compare it against its base. Don't switch the user's working tree to another branch if it has uncommitted changes; read files from the fetched ref (`git show <ref>:<path>`) instead.

**Nothing to review.** If the scope has no changes, say so and ask what to review.

## 2. Gather context

Before judging anything:

1. **List the changed files** with their status (added, modified, deleted, renamed) and the size of the change. With that list, choose the review mode (step 3) before going on: it decides how much of the rest of this step you need.
2. **Understand the intent and the requirements.** Read the commit messages and, for a pull request, its title, description and linked issues or acceptance criteria. If the intent isn't clear, infer it from the changes and state your assumption in the report.
3. **Discover the project's standards.** Look for, when they exist (don't assume they do):
   - `README`, technical documentation and architecture decision records.
   - Agent instruction files: `AGENTS.md`, `CLAUDE.md` and similar.
   - The scaffold: directory structure, modules and packages, and where each kind of code lives.
   - Architecture and dependency rules: layers, module boundaries, allowed dependencies.
   - Naming and style conventions; linter, formatter and static analysis configuration.
   - Testing standards and coverage thresholds.
   - API and event contracts (OpenAPI, schemas, `.proto` files).
   - Security and data handling policies.
   - Build, CI/CD and deployment configuration.
   - The project's own severity or priority scale, if it has one.
4. **Read the changed files in full**, not just the diff, plus the consumers and dependencies of the changed parts that the change can affect.
5. **Ignore generated and vendored files** (lock files, build output, generated code, minified files, third-party code), but check that the change doesn't add build artifacts, binaries or temporary files by accident.

## 3. Choose the review mode

The size and the risk of the change decide how much work the review does. Choose the mode after listing the changed files, and before reading anything else:

| Mode | When | Checklist | Validations | Report |
|---|---|---|---|---|
| **Quick** | Small change (a few files, roughly under 100 changed lines) that touches no sensitive area | Level 1 only | Fast ones: lint, format check, type check | Short: header, summary, findings, validations |
| **Standard** | Medium or large change, or a small one that touches a sensitive area | Level 1 + Level 2 in the areas the change touches | Fast ones + the tests related to the change | Full |
| **Deep** | Changes to critical systems, sensitive data, financial operations, security or high-availability components | Levels 1, 2 and 3 | Fast ones + the full test suite and the build (ask first if slow) | Full |

**Sensitive areas:** authentication and authorization, secrets and cryptography, personal or financial data, persistence and migrations, public API or event contracts, concurrency, configuration and infrastructure. A change that touches any of them is at least Standard.

Rules:

- The user can force a mode ("quick review", "deep review"). Respect it, but if a quick review finds a sensitive area, say so and suggest a Standard one.
- If, while reviewing, the change turns out riskier than it looked, move up a mode and say so in the report.
- If the change is very large, review the highest-risk files in depth and list in the report what got a lighter review.
- The mode also limits the context you gather: in Quick mode, read only the agent instruction files (`AGENTS.md`, `CLAUDE.md`), the linter configuration and the code around the change; skip the rest of the standards search in step 2.

## 4. Review

Go through the changes with `references/checklist.md`, according to the mode:

- **Level 1** (every mode) is a short list at the top of the checklist. Go through all of it.
- **Level 2** (Standard and Deep): read only the checklist sections for the areas the change touches. A change with no database code doesn't need the persistence section. Within a section, apply only the items relevant to the change; don't go through them one by one looking for something to report.
- **Level 3** (Deep only): the extra points listed in the checklist for critical changes.

For each finding, record:

- **Priority:** with the scale in the checklist (P0 to P3, or Info), based on impact, reach, likelihood and existing safeguards. If the project has its own scale, use it instead.
- **Type:** confirmed defect, potential risk or suggestion.
- **Origin:** introduced by the change or pre-existing.
- **Location, problem, conditions, impact, evidence and recommendation**, as described in `references/report-template.md`.

Also note briefly what's done well. It tells the author what to keep doing.

## 5. Run the available validations

Run the checks the project already defines, to back the review with real results. Use the project's own commands (`package.json` scripts, `Makefile`, Gradle or Maven tasks, CI configuration, and so on), and run only what the mode calls for (see the table in step 3):

- **Fast checks**, in every mode: linters, format checks (in check mode) and type checks. Limit them to the changed files when the tool allows it.
- **Related tests**, from Standard mode on: the tests of the changed modules, if the project's tools can run them separately. If they can't, the full suite counts as a slow check.
- **Full suite and build**, in Deep mode.

Limits:

- Don't run anything that modifies files (formatters in write mode, `--fix`), installs dependencies, migrates or alters data, deploys, or needs credentials or production services.
- If the tests are slow, need external services (databases, containers) or you aren't sure a command is safe, ask before running it.
- If a validation fails because of the environment (missing tool, service down), say so and don't report it as a code defect.
- Record what ran and its result, what failed and what couldn't run, and why.

## 6. Verify the findings

Before writing the report, check each finding against these questions:

1. Is there a concrete problem?
2. Can you explain when it happens?
3. Is the impact relevant?
4. Is there enough evidence?
5. Does it belong to the change, or to an effect of the change?
6. Does the recommendation fix the problem without adding unnecessary complexity, and does it fit the project's conventions?
7. Is it already covered by another finding? Merge findings that share a root cause.

If you can't answer them with enough confidence, don't present the finding as a confirmed defect: report it as a potential risk and say what would confirm it, or drop it. Check that the priority isn't inflated: breaking a design principle doesn't make a finding critical on its own.

## 7. Write the report

Use `references/report-template.md`. In Quick mode, write the short report the template describes. In every mode, P0, P1 and P2 findings use the full format, and P3 and Info findings the compact one-line format.

**Location:** `.reviews/<branch>/review-<n>.md`, in this folder:

- **Single-project repository:** the root of the repository.
- **Monorepo, changes in one component:** the root folder of that microservice, app or package (for example, `services/orders/.reviews/`).
- **Monorepo, changes in several components:** the root of the repository. List the components the changes touch in the report's header.
- **Later rounds** stay in the folder of the first round, even if the components the changes touch are different now.

From here on, `<folder>` is that folder.

- `<branch>` is the branch name with `/` replaced by `-` (`feat/login` → `feat-login`). For a pull request reviewed without its branch checked out, use `pr-<number>`. With a detached HEAD, use `commit-<short sha>`.
- `<n>` is the next round number: `1` for the first review of that branch, `2` for the next one, and so on.
- The report's header records the date, the branch, the base, the reviewed commit and whether uncommitted changes were included.

**Keep reports out of git.** Reports are personal working files and must never be committed or pushed. Before writing the report:

1. Check whether the folder is ignored: `git check-ignore -q <folder>/.reviews/`.
2. If it isn't, add `.reviews/` to a `.gitignore`: the one in `<folder>` if it has one, otherwise the one at the root of the repository (create it if it doesn't exist). Put it on its own line with a comment: `# Code review reports (review-changes)` followed by `.reviews/`. In the root `.gitignore`, the pattern has no leading `/`, so it also covers the `.reviews/` folders of the other components in a monorepo. Don't change anything else in the file.
3. Tell the user which `.gitignore` changed and that they need to commit it. Don't commit it yourself.
4. If `.reviews/` was already committed (`git ls-files <folder>/.reviews` lists files), ignoring it isn't enough: warn the user and suggest `git rm -r --cached <folder>/.reviews` to stop tracking it without deleting the reports.

In later reviews, don't report that `.gitignore` line as a finding or count it as part of the change.

**Finding IDs.** Number the findings `F1`, `F2`, ... in order of priority. IDs restart in each round; later rounds refer to earlier findings with the round number in front (`R1-F3` is finding F3 of round 1).

If there are no relevant defects, say so explicitly, without claiming the code is bug-free.

When the report is written, give the user a short summary in the conversation: the mode, the verdict, the number of findings per priority, the most important ones, the validations that ran and the path to the report, relative to the root of the repository. Don't paste the whole report.

## 8. Fix (with approval)

After the summary, offer to apply the fixes. Ask which ones: all, by priority (for example, "P0 and P1") or by ID ("F1, F3 and F4"). If the user doesn't want any, stop here.

When the user approves:

- Apply only the approved findings, following the recommendation in the report. If a fix turns out to need a different approach, explain it before applying it.
- Don't refactor or change anything else along the way.
- Run the relevant validations again, with the same limits as in step 5.
- Don't commit. The user decides when to commit.
- When you finish, list what you changed per finding and suggest running a re-review.

## 9. Re-review

When the user asks to review again (for example, "review again", "check whether it's fixed"), and there's already a report for the branch:

1. **Read the previous report** (`review-<n-1>.md`, in the same `<folder>/.reviews/<branch>/` as the earlier rounds): its findings, the commit it reviewed, its mode and the standards it consulted.
2. **Review the same scope again** as in step 1, with the current state of the code, and run the validations again. Reuse the standards listed in the previous report instead of searching for them again; look again only at the ones that changed since that commit. Choose the mode again for the current change: it can go up or down.
3. **Check each previous finding** and mark it:
   - ✅ **Fixed:** the problem is gone and the fix introduces no new problem.
   - 🔄 **Partially fixed:** it improved but something remains. Say what.
   - ❌ **Still open:** unchanged.
   - ➖ **No longer applies:** the code was removed or rewritten, so the finding doesn't apply anymore.
4. **Review what's new:** the changes since the previous round's commit, and the fixes themselves. Report new findings with new IDs; mark the ones that come from a fix.
5. **Write `review-<n>.md`** with the "Previous findings" section filled in, and summarize the progress to the user (for example, "4 of 6 fixed, 1 new P3").

The fix and re-review cycle can be repeated as many times as needed. Earlier reports are never edited; each round is a new file.

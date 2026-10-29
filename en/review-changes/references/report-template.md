# Report template

Structure of the report saved to `.reviews/<branch>/review-<n>.md`. It should be short, prioritized and focused on decisions. Write it in the user's language. Leave out sections with no content, except the header, the summary, the findings and the validations.

## Report size by mode

- **Quick:** header, summary, findings and validations. Leave out the other sections; mention anything important that wasn't verified in the summary.
- **Standard and Deep:** every section with content.

## Finding formats

- **Full format** for P0, P1 and P2: ID, priority, type, origin, location as `path:line` (or `path:start-end`), problem, conditions, impact, evidence and recommendation. See F1 in the template.
- **Compact format** for P3 and Info: one line with the ID, priority, location, problem and recommendation. For example: F7 · 🔵 P3 · `src/orders/service.ts:88` · `calc` doesn't say what it calculates → rename it to `calculateShippingCost`.

## Rules

- Order the findings by priority, highest first, and within the same priority by file.
- Evidence is what backs the finding: the relevant code, the execution flow, the contract or the observed behavior. Keep snippets short: just the relevant lines.
- Show proposed code only when it makes the recommendation clearer.
- One finding per root cause. Group repeated minor issues (for example, the same naming problem in five places) into a single finding with all the locations.
- Info items are optional improvements. Don't make them blocking without a concrete reason.
- Never copy the value of a secret into the report.
- If there are no relevant defects, say so explicitly, without claiming the code is bug-free.

## Template

````markdown
# Code review: <branch> · round <n>

| | |
|---|---|
| **Date** | <YYYY-MM-DD HH:MM> |
| **Branch** | `<branch>` → `<base branch>` |
| **Reviewed commit** | `<short sha>` <+ uncommitted changes, if included> |
| **Range** | `<merge base short sha>..<short sha>` (<n> commits) |
| **Pull request** | <#number and title, if any> |
| **Files** | <n> reviewed (<+added> / <-removed> lines) |
| **Mode** | <Quick | Standard: areas reviewed in depth | Deep: why> |
| **Standards consulted** | <files and rules used, for example `AGENTS.md`, `.eslintrc`, `docs/architecture.md`> |
| **Previous round** | <`review-<n-1>.md`, or "None"> |

## Summary

**Verdict:** <✅ Ready | ⚠️ Ready with changes | ❌ Needs work>

<What was reviewed and what kind of change it is (the intent), the overall result, the main risks found and the relevant limits of the review. Three to five sentences.>

| 🔴 P0 | 🟠 P1 | 🟡 P2 | 🔵 P3 | 💡 Info |
|---|---|---|---|---|
| <n> | <n> | <n> | <n> | <n> |

## Previous findings

<Only from round 2 on.>

| ID | Finding | Status | Notes |
|---|---|---|---|
| R<n-1>-F1 | <short title> | ✅ Fixed | |
| R<n-1>-F2 | <short title> | 🔄 Partially fixed | <what remains> |
| R<n-1>-F3 | <short title> | ❌ Still open | See F1 in this round |
| R<n-1>-F4 | <short title> | ➖ No longer applies | <why> |

## Findings

### F1 · 🔴 P0 · <short title>

| | |
|---|---|
| **Location** | `<path>:<line>` |
| **Category** | <checklist section, for example "Persistence and data integrity"> |
| **Type** | <Confirmed defect | Potential risk> |
| **Origin** | <Introduced by the change | Pre-existing> <· Comes from a fix of R<n-1>-F<m>, if it does> |

**Problem:** <what's wrong and why.>

**Conditions:** <when or how it happens.>

**Impact:** <the functional, technical, security or operational consequence.>

**Evidence:** <the code, flow, contract or behavior that backs it.>

```<language>
<relevant code>
```

**Recommendation:** <concrete action to fix it or reduce the risk.>

```<language>
<proposed code, if it helps>
```

<For a potential risk, add: **To confirm:** <what information or validation would confirm it.>>

### F2 · 🟠 P1 · <short title>

...

### P3 findings

- F6 · 🔵 P3 · `<path>:<line>` · <problem> → <recommendation>

## Optional improvements

- F8 · 💡 Info · `<path>:<line>` · <what to improve> → <how>

## Validations

| Validation | Command | Result |
|---|---|---|
| <Lint> | `<command>` | <✅ Passed | ❌ Failed: summary | ⏭️ Not run: reason> |
| <Tests> | `<command>` | <...> |

<Limits of the environment or of the available information, if any.>

## Risks not verified

- <Relevant risks that couldn't be confirmed or validated, and what evidence or validation would be needed.>

## What's done well

- <Brief, specific points worth keeping.>

## Not reviewed

- <Generated or vendored files, files that got a lighter review in a large change, and anything outside the scope.>

## Next steps

1. <Fix the blocking findings first: F1, F2, ...>
2. <Ask the agent to apply fixes by ID, then run a new round to check them.>
````

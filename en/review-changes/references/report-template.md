# Report template

Structure of the report saved to `.reviews/<branch>/review-<n>.md`. Write it in the user's language. Leave out sections with no content, except the header, the summary and the findings.

## Rules

- Every finding has an ID (`F1`, `F2`, ...), a location as `path:line` (or `path:start-end`), the problem, why it matters and a proposed fix.
- Order the findings by severity, and within the same severity by file.
- Show the current code and the proposed code only when it makes the fix clearer. Keep snippets short: just the relevant lines.
- Group repeated minor issues (for example, the same naming problem in five places) into a single finding with all the locations.
- Questions (findings you couldn't confirm) go under their severity, starting with **Question:**.
- Never copy the value of a secret into the report.

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
| **Previous round** | <`review-<n-1>.md`, or "None"> |

## Summary

**Verdict:** <✅ Ready | ⚠️ Ready with changes | ❌ Needs work>

<Two or three sentences: what the change does (the intent) and the overall assessment.>

| 🔴 Critical | 🟠 Major | 🟡 Minor | 💡 Suggestion |
|---|---|---|---|
| <n> | <n> | <n> | <n> |

## Previous findings

<Only from round 2 on.>

| ID | Finding | Status | Notes |
|---|---|---|---|
| R<n-1>-F1 | <short title> | ✅ Fixed | |
| R<n-1>-F2 | <short title> | 🔄 Partially fixed | <what remains> |
| R<n-1>-F3 | <short title> | ❌ Still open | See F1 in this round |
| R<n-1>-F4 | <short title> | ➖ No longer applies | <why> |

## Findings

### 🔴 Critical

#### F1 · <short title>

**Location:** `<path>:<line>`
**Category:** <Design and structure | Clean code | Bugs and logic | Error handling | Security | Tests | Performance>

<What's wrong, in one or two sentences.>

**Why it matters:** <the consequence: what breaks, what gets harder, what risk it opens.>

**Proposed fix:** <what to do.>

```<language>
<proposed code, if it helps>
```

### 🟠 Major

#### F2 · <short title>

...

### 🟡 Minor

...

### 💡 Suggestions

...

## What's done well

- <Brief, specific points worth keeping.>

## Not reviewed

- <Generated or vendored files, files that got a lighter review in a large change, and anything you couldn't check.>

## Next steps

1. <Fix the Critical and Major findings first: F1, F2, ...>
2. <Ask the agent to apply fixes by ID, then run a new round to check them.>
````

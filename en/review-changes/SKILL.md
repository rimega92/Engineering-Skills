---
name: review-changes
description: Reviews code changes before a commit or a pull request (uncommitted changes, a branch's commits or an open pull request) for good practices, clean code, design and structural problems and bugs, and writes a report with a proposed fix for each finding. It can apply the fixes once the user approves them, and re-review the changes later to check the fixes and catch anything new. Use it when the user asks to review their changes, review code before committing or opening a pull request, review a pull request, or check whether earlier review findings were fixed.
---

# review-changes

Reviews code changes the way a careful senior teammate would: design and structure first, then clean code, bugs and good practices. Works with any language and technology. The result is a report saved in the project, with a proposed fix for each finding.

The flow has three steps:

1. **Review:** analyze the changes and write the report.
2. **Fix (optional):** apply the fixes the user approves.
3. **Re-review:** run again on the same branch to check what was fixed and whether anything new appeared.

## Principles

- **Review the change, in its context.** Judge the lines that changed, but read enough of the surrounding code to understand them. Don't report problems in untouched code, unless the change makes them worse or depends on them.
- **Follow the project's conventions.** Before suggesting a style or a pattern, check how the project already does it. A suggestion that goes against the rest of the code isn't an improvement.
- **Every finding is verified.** Report something only after checking it against the code. If you aren't sure, say so and mark it as a question instead of stating it as a fact.
- **Every finding has a fix.** Say what's wrong, why it matters and how to fix it, with code when it helps.
- **Proportional and useful.** Prioritize what matters. Don't pad the report with trivial remarks; group repeated minor issues into one finding.
- **Don't touch the code without approval.** The review only reads. Fixes are applied only to the findings the user approves.
- **Never secrets.** If the changes contain a credential or token, report it without copying its value into the report.
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

**Pull requests.** If the platform's CLI is installed and authenticated (`gh` for GitHub, `glab` for GitLab), use it to get the pull request's base, title, description and diff. If not, fetch the pull request's branch (`git fetch origin pull/<n>/head:<local-branch>` on GitHub) and compare it against its base. Don't switch the user's working tree to another branch if it has uncommitted changes; read files from the fetched ref (`git show <ref>:<path>`) instead.

**Nothing to review.** If the scope has no changes, say so and ask what to review.

## 2. Gather context

Before judging anything:

1. **List the changed files** with their status (added, modified, deleted, renamed) and the size of the change.
2. **Understand the intent.** Read the commit messages and, for a pull request, its title and description. If the intent isn't clear, infer it from the changes and state your assumption in the report.
3. **Read the project's conventions:** linter and formatter configuration, `.editorconfig`, `AGENTS.md`, `CONTRIBUTING.md`, architecture docs, and how similar code is written elsewhere in the project.
4. **Read the changed files in full**, not just the diff, plus the code that calls or is called by the changed parts when it matters for the review.
5. **Ignore generated and vendored files** (lock files, build output, generated code, minified files, third-party code). Mention them in the report as not reviewed.

If the change is very large, review the most important files in depth (business logic, public interfaces, security-sensitive code) and list in the report what got a lighter review.

## 3. Review

Go through the changes with `references/checklist.md`, in its order of priority:

1. Design and structure
2. Clean code
3. Bugs and logic
4. Error handling
5. Security
6. Tests
7. Performance

Classify each finding with the severity scale in the checklist (🔴 Critical, 🟠 Major, 🟡 Minor, 💡 Suggestion). If the project has its own rules (in `AGENTS.md`, `CONTRIBUTING.md` or the linter configuration), breaking them is a finding too.

Also note what's done well, briefly. It tells the author what to keep doing.

## 4. Verify the findings

Before writing the report, go over each finding:

- **Is it real?** Re-read the code around it. Check that the case you describe can actually happen (for example, that a value can really be null there) and that it isn't already handled somewhere else.
- **Does it fit the project?** Check that the proposed fix follows the project's conventions and works with its language version and dependencies.
- **Is the severity right?** Don't inflate it. A naming issue isn't Major.
- **Is it in the change?** Drop findings about code the change didn't touch or affect.

Drop what doesn't hold up. Keep the doubtful ones only as questions ("Can `user` be null here? If so, ...").

## 5. Write the report

Use `references/report-template.md`.

**Location:** `.reviews/<branch>/review-<n>.md` at the root of the repository.

- `<branch>` is the branch name with `/` replaced by `-` (`feat/login` → `feat-login`). For a pull request reviewed without its branch checked out, use `pr-<number>`. With a detached HEAD, use `commit-<short sha>`.
- `<n>` is the next round number: `1` for the first review of that branch, `2` for the next one, and so on.
- The report's header records the date, the branch, the base, the reviewed commit and whether uncommitted changes were included.

**Keep reports out of git.** Reports are personal working files. The first time, check whether `.reviews/` is ignored (`git check-ignore -q .reviews/`). If it isn't, add `.reviews/` to `.git/info/exclude`: that file is local to the user's clone, so the project's `.gitignore` stays untouched. Mention it to the user.

**Finding IDs.** Number the findings `F1`, `F2`, ... in order of severity. IDs restart in each round; later rounds refer to earlier findings with the round number in front (`R1-F3` is finding F3 of round 1).

When the report is written, give the user a short summary in the conversation: the verdict, the number of findings per severity, the most important ones and the path to the report. Don't paste the whole report.

## 6. Fix (with approval)

After the summary, offer to apply the fixes. Ask which ones: all, by severity (for example, "the Critical and Major ones") or by ID ("F1, F3 and F4"). If the user doesn't want any, stop here.

When the user approves:

- Apply only the approved findings, following the fix proposed in the report. If a fix turns out to need a different approach, explain it before applying it.
- Don't make other changes along the way.
- Don't commit. The user decides when to commit.
- When you finish, list what you changed per finding and suggest running a re-review.

## 7. Re-review

When the user asks to review again (for example, "review again", "check whether it's fixed"), and there's already a report for the branch:

1. **Read the previous report** (`review-<n-1>.md`): its findings and the commit it reviewed.
2. **Review the same scope again** as in step 1, with the current state of the code.
3. **Check each previous finding** and mark it:
   - ✅ **Fixed:** the problem is gone and the fix introduces no new problem.
   - 🔄 **Partially fixed:** it improved but something remains. Say what.
   - ❌ **Still open:** unchanged.
   - ➖ **No longer applies:** the code was removed or rewritten, so the finding doesn't apply anymore.
4. **Review what's new:** the changes since the previous round's commit, and the fixes themselves. Report new findings with new IDs; mark the ones that come from a fix.
5. **Write `review-<n>.md`** with the "Previous findings" section filled in, and summarize the progress to the user (for example, "4 of 6 fixed, 1 new Minor").

The fix and re-review cycle can be repeated as many times as needed. Earlier reports are never edited; each round is a new file.

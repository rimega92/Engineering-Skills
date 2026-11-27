---
name: developer-contribution-analysis
description: Gives an honest, data-backed picture of what one developer really contributed to a git repository. Counts commits, PRs, added lines and lines still present (blame of the whole repository), separates the developer's own code from templates, generated files, copies of other files in the repository, configuration tweaks and junk, reviews the quality of each commit, follows what happened to their code (whether it survives or others deleted or rewrote it), compares them with the rest of the team and scores them from 0 to 100 with a per-dimension rubric. Produces a single, complete and well-structured Markdown file with charts, evidence-backed findings, what they did contribute, what the analysis can't see and, on request, questions for a follow-up conversation. It doesn't modify the repository. Use it when the user wants to know what a person really did in a repository, evaluate or track their contribution, run a "blame" on a developer, or prepare a performance conversation with data.
---

# developer-contribution-analysis

Analyzes what a person really did in a repository: how much, which part is theirs, which part is a template or a copy, how good it is, what survived and how they compare with the rest of the team. The result is **a single Markdown file**, complete and self-contained, with real data, charts, a score and the evidence behind every claim.

The goal isn't the line count, which is easy to inflate with templates and copies. It's an honest picture of the contribution: what the person built, what they left to others and what the repository can't show.

The workflow has seven steps:

1. **Identify** the person and the scope.
2. **Collect** the data with the script.
3. **Review** commit by commit.
4. **Look for** what git doesn't show.
5. **Score** with the rubric.
6. **Write** the report.
7. **Save** and deliver.

## Principles

- **Real data only.** Every figure in the report comes from the script or from a git command you can cite. Don't estimate, don't round in either direction and don't invent values for a chart. If a figure doesn't exist or couldn't be computed, say so.
- **No sugarcoating.** Say what the data shows in plain words. A low contribution is called low, and a high one is called high. Don't soften or exaggerate. "None of their logic remains in the repository today" is plain; "their contribution had a more operational focus" sugarcoats.
- **Facts about the work, not judgments about the person.** Describe what they did and what's missing: "0 commits between September 21 and October 11", not "lazy". No adjectives about their character, intent or ability.
- **Fair.** Credit everything they did contribute, however small. Separate absence of evidence in git (reviews, design, support, other repositories) from evidence of absence. Take the role into account: infrastructure work by someone in DevOps isn't "just configuration".
- **Citable evidence.** Every finding points to a commit (`sha`), a file (`path:line`) or a PR. A claim without evidence doesn't go in the report.
- **Confirm before you claim.** The script gives hints (copy percentage, template markers, possible secrets). Before writing "copied from" or "bug", confirm it by reading the diff.
- **Read-only.** Never modify the repository: no commits, no branches, no configuration. Only read and run commands that change nothing.
- **Personal data.** The analysis evaluates a person. Keep it out of git, don't send it to external services and never copy secret values, only their location.
- **The user's language.** Write the report in the language the user writes to you in.

## 1. Identify the person and the scope

1. **Find their identities.** A person often appears with several names and emails (`jsmith`, `John Smith`, a personal email). List the repository's authors:

   ```bash
   python3 -I <skill-folder>/scripts/collect_contribution.py --repo <repo> --list-authors
   ```

   Mark the identities that look like the person's.
2. **Ask, in a single message and with a default answer for each point**, whatever the request leaves unclear:
   - **Identities:** the ones you found for the person. Are they all theirs? Is any missing?
   - **Repository and branch:** by default, the current repository and its main branch (`origin/HEAD` if it exists, otherwise `HEAD`).
   - **Period:** by default, the whole history. If the person joined or left the project on specific dates, use those dates.
   - **Expected role:** developer (default), DevOps or platform, QA or automation, tech lead, or intern. The role changes what counts as their own work and the scoring weights (`references/scoring.md`).
   - **Purpose:** tracking, evaluation, or preparing a conversation with the person. If the purpose is a conversation, the report includes evidence-backed questions.
   - **Exclusions:** third-party, generated or vendored folders that shouldn't count (for example, `vendor/**` or `**/generated/**`).
   - **Where to save the report:** by default, `.contribution-analysis/` at the repository root (see step 7).
3. If the user already gave a detail, don't ask for it. If they leave something unanswered, use the default and note it as an assumption in the report.
4. **Other people with several emails.** If someone on the team appears with two emails, the team comparison counts them as two people. To merge them, create a temporary mailmap outside the repository and pass it with `--mailmap` (format: `Canonical Name <main@email> <alias@email>`, one line per alias).

## 2. Collect the data

Run the script from the skill folder. It needs `git` and Python 3.9 or later, and installs nothing:

```bash
python3 -I <skill-folder>/scripts/collect_contribution.py \
  --repo <repo> \
  --author <email> --author "<name or alias>" \
  [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--ref <branch>] \
  [--exclude 'vendor/**'] [--mailmap <file>] [--lang en] \
  --out <temp-folder>
```

- `--author` takes an email (exact match) or a name fragment. Repeat it for each identity.
- `--out`: a temporary working folder **outside the repository**, for example one created by `mktemp -d`. Its files are working material and aren't delivered: everything that matters goes into the report (step 6), and the folder is deleted at the end (step 7).
- `--blame-copies` attributes lines moved or copied between files to their original author. It's fairer when a lot of code was moved, but much slower in large repositories.

The script writes three working files:

| File | Contents |
|---|---|
| `data.json` | Every metric: commits with their files, category, copy percentage and source, template markers and possible secrets; PRs; blame of the whole repository; what happened to each file they touched; weekly activity; team comparison; signals. |
| `summary.md` | The same data as readable tables. It's your starting point for the analysis. |
| `charts.md` | Charts ready to paste into the report, in Mermaid and as text bars, built from the real data. |

What the script measures and how:

- **Commits and lines:** non-merge commits from all branches and tags, with lines added and deleted per file.
- **Category of each file**, by its path: production code, test code, deployment and CI, build, configuration, documentation, test templates and data, standard files (wrappers, `.gitignore`, lockfiles) and files that shouldn't be in git (logs, compiled binaries, `.env`).
- **Copying:** for each file they touched, it compares their added lines with every earlier version of files with the same name written by other people. The percentage is the share of their significant lines that already existed verbatim. It also flags very similar files that others created later, which points to a common source.
- **Lines still present:** `git blame -w -M` of every text file on the analyzed branch, for the person and for the whole team.
- **Fate of their code:** for each file they touched, how many of their lines remain, who owns the rest and, if the file no longer exists, who deleted it and in which commit.
- **PRs:** merges that contain their commits, separating PRs from branch syncs, and who completed each one.
- **Signals to review:** commit subjects repeated on the same day, very large commits, files that shouldn't be in git, template markers (`TODO`, `sample`, `my-operation`…), possible secrets and fixes to one of their own commits from the previous days.

**Check the data before using it:**

1. The commit count matches `git log --branches --remotes --tags --no-merges --author=<email> --oneline | wc -l` (adding up all their identities).
2. The identities in `summary.md` all belong to the person, and none of the ones you saw in `--list-authors` is missing.
3. If a large repository takes too long, narrow it with `--since`, `--until` or `--exclude`, and say so in the report.

If Python isn't available, get the same data with git (`git log --numstat`, `git blame --line-porcelain`, `git log --merges`) and say in the report that the script wasn't used.

## 3. Review commit by commit

Read `references/classification.md`. Then:

1. **Choose the depth.**
   - Up to 40 commits: review them all.
   - More than 40: review every commit that touches production or test code, every one listed in the signals and the 15 largest. Group the rest by type, with counts and examples.
2. **Read the diff of each commit** (`git show --stat <sha>` and `git show <sha> -- <file>`). Using the copy column in `summary.md` and the diff, classify the commit according to `references/classification.md` and note what it did in one or two concrete sentences.
3. **Confirm the important copies.** For heavy files the script flags as copies, compare the file with its source (`git diff -w <source-sha>:<source-path> <sha>:<path>`). If two similar files have very close dates, or the similarity is with a later file, don't claim who copied whom: say they share a source.
4. **Tell templates and copies apart.** A file created by a tool (scaffold, `init`, code generators) or a standard file isn't a copy of a teammate's work, but it isn't the person's own work either. Call each thing by its name.
5. **Review the quality of their own code** with the list in `references/classification.md`: bugs, hard-coded values, unused parameters, commented-out code, tests that test nothing, files that shouldn't be in git, contradictory configuration, trial and error in PRs.
6. **Follow the fate of their code.** In the file fate table, see which of their parts other people deleted or rewrote, and read those commits (`git log --format='%h %an %ad %s' -- <path>`) to understand why: a bug, a refactor or a change in requirements. Code replaced because it was wrong isn't the same as code replaced because the business changed.

## 4. Look for what git doesn't show

The history doesn't capture all the work: PR reviews, comments, design, support, wiki documentation, work in other repositories, pair programming or assigned tasks.

- **PR reviews and comments.** If the platform's CLI is installed and authenticated, query it read-only. For example, `gh pr list --search "reviewed-by:<user>" --state all` on GitHub, `az repos pr list --reviewer <email> --status all` on Azure DevOps or `glab mr list --reviewer=<user>` on GitLab. If it isn't available, say so and explain how to get that data.
- **Co-authorship.** The script counts other people's commits with a `Co-authored-by` for this person.
- **The user's context.** Ask only if it changes the conclusion. For example, whether the person had tasks outside the repository, vacation or leave during the period, or changed roles.

Everything you couldn't verify goes into the "What this analysis can't see" section and lowers the score's confidence.

## 5. Score

Apply `references/scoring.md`: six dimensions from 1 to 5 with concrete anchors, role-based weights, a score from 0 to 100, a level and a confidence. Each score cites the metrics or commits that justify it. Don't adjust a score to make the result "look better" or "look worse": if the rubric doesn't fit a case, say so and explain the adjustment.

## 6. Write the report

Follow `references/report-template.md`. Rules:

- **Start with the verdict:** score, level, confidence and two unvarnished paragraphs about the real contribution.
- **One self-contained file.** Everything goes into the report: the analysis, the charts and, in the appendices, the full tables from `summary.md` (commits, files per commit with their source, fate of the code, team, PRs, signals and lines still present per file) and how to reproduce it. Whoever reads it shouldn't need any other file.
- **Use the charts in `charts.md`.** Paste the ones that apply. If you make another chart, build it only from values in `data.json` or from a command you cite.
- **Every figure must be traceable** to the report's appendices or a git command.
- **Include what they did contribute**, with the same precision as the problems.
- **Include the conversation questions** only if the purpose is a conversation with the person or the user asks for them. Each question cites its evidence and asks for facts, not opinions.

## 7. Save and deliver

**The deliverable is a single file:** the report. By default it goes at the root of the analyzed repository:

```text
.contribution-analysis/<person>-<YYYY-MM-DD>.md
```

`<person>` is the person's name in kebab-case without accents (`john-smith`). If the user asks for another location (for example, the desktop), use it. If a report with that name already exists, ask whether to replace it or create `<person>-<YYYY-MM-DD>-2.md`.

**Delete the script's temporary folder** once the report is written. Don't leave `data.json`, `summary.md` or `charts.md` anywhere: the only file left is the report.

**Keep the analysis out of git.** It evaluates a person and must never be committed. If you save it inside the repository:

1. Check whether the folder is ignored: `git check-ignore -q .contribution-analysis/`.
2. If it isn't, add `.contribution-analysis/` to the root `.gitignore` (create it if it doesn't exist), on its own line, with the comment `# Developer contribution analyses (developer-contribution-analysis)`. Don't change anything else in the file.
3. Tell the user you changed `.gitignore` and that they need to commit that change. Don't do it yourself.
4. If `.contribution-analysis/` was already committed, tell the user and suggest `git rm -r --cached .contribution-analysis` to stop tracking it without deleting the files.

**Delivery.** When you finish, say in the conversation:

- The score, the level and the confidence, with the verdict in two or three sentences.
- The report's path, relative and absolute.
- How to open it: in an editor with a Markdown preview. Mermaid charts render on GitHub, GitLab, Azure DevOps Wiki and VS Code (with a Mermaid extension); the text bars render in any viewer.
- What remained unverified and how to complete it, for example PR reviews.

## Verify before delivering

1. The figures in the verdict, tables, charts and appendices match each other and `data.json`.
2. Every claim of copying, templates or bugs is confirmed in the diff, not only by the script's percentage.
3. Every dimension score has its evidence, and the final score is the one the formula gives.
4. "What they did contribute" is complete, and nothing in the person's favor was left out.
5. The limitations are written down: period, branches, identities, what couldn't be queried.
6. The text has no judgments about the person and no words that soften or exaggerate the data.
7. The report contains no secret values.
8. The result is a single self-contained Markdown file, and the script's temporary folder is deleted.

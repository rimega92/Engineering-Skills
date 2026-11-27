# Report template

Structure of the contribution report. The report is the only deliverable: a single, self-contained Markdown file with the whole analysis and all the data. Write it in the user's language. Leave out sections with no content, except the verdict, the figures, the score and what the analysis can't see.

## Rules

- **The verdict comes first:** the reader should get the conclusion in the first lines.
- **Every figure is traceable** to the report's appendices or a git command.
- **Self-contained:** the appendices carry the full tables from `summary.md`. Nothing points to files that aren't delivered.
- **Every finding has evidence:** commit `sha`, `path` or `path:line`, PR number.
- **Charts come from `charts.md`** or from values in `data.json`. Put each chart in Mermaid and, below it, the text-bar version, which renders in any viewer.
- **Plain language, no adjectives about the person.** "Copied", "there are no tests", "another person rewrote it", "0 commits in 6 weeks". No "unfortunately", "it seems", "could improve" or "lazy".
- **What they did contribute** gets the same detail as the problems.
- **Group repetition:** the same change in three services goes on one line with all three locations.
- **Never copy a secret's value.**

## Class legend

🟥 Template, generated or copy · 🟧 Adaptation or configuration tweak · 🟦 Own infrastructure · 🟩 Own code · 🟨 Own code with problems · ⬛ Junk or accidental · ⬜ No content

## Template

````markdown
# Contribution of <name> to <repository>

| | |
|---|---|
| **Person** | <name> |
| **Git identities** | <name <email>>, <alias <email>> |
| **Repository** | <name> · branch `<branch>` (`<sha>`) |
| **Period analyzed** | <YYYY-MM-DD> → <YYYY-MM-DD> |
| **Role considered** | <Developer | DevOps | QA | Tech lead | Intern> |
| **Analysis date** | <YYYY-MM-DD> |
| **Assumptions** | <defaults that were used, or "None"> |

---

## 0. Verdict

| Score | Level | Confidence |
|---|---|---|
| **<0–100> / 100** | <level> | <High | Medium | Low> |

<Paragraph 1: what they really did in code. Key figures: how much is their own, how much is template or copy, what's still present and what happened to their code.>

<Paragraph 2: what other work they did contribute (configuration, infrastructure, coordination…), its quality, their consistency and the conclusion in one sentence, without sugarcoating.>

**Key facts**

| # | Fact | Evidence |
|---|---|---|
| 1 | <fact with a figure> | <commit, file, PR or metric> |

---

## 1. Figures

| Metric | Value |
|---|---|
| Active period | <first commit> → <last commit> |
| Non-merge commits | <n> |
| PRs with their commits / completed by the person | <n> / <n> |
| Lines added / deleted | +<n> / −<n> |
| Own-work lines added (no templates, copies or junk) | <n> (<%> of the total) |
| Their lines still present today | <n> of <repository total> (<%>) |
| Of those, own work | <n> |
| Weeks with commits / weeks in the period | <n> / <n> |
| Days from their last commit to the repository's last commit | <n> |

---

## 2. What the contribution is made of

<Chart: added lines by category (charts.md).>

<Chart: copied from existing files vs. new lines in the repository (charts.md).>

| Class | Lines added | % | Commits |
|---|---|---|---|
| 🟥 Template, generated or copy | <n> | <%> | `<sha>`, … |
| 🟧 Configuration tweaks | <n> | <%> | <n> commits |
| 🟦 Own infrastructure | <n> | <%> | … |
| 🟩 Own code | <n> | <%> | … |
| 🟨 Own code with problems | <n> | <%> | … |
| ⬛ Junk or accidental | <n> | <%> | … |
| **Total** | <n> | 100% | <n> |

---

## 3. Comparison with the team

<Charts: commits, lines still present and production code still present by author (charts.md).>

| Author | Commits | Lines still present | Production code still present | Test code still present |
|---|---|---|---|---|
| **<person>** | … | … | … | … |
| <other author> | … | … | … | … |

<One or two sentences on what the comparison shows. Remember the team's figures include their own templates.>

---

## 4. Activity over time

<Chart and table of commits per week (charts.md).>

<Reading: which weeks their activity concentrated in, long gaps and how it compares with the team's activity.>

---

## 5. What happened to their code

| Commit | Lines added | Still present | What they are |
|---|---|---|---|
| `<sha>` | <n> | <n> | <description> |

| File or part | Fate | Who and when | Reason according to the commit |
|---|---|---|---|
| `<path>` | <Present | Modified | Rewritten | Deleted> | <author, `sha`, date> | <reason> |

---

## 6. Commit by commit

### 6.<n> `<sha>` · <YYYY-MM-DD> · "<subject>" · <class>

**+<n> / −<n> · <n> files · <component>**

- <What it did, concretely.>
- <Source: "92% identical to `<path>` by <author> (`<sha>`, <date>)", or "new to the repository".>
- <Problems found, with `path:line`.>
- <Fate: how many lines remain today and who changed the rest.>

<With more than 40 commits: one section per important commit and a table with the rest grouped by class.>

---

## 7. Quality findings

| # | Finding | Severity | Evidence | Who fixed it? |
|---|---|---|---|---|
| 1 | <what> | <High | Medium | Low> | `<sha>` `<path:line>` | <author, `sha`> or "Unchanged" |

---

## 8. What they did contribute

- <Concrete contribution, with evidence.>

---

## 9. Score

| Dimension | Weight | Score (1–5) | Contribution | Evidence |
|---|---|---|---|---|
| D1 Volume of own work | <w> | <n> | <w × (n − 1) / 4> | <metric vs. team median> |
| D2 Complexity and value | <w> | <n> | … | … |
| D3 Quality | <w> | <n> | … | … |
| D4 Durability | <w> | <n> | … | … |
| D5 Tests | <w> | <n | N/A> | … | … |
| D6 Consistency | <w> | <n> | … | … |
| **Total** | 100 | | **<score>** | **<level>** |

**Confidence: <High | Medium | Low>.** <Why, and what would raise it.>

> The score describes the contribution to this repository during this period, not the person's worth as a professional.

---

## 10. What this analysis can't see

- <PR reviews and comments: queried with <tool>, or not queried and how to get them.>
- <Work in other repositories, assigned tasks, support, design, documentation outside the repository.>
- <Method limitations: period, branches, identities, excluded files, copy detection only within this repository.>

---

## 11. Questions for the conversation

<Only if the purpose is a conversation with the person or the user asked for them. Group them by topic. Each question cites its evidence and asks for facts.>

### Volume and consistency
1. <question> (<evidence>)

### Authorship
### Quality
### Way of working
### Closing
1. If you had to show one contribution of yours that the team wouldn't have had without you, which would it be? Show it in the code.
2. Which part of your work isn't in this repository, and where is the evidence?

---

## Appendices

<The full tables from `summary.md`, so the report doesn't depend on any other file.>

### A. All commits

| Commit | Date | + | − | % copy | Still present | Class | Subject |
|---|---|---|---|---|---|---|---|

### B. Files per commit and their source

<One table per commit: file, category, +, −, % copy, source (author, commit, date, path), similar later file, template markers, possible secrets.>

### C. Fate of the files they touched

| File | Category | + theirs | Created by them | Exists today | Theirs today / total | Other authors today or who deleted it |
|---|---|---|---|---|---|---|

### D. Team

| Author | Email | Commits | + | − | First | Last | Still present | Production present | Tests present |
|---|---|---|---|---|---|---|---|---|---|

### E. Pull requests

| Merge | Date | PR | Completed by | Their commits / total | Title |
|---|---|---|---|---|---|

<Other merges that carried their commits (branch syncs or without a PR number).>

### F. Script signals

| Type | Commit | Detail | Review |
|---|---|---|---|
| <type> | `<sha>` | <path or subject> | <Confirmed | False positive: why> |

### G. Lines still present per file

| Lines | File |
|---|---|

### H. How to reproduce

```bash
python3 -I <skill-folder>/scripts/collect_contribution.py --repo <repo> --author <email> [...] --out "$(mktemp -d)"
git log --branches --remotes --tags --no-merges --author=<email> --numstat
git show <sha>
git blame -w -M --line-porcelain <file> | grep '^author-mail' | sort | uniq -c
```
````

# Report template

Structure of the contribution report. The report is the only deliverable: a single, self-contained Markdown file with the whole analysis and all the data. Write it in the user's language. Leave out sections with no content, except the verdict, the figures, the score and what the analysis can't see.

## Rules

- **The verdict comes first:** the reader should get the conclusion in the first lines.
- **Every figure is traceable** to the report's appendices or a git command.
- **Self-contained:** the appendices are the contents of `annex.md` as is, in the report's language. Nothing points to files that aren't delivered.
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

## Changes since the previous report

<Only if there's an earlier report for the same person. Compare with its `<!-- developer-contribution-analysis: … -->` marker.>

| | Previous report (<date>, `<sha>`) | Now | Change |
|---|---|---|---|
| Score | <n> | <n> | <±n> |
| Commits | <n> | <n> | <±n> |
| Own work added | <n> | <n> | <±n> |
| Own work still present | <n> | <n> | <±n> |
| Weeks with commits | <n> | <n> | <±n> |

<New findings and findings that were resolved, with evidence.>

---

## 1. Figures

| Metric | Value |
|---|---|
| Active period | <first commit> → <last commit> |
| Non-merge commits | <n> |
| PRs with their commits / completed by the person | <n> / <n> |
| Lines added / deleted | +<n> / −<n> |
| Own-work lines added (no templates, copies or junk) | <n> (<%> of the total) |
| Own PRs on the platform / others' PRs they reviewed | <n> / <n>, or "not queried" |
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

<Charts: commits, lines still present and own work still present by author (charts.md).>

| Author | Commits | Lines still present | Own work added | Own work still present | Durability |
|---|---|---|---|---|---|
| **<person>** | … | … | … | … | … |
| <other author> | … | … | … | … | … |

<One or two sentences on what the comparison shows. Own work is measured the same way for everyone; lines still present include templates and copies.>

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

## Appendices

<The contents of `annex.md` as is, with the "Review" column of appendix F filled in (Confirmed or False positive, with the reason) and the `<!-- developer-contribution-analysis: … -->` marker at the end. It has these sections:>

- A. All commits
- B. Files per commit and their source
- C. Fate of the files they touched
- D. Team
- E. Pull requests (and, if queried, the platform's PRs)
- F. Script signals
- G. Lines still present per file
- H. How to reproduce
````

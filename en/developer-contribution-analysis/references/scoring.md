# Scoring

How to score a person's contribution to a repository. Six dimensions from 1 to 5, with concrete anchors, role-based weights, a score from 0 to 100, a level and a confidence.

## Team reference data

Several dimensions compare the person with the team. Compute these references from the `team` table in `data.json`:

- **Active people:** authors with at least 5 commits in the period, not counting the analyzed person or service accounts and bots (`svc…`, `bot`, `jenkins`, `azure-pipelines`, `dependabot`…).
- **Team median:** the median of a metric across active people. If there are fewer than 2, there's no comparison: score with the absolute anchors and say so.

The team's figures include their own templates and copies, because the script only detects copying for the analyzed person. The comparison favors the person, so it's conservative.

## Dimensions

### D1. Volume of own work

How much of their own work they produced, not counting templates, copies, junk or standard files. What counts as their own depends on the role (`references/classification.md`).

**Metric:** the person's lines of own work still present (for a developer, for example, production and test code with copy < 50%) against the team median of lines still present in the same categories.

| Score | Anchor |
|---|---|
| 5 | ≥ 100% of the team median |
| 4 | 60% to 99% |
| 3 | 30% to 59% |
| 2 | 10% to 29% |
| 1 | < 10%, or no own work still present |

### D2. Complexity and value

How hard and how important for the product their work is. Scored from the commit-by-commit review.

| Score | Anchor |
|---|---|
| 5 | Complete business features, hard integrations, component design or technical decisions others build on |
| 4 | Features with their own logic and a clear scope |
| 3 | Small features, integration wiring, fixes that required analysis |
| 2 | Configuration, version bumps, manifest tweaks, one-line fixes |
| 1 | Nothing beyond templates, copies or changes without content |

### D3. Quality

How correct and clean their deliverables are. Use the problem list in `references/classification.md`.

| Score | Anchor |
|---|---|
| 5 | No defects found, clean commits, real tests, nothing others had to fix |
| 4 | Minor problems (style, poor commit messages, some commented-out code) |
| 3 | A real defect the person fixed themselves, or several minor problems |
| 2 | Defects other people had to fix, junk files in git, trial and error in PRs, contradictory configuration |
| 1 | Serious defects (security, data loss, broken behavior in production), secrets in git, or defects repeated across most of their own code |

### D4. Durability

How much of their own work is still standing and whether others had to redo it.

**Metric:** the percentage of their own-work lines (copy < 50%, no junk) that are still present, and the fate of their code (`references/classification.md`).

| Score | Anchor |
|---|---|
| 5 | ≥ 70% still present and no rewrites due to defects |
| 4 | 50% to 69%, or rewritten only because of requirements changes or general refactors |
| 3 | 30% to 49% |
| 2 | 10% to 29%, or most of it rewritten or deleted by other people because of defects |
| 1 | < 10% still present |

A repository with a lot of requirements churn has low durability for everyone. If the team's durability is also low, say so and raise the score by one point at most.

### D5. Tests

Whether they wrote tests that verify the behavior of their code.

| Score | Anchor |
|---|---|
| 5 | Tests with real assertions covering the logic they wrote, including error cases |
| 4 | Real tests for most of their logic |
| 3 | Some real tests, with significant gaps |
| 2 | Minimal tests, or tests that verify very little |
| 1 | No tests, or template tests only |

**Not applicable** if the person wrote no testable logic (for example, a DevOps profile without scripts that contain logic). In that case, spread its weight proportionally across the other dimensions and say so.

### D6. Consistency

Whether they contributed steadily during the time they were supposed to.

**Metric:** weeks with at least one commit, against the weeks in the period when the repository was active while the person was assigned (by default, from their first commit to the repository's last commit in the period).

| Score | Anchor |
|---|---|
| 5 | ≥ 80% of the weeks |
| 4 | 60% to 79% |
| 3 | 40% to 59% |
| 2 | 20% to 39% |
| 1 | < 20% |

If they've gone more than 4 weeks without commits while the repository is still active, the maximum score is 2, unless the user confirms the person was assigned to something else (vacation, another project, leave). In that case, recompute with the real assignment period.

## Weights by role

| Dimension | Developer | DevOps or platform | QA or automation | Tech lead |
|---|---|---|---|---|
| D1 Volume of own work | 25 | 25 | 25 | 15 |
| D2 Complexity and value | 20 | 25 | 20 | 30 |
| D3 Quality | 20 | 25 | 20 | 25 |
| D4 Durability | 15 | 15 | 15 | 15 |
| D5 Tests | 10 | 0 | 10 | 5 |
| D6 Consistency | 10 | 10 | 10 | 10 |

Intern or junior: use the developer weights. You can comment in the report on what the level is expected to deliver, but don't change the scores.

For a tech lead, PR reviews and design decisions matter a lot and are rarely in git. If you couldn't query them, confidence is Low.

## Final score

```text
score = Σ weight_i × (score_i − 1) / 4
```

The result ranges from 0 to 100. Round it to an integer. Write the table with each dimension, its weight, its score, its contribution to the final score and the evidence.

| Score | Level |
|---|---|
| 85 – 100 | **Outstanding**: high, good-quality, sustained own contribution |
| 70 – 84 | **Solid**: clear own contribution, with minor problems |
| 50 – 69 | **Acceptable with gaps**: contributes, but with significant gaps in volume, quality or consistency |
| 30 – 49 | **Low**: little own work, or own work with serious problems |
| 0 – 29 | **Very low**: almost no own work still present, or serious defects |

## Confidence

| Confidence | When |
|---|---|
| **High** | All their identities confirmed, full period, PR reviews queried or irrelevant to the role, and nothing important outside git |
| **Medium** | Data from outside git is missing (PR reviews, assigned tasks) that could move one score by one point |
| **Low** | Missing data could change the conclusion: a lead role without reviews, known work in other repositories, a short period (under 4 weeks) or doubtful identities |

Always say what would raise the confidence.

## Rules

- Every score cites its metrics or commits. "D3 = 2: their only own code (`a1b2c3d4`) hard-coded a 1500 s timeout, and a teammate rewrote it entirely" is a justification; "D3 = 2: quality could improve" isn't.
- Don't average by eye. Compute the score with the formula.
- If the rubric doesn't fit a case (for example, a documentation-only repository), say so and explain how you scored it.
- The score describes the contribution to this repository during this period, not the person's worth as a professional. Write it that way in the report.

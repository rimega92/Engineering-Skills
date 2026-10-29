# Assessment and estimation

How to assess a change and estimate its effort. The estimate is a reasoned range, not a commitment: it's meant to compare options, plan and decide what to check first.

## Assessment

Three separate axes, each with a short justification. Keep them apart: a change can be easy to write and very risky (a data migration), or hard to write and low risk (an isolated new module).

### Complexity: how hard it is to implement

| Level | Signals |
|---|---|
| **Low** | One module, a few files, a known pattern repeated in the project, no contracts or data involved |
| **Medium** | Several files or modules, some new logic, a compatible contract change or a simple migration |
| **High** | Several modules or services, new logic with many cases, a breaking contract change, a migration with backfill |
| **Very high** | Cross-cutting change (architecture, platform, data model), coordination between teams, coexistence of old and new versions |

### Risk: what can go wrong and how much it would hurt

| Level | Signals |
|---|---|
| **Low** | Isolated change, good test coverage, easy to revert, no sensitive data |
| **Medium** | Affects a core flow or has partial coverage, but it's reversible |
| **High** | Touches a sensitive area, existing data, external consumers or code without tests; hard to revert |
| **Very high** | Can corrupt or expose data, break critical operations or consumers you can't see, and can't be reverted easily |

### Confidence: how sure the analysis is

| Level | Signals |
|---|---|
| **High** | All the touchpoints were found in the code, the consumers are visible and the area has tests |
| **Medium** | Most of it is confirmed, but there are consumers or behaviors to confirm |
| **Low** | Key parts are outside the repository, the code is hard to follow (reflection, dynamic configuration), or the requirements are still open |

## Size and estimate

The estimate is for **one developer who knows the code**, from the start of the work to the change being ready to merge: implementation, tests, migrations and review fixes. It doesn't include waiting time (other teams, QA queues, approvals, deploy windows); list that separately as "not included".

| Size | Typical range | Typical shape |
|---|---|---|
| **XS** | Under 2 hours | One or two files, no new tests or one simple test |
| **S** | 2 hours to 1 day | A few files in one module, with its tests |
| **M** | 1 to 3 days | Several modules, or a compatible contract or data change |
| **L** | 3 to 10 days | Several modules and consumers, a migration with backfill, or a breaking contract change |
| **XL** | More than 2 weeks | Recommend splitting it into smaller changes and estimate each one |

## How to estimate

1. **Break it down by activity**, with a range for each one, only for the ones that apply:
   - Implementation (production code).
   - Tests (modify existing ones and write new ones; also tests written first where coverage is missing).
   - Migrations, scripts and backfill.
   - Contracts and consumers (versioning, generated clients, consumer updates in the repository).
   - Configuration, infrastructure and observability.
   - Documentation.
   - Review and fixes.
2. **Add up the ranges** and round to a range that sounds like a real estimate ("2 to 4 days", not "13.5 to 27 hours").
3. **Widen the range when confidence is lower:** with Medium confidence, raise the upper bound by about half; with Low, double it and say what would narrow it.
4. **Say what makes it grow:** the specific facts that would move the estimate up (for example, "if the mobile app needs the field, add 1 to 2 days").
5. **Say what's not included:** waiting time, coordination, QA, deploy.

## Rules

- Base the estimate on the impact you found, not on the description of the request.
- Never give a single exact figure. A range and the reasons behind it are more useful.
- Don't pad the estimate to be safe; the confidence and the "what makes it grow" list already express the uncertainty.
- If there's a minimal scope and a full one, estimate both.
- If the project has its own estimation scale (story points, sizes), add it alongside, but keep the range.

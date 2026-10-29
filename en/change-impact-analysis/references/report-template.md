# Analysis template

Structure of the impact analysis. Use it for the answer in the conversation and, if the user asks for it, for the file saved to `.impact/<change>.md`; both have the same content. Write it in the user's language. Leave out sections with no content, except the summary, the impact and the estimate.

## Size by mode

- **Quick:** summary, decisions and assumptions, impact by area (one line for each dimension that doesn't apply), count, estimate and before you start.
- **Deep:** every section with content.

## Rules

- Start with the summary: the user should get the answer from the first lines.
- Every affected item has a location (`path:line` or `path`) and a short reason.
- Group repeated items (for example, the same change in eight DTOs) into one line with all the locations.
- A dimension with no impact gets one line saying what was checked: "No impact: no consumer reads `orders.status` outside this module (searched in `src/`, `scripts/` and `infra/`)".
- Items you couldn't verify go in "To confirm", with how to confirm them.
- Never copy the value of a secret.

## Template

````markdown
# Impact analysis: <short title of the change>

| | |
|---|---|
| **Date** | <YYYY-MM-DD> |
| **Project** | <repository or service name> |
| **Components** | <in a monorepo, the components the change touches> |
| **Analyzed commit** | `<short sha>` on `<branch>` <+ uncommitted changes, if any> |
| **Mode** | <Quick | Deep: why> |
| **Request** | <the change as the user described it> |
| **Understood as** | <goal and solution, in one or two sentences> |

## Summary

| Size | Estimate | Complexity | Risk | Confidence |
|---|---|---|---|---|
| <XS–XL> | <range, for example "2 to 4 days"> | <Low–Very high> | <Low–Very high> | <High | Medium | Low> |

<What the change involves, the main impacts, the biggest risk and what to settle before starting. Three to five sentences.>

**Complexity:** <justification in one sentence.>
**Risk:** <justification in one sentence.>
**Confidence:** <justification in one sentence, and what would raise it.>

## Decisions and assumptions

| Topic | Decision | Source |
|---|---|---|
| <Existing data> | <Existing orders get `currency = EUR`> | <User's answer | Assumption> |

## Scope

| | Minimal | Full |
|---|---|---|
| **Includes** | <what> | <what> |
| **Leaves out** | <what> | <—> |
| **Estimate** | <range> | <range> |

<Recommendation: which one to do first and why.>

## Impact by area

### Code

| Location | What changes | Impact | Evidence |
|---|---|---|---|
| `<path>:<line>` | <brief> | <Direct | Indirect> | <call, import, serialization...> |

### Processes and flows

...

### Contracts

<For each contract: what changes and whether it's compatible or breaking.>

### Data

...

### Tests

| Location | Action | Why |
|---|---|---|
| `<path>` | <Modify | Create> | <brief> |

### Consumers

| Consumer | Visible | What it needs |
|---|---|---|
| <web frontend, `web/src/orders/`> | ✅ In the repository | <Show the new field> |
| <billing service> | ❓ To confirm | <Check whether it reads `OrderCreated`> |

### Configuration, infrastructure, security, operations and documentation

<Only what applies; one line for the rest.>

## Count

| Kind | Modify | Create | Delete |
|---|---|---|---|
| Production files | <n> | <n> | <n> |
| Tests | <n> | <n> | <n> |
| Migrations and scripts | <n> | <n> | <n> |
| Configuration and infrastructure | <n> | <n> | <n> |
| Documentation | <n> | <n> | <n> |
| **Total** | <n> | <n> | <n> |

<Units affected, if useful: for example "7 classes, 2 interfaces, 1 component".>

## Effort estimate

| Activity | Estimate | Notes |
|---|---|---|
| Implementation | <range> | |
| Tests | <range> | |
| Migrations and backfill | <range> | |
| Contracts and consumers | <range> | |
| Review and fixes | <range> | |
| **Total** | **<range>** | Size <XS–XL>, confidence <level> |

**What makes it grow:** <specific facts that would move it up.>
**Not included:** <waiting time, coordination, QA, deploy.>

## Before you start

- [ ] <Decision to make, data to inspect, consumer to confirm, test to write first...>

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <Old app versions fail on the new field> | <Low | Medium | High> | <Low | Medium | High> | <Make the field optional> |

## Suggested order

1. <Step that can be merged on its own, for example "compatible migration: nullable column">
2. <...>

## To confirm

- <Item not verifiable from the repository, and how to confirm it.>
````

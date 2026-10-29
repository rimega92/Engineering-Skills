# Readiness checklist

The areas to check before a story is ready for development. For each area: what the story should make clear, what to look for in the code, and typical questions. Use the questions as inspiration, not as a list to copy: ask only what the story and the code leave open, and phrase it with what you found.

Give each area a status: ✅ Clear, ⚠️ Ambiguous, ❌ Missing or ➖ Not applicable. A ⚠️ or ❌ area turns into a question, an assumption or an open question.

## 1. Value and user

- **The story should say:** who needs it (role or user type), what they want to do and why. The "why" decides the trade-offs when something isn't specified.
- **In the code:** the roles and user types that exist.
- **Typical questions:** which user types are included? What problem does it solve, and how will we know it's solved?

## 2. Scope and size

- **The story should say:** what's included and what's explicitly left out, and which platforms or channels (web, mobile, back office, public API).
- **In the code:** every place where the same behavior lives (for example, the same screen in web and mobile, or the same rule in two services).
- **Typical questions:** does it apply to the mobile app too? Does it cover existing records or only new ones?
- **Size:** if the story mixes several independent behaviors, user types or deliveries, propose splitting it. Each part should deliver value on its own and be testable.

## 3. Acceptance criteria

- **The story should say:** observable, verifiable conditions for the main flow, the alternatives and the errors. "Works correctly" or "is fast" aren't criteria.
- **In the code:** the existing tests of the area, which show how its behavior is verified today.
- **Typical questions:** what does the user see when it works, and when it fails? Which result proves the story is done?

## 4. Business rules and validations

- **The story should say:** rules, calculations, limits, formats, required fields, states and transitions.
- **In the code:** existing validations, state machines, calculations and constants. This is where most contradictions show up: a field that is required in the API but optional in the story, a status the entity doesn't have, a limit that is different.
- **Typical questions:** the code rejects X (`path:line`); should that change? What happens at the limit (zero, maximum, empty)? Who wins if two rules conflict?

## 5. Edge cases and errors

- **The story should say:** what happens with empty or invalid input, duplicates, simultaneous actions, timeouts, partial failures and unavailable dependencies.
- **In the code:** how the area handles errors today (messages, retries, error codes, rollback).
- **Typical questions:** what if the external service doesn't answer? Can the user do it twice? What if half of the records fail?

## 6. Data

- **The story should say:** new or changed data, what happens to existing records, where the data comes from, how long it's kept, and whether it includes personal or sensitive data.
- **In the code:** entities, tables, columns, migrations, and who else reads that data.
- **Typical questions:** what value do existing records get? Is it calculated or stored? Is it personal data, and who can see it?

## 7. Contracts and integrations

- **The story should say:** which APIs, events, files or third-party integrations change, and whether current consumers must keep working.
- **In the code:** endpoints, request and response models, events, clients of other services, API specs (OpenAPI, GraphQL schemas, Protobuf), and the consumers you can see.
- **Typical questions:** should the new field appear in every endpoint that returns this entity? Is a breaking change acceptable, or must it be compatible? Who consumes this event outside this repository?

## 8. Design, texts and user experience

- **The story should say:** the screens or the link to the designs, the texts and their translations, and the states: loading, empty, error, success, and no permission.
- **In the code:** existing components that can be reused, translation files, accessibility conventions.
- **Typical questions:** is there a design? What does the user see while it loads, or when there's nothing to show? Do the texts need translations?

## 9. Permissions and security

- **The story should say:** who can see and do what, and what happens when someone without permission tries.
- **In the code:** roles, permission checks, guards and policies on the screens and endpoints involved.
- **Typical questions:** can every role do it, or only admins? Can a user act on someone else's data? Does it need an audit trail?

## 10. Non-functional requirements

- **The story should say:** volume, response time, availability, audit, compliance, and analytics or tracking, only when they matter for this story.
- **In the code:** pagination, limits, caches, existing analytics events and metrics.
- **Typical questions:** how many records at most (an export of 100 rows isn't one of a million)? Does it need an analytics event? Is there a legal or compliance requirement?

## 11. Dependencies and rollout

- **The story should say:** what it depends on (other teams, other stories, third parties, data), and how it's released (all at once, behind a feature flag, gradually).
- **In the code:** feature flags, configuration per environment, clients of external services.
- **Typical questions:** does another team need to change something first? Should it go behind a feature flag? Is it needed in every environment and country?

## 12. Testability

- **The story should say:** enough to know how it will be tested: test data, environments, and the dependencies to simulate.
- **In the code:** test types and tools in use, fixtures, mocks of external services.
- **Typical questions:** is there test data for this case in the test environment? Can the third party be used in tests, or does it need a mock?

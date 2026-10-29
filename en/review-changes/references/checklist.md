# Review checklist

What to look for in a change, in order of priority, and how to rate each finding. The items are language-agnostic: apply each one with the idioms of the project's language and framework.

Not every item applies to every change. Use them as a guide, not as a form to fill in.

## Severity

| Level | Meaning | Examples |
|---|---|---|
| 🔴 Critical | Must be fixed before merging. Breaks behavior, loses or corrupts data, or opens a security hole. | Logic error in the main flow, SQL injection, secret committed, migration that drops data |
| 🟠 Major | Should be fixed before merging. A real problem that isn't urgent yet: it will cause bugs or make the code hard to change. | Unhandled error on a likely path, business logic in the wrong layer, missing tests for new logic, duplicated logic that will drift |
| 🟡 Minor | Worth fixing, in this change or soon. Readability and maintainability. | Unclear names, long function, magic number, misleading comment |
| 💡 Suggestion | Optional improvement or alternative. The author decides. | A simpler way to write something, a library function that already does it |

**Verdict** of the review:

- ✅ **Ready:** no Critical or Major findings.
- ⚠️ **Ready with changes:** no Critical findings, but there are Major ones to fix first.
- ❌ **Needs work:** at least one Critical finding, or the approach itself needs rethinking.

## 1. Design and structure

- **Single responsibility.** Does each new or changed function, class or module do one thing? Mixed responsibilities (for example, validation, business rules and data access in the same function) are a finding.
- **Right place.** Is the code in the layer or module where the project puts that kind of code? Business logic in controllers or views, or data access in the domain, breaks the architecture.
- **Dependencies point the right way.** Does the change introduce a dependency that goes against the project's layering (for example, the domain importing from the infrastructure), or a circular dependency?
- **Coupling.** Does it reach into other modules' internals instead of using their public interface? Does a change here force changes in many unrelated places?
- **Abstraction level.** Is there a missing abstraction (the same structure repeated) or an unnecessary one (an interface with a single implementation and no reason for it, layers that only forward calls)?
- **Consistency.** Does it solve a problem the project already solves in a different way? Reuse the existing solution or justify the new one.
- **Public interfaces.** Are new APIs, function signatures and types easy to use correctly and hard to misuse? Are breaking changes to existing interfaces intended and handled?
- **Size of the change.** Does it mix unrelated changes (a feature, a refactor and a formatting pass) that would be easier to review separately?

## 2. Clean code

- **Names.** Do names say what things are or do, in the project's vocabulary? Avoid vague names (`data`, `info`, `manager`, `handle`), abbreviations nobody knows and names that lie about what the code does.
- **Functions.** Short, at one level of abstraction, with few parameters. Boolean flag parameters that switch behavior usually hide two functions.
- **Duplication.** Copied logic that will have to change in several places. Three similar lines aren't always duplication; the same rule in two places is.
- **Complexity.** Deep nesting, long conditionals, hard-to-follow flow. Early returns, extracted functions or clearer data structures can help.
- **Magic values.** Unexplained numbers or strings that should be named constants or configuration.
- **Dead code.** Unused variables, functions, imports, parameters, commented-out code and leftover debugging (`print`, `console.log`, breakpoints).
- **Comments.** They should explain why, not repeat what. Outdated or misleading comments are worse than none. `TODO` comments without context or owner.
- **Formatting and style.** Only what the project's formatter or linter doesn't already enforce, and only if it's inconsistent with the rest of the code.

## 3. Bugs and logic

- **Does it do what it intends?** Compare the behavior with the intent from the commit messages or pull request.
- **Edge cases.** Empty collections, null or missing values, zero, negative numbers, very large inputs, duplicates, unexpected types, time zones and dates, text encoding.
- **Conditions.** Off-by-one errors, inverted conditions, wrong operators, missing `else` branches, incomplete `switch` or `match` cases.
- **State.** Shared mutable state, values modified while being read, objects left in an inconsistent state on failure.
- **Concurrency.** Race conditions, missing locks or awaits, operations that assume order, unawaited async calls.
- **Resources.** Files, connections, subscriptions or listeners that are opened and never closed or released.
- **Data changes.** Migrations that can't be rolled back or that lose data; changes to stored formats that break existing data.

## 4. Error handling

- **Errors aren't swallowed.** Empty `catch` blocks, errors logged and ignored where the caller needed to know, return values that signal failure and aren't checked.
- **Errors are handled at the right level**, with enough context to diagnose them, and following the project's error strategy.
- **Failure leaves things consistent.** Partial writes, transactions that aren't rolled back, retries that duplicate effects.
- **The user sees a useful message**, without internal details or stack traces.

## 5. Security

- **Input validation.** Data from users, files, external services or the network is validated before use.
- **Injection.** SQL, commands, paths, templates or queries built by concatenating untrusted input.
- **Secrets.** Credentials, tokens or keys in the code, configuration, tests or logs. Report the location, never the value.
- **Authentication and authorization.** New endpoints or actions without access checks; checks done only on the client.
- **Sensitive data.** Personal or sensitive data logged, exposed in responses or stored without protection.
- **Dependencies.** New dependencies that are unmaintained, unnecessary or pulled from untrusted sources.

## 6. Tests

- **New logic has tests**, following the project's testing conventions. A bug fix ideally has a test that would have caught it.
- **Tests check behavior**, not implementation details, and would fail if the code broke.
- **Edge cases and errors** from section 3 are covered where they matter.
- **Tests are reliable:** no dependence on order, time, network or randomness without control.
- **Changed behavior** is reflected in the existing tests, not worked around by deleting or weakening them.

## 7. Performance

Only obvious problems; don't speculate about micro-optimizations.

- **Repeated work:** queries or calls inside loops (N+1), the same expensive computation done several times.
- **Unbounded work:** loading whole tables or files into memory, missing pagination, unbounded collections or caches.
- **Blocking:** slow operations on the main or UI thread, synchronous calls where the project is asynchronous.
- **Inefficient structures:** linear searches in hot paths where a map or set would do.

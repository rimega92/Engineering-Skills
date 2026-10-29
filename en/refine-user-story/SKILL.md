---
name: refine-user-story
description: Refines a user story before it's implemented. It reads the story, explores the code of the frontends, services and APIs it affects, and checks whether the story is clear and complete enough to build: value, scope, acceptance criteria, business rules, edge cases, data, contracts, design, permissions, non-functional requirements and dependencies. It flags what's missing, what's ambiguous and what contradicts the current code, asks questions grouped by who should answer them, in one or two rounds, and delivers a readiness verdict and the refined story, with testable acceptance criteria, technical notes, assumptions and open questions. It saves the result to a file kept out of git, and can update it when the user brings a new version of the story or answers to open questions. It doesn't modify code or estimate effort. Use it when the user shares a user story, ticket or requirement and asks to refine it, review it, check whether it's ready for development or what's missing.
---

# refine-user-story

Checks whether a user story is ready to be implemented and turns it into a refined story. Works with any language, framework and architecture, and with stories that touch one component or several (frontend, services, APIs). The result is a readiness verdict and the text of the refined story, saved to a file.

The goal isn't to rewrite the story more nicely, but to make sure that a developer can implement it and a tester can verify it without guessing: every gap is either answered, turned into an explicit assumption, or left as a visible open question.

The flow has six steps:

1. **Read** the story.
2. **Explore** the code it affects.
3. **Diagnose** whether it's ready.
4. **Ask** the questions that close the gaps, in one or two rounds.
5. **Write** the refined story and deliver it.
6. **Save** it to a file.

A story that was already refined can be **updated** with a new version of its text or with answers to its open questions (see "Update a refined story").

## Principles

- **Read only.** The refinement never modifies code, data or configuration. The only file it writes is the refined story, and the `.gitignore` line that keeps it out of git.
- **The story describes behavior, the code shows the current state.** Use the code to find what already exists, what the story would change and where it contradicts the current behavior. Don't turn the story into a technical design.
- **Evidence from the code.** Every technical note and every contradiction points to a location (`path:line` or `path`).
- **Don't invent requirements.** Business decisions belong to the people who own the story. Propose an answer for each question, but if nobody confirms it, it's an assumption and is marked as one.
- **Visible and not visible.** What lives outside the repositories you can read (other teams' services, third parties, designs) is listed as "to confirm", never presented as certain.
- **No estimates.** The refinement says what the story needs, not how long it takes. For effort and impact, offer the `change-impact-analysis` skill, if it's installed.
- **Two audiences.** The functional part of the story is written for the whole team, in plain language and without code paths. Technical details go in a separate section.
- **Never secrets.** If you find a credential or token, mention its location without copying its value.
- **The user's language.** Write the refined story in the language of the original story, unless the user asks for another one.

## 1. Read the story

1. **Get the text.** The user pastes it, points to a file, or gives a ticket ID. If the agent has access to the issue tracker, it can read the ticket from there; otherwise ask the user to paste it. Keep the original text exactly as given: it goes into the saved file.
2. **Identify the ID** (for example `PROJ-123`) if the story has one, and a short title.
3. **Check whether it was already refined:** look for `.stories/` files whose name starts with that ID or matches the title (see step 6 for where they live). If one exists, follow "Update a refined story" instead.
4. **Restate the story in one or two sentences:** who, what and why, the way you understood it. Separate the need from any solution the story imposes ("add a button that exports to CSV" may hide the need "send orders to accounting").
5. **Identify the components** the story implies (web or mobile frontend, services, APIs, batch processes, databases) and where their code is:
   - In the current repository or monorepo, find them by their folders and names.
   - If a component lives in another repository, ask the user for its local path. Read it the same way, read only.
   - A component you can't read is listed as "to confirm".
6. If the project uses its own story template or Definition of Ready (in the repository's docs or agent instruction files, or given by the user), use it as the base for the checklist and the result, and fill the gaps with `references/readiness-checklist.md` and `references/story-template.md`.

## 2. Explore the code

A targeted pass over each affected component, to learn what exists today:

1. **Read the project's context:** `README`, agent instruction files (`AGENTS.md`, `CLAUDE.md` and similar), architecture docs and the directory structure.
2. **Find what the story touches:** screens and components, routes, endpoints and their request and response models, events, domain entities, validations, business rules, permissions and roles, tables and columns, feature flags, texts shown to users and their translations. Search by the story's own words, by the names of the entities it mentions and by user-visible texts.
3. **Note the current behavior** that the story relies on or changes: a validation that already exists, a field that is required, a status the entity can't have, a role that can't see the screen.
4. **Note contradictions and overlaps:** the story asks for something the code already does, or something it doesn't allow, or something another part of the code does differently.

Don't go deeper than the refinement needs. The full impact analysis belongs to `change-impact-analysis`.

## 3. Diagnose

Go through the areas in `references/readiness-checklist.md` and give each one a status:

- ✅ **Clear:** the story says it, and it's consistent with the code.
- ⚠️ **Ambiguous:** the story says it, but it can be read in more than one way, or it contradicts the code.
- ❌ **Missing:** the story doesn't say it, and the implementation needs it.
- ➖ **Not applicable.**

Check also the size: if the story covers several independent behaviors, several user types or several components that could be delivered separately, propose splitting it, with a title and a one-line goal for each part.

## 4. Ask

Ask the questions whose answer changes what gets built or how it's verified, in **at most two rounds**.

**First round:** one message with:

- A short diagnosis: the restated story, the components found, and the ⚠️ and ❌ areas in one line each.
- The questions, **at most eight**, most important first, **grouped by who should answer them**: product or business, design or UX, technical, another team or third party.

For each question:

- Base it on what you found in the code, not on generic templates. For example: "The API rejects orders without `shippingAddress` (`OrderValidator.java:58`), but the story allows pickup in store. Should pickup orders skip that validation?".
- Say why it matters, in a few words.
- Mark it as **blocking** if the story can't be implemented without the answer.
- Propose an answer: the one you'd choose.

Tell the user they can answer some questions, all of them, or none, and that anything without an answer becomes an assumption (if it has a proposed answer and isn't blocking) or an open question. Many answers depend on people who aren't in the conversation: that's expected, and the open questions are meant to be taken to them.

**Second round:** only if the answers raise new questions or contradict each other or the code, and only with those questions (at most four). If the first round left nothing new, skip it. Never a third round: whatever is still unanswered becomes an assumption or an open question.

If the story is clear and nothing is ambiguous, skip the questions, say so, and go to step 5.

## 5. Write and deliver

Write the refined story with the structure in `references/story-template.md`. Then give the verdict:

- ✅ **Ready:** no area is ❌ or ⚠️, and there are no open questions.
- ⚠️ **Ready with assumptions:** no blocking question is open; the remaining gaps are covered by assumptions or non-blocking open questions.
- ❌ **Not ready:** at least one blocking question is open, or the acceptance criteria can't be written.

Before delivering, check that:

1. Every acceptance criterion is observable and verifiable, and the criteria cover the main flow, the alternatives and the errors that the story or the code implies.
2. Every decision comes from an answer or is marked as an assumption.
3. Every technical note and contradiction has a location in the code.
4. The functional part has no code paths or internal names that the team wouldn't understand.
5. Nothing contradicts the answers the user gave.

In the conversation, show the verdict with its reason, the functional part of the refined story (ready to copy into the issue tracker), the open questions, and a summary of the technical notes in a few lines. The full content goes to the file.

At the end, offer the next steps:

- Take the open questions to the people who should answer them, and come back with the answers or a new version of the story to update the refinement.
- Analyze the impact and effort of the story (for example, with the `change-impact-analysis` skill, if it's installed).
- Implement it. Don't start without the user's approval.

## 6. Save the refined story

Always save it: the file is the deliverable.

**Location:** `.stories/<story>.md`, in this folder:

- **Single-project repository:** the root of the repository.
- **Monorepo, story in one component:** the root folder of that microservice, app or package (for example, `services/orders/.stories/`).
- **Monorepo, story in several components:** the root of the repository.
- **Several repositories:** the root of the current repository (the one the conversation started in). List every repository in the file's header.
- **Without git:** the project's root folder.

From here on, `<folder>` is that folder.

- `<story>` is the ID followed by a short kebab-case title, in English (`PROJ-123-export-orders-csv`), or only the title if the story has no ID.
- If a file with that name exists but belongs to a different story, ask for another name.

**Keep stories out of git.** They're working files and must never be committed or pushed. Before writing the file:

1. Check whether the folder is ignored: `git check-ignore -q <folder>/.stories/`.
2. If it isn't, add `.stories/` to a `.gitignore`: the one in `<folder>` if it has one, otherwise the one at the root of the repository (create it if it doesn't exist). Put it on its own line with a comment: `# Refined user stories (refine-user-story)` followed by `.stories/`. In the root `.gitignore`, the pattern has no leading `/`, so it also covers the `.stories/` folders of the other services in a monorepo. Don't change anything else in the file.
3. Tell the user which `.gitignore` changed and that they need to commit it. Don't commit it yourself.
4. If `.stories/` was already committed (`git ls-files <folder>/.stories` lists files), ignoring it isn't enough: warn the user and suggest `git rm -r --cached <folder>/.stories` to stop tracking it without deleting the files.

**Tell the user where the file is.** When it's written, give its path relative to the root of the repository and its absolute path, for example: "The refined story is in `.stories/PROJ-123-export-orders-csv.md` (`/home/user/projects/shop/.stories/PROJ-123-export-orders-csv.md`)".

## Update a refined story

Use this flow when a `.stories/` file already exists for the story and the user brings a new version of its text (for example, after the product owner changed it), answers to open questions, or both.

1. **Read the saved file:** the refined story, decisions, assumptions, open questions and the original text.
2. **Compare the new text with the previous original.** List what was added, removed or changed, in a few lines.
3. **Review the earlier decisions and assumptions.** Keep the ones that still hold, update the ones the new text or the answers settle, and drop the ones that no longer apply, saying why.
4. **Check the code again only where the changes land.** If the code changed since the last refinement (compare with the commit in the header), check whether that changes any technical note.
5. **Diagnose again** and ask only the new questions, with the same rule of at most two rounds.
6. **Update the file:** new refined story, version number plus one, the new text in "Original story", the previous original inside the history entry, and a line in the history saying what changed. Don't create a new file.
7. **Deliver** as in step 5, starting with what changed since the previous version and whether the verdict changed.

If the user brings only answers, without a new text, skip steps 2 and 4.

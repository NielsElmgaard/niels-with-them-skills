---
name: grill-and-align
description: Extracts underlying intent, stress-tests architecture, scopes the MVP, and records living project documentation (GLOSSARY.md and ADRs) through a Socratic grilling interview before technical specification. Use when starting a new feature, exploring ambiguous requirements, or resolving design trade-offs before drafting specs or code.
---

# Grill and Align

A structured, repo-aware discovery and architectural grilling process that transforms raw requests into validated intent, established domain vocabulary, and documented architectural decisions before any code or spec is written.

## Overview

What users ask for and what they actually need are rarely identical. Users frequently ask for conventional solutions ("build a dashboard", "make it scalable") when their real problem requires something simpler. Jumping straight into specs or code locks in misalignment at the highest cost.

`grill-and-align` represents **Stage 1 (Intent & Alignment)** of the AI-Native SDLC. It inspects your codebase first, stress-tests requirements through a one-question-at-a-time design tree interview, establishes canonical domain terms in `GLOSSARY.md`, captures irreversible trade-offs in Architecture Decision Records (`docs/adr/`), and locks down the MVP scope and "Not Doing" list in a confirmed `docs/intent/<feature>.md`.

## When to Use

Use this skill when:
- Starting a new feature, capability, or major architectural refactor.
- Requirements are underspecified (missing target persona, success criteria, or binding constraints).
- The request relies on buzzwords or conventions ("clean architecture", "dashboard", "faster") without concrete targets.
- Facing high-stakes architectural forks that require permanent documentation (ADRs).
- Establishing or updating ubiquitous language in the codebase.
- Explicitly invoked via phrases like: `"grill me"`, `"interview me"`, `"align intent"`, `"stress-test my thinking"`, or `"before we start, are we sure?"`.

When NOT to use:
- Unambiguous, self-contained mechanical changes (bug fixes with clear reproduction, typo fixes, variable renames).
- Designing detailed type schemas, REST/GraphQL endpoints, or module interfaces after intent is settled (use [design-api-and-interface](../design-api-and-interface/SKILL.md)).
- Generating task tickets or dependency graphs (use downstream planning skills).
- Non-interactive or headless execution environments (CI runs, scheduled cron tasks).

## Core Workflow

```
[1. Repo Context Check] ──> [2. Socratic Grilling] ──> [3. Real-Time Docs] ──> [4. Scope & "Not Doing"] ──> [5. Terminal Intent Gate]
```

---

### Step 1: Repo Context & Prior Art

Never ask the user a question the codebase can already answer.

1. **Scan Existing Architecture**: Search for existing models, routes, or utilities touching the topic using directory listings and targeted file searches.
2. **Consult Existing Documentation**:
   - Check `GLOSSARY.md` for settled domain terms.
   - Check `docs/adr/` for historical decisions and architectural constraints.
3. **Anchor the Topic**: Formulate your initial understanding based on the delta between what exists and what is being asked.

---

### Step 2: Socratic Design-Tree Interview

Follow a strict, one-question-at-a-time interview loop to systematically prune the decision tree.

1. **State Hypothesis and Confidence**:
   Before asking a question, explicitly state your current read and an honest confidence score (0–100%):
   ```markdown
   HYPOTHESIS: You want an automated export of transaction history because accounting is manually reconciling CSVs at month-end.
   CONFIDENCE: ~40% — missing: who triggers the export, format requirements, and delivery destination.
   ```
   *Rule:* If confidence is below ~70%, append a concise note on the same line explaining what is missing.

2. **Ask One Question at a Time with an Attached Guess**:
   ```markdown
   Q: Who is the primary consumer of this export, and how often will they run it?
   GUESS: The finance team once a month during closing, meaning a background batch job is better than real-time streaming.
   ```
   *Why attach a guess?* Users react faster and more accurately to a visible hypothesis than generating requirements from an empty prompt.

3. **Probe "Want vs. Should Want"**:
   Listen for convention-signaling answers (*"we should probably make it a microservice"*, *"industry standard is GraphQL"*, *"make it scalable"*). When detected, probe directly:
   > *"If you didn't have to justify this architecture to anyone else, what is the simplest solution you would actually want?"*

4. **The 95% Confidence Stop Rule**:
   Continue the single-question loop until you can answer **YES** to:
   > *Can I accurately predict the user's reaction to the next three questions I would ask?*

---

### Step 3: Real-Time Living Documentation

Do not wait until the end of the session to write documentation. Document choices the moment they crystallize.

#### 1. Ubiquitous Vocabulary (`GLOSSARY.md`)
The moment a term's definition is agreed upon, update or append to `GLOSSARY.md` at the project root:
```markdown
### [Term Name]
**Definition**: One concise paragraph defining what the term means in this project.
**Distinction**: Explicitly state what this term is NOT (to avoid semantic collision with existing concepts).
```
*Rule:* Keep `GLOSSARY.md` strictly as domain vocabulary. No implementation details, test notes, or file paths.

#### 2. Architecture Decision Records (`docs/adr/NNNN-<slug>.md`)
If and only if a decision satisfies all three criteria:
1. **Hard to reverse** (high cost to undo later).
2. **Surprising without context** (a future developer would wonder "why did they do that?").
3. **Involves real trade-offs** (chose benefit A at the expense of drawback B).

Create an ADR in `docs/adr/` following standard format (Status, Context, Decision, Consequences). If a decision does not meet all three gates, it belongs in the conversation or the downstream spec, not in an ADR.

---

### Step 4: MVP Scoping & The "Not Doing" List

Great intent definition is defined by what is left out.

1. **Find the 10x Simpler Slice**: Challenge complexity. What is the minimal slice that validates the core assumption?
2. **Define the "Not Doing" Boundary**: Explicitly document good ideas that are intentionally deferred to future iterations.
3. **Log Open Technical Spikes for Stage 2**:
   Record unresolved technical questions that require code inspection or prototyping during the specification phase (e.g., verifying third-party rate limits, schema column nullability).

---

### Step 5: Terminal Intent Gate & Stop Rule

When intent is locked, produce the final **Statement of Intent** and hand control back to the user.

1. **Present the Statement of Intent**:
   ```markdown
   ## Statement of Intent: [Feature Name]

   - **Problem Statement**: [One crisp sentence describing the human problem]
   - **Target Persona**: [Who specifically uses this]
   - **Why Now**: [The immediate trigger or business driver]
   - **Success Criteria**: [Measurable outcome defining done]
   - **MVP Scope**: [The minimal viable slice to build]
   - **Not Doing (Non-Goals)**:
     - [Explicitly excluded capability and rationale]
   - **Binding Constraints**: [Tech stack, performance, deadlines, security]
   - **Open Technical Questions for Spec Phase**:
     - [ ] [Technical unknown to be resolved during Stage 2 specification]
   ```
2. **Offer File Persistence**:
   Offer to save the statement to `docs/intent/<feature-name>.md`. Save only upon user confirmation.
3. **CRITICAL STOP RULE**:
   Once the user confirms the intent, **STOP YOUR TURN IMMEDIATELY**.
   - Do NOT invoke downstream spec tools.
   - Do NOT start drafting code or tasks in the same turn.
   - Offer the logical next step: hand off to Stage 2 (`spec-driven-dev`).

---

### Downstream Pipeline Handoff

Following [orchestration-patterns.md](../../references/orchestration-patterns.md), transitions between stages require human confirmation. The artifacts produced here feed downstream stages:

```
grill-and-align  ──>  [Human Approval]  ──>  spec-driven-dev  ──>  make-those-tickets
(intent.md,                                  (Resolves open        (Decomposes into
 GLOSSARY.md,                                 questions into        atomic tickets)
 docs/adr/*.md)                               type contracts)
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The user's prompt was detailed, so I can skip the interview." | Detailed prompts often specify implementation mechanisms rather than the root problem. Verify the underlying intent first. |
| "I'll batch all five of my questions into one message to save time." | Batching overwhelms the user, encourages skimmed answers, and locks in faulty assumptions from the first question. Ask one at a time. |
| "Asking questions without a guess is more neutral." | A blank question forces the user to start from scratch. A concrete guess gives them something to quickly confirm, refute, or refine. |
| "I'll write the ADR and glossary after the code is working." | Decisions made during implementation are forgotten or undocumented. Documenting them live establishes the boundary before code is typed. |
| "The user said 'looks good', so I should immediately start building." | 'Looks good' closes Stage 1. Respect the terminal stop rule and allow the human to authorize the transition to Stage 2 (Spec). |

---

## Red Flags

- Asking three or more questions in a single conversational turn.
- Asking a question without providing an explicit hypothesis and rationale.
- Asking questions about existing types, endpoints, or file structures that can be found by searching the repository.
- Generating a spec or source code in the same turn that intent was confirmed.
- Omitting the "Not Doing" (out-of-scope) section from the Statement of Intent.
- Recording trivial implementation details as ADRs instead of reserving them for high-impact trade-offs.
- Allowing confidence score to stay below 70% across three consecutive questions without stepping back to reframe.

---

## Verification Checklist

Before completing this skill and closing Stage 1:

- [ ] Repository and existing documentation (`GLOSSARY.md`, `docs/adr/`) were inspected before interviewing.
- [ ] Questions were asked one at a time, each accompanied by an explicit hypothesis and guess.
- [ ] Probed for true desire when the user relied on buzzwords or standard conventions.
- [ ] Reached ≥95% confidence on underlying intent (able to predict reactions to follow-up questions).
- [ ] Newly resolved domain terms were recorded in `GLOSSARY.md`.
- [ ] Any high-stakes architectural trade-offs meeting all three criteria were written to `docs/adr/`.
- [ ] An explicit "Not Doing" list was established.
- [ ] Technical spikes and unresolved contract questions were documented for Stage 2.
- [ ] Statement of Intent was presented and approved by the user (saved to `docs/intent/<feature>.md`).
- [ ] Stopped turn immediately upon confirmation without triggering downstream tools.

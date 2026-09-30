---
name: make-those-tickets
description: Decomposes approved technical specifications into small, dependency-ordered, verifiable task tickets. Generates scoped work units with test acceptance criteria, rollback plans, and file targets. Use after spec approval, before planning individual tickets, or when invoked with "make those tickets", "break into tickets", or "create tasks".
---

# Make Those Tickets!

A structured task decomposition and planning workflow that translates technical specifications into dependency-ordered, verifiable tickets sized for incremental execution and review.

## Overview

Large, monolithic tasks overwhelm an AI agent's context window, create messy git commits, and produce unreviewable pull requests. Attempting to build an entire feature in one leap leads to regressions, lost save points, and untracked assumptions.

`make-those-tickets` represents **Stage 3 (Plan with Tickets)** of the AI-Native SDLC. It ingests an approved `docs/specs/<feature>-spec.md`, maps dependencies, sizes tasks into atomic slices (~100–300 lines of change), defines deterministic test acceptance criteria, and generates individual ticket files in `docs/tasks/<feature>/` ready for individual ticket preparation via [plan-that-ticket](../plan-that-ticket/SKILL.md) and incremental implementation via [tdd-implement](../tdd-implement/SKILL.md).

## When to Use

Use this skill when:
- A technical specification has been reviewed and approved (`docs/specs/<feature>-spec.md` exists).
- Breaking down a complex feature, schema migration, or multi-component refactor into ordered, testable steps.
- Sizing work units to fit the ~100–300 line diff sweet spot required by [review-that-code](../review-that-code/SKILL.md).
- Explicitly invoked via phrases like: `"make those tickets"`, `"break into tickets"`, `"plan tasks"`, or `"create implementation tickets"`.

When NOT to use:
- The technical specification or type contracts are still unwritten or ambiguous (use [spec-driven-dev](../spec-driven-dev/SKILL.md)).
- Product intent, problem framing, or scope boundaries are unresolved (use [grill-and-align](../grill-and-align/SKILL.md)).
- Actively executing code changes or writing tests (use [git-keeper](../git-keeper/SKILL.md)).
- Evaluating diffs or pull requests (use [review-that-code](../review-that-code/SKILL.md)).

## Core Workflow

```
[1. Ingest Spec] ──> [2. Resolve Rollout Risks] ──> [3. Slice Vertical Tasks] ──> [4. Define Verification] ──> [5. Ticket Gate]
```

---

### Step 1: Ingest Spec & Map Capabilities

Read the specification and identify logical components:

1. **Load Upstream Artifacts**:
   - Primary: `docs/specs/<feature>-spec.md`
   - Context: `docs/intent/<feature>.md` (to verify non-goals and scope boundaries)
   - Vocabulary: `GLOSSARY.md`
2. **Extract Capability Boundaries**:
   - Identify data models / schemas, domain services, interface endpoints, and test suites.
   - Map dependency direction: what depends on what? What must exist first before downstream layers can compile?

---

### Step 2: Resolve Sequencing & Rollout Risks

If the spec involves breaking changes, migrations, or rollout complexity, resolve sequencing before creating tickets.

Follow the **Rule for Operational Inquiries**:
- Check if [phasing-out-and-migration](../phasing-out-and-migration/SKILL.md) applies (e.g. expand/contract for zero-downtime DB changes).
- Never ask open-ended questions. Present closed options with an operational recommendation:
  ```markdown
  Operational clarification for Task 1:
  - Option A (Recommended): Dual-write migration (add nullable column first, backfill, make required later) per phasing-out-and-migration.
  - Option B: Single-step table migration during planned downtime.
  Recommendation: Option A to ensure zero-downtime deployment. Do you approve?
  ```

---

### Step 3: Slice Vertical Tasks (~100–300 Lines)

Decompose the work into discrete, incremental slices following [orchestration-patterns.md](../../references/orchestration-patterns.md):

1. **Enforce Diff Sizing Limits**:
   - Each task should result in approximately **100–300 lines of change**.
   - No single task should touch more than **~5 files**.
2. **Favor Vertical Slices over Horizontal Layers**:
   - Avoid purely abstract plumbing that cannot be verified.
   - Where possible, pair a data layer change with its test, or a service method with its unit verification.
3. **Establish Dependency Order**:
   - Order tasks topologically: Task `N+1` should only depend on tasks `1..N`.
   - Identify which tasks are decoupled and could be parallelized across git worktrees (Pattern 2 in [orchestration-patterns.md](../../references/orchestration-patterns.md)).

---

### Step 4: Define Deterministic Acceptance & Verification

Every ticket must have non-negotiable exit criteria. Never write a ticket with vague instructions like *"make sure it works"*.

Each ticket must specify:
1. **Target Files**: Exact files to create, modify, or delete.
2. **Test Criteria**: Specific test scenarios from the spec to implement or run.
3. **Execution Command**: The exact verification command (e.g., `npm test tests/unit/payment.test.ts`, `npm run lint`).
4. **Definition of Done Check**: Alignment with [definition-of-done.md](../../references/definition-of-done.md).

---

### Step 5: Output Version-Controlled Tickets

Generate the plan index and individual ticket files in `docs/tasks/<feature>/`:

1. **Master Plan Index (`docs/tasks/<feature>/README.md`)**:
   ```markdown
   # Implementation Plan: [Feature Name]

   - **Spec Reference**: [docs/specs/<feature>-spec.md](../../specs/<feature>-spec.md)
   - **Total Tasks**: [N]
   - **Dependency Graph**:
     ```
     Task 01 (Schema) ──> Task 02 (Service Core) ──> Task 03 (API Route)
                                                └──> Task 04 (Integration E2E)
     ```

   ## Ticket Breakdown
   - [ ] [01-data-model.md](./01-data-model.md): [Brief summary]
   - [ ] [02-domain-service.md](./02-domain-service.md): [Brief summary]
   - [ ] [03-api-endpoint.md](./03-api-endpoint.md): [Brief summary]
   ```

2. **Individual Ticket Format (`docs/tasks/<feature>/<NN>-<slug>.md`)**:
   ```markdown
   # Ticket [NN]: [Task Title]

   ## 1. Context & Scope
   - **Prerequisites**: [Preceding ticket numbers that must be completed]
   - **Goal**: [Specific capability delivered by this ticket]
   - **Estimated Diff**: [e.g., ~150 lines, 3 files]

   ## 2. File Targets
   - Modify: `src/models/user.ts`
   - Create: `src/services/billing.ts`
   - Test: `tests/services/billing.test.ts`

   ## 3. Acceptance Criteria
   - [ ] Implements [contract/method] according to spec section 2.
   - [ ] Handles edge case: [null input / invalid token / error code].
   - [ ] All new logic accompanied by automated tests per testing-patterns.md.

   ## 4. Verification Command
   ```bash
   npm test tests/services/billing.test.ts
   npm run typecheck
   ```

   ## 5. Git Save Point Guidance
   - Commit message: `feat(billing): add core billing calculation service`
   - Branch/Worktree: Follow git-keeper conventions.
   ```

---

### Step 6: Terminal Gate & Stop Rule

Following [orchestration-patterns.md](../../references/orchestration-patterns.md), transitions between stages require human confirmation.

1. **Present the Plan Summary**:
   Provide the user with the ordered task list, dependency sequence, and verification commands.
2. **CRITICAL STOP RULE**:
   **STOP YOUR TURN IMMEDIATELY** once the plan and tickets are generated.
   - Do NOT begin executing Ticket 01 in the same turn.
   - Hand control back to the user to review the ticket sequence and authorize the transition to Stage 4 (Implementation via [git-keeper](../git-keeper/SKILL.md)).

---

### Downstream Pipeline Handoff

```
spec-driven-dev   ──>   make-those-tickets   ──>   [Human Approval]   ──>   git-keeper + TDD
(docs/specs/*.md)       (docs/tasks/*)                                  (Executes ticket 01,
                                                                         commits save point)
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The spec is already broken into sections, so tickets are redundant." | Specs describe the contract; tickets describe the *execution slices*, exact target files, and test commands. |
| "I'll make one big ticket for the whole backend and one for the frontend." | Multi-component tickets exceed 500 lines, mix concerns, and fail review under [review-that-code](../review-that-code/SKILL.md). |
| "I don't need verification commands for small tasks." | Without an executable verification command, agents cannot verify their own work, leading to broken intermediate commits. |
| "I generated the tickets, so I should immediately implement Ticket 1." | Stage transitions are human checkpoints. The human must review the breakdown and authorize the implementation loop. |

---

## Red Flags

- Creating tickets that touch more than 5 distinct files or exceed ~300 lines of estimated diff.
- Tickets with subjective acceptance criteria (*"make it performant"*, *"ensure UI looks nice"*).
- Tickets missing concrete verification commands (e.g. test or build commands).
- Circular dependencies between tickets (Task A requires Task B, but Task B touches files from Task A).
- Starting code implementation in the same turn tickets were generated.

---

## Verification Checklist

Before completing this skill and closing Stage 3:

- [ ] Spec document (`docs/specs/<feature>-spec.md`) was ingested and referenced.
- [ ] Operational and migration risks were evaluated (consulting [phasing-out-and-migration](../phasing-out-and-migration/SKILL.md) if needed).
- [ ] Work decomposed into vertical slices sized between 100–300 lines of diff.
- [ ] Dependency sequence is topological (no circular prerequisites).
- [ ] Each ticket file in `docs/tasks/<feature>/` defines exact file targets, acceptance criteria, and verification commands.
- [ ] Plan index generated at `docs/tasks/<feature>/README.md`.
- [ ] Stopped turn immediately upon presenting the plan, waiting for user confirmation before starting implementation.

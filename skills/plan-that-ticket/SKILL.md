---
name: plan-that-ticket
description: Prepares an individual task ticket for implementation by isolating context, inspecting target files, and generating a detailed micro-plan (plan.md). Use when picking up a ticket from make-those-tickets, before writing code, or when invoked with "plan that ticket", "plan ticket", or "prepare ticket".
---

# Plan That Ticket!

A targeted preparation workflow that takes a single ticket from the master plan, isolates its context, inspects target files, and generates a concrete micro-implementation plan (`plan.md`) ready for test-driven execution.

## Overview

Loading an entire feature spec and full codebase history into an agent's context when working on a single ticket causes distraction, high token usage, and out-of-scope edits. A ticket describes *what* needs to be built and *which files* to touch, but jumping straight into code without a micro-plan leads to skipped tests and messy implementations.

`plan-that-ticket` acts as the **Ticket Preparation Gate** in Stage 4 (Implementation). It loads *only* the active ticket (`docs/tasks/<feature>/<NN>-<slug>.md`) and its immediate spec requirements, inspects the target source and test files, breaks the ticket down into 2–4 Red-Green-Refactor micro-steps, and outputs a concrete `plan.md` to be executed by [tdd-implement](../tdd-implement/SKILL.md).

## When to Use

Use this skill when:
- Starting work on an individual ticket produced by [make-those-tickets](../make-those-tickets/SKILL.md).
- Preparing a concrete, low-level execution plan (`plan.md`) before writing any test or implementation code.
- Scoping context to only the target files required for the current ticket.
- Explicitly invoked via phrases like: `"build that ticket"`, `"prepare ticket"`, `"plan ticket 01"`, or `"start ticket"`.

When NOT to use:
- Generating the high-level feature breakdown and initial tickets (use [make-those-tickets](../make-those-tickets/SKILL.md)).
- Actively executing the TDD cycle, running tests, or writing code (use [tdd-implement](../tdd-implement/SKILL.md)).
- Reviewing completed ticket pull requests or diffs (use [review-that-code](../review-that-code/SKILL.md)).

## Core Workflow

```
[1. Ingest Ticket] ──> [2. Inspect Target Files] ──> [3. Draft Micro-Steps] ──> [4. Output plan.md] ──> [5. Handoff Gate]
```

---

### Step 1: Ingest Ticket & Isolate Context

Keep the context window clean by loading only what is strictly necessary for this ticket:

1. **Read the Target Ticket**: Load `docs/tasks/<feature>/<NN>-<slug>.md`.
2. **Read Associated Spec Slice**: Read *only* the specific section of `docs/specs/<feature>-spec.md` that defines the contract for this ticket. Do NOT load unrelated spec sections.
3. **Verify Prerequisites**: Confirm that any preceding tickets listed under `Prerequisites` have been completed.

---

### Step 2: Inspect Target Files & Existing Seams

Inspect the codebase reality before writing the micro-plan:

1. **Inspect Target Files**: Read each file listed under `File Targets` in the ticket.
   - Note existing export patterns, type imports, and function signatures.
   - Verify that target file paths actually exist (or confirm they are marked to be created).
2. **Inspect Existing Test Utilities**:
   - Locate adjacent test files to identify testing libraries (e.g., Vitest, Jest, Pytest), assertion helpers, and fixtures.
   - Respect patterns documented in [testing-patterns.md](../../references/testing-patterns.md).

---

### Step 3: Decompose into TDD Micro-Steps

Break the ticket into 2–4 sequential micro-steps. Each micro-step represents a single Red-Green-Refactor loop:

1. **Step A: Test Specification (Red)**:
   - What specific test case will be written first?
   - What is the test function name, input data, and expected assertion?
   - How will we confirm the test fails for the right reason?
2. **Step B: Implementation Delta (Green)**:
   - What minimal code change (new function, type extension, handler) will satisfy the test?
3. **Step C: Refactor & Clean**:
   - What typing, formatting, or extraction needs to happen once green?

---

### Step 4: Write `plan.md` for the Ticket

Save the execution plan to `docs/tasks/<feature>/<NN>-<slug>/plan.md` (or alongside the ticket as `<NN>-<slug>-plan.md`):

```markdown
# Micro-Plan: Ticket [NN] - [Title]

- **Ticket Reference**: [docs/tasks/<feature>/<NN>-<slug>.md](../<NN>-<slug>.md)
- **Target Files**:
  - `src/services/billing.ts` (Modify)
  - `tests/services/billing.test.ts` (Create/Modify)
- **Deterministic Verify Command**: `npm test tests/services/billing.test.ts`

---

## Micro-Steps (Red -> Green -> Refactor)

### Step 1: [First Capability, e.g. Input Validation]
- **RED (Test)**: Add test case `rejects negative transaction amounts with InvalidAmountError` in `tests/services/billing.test.ts`. Verify failure.
- **GREEN (Code)**: Add amount validation check in `calculateTotal()` in `src/services/billing.ts`. Verify pass.
- **REFACTOR**: Ensure error matches domain error taxonomy from GLOSSARY.md.

### Step 2: [Second Capability, e.g. Tax Calculation]
- **RED (Test)**: Add test case `calculates 20% VAT for standard taxable items`. Verify failure.
- **GREEN (Code)**: Implement tax calculation formula in `calculateTotal()`. Verify pass.
- **REFACTOR**: Extract tax rate constant to configuration module.

---

## Verification & Save Point
- [ ] Run full ticket verification command: `npm test tests/services/billing.test.ts && npm run typecheck`
- [ ] Git commit message: `feat(billing): implement tax and validation logic for ticket [NN]`
```

---

### Step 5: Terminal Gate & Handoff to `tdd-implement`

Following [orchestration-patterns.md](../../references/orchestration-patterns.md), transitions require user visibility:

1. Present the micro-plan summary to the user.
2. Confirm the test cases and file targets are aligned with expectations.
3. Hand off execution to [tdd-implement](../tdd-implement/SKILL.md) to run the Red-Green-Refactor loops.

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The ticket is small enough, I don't need a plan.md." | Small tickets still fail if you implement before designing the test. A 10-line micro-plan guarantees test-first discipline. |
| "I should load the entire spec and all previous tickets." | Flooding the context window with the entire repository history degrades agent focus and invites hallucinations. Isolate context. |
| "I can skip inspecting existing test files." | Without inspecting existing tests, agents introduce foreign assertion libraries or inconsistent mocking patterns. |
| "I'll plan the code first, and figure out the tests later." | That is implementation-first, not test-driven. The micro-plan must define the RED test before the GREEN code. |

---

## Red Flags

- Generating a micro-plan that introduces new dependencies or files not authorized by the upstream ticket.
- Writing a micro-plan without specifying the exact test assertion for each step.
- Planning all code changes before any test steps.
- Attempting to execute the code within this skill instead of handing off to `tdd-implement`.

---

## Verification Checklist

Before completing this skill and handing off to implementation:

- [ ] Target ticket ingested and prerequisites confirmed complete.
- [ ] Target source and test files inspected for existing patterns.
- [ ] Ticket decomposed into 2–4 sequential Red-Green-Refactor micro-steps.
- [ ] Each micro-step defines the failing test first, followed by the minimal code change.
- [ ] Deterministic verification command from the ticket is preserved.
- [ ] `plan.md` written and presented for user review before invoking `tdd-implement`.

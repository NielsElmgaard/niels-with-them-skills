---
name: spec-driven-dev
description: Synthesizes confirmed intent, architectural decisions, and domain vocabulary into a rigorous technical specification. Resolves open technical questions, defines API and type contracts, establishes test seams, and defines execution boundaries. Use after intent alignment, before task planning or coding, or when invoked with "write spec" or "draft spec".
---

# Spec-Driven Development

A structured, contract-first process that translates validated intent into an actionable, unambiguous technical specification before decomposing tasks or writing implementation code.

## Overview

The most expensive bugs are not syntax errors; they are mismatched assumptions about interfaces, schemas, and failure states. Moving directly from high-level intent to writing code causes agents to invent contracts on the fly, introduce subtle type leaks, and tangle business logic with plumbing.

`spec-driven-dev` represents **Stage 2 (Specification)** of the AI-Native SDLC. It ingests the confirmed `docs/intent/<feature>.md`, burns down open technical questions through targeted codebase inspection, defines strict type contracts (leveraging [design-api-and-interface](../design-api-and-interface/SKILL.md)), maps testing seams ([testing-patterns.md](../../references/testing-patterns.md)), and establishes three-tier execution boundaries before saving a version-controlled `docs/specs/<feature>-spec.md`.

## When to Use

Use this skill when:
- Stage 1 intent is confirmed (`docs/intent/<feature>.md` exists or the user gave clear, scoped requirements).
- Resolving technical ambiguities, schemas, type contracts, and failure modes before writing code.
- Defining integration points, database migrations, or public API endpoints for a feature.
- Explicitly invoked via phrases like: `"write spec"`, `"draft spec"`, `"spec this out"`, or `"create technical specification"`.

When NOT to use:
- Intent, target user, or problem statement is still ambiguous or unvalidated (use [grill-and-align](../grill-and-align/SKILL.md)).
- Decomposing an already approved specification into ticketed work units (use downstream task-planning skills).
- Writing code or executing tests (use [git-keeper](../git-keeper/SKILL.md)).
- Reviewing pull requests or uncommitted diffs (use [review-that-code](../review-that-code/SKILL.md)).

## Core Workflow

```
[1. Context Ingestion] ──> [2. Burn Down Open Questions] ──> [3. Interface Contracts] ──> [4. Test Seams] ──> [5. Spec Gate]
```

---

### Step 1: Context Ingestion & Prior Art

Gather existing project invariants before drafting any specification:

1. **Read Intent Artifacts**: Load `docs/intent/<feature>.md` (or the confirmed statement of intent from the current conversation).
2. **Review Domain Language & Decisions**:
   - Check `GLOSSARY.md` to ensure consistent entity names.
   - Check `docs/adr/` for applicable architectural decisions.
3. **Inspect Relevant Codebase Patterns**:
   - Locate adjacent routes, schemas, models, or service boundaries.
   - Note existing error envelope formats, validation libraries (e.g. Zod, Pydantic), and database patterns.

---

### Step 2: Burn Down Open Technical Questions

Stage 1 intentionally leaves technical spikes and edge-case questions open. Stage 2 must eliminate them.

Follow the **Three Rules for Technical Clarifications**:

1. **Codebase First**: Check if the codebase already answers the question (e.g., existing enum values, table indexes, error codes). If code answers it, adopt that pattern without asking the user.
2. **Never Re-litigate Upstream Intent**: Do not ask *"Why are we building this?"* or *"Who is the user?"*. Intent is settled. Only clarify technical contracts, edge cases, and failure modes.
3. **Closed Options with Recommendations**: Never ask open-ended questions like *"How should we handle errors?"*. Always provide concrete options and a recommendation:
   ```markdown
   Stage 1 left open: Handling duplicate email registrations during import.
   - Option A (Recommended): Return 409 Conflict with detailed item error payload, matching `src/api/errors.ts`.
   - Option B: Silently skip duplicates and return a summary count in 200 OK.
   Recommendation: Option A to preserve idempotent auditing. Do you approve?
   ```

---

### Step 3: Define Interface & Data Contracts

Every spec must define unambiguous interface boundaries. Follow the principles in [design-api-and-interface](../design-api-and-interface/SKILL.md):

1. **Exact Type Signatures**: Write explicit TypeScript, Python, or Go types for inputs, outputs, and internal domain states. Avoid loose types (`any`, generic `dict`).
2. **Boundary Validation**: Specify validation schemas (e.g., required fields, string lengths, regex patterns, enum sets) that run at the system edge.
3. **Explicit Error Envelopes**: Define status codes, machine-readable error codes (e.g., `RESOURCE_NOT_FOUND`, `INVALID_PAYLOAD`), and error payload schemas.

---

### Step 4: Map Testing Seams & Failure Modes

Define how the implementation will be verified without relying on excessive mocking. Follow [testing-patterns.md](../../references/testing-patterns.md):

1. **Identify the Highest Test Seam**:
   - Prefer testing through the public API or service boundary (HTTP endpoint, CLI entry point, or exported service function).
   - Avoid creating artificial seams deep inside private implementation details.
2. **Document Required Test Cases**:
   - **Happy Path**: Core user story scenarios.
   - **Edge Cases**: Empty collections, null fields, boundary numbers, unusual characters.
   - **Failure Paths**: Timeout, unauthorized access, invalid input, database constraint violation.

---

### Step 5: Establish Operational Boundaries

Define what an executing agent is and is not permitted to do during implementation:

- **Always**: Run tests before committing, follow naming conventions from `GLOSSARY.md`, validate inputs at boundaries.
- **Ask First**: Modifying existing database tables, adding external dependencies, changing global configurations.
- **Never**: Commit credentials, alter unrelated files, bypass type checking, or remove failing tests without approval.

---

### Step 6: Produce Spec & Terminal Approval Gate

Synthesize the specification into a single document and present it for user review.

1. **Write the Spec Document**: Save to `docs/specs/<feature-name>-spec.md`.
2. **Spec Document Format**:
   ```markdown
   # Spec: [Feature Name]

   ## 1. Context & Objectives
   - **Intent Reference**: [Link to docs/intent/<feature>.md]
   - **Goal**: [Crisp summary of what this technical specification delivers]
   - **Non-Goals**: [Explicit exclusions carried over from intent]

   ## 2. Domain & Schema Contracts
   - **Glossary Terms Used**: [Referenced terms from GLOSSARY.md]
   - **Types & Interfaces**:
     ```typescript
     // Exact types and payload contracts
     ```
   - **Validation Rules**: [Input constraints, required fields, formats]
   - **Error Handling**: [Status codes, error types, error responses]

   ## 3. Architecture & Data Flow
   - **Affected Components**: [Existing and new files/modules]
   - **ADRs Applied**: [Relevant ADR numbers from docs/adr/]
   - **Database Changes**: [New tables, columns, indexes, or migrations (if applicable)]

   ## 4. Testing Strategy
   - **Test Seam**: [Public interface where automated tests will execute]
   - **Coverage Scenarios**:
     - [ ] Happy path scenario
     - [ ] Validation failure scenario
     - [ ] Downstream outage / edge case scenario

   ## 5. Execution Boundaries
   - **Always**: [...]
   - **Ask First**: [...]
   - **Never**: [...]
   ```

3. **CRITICAL STOP RULE**:
   Following [orchestration-patterns.md](../../references/orchestration-patterns.md), **STOP YOUR TURN IMMEDIATELY** once the spec is drafted and presented.
   - Do NOT immediately generate task tickets.
   - Do NOT begin coding in the same turn.
   - Wait for explicit user confirmation (`"spec approved"`, `"proceed to planning"`).

---

### Downstream Pipeline Handoff

```
grill-and-align  ──>  spec-driven-dev  ──>  [Human Approval]  ──>  make-those-tickets
(Intent & ADRs)       (Contract & Types)                           (Decomposes into
                                                                    100-300 line tasks)
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The feature is simple, so writing a full spec is overkill." | Simple features still have boundary inputs, errors, and type definitions. A concise 1-page spec prevents hours of refactoring. |
| "I'll figure out the type shapes while writing the code." | Deferring types to implementation creates leaky abstractions and forces downstream refactors across multiple files. |
| "The intent doc answered everything; no spec is needed." | Intent answers *why* and *who*. The spec answers *what*, *exact data types*, and *how failure is signaled*. |
| "I have an open technical question, so I'll just pick an option silently." | Silent decisions are the primary cause of architectural drift. Present closed options with a clear recommendation. |
| "I wrote the spec, so I should start generating tickets right now." | Stage transitions are human checkpoints. The user must review and approve the technical contract before planning. |

---

## Red Flags

- Re-asking product questions (*"Who will use this?"*, *"Is this really necessary?"*) that belong in Stage 1.
- Asking open-ended questions without checking the codebase first or without providing a recommended choice.
- Omitting explicit type signatures or error response shapes from the specification.
- Defining tests that assert against private implementation details instead of public interface seams.
- Proceeding to task creation or implementation without explicit user approval of the spec.
- Modifying database schemas without explicit approval under the "Ask First" boundary.

---

## Verification Checklist

Before completing this skill and closing Stage 2:

- [ ] `docs/intent/<feature>.md` and applicable ADRs were ingested.
- [ ] All open technical spikes from Stage 1 were resolved (via code inspection or closed-choice user questions).
- [ ] Domain terms match definitions in `GLOSSARY.md`.
- [ ] Concrete types, schemas, and error envelopes were specified following [design-api-and-interface](../design-api-and-interface/SKILL.md).
- [ ] Test seams and critical test scenarios were defined following [testing-patterns.md](../../references/testing-patterns.md).
- [ ] Three-tier boundaries (Always, Ask First, Never) were documented.
- [ ] Specification was written to `docs/specs/<feature>-spec.md`.
- [ ] Stopped turn immediately upon presenting the spec, waiting for human approval before moving to Stage 3.

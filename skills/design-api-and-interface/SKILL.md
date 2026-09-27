---
name: design-api-and-interface
description: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.
---

# Design API and Interface

A practical guide for designing stable, predictable, and backward-compatible interfaces that are easy to consume and hard to misuse.

## Overview

Good interfaces establish clear contracts before implementation begins. Whether defining REST endpoints, GraphQL schemas, module boundaries, or TypeScript contracts, predictable APIs prevent coupling and ensure systems can evolve safely without breaking consumers.

## When to Use

Use this skill when:
- Designing new API endpoints or webhook payloads.
- Defining module boundaries or type contracts between services/layers.
- Structuring request/response schemas and database-to-API mappings.
- Evolving existing public interfaces while preserving backward compatibility.

When NOT to use:
- Managing phased deprecation or database migration rollouts (use `phasing-out-and-migration`).
- Reviewing implementation diffs or pull requests (use `review-that-code`).
- Code-level refactoring within internal modules.

## Core Design Workflow

```
[1. Contract First] ──> [2. Boundary Validation] ──> [3. REST & Resource Conventions] ──> [4. Error Shapes] ──> [5. Evolution & Safety]
```

### Step 1: Contract-First Definition

Define input and output contracts before writing execution logic. Keep caller input separated from server output:

```typescript
// 1. Input: What the caller provides (strictly validated)
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
}

// 2. Output: What the system returns (includes server-managed metadata)
interface Task {
  id: string;
  title: string;
  description: string | null;
  priority: 'low' | 'medium' | 'high';
  createdAt: string;
  updatedAt: string;
}
```

### Step 2: Validate at the Boundary

Treat all external input (HTTP requests, query parameters, webhooks, third-party API payloads) as untrusted. Validate immediately at the edge:

- **Edge Validation**: Use schema validators (e.g. Zod, Joi, Pydantic) in the controller or route handler.
- **Trust Internals**: Once validated at the boundary, pass strongly-typed data to internal domain logic—do not scatter redundant defensive checks throughout internal helpers.
- For boundary validation and sanitization standards, see [security-checklist.md](../../references/security-checklist.md#input-validation).

```typescript
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: { code: 'VALIDATION_FAILED', message: 'Invalid payload', details: result.error.flatten() },
    });
  }
  const task = await taskService.create(result.data);
  return res.status(201).json({ data: task });
});
```

### Step 3: Resource Conventions & REST Patterns

Design endpoints around predictable noun resources and standard HTTP methods:

- **Resource Nouns (No Verbs)**:
  - `GET /api/tasks` — List tasks
  - `POST /api/tasks` — Create a task
  - `GET /api/tasks/:id` — Fetch task details
  - `PATCH /api/tasks/:id` — Partial update (modify only supplied fields)
  - `DELETE /api/tasks/:id` — Remove task
  - `GET /api/tasks/:id/comments` — Nested sub-resource
- **Pagination & Filtering**:
  - Always paginate list endpoints: `GET /api/tasks?page=1&pageSize=20&status=open`.
  - Return standardized metadata: `{ data: [...], pagination: { page, pageSize, totalItems, totalPages } }`.
- **Naming Consistency**: Use `camelCase` for JSON payload fields and query parameters. Use `UPPER_SNAKE` for enum constants.

### Step 4: Consistent Error Semantics

Return a uniform error structure across the entire API so clients can parse failures reliably:

```typescript
interface APIErrorResponse {
  error: {
    code: string;       // Machine-readable: "NOT_FOUND", "VALIDATION_FAILED"
    message: string;    // Human-readable summary
    details?: unknown;  // Optional field-level error breakdown
  };
}
```

Standardize HTTP status codes:
- `400 Bad Request`: Malformed syntax or request parameters.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Authenticated, but lacking permission.
- `404 Not Found`: Target resource does not exist.
- `409 Conflict`: State conflict (e.g. duplicate key or version mismatch).
- `422 Unprocessable Entity`: Well-formed payload failing semantic validation.
- `500 Internal Server Error`: Unhandled server failure (never leak internal stack traces).

### Step 5: Safe Evolution & Idempotency

- **Prefer Additive Changes**: Add optional fields rather than altering or removing existing properties.
- **Support Idempotency on Critical Mutations**: For payment, ordering, or critical state-changing endpoints, accept an `Idempotency-Key` header and enforce it atomically with a database unique constraint to prevent duplicate processing on retries.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll define the exact types after writing the handler logic." | Defining contracts first catches design flaws early and prevents internal database representations from leaking into public APIs. |
| "We don't need pagination yet because we only have a few records." | Collections grow unpredictably. Unpaginated endpoints inevitably degrade into severe performance bottlenecks. |
| "It's an internal API, so consistency and status codes don't matter." | Inconsistent interfaces confuse team members, slow down development, and lead to fragile client-side error handling. |
| "PUT is simpler than PATCH." | `PUT` requires sending the full representation every time, making concurrent edits prone to accidental data loss. `PATCH` is what clients actually need. |
| "Removing this unused field won't break anything." | Any observable field in an API is likely depended on by somebody. Treat schema changes as contracts. |

## Red Flags

- Verbs in endpoint paths (`/api/createTask`, `/api/deleteUser`).
- Inconsistent response wrappers (some endpoints return arrays directly, others wrap in `{ data }`).
- List endpoints without pagination limits.
- Inconsistent error formats across different controllers or services.
- Validation logic scattered deep inside database queries or utility functions instead of at system boundaries.
- Removing or renaming fields in existing public interfaces without a deprecation plan.

## Verification Checklist

Before finalizing an API or interface design:

- [ ] Input and output interfaces are explicitly separated and strongly typed.
- [ ] Boundary validation is in place for all incoming user and external inputs.
- [ ] Endpoints use plural nouns and standard HTTP methods (`GET`, `POST`, `PATCH`, `DELETE`).
- [ ] List endpoints support pagination and filtering.
- [ ] Error responses follow a uniform `{ error: { code, message, details } }` contract.
- [ ] All schema modifications are additive and backward-compatible.
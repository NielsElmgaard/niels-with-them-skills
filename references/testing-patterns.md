# Testing Patterns Reference

A concise guide to essential testing patterns, naming conventions, boundary mocking, and anti-patterns. While examples use JavaScript/TypeScript, the principles apply universally across testing frameworks and languages.

## Test Structure (Arrange-Act-Assert)

Structure tests into three explicit steps: setup preconditions, perform the operation, and verify the expected outcome.

```typescript
it('should create a task with pending status when initialized', () => {
  // Arrange: Set up test data and preconditions
  const input = { title: 'Release v1.0', priority: 'high' };

  // Act: Execute the unit under test
  const task = createTask(input);

  // Assert: Verify expected outcome
  expect(task).toMatchObject({
    title: 'Release v1.0',
    status: 'pending',
  });
});
```

## Test Naming Conventions

Use descriptive names communicating expected behavior and trigger conditions following the `should <expected> when <condition>` pattern.

```typescript
describe('TaskService.createTask', () => {
  it('should assign pending status when task is initialized', () => {});
  it('should throw ValidationError when title is empty', () => {});
  it('should trim surrounding whitespace when title contains padding', () => {});
  it('should generate a unique ID when persisting a new record', () => {});
});
```

## Mocking Discipline

Mock only at external system boundaries (network calls, databases, filesystem, clocks). Avoid mocking internal business logic, utility functions, or domain classes, which creates fragile tests that mirror implementation rather than verifying behavior.

| Mock at System Boundaries | Do Not Mock Internal Details |
|---|---|
| HTTP / External API clients | Pure utility functions |
| Database client connections | Domain calculations & rules |
| File system I/O | Data mapping & transformations |
| System time / random seed generators | Validation schemas |

```typescript
// Mock at boundary: stub network client, exercise actual domain handler
jest.mock('./payment-gateway', () => ({
  chargeCard: jest.fn().mockResolvedValue({ id: 'txn_123', status: 'succeeded' }),
}));
```

## Integration & API Testing

Test end-to-end HTTP request/response pipelines using route-level integration testing (e.g., Supertest or fetch against test server) to verify routing, middleware, status codes, and schema contracts.

```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/tasks', () => {
  it('should return 201 with created task when payload is valid', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({ title: 'Deploy release' })
      .set('Authorization', `Bearer ${testToken}`)
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      title: 'Deploy release',
      status: 'pending',
    });
  });

  it('should return 422 when title is missing', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({})
      .set('Authorization', `Bearer ${testToken}`)
      .expect(422);

    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## Test Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|---|---|---|
| **Testing implementation details** | Tests break during refactoring even if public behavior is unchanged. | Test public interfaces, observable outputs, and boundary interactions. |
| **Brittle selectors** (e.g. CSS paths, tag hierarchies) | Incidental styling or markup refactors break tests. | Query accessible roles, semantic labels, or text visible to the user. |
| **Sleeping / arbitrary timeouts** (`sleep(1000)`) | Slows test suites and produces flaky runs under varying CI load. | Await explicit assertions, promises, or reactive state conditions. |
| **Shared mutable state** | Tests pollute each other; order-dependent failures are hard to debug. | Isolate fixtures; clean up or reconstruct state in `beforeEach`/`afterEach`. |
| **Over-mocking internal code** | Tests pass while real integrated components fail together. | Test components together; mock only external boundary I/O. |

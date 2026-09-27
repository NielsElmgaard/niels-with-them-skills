---
name: phasing-out-and-migration
description: Manages phasing out and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when migrating a database schema in production, such as renaming or dropping a column without downtime (expand/contract). Use when deciding whether to maintain or sunset existing code.
---

# Phasing Out and Migration

A practical guide for retiring legacy systems, safely migrating consumers, and executing zero-downtime database schema migrations.

## Overview

Removing code safely is as critical as adding it. Unmaintained legacy systems accumulate security liabilities, dependency drift, and technical debt. A structured migration process moves users seamlessly to new implementations and ensures old code and database structures are retired without downtime or data loss.

## When to Use

Use this skill when:
- Sunsetting an obsolete feature, API endpoint, or legacy service.
- Migrating consumers from an old interface or client to a new replacement.
- Altering production database schemas (renaming columns, dropping tables, changing constraints) with zero downtime.
- Evaluating whether to maintain legacy code or invest in full deprecation.

When NOT to use:
- Cleaning up commented-out code, dead docstrings, or phantom file paths (use `audit-align`).
- Designing new public interfaces or schemas from scratch (use `design-api-and-interface`).
- Managing code review quality gates (use `review-that-code`).

## Core Migration Process

```
[1. Replacement Ready] ──> [2. Adapter / Shims] ──> [3. Consumer Cutover] ──> [4. Verify Zero Traffic] ──> [5. Clean Removal]
```

### Step 1: Establish the Proven Replacement

Never deprecate or sunset a system without a working alternative in place:
- **Feature Parity**: Ensure the replacement covers all critical workflows of the legacy system.
- **Production Proven**: Verify the replacement is stable in production under real traffic before initiating consumer migration.
- **Migration Documentation**: Provide concise examples showing old vs new syntax and configurations.

### Step 2: Bridge Interfaces with Adapters

Decouple the backend migration from consumer updates using adapters:
- **Adapter / Shim**: Implement a lightweight wrapper matching the old interface that internally delegates to the new system.
- **Dual-Write**: When migrating stateful services, write to both systems concurrently while continuing to read from the primary.

### Step 3: Zero-Downtime Database Migrations (Expand / Contract)

Database schema alterations are the highest-risk migrations. **Never rename or drop a column in place.** Changing a column in the same deploy that updates application code causes outages while old and new instances run together.

Follow the four-phase **Expand / Contract** sequence:

```
[1. Expand] ──────────> [2. Dual-Write & Backfill] ──> [3. Switch Reads] ──────────> [4. Contract]
Add new nullable        App writes both old+new;       App reads exclusively from     Drop old column in a
column alongside old    batch-backfill existing rows   new column; keeps writing both  separate, later deploy
```

1. **Expand**: Add the new column/table as nullable. Deploy application code safely.
2. **Dual-Write & Backfill**: Update application to write to both old and new columns. Run a background, batched backfill for historical rows without locking the table.
3. **Switch Reads**: Update application code to read from the new column while maintaining dual writes. Deploy and monitor.
4. **Contract**: Stop writing to the old column. In a subsequent, separate deployment, drop the legacy column.
5. **Always Test Rollbacks**: Every migration file must include a tested down/rollback path.

### Step 4: Verify Zero Active Consumers

Before physically deleting deprecated code, prove that usage has stopped:
- Inspect request logs, telemetry, and metrics to confirm zero incoming requests.
- Search the codebase for lingering imports or references to the deprecated module.

### Step 5: Clean Code Removal

Once usage is definitively zero:
- Delete the deprecated service files, adapters, and legacy routes.
- Remove obsolete unit and integration tests associated with the retired code.
- Clean up any temporary feature flags used to manage the cutover.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The legacy code still works, so keeping it around is harmless." | Unmaintained code accumulates security vulnerabilities, breaks under toolchain updates, and confuses new team members. |
| "Users will migrate on their own if we put a notice in the docs." | Without clear shims, automated warnings, or active coordination, consumers rarely prioritize migration until forced. |
| "Renaming a database column is just a simple one-line migration." | During deployment, old and new instances run concurrently. One of them will query a column that doesn't exist. Always use expand/contract. |
| "We can add the new column and drop the old one in the same deploy." | Coupling additive and destructive operations eliminates the ability to roll back safely if issues arise. |
| "We don't need a rollback script for this migration." | A database migration with no rollback path turns a minor deployment hitch into an irreversible outage. |

## Red Flags

- Sunsetting a system with no replacement available or tested in production.
- Renaming or dropping database columns in a single deploy alongside application code changes.
- Database migrations merged without a verified `down` / rollback script.
- Backfilling millions of rows in a single blocking `UPDATE` transaction instead of throttled batches.
- Removing deprecated code before confirming zero active traffic via metrics or logs.
- Continuing to add new features to a system marked for deprecation.

## Verification Checklist

Before completing a system or API deprecation:

- [ ] Replacement system verified in production with necessary feature parity.
- [ ] Clear migration guidance documented for all consumers.
- [ ] Telemetry and logs confirm zero active requests to the legacy system.
- [ ] Legacy code, adapters, and associated test files completely deleted.

Before executing a database schema migration:

- [ ] Schema changes follow the multi-step Expand/Contract pattern across separate deployments.
- [ ] Backward compatibility maintained so old and new code run safely against the schema.
- [ ] Backfill scripts run asynchronously in throttled batches to prevent table locking.
- [ ] Rollback (`down`) migration script tested and verified.
- [ ] Destructive drops occur in an isolated deployment only after old columns are fully unreferenced.
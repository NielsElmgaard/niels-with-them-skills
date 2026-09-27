---
name: prepare-shipping
description: Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy.
---

# Prepare Shipping

A practical guide for shipping changes safely to production with verified readiness, staged rollouts, active monitoring, and instant rollback plans.

## Overview

The goal of shipping is not just deploying code—it is deploying safely. Every production launch must be observable, incremental, and reversible. Following a structured launch procedure prevents outages and ensures issues are caught before they impact users.

## When to Use

Use this skill when:
- Deploying a new feature, service, or major refactor to production.
- Setting up staged rollouts using feature flags or canary releases.
- Preparing deployment rollback plans and health check verification.
- Monitoring system health and error rates immediately following a release.

When NOT to use:
- Performing code review or assessing pull requests (use `review-that-code`).
- Structuring git commits, branching, or tagging (use `git-keeper`).
- Schema migrations and phasing out deprecated APIs (use `phasing-out-and-migration`).

## Core Launch Process

```
[1. Pre-Flight Readiness] ──> [2. Staged Rollout Strategy] ──> [3. Rollback Preparation] ──> [4. Deploy & Verify]
```

### Step 1: Pre-Flight Readiness

Before triggering deployment, confirm baseline system requirements:

- **Build & Quality**: All CI tests pass, build succeeds with zero warnings, and code review is approved.
- **Standing Bar**: Verify the change clears the project [definition-of-done.md](../../references/definition-of-done.md).
- **Environment & Secrets**: Required environment variables are configured in the target environment (never committed to repository).
- **Database & State**: Any required database migrations are executed or queued with backward compatibility.
- **Health Checks**: A dedicated health check endpoint exists (e.g. `GET /healthz` or `/api/health`) and returns `200 OK`.
- **Domain Checklists**: If applicable, cross-check [security-checklist.md](../../references/security-checklist.md), [performance-checklist.md](../../references/performance-checklist.md), and [accessibility-checklist.md](../../references/accessibility-checklist.md).

### Step 2: Staged Rollout & Feature Flags

Decouple deployment from release whenever changes carry risk:

1. **Deploy Inactive (Flag OFF)**: Code ships to production behind a feature flag or kill switch with zero traffic impact.
2. **Internal Smoke Test**: Enable the flag for internal team members or beta testers in production.
3. **Gradual Ramp**: Increase exposure incrementally (e.g. 10% → 50% → 100%) while watching error rates.
4. **Flag Retirement**: Schedule flag removal within 1–2 weeks of reaching 100% rollout to avoid technical debt.

### Step 3: Rollback Preparation

Never deploy without a concrete, documented rollback path:

- **Trigger Conditions**: Clearly define when to abort (e.g. error rate spikes above 2x baseline, critical user flow fails, or P95 latency doubles).
- **Rollback Mechanism**:
  - *Feature flag*: Disable the flag immediately (< 1 minute).
  - *Code rollback*: Revert the commit (`git revert <commit>`) or redeploy the last known-good container image (< 5 minutes).
  - *Database*: Ensure schema changes are backward-compatible so rolling back application code does not corrupt data.

### Step 4: Post-Launch Verification

Actively inspect telemetry during the first 15–60 minutes following deployment:

1. **Check Health**: Confirm health check endpoints report healthy status.
2. **Monitor Error Rates**: Inspect error tracking (e.g. Sentry, Datadog) for new exception types or elevated 5xx responses.
3. **Check Latency**: Verify P95 response times have not regressed.
4. **Execute Smoke Test**: Manually test the critical user journey in production to confirm end-to-end functionality.
- For telemetry, logging, and metrics setup, see [observability-checklist.md](../../references/observability-checklist.md).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It worked in staging, so it's guaranteed to work in production." | Production has distinct data volumes, traffic concurrency, and third-party integrations. Always monitor actively after deployment. |
| "This change is so small it doesn't need a rollback plan." | Even one-line configuration changes can cause cascading outages. A rollback mechanism must always be defined. |
| "We'll set up error alerts and dashboards after the release." | Without monitoring, your users become your alerting system. Set up visibility before shipping. |
| "Rolling back is admitting failure." | Fast, clean rollback is responsible engineering. Leaving broken code in production while trying to debug under pressure causes worse incidents. |
| "We can ship on Friday afternoon because it's already tested." | Deploying right before off-hours creates high risk if delayed issues emerge. Deploy when team coverage is available. |

## Red Flags

- Deploying to production without a verified rollback mechanism.
- Shipping changes without monitoring error tracking dashboards in the first hour.
- Relying on manual database edits or unrecorded environment variable changes during deploy.
- Releasing complex features in a single "big bang" without flags or staged traffic.
- Accumulating stale feature flags indefinitely in the codebase.
- Deploying during high-traffic peaks or off-hours without immediate on-call support.

## Verification Checklist

Before deploying:

- [ ] CI suite, linting, and build pass completely.
- [ ] Pre-launch items satisfy the project [definition-of-done.md](../../references/definition-of-done.md).
- [ ] Production environment variables and secrets verified.
- [ ] Database migrations tested and backward-compatible.
- [ ] Rollback steps explicitly identified (flag toggle or previous build redeploy).

After deploying:

- [ ] Health check endpoint responds with `200 OK`.
- [ ] Error tracking monitored for at least 15 minutes with no novel error spikes.
- [ ] P95 latency and resource utilization remain within normal baseline.
- [ ] Core user flows verified via post-deploy smoke test.
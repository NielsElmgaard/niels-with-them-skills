# Observability Checklist

Practical checklist for instrumenting production systems, establishing reliable telemetry signals, and verifying observability before shipping.

## Table of Contents

- [Structured Logging](#structured-logging)
- [Metrics](#metrics)
- [Tracing & Context Propagation](#tracing--context-propagation)
- [Alerting](#alerting)
- [Health Checks & Verification](#health-checks--verification)

## Structured Logging

- [ ] **JSON format**: Logs are emitted as structured JSON with stable event names rather than unstructured strings.
- [ ] **Standard fields**: Consistent baseline fields are present on every log entry (`timestamp`, `level`, `service`, `trace_id`, `user_id`).
- [ ] **Consistent log levels**:
  - `error`: Invariant broken or failure requiring human attention.
  - `warn`: Recoverable or degraded condition handled by the system.
  - `info`: Key lifecycle or business events.
  - `debug`: Detailed diagnostics (disabled by default in production).
- [ ] **No sensitive credentials**: Passwords, API tokens, authorization headers, and unredacted PII are strictly excluded.
- [ ] **Sanitized payloads**: Log allowlisted metadata (endpoint, status, duration) rather than full request/response bodies.

## Metrics

- [ ] **RED method**: Instrumented for every service endpoint and external dependency:
  - **Rate**: Request throughput (requests per second).
  - **Errors**: Number and rate of failed requests.
  - **Duration**: Request latency distributions.
- [ ] **Key business metrics**: Essential domain metrics tracked (e.g., checkout transactions, jobs processed, user signups).
- [ ] **System resource utilization**: Host and runtime saturation tracked (CPU, memory, disk I/O, connection pool usage).
- [ ] **Percentiles over averages**: Latency tracked as histograms to query p50, p95, and p99 percentiles (never averages).
- [ ] **Low cardinality**: Labels use small, bounded sets (route template, status class); unbounded values (IDs, emails, URLs) are omitted.

## Tracing & Context Propagation

- [ ] **Startup initialization**: Tracing SDK (e.g., OpenTelemetry) initialized at service startup before application handlers.
- [ ] **Trace propagation**: Trace context (`traceparent`, `tracestate`) propagated across all inbound and outbound HTTP/gRPC calls.
- [ ] **Async boundaries**: Context propagated through message queues, background workers, and scheduled tasks.
- [ ] **Actionable spans**: Manual spans created for discrete units of work with high-value filtering attributes, excluding sensitive data.

## Alerting

- [ ] **Actionable symptoms**: Alerts trigger on user-impacting symptoms (elevated error rate, P95/P99 latency breaches) rather than internal causes.
- [ ] **Avoid alert fatigue**: Every alert has a clear corrective action; flaky, noisy, or self-healing alerts are removed or silenced.
- [ ] **Runbooks included**: Every alert links directly to a concise runbook detailing triage queries and escalation paths.
- [ ] **SLO-aligned thresholds**: Alert thresholds and evaluation windows are justified by SLOs or historical baselines.
- [ ] **Severity tiers**: Strict separation between urgent notifications (`page`) and non-interruptive issues (`ticket`).

## Health Checks & Verification

- [ ] **Health check endpoint**: `/healthz` (or separate `/livez` and `/readyz`) returns liveness and validates critical dependency readiness.
- [ ] **Log backend verification**: Test errors verified in the log aggregation backend, confirming JSON schema and `trace_id` indexing.
- [ ] **Metrics backend verification**: Synthetic traffic verified in metrics dashboards, ensuring proper label dimensions and counters.
- [ ] **Distributed trace verification**: End-to-end request traced through all downstream services without broken spans.
- [ ] **Pre-launch signoff**: Staging failure diagnosed using telemetry alone before deploying to production.

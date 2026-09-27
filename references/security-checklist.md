# Security Checklist

A practical, actionable security checklist for web applications, APIs, and AI-assisted workflows.

## Threat Modeling
- [ ] **Trust boundaries**: Identify all entry points (client requests, public webhooks, file uploads, third-party APIs, LLM outputs).
- [ ] **Critical assets**: Catalog high-value data (credentials, secrets, PII, payment info, administrative operations).
- [ ] **STRIDE analysis**: Review each boundary against Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.
- [ ] **Abuse cases**: Formulate misuse and abuse cases alongside functional features ("how could an attacker exploit this?").

## Pre-Commit Checks
- [ ] Scan staged changes for hardcoded secrets: `git diff --cached | grep -iE "password|secret|api_key|token|private_key"`.
- [ ] Verify `.gitignore` covers sensitive local files (`.env`, `.env.*`, `*.pem`, `*.key`, local credentials).
- [ ] Verify `.env.example` provides non-sensitive dummy placeholders only.

## Authentication & Sessions
- [ ] **Password hashing**: Use strong, salted one-way hashing (bcrypt cost ≥ 12, argon2id, or scrypt).
- [ ] **Session cookies**: Enforce `HttpOnly`, `Secure`, and `SameSite=Lax` (or `SameSite=Strict`).
- [ ] **Session lifetimes**: Enforce sensible idle timeouts and absolute session expirations.
- [ ] **Rate limiting**: Restrict brute-force attempts on login, registration, and password-reset endpoints.
- [ ] **Password reset**: Reset tokens must be cryptographically random, single-use, and short-lived (≤ 1 hour).
- [ ] **Multi-Factor Authentication (MFA)**: Support or enforce MFA for privileged and sensitive accounts.

## Authorization & Access Control
- [ ] Enforce authentication and permission checks on every non-public endpoint and background job.
- [ ] Validate object-level resource ownership on every access (prevent IDOR / BOLA).
- [ ] Enforce role-based or attribute-based access control (RBAC/ABAC) on administrative endpoints.
- [ ] Validate JWT signatures, expiration (`exp`), issuer (`iss`), and audience (`aud`); explicitly reject `alg: none`.
- [ ] Apply least privilege: scope API tokens, service accounts, and database credentials to minimum required access.

<a id="input-validation"></a>
## Input Validation & Sanitization
- [ ] Validate all incoming data at API boundaries against strict allowlists and schema contracts (Zod, Joi, Pydantic, etc.).
- [ ] Enforce type, length, range, and format constraints on strings, numbers, dates, emails, and URLs.
- [ ] **File uploads**: Validate file extensions and MIME types via magic bytes; enforce maximum file size; store files outside web root with randomized names.
- [ ] **SSRF prevention**: Block server-side requests to private/reserved IP ranges (RFC 1918, link-local, loopback) and use destination allowlists.
- [ ] **Path traversal prevention**: Resolve canonical file paths (`realpath`) and confirm targets reside strictly within intended root directories.

## SQL & Command Injection Prevention
- [ ] Parameterize all database queries (use prepared statements or ORMs); never concatenate user input into SQL or NoSQL queries.
- [ ] Avoid raw shell execution APIs (`child_process.exec`, `os.system`); use parameter-array APIs (`execFile`, `spawn`) with `shell: false`.
- [ ] Contextually encode dynamic output in templates (rely on framework auto-escaping) to prevent XSS.
- [ ] Validate and allowlist redirect URLs against a trusted host list to prevent open redirect vulnerabilities.

## Security Headers & CORS
- [ ] Set essential HTTP security headers on all responses:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self'
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  ```
- [ ] Restrict CORS to trusted, explicitly allowlisted origins; never use wildcard `*` with `credentials: true`.

## Secrets & Sensitive Data Protection
- [ ] Redact sensitive fields (`passwordHash`, reset tokens, internal keys) from API responses and data transfer objects.
- [ ] Enforce TLS 1.2+ for all data in transit across public and internal networks.
- [ ] Encrypt sensitive data and PII at rest; ensure database backups are encrypted and access-restricted.
- [ ] Enforce retention policies with auditable, verifiable data deletion routines (including caches and indexes).

## Error Handling & Logging
- [ ] Return generic error messages to clients in production; never leak stack traces, SQL queries, or internal file paths.
- [ ] Log security-relevant events (failed logins, authorization failures, input anomalies) with structured metadata.
- [ ] Strip credentials, authorization tokens, payment details, and PII from application logs.

## Dependency Audits & Supply Chain
- [ ] Commit authoritative lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) and enforce immutable installs in CI (`npm ci`, `pnpm install --frozen-lockfile`).
- [ ] Run automated vulnerability scans (`npm audit`, `pnpm audit`, `pip-audit`, Dependabot) and triage high/critical findings.
- [ ] Block or gate arbitrary dependency lifecycle scripts during package installation (`--ignore-scripts` or explicit manager allowlists).
- [ ] Review new dependencies for maintenance activity, release age, repository provenance, and typosquatting risk.

## AI & LLM Security
- [ ] Treat model outputs as untrusted input; never pass model responses directly into shell commands, SQL queries, or `innerHTML`.
- [ ] Enforce authorization and business logic in deterministic application code, never solely in system prompts.
- [ ] Keep secrets, private API keys, and sensitive tenant data out of model context windows and prompts.
- [ ] Scope agent and tool capabilities to least privilege; require explicit user confirmation for destructive or irreversible actions.
- [ ] Enforce token budgets, rate limits, and recursion caps on agent loops to prevent runaway execution.

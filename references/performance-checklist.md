# Performance Checklist

Quick reference checklist for web application and backend performance optimization.

## Core Web Vitals Targets

| Metric | Target (p75) | Needs Work | Poor | Primary Lever |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s – 4.0s | > 4.0s | Hero image optimization, priority hints, server TTFB |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms – 500ms | > 500ms | Main thread unblocking, task chunking, lightweight handlers |
| **CLS** (Cumulative Layout Shift) | ≤ 0.10 | 0.10 – 0.25 | > 0.25 | Explicit image/embed dimensions, reserved layout space |

## Fast TTFB (Time to First Byte)

Target: TTFB < 800ms (ideal < 200ms):
- [ ] **DNS Resolution**: Add `<link rel="preconnect">` or `<link rel="dns-prefetch">` for critical third-party origins.
- [ ] **Handshake & TLS**: Enable HTTP/2 or HTTP/3, terminate TLS close to users via CDN/edge deployment, verify keep-alive.
- [ ] **Server Processing**: Profile backend endpoints, optimize slow queries, and cache dynamic responses.

## Frontend Checklist

### Images & Media
- [ ] Modern formats (AVIF, WebP) with responsive sizing (`srcset` and `sizes`).
- [ ] Explicit `width` and `height` on images and embeds to prevent layout shift.
- [ ] `loading="lazy"` and `decoding="async"` on below-the-fold images.
- [ ] `fetchpriority="high"` on the hero/LCP image (never lazy-load LCP images).

### JavaScript & CSS
- [ ] Initial bundle size under 200KB gzipped; audit dependencies with bundle analyzer.
- [ ] Code splitting with dynamic `import()` for distinct routes and heavy interactive dialogs.
- [ ] Eliminate render-blocking scripts in `<head>` (use `defer` or `async`).
- [ ] Inline critical CSS; defer or asynchronously load non-critical stylesheets.
- [ ] Break long tasks (> 50ms) using `scheduler.yield()` or `requestIdleCallback` to protect INP.
- [ ] Defer non-critical telemetry and logging out of interactive event handlers.

### Fonts & Rendering
- [ ] Self-host WOFF2 fonts; limit font families and weights (2–3 max).
- [ ] Use `font-display: swap` (or `optional`) and preload primary body/heading fonts.
- [ ] Virtualize long lists and tabular data (e.g., `react-window`) instead of rendering full node trees.
- [ ] Avoid layout thrashing (batch DOM reads before writes); animate only `transform` and `opacity`.

## Backend & Database Checklist

### Database & Queries
- [ ] **No N+1 queries**: Use eager loading (`JOIN`, `includes`, batch loaders) instead of querying inside loops.
- [ ] **Indexes**: Composite indexes matching equality-first, range/sort-second column order; index foreign keys.
- [ ] **Query plans**: Validate queries with `EXPLAIN (ANALYZE)` before and after indexing to verify index utilization.
- [ ] **Pagination limits**: Enforce `LIMIT` and cursor/keyset pagination; reject unbounded queries (`SELECT *`).
- [ ] **Connection pooling**: Configure a single pool per process sized within `instances × pool_size ≤ max_connections`; use a multiplexing proxy (PgBouncer) for serverless.

### API & Processing
- [ ] Response compression enabled (Brotli/Gzip) for text and JSON payloads.
- [ ] Offload long-running calculations, exports, and third-party API calls to asynchronous background queues.
- [ ] Provide bulk/batch endpoints instead of requiring repeated single-entity roundtrips.

## Caching Strategy

- [ ] **Static assets**: Content-hashed assets cached long-term (`Cache-Control: public, max-age=31536000, immutable`).
- [ ] **API responses**: Cache headers configured (`Cache-Control: private/public, s-maxage=..., stale-while-revalidate=...`).
- [ ] **Cache keys**: Include all dimensions responses vary on (tenant, user/role, locale, query parameters).
- [ ] **Stampede protection**: Request coalescing, distributed lock, or `stale-while-revalidate` on hot keys.
- [ ] **Negative caching**: Cache 404/not-found lookups with short TTLs; never cache 5xx server errors.

## Quick Measurement Commands

```bash
# Audit performance with Lighthouse
npx lighthouse https://example.com --only-categories=performance --view

# Inspect bundle composition
npx webpack-bundle-analyzer stats.json   # or: npx vite-bundle-visualizer

# Track Core Web Vitals in application code
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log); onINP(console.log); onCLS(console.log);
```

## Common Anti-Patterns

| Anti-Pattern | Impact | Solution |
|---|---|---|
| Unbounded `SELECT *` | Memory exhaustion and timeouts | Add mandatory `LIMIT` and paginated cursors |
| N+1 queries in loops | Database connection starvation | Eager-load relations or use batch dataloaders |
| Missing query indexes | Full table scans on growth | Add targeted composite index; verify via `EXPLAIN` |
| Connection pool per request | Exhausts DB `max_connections` | Use single process-level pool or connection proxy |
| Unsized images / fonts | High CLS during page load | Set explicit dimensions; use `font-display: swap` |
| Heavy main-thread JS | Slow INP and unresponsive UI | Code-split bundles; chunk tasks with `scheduler.yield()` |
| Missing cache headers | High origin server load | Set content hashing + immutable headers for static assets |

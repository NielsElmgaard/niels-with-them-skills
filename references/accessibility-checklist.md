# Accessibility Checklist (WCAG 2.1 AA)

Actionable checklist and verification guide for building accessible web applications to WCAG 2.1 AA standards.

## 1. Keyboard Navigation
- [ ] **Logical Tab Order**: Interactive elements follow natural reading and DOM order. Never use positive `tabindex` (`tabindex > 0`).
- [ ] **Visible Focus**: Every interactive element shows an unmistakable focus indicator (never set `outline: none` without a custom replacement).
- [ ] **Keyboard Operable**: All interactive controls can be activated via keyboard (`Enter` for buttons/links, `Space` for buttons/checkboxes, arrow keys for lists/radios).
- [ ] **No Traps**: Users can Tab into and away from all components without getting stuck.
- [ ] **Skip Links**: Provide a skip-to-content link at the top of the page, visible on keyboard focus.
- [ ] **Modal Focus Management**: Dialogs trap focus while open, close on `Escape`, and return focus to the trigger element when closed.
- [ ] **Touch & Pointer Targets**: Interactive targets meet minimum size recommendations (at least 24×24px, preferably 44×44px).

## 2. Semantic HTML & Structure
- [ ] **Buttons vs. Links**: Use `<button>` for actions and state changes; use `<a href="...">` for navigation. Never attach click handlers to `<div>` or `<span>`.
- [ ] **Form Labels**: Every input has an associated `<label>` via `for`/`id` matching or wrapping `<label>`. Use `aria-label` only when a visible label is not possible.
- [ ] **Heading Hierarchy**: Maintain a single `<h1>` per page. Nest headings (`<h2>` through `<h6>`) logically without skipping levels.
- [ ] **Images & Icons**: Provide descriptive `alt` text for informative images, `alt=""` for decorative images, and `aria-label` for icon-only buttons.
- [ ] **Document Metadata**: Declare language on `<html lang="...">` and provide a descriptive, unique `<title>` for every page.
- [ ] **Form Error Association**: Form field errors are programmatically linked to inputs using `aria-describedby` and flagged with `aria-invalid="true"`.
- [ ] **Landmarks & Tables**: Use semantic landmark tags (`<main>`, `<nav>`, `<header>`, `<footer>`). Data tables use `<th>` with `scope`.

## 3. Contrast & Visuals
- [ ] **Text Contrast**: Normal text has at least 4.5:1 contrast against its background. Large text (≥ 18pt or 14pt bold) requires at least 3:1.
- [ ] **UI Component Contrast**: Interactive elements, borders, icons, and focus rings maintain at least 3:1 contrast against adjacent background colors.
- [ ] **Color Independence**: Color is never the sole medium for conveying state, error, or selection; supplement with text, icons, or patterns.
- [ ] **Zoom & Scaling**: Text and layouts zoom up to 200% without clipping, overlapping, or horizontal scrolling.
- [ ] **Motion & Flashing**: Avoid flashing elements (>3 times/sec). Honor user motion preferences with `@media (prefers-reduced-motion: reduce)`.

## 4. ARIA & Dynamic Updates
- [ ] **First Rule of ARIA**: Use native semantic HTML elements before using ARIA attributes or roles.
- [ ] **Dynamic Live Regions**: Announce asynchronous changes and notifications:
  - `aria-live="polite"` (or `role="status"`): For non-urgent status messages, toast notifications, and background saves.
  - `aria-live="assertive"` (or `role="alert"`): For critical errors and time-sensitive alerts requiring immediate attention.
- [ ] **Widget State**: Keep dynamic states synchronized on custom components (`aria-expanded`, `aria-selected`, `aria-checked`, `aria-disabled`).
- [ ] **Modal Dialog Semantics**: Custom dialogs use `role="dialog"` (or `<dialog>`), `aria-modal="true"`, and link titles via `aria-labelledby`.
- [ ] **Loading Indicators**: Mark containers loading asynchronous data with `aria-busy="true"`.

## 5. Testing & Verification

### Automated Scanners
- **Lighthouse**: Run Chrome DevTools Lighthouse audit for baseline automated checks.
- **axe-core**: Run `npx axe-core` or `@axe-core/cli` in CI/test pipelines.

### Manual Verification
- [ ] **Keyboard Only**: Unplug the mouse. Walk through all user flows using `Tab`, `Shift+Tab`, `Enter`, `Space`, `Arrow keys`, and `Escape`.
- [ ] **Focus Check**: Verify focus indicator remains visible on every single control throughout the flow.
- [ ] **Screen Reader Smoke Test**: Verify core flows using native screen readers:
  - macOS / iOS: VoiceOver (`Cmd + F5`)
  - Windows: NVDA (`Ctrl + Alt + N`)
  - Linux: Orca

## Common Anti-Patterns

| Anti-Pattern | Problem | WCAG Fix |
|---|---|---|
| `<div onClick={...}>` | Missing keyboard focus and role | Use native `<button>` |
| `outline: none` | Keyboard users lose visual location | Provide styled `:focus-visible` ring |
| Missing `alt` on `<img>` | Screen readers announce file URL | Add descriptive `alt` or `alt=""` if decorative |
| Empty icon buttons | Screen readers announce unlabelled control | Add `aria-label` or visually hidden text |
| Color-only validation | Unusable for color-blind users | Add icon and descriptive text message |
| Untrapped modals | Background content reachable while open | Confine Tab focus within active dialog |
| `tabindex > 0` | Disrupts natural reading/tab order | Use `tabindex="0"` or `-1` only |

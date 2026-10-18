---
name: factory
description: Orchestrates a visual multi-agent software factory loop across spec writing, worktree-isolated building, parallel multi-axis review rounds, and merge gates. Use when running features through an automated spec-build-review pipeline, processing a feature backlog, or managing factory jobs and dashboard state.
---

# AI Software Factory (`/factory`)

A visual, file-driven multi-agent software factory that takes features from specification through isolated git worktree implementation, parallel specialist reviews, and deterministic merge gates.

## Overview

Whichever agent session runs `/factory` becomes the **orchestrator**. The orchestrator drives the pipeline loop, spawns leaf subagents with file-based context, enforces the `WAIT FOR ALL` review barrier, runs deterministic test gates, and is the **sole writer of `factory/board.json`**.

## When to Use

Use this skill when:
- Running a feature or bug fix end-to-end through an automated spec → build → parallel review → merge pipeline (`/factory <feature>`).
- Generating a grounded feature specification with a human review checkpoint before building (`/factory spec <feature>`).
- Working through a prioritized queue of features in `factory/backlog.md` (`/factory next`).
- Approving, merging, or sending factory jobs back for rework (`/factory approve <job-id>`, `/factory rework <job-id> <note>`).

When NOT to use:
- Single-line edits or trivial typo fixes (edit directly and commit via `git-keeper`).
- Standalone interactive code review without building a job (use `review-that-code`).
- Auditing repository documentation alignment (use `audit-align`).

## Model Tiers (Claude & Gemini Equivalents)

Each agent persona in the factory maps to either the **Frontier / Deep Reasoning** tier or the **Fast Specialist** tier:

| Persona | Factory Stage | Claude Code (`model`) | Gemini / Antigravity (`gemini_model` / `tier`) |
|---|---|---|---|
| [`spec-writer`](../../agents/spec-writer.md) | Spec (`spec.md`) | `opus` | `Gemini 4 Argon` (`pro`) |
| [`builder`](../../agents/builder.md) | Build (`build.md`) | `opus` | `Gemini 4 Argon` (`pro`) |
| [`security-auditor`](../../agents/security-auditor.md) | Review (`review-security.md`) | `opus` | `Gemini 4 Argon` (`pro`) |
| [`code-reviewer`](../../agents/code-reviewer.md) | Review (`review-code.md`) | `sonnet` | `Gemini 3.8 Flash` (`flash`) |
| [`test-engineer`](../../agents/test-engineer.md) | Review (`review-tests.md`) | `sonnet` | `Gemini 3.8 Flash` (`flash`) |
| [`ui-ux-reviewer`](../../agents/ui-ux-reviewer.md) | Review (`review-ui-ux.md`) | `sonnet` | `Gemini 3.8 Flash` (`flash`) |

## The Orchestration Loop

```text
                       ┌──────────────────────────┐
                       │  /factory <feature>      │
                       │  or /factory next        │
                       └────────────┬─────────────┘
                                    ▼
                       ┌──────────────────────────┐
                       │       spec-writer        │
                       │  opus / Gemini 4 Argon   │
                       └────────────┬─────────────┘
                                    │ writes jobs/<id>/spec.md
                                    │ (sets UI_IMPACT & TEST_COMMAND)
             (/factory spec pauses) ▼
                       ┌──────────────────────────┐
                       │    git worktree add      │
                       │  .worktrees/<job-id>     │
                       │  branch: factory/<id>    │
                       └────────────┬─────────────┘
                                    ▼
                       ┌──────────────────────────┐
                       │    builder-<job-id>      │◄─────────────────────────┐
                       │  opus / Gemini 4 Argon   │                          │
                       └────────────┬─────────────┘                          │
         ┌───────────────────┬──────┴──────┬───────────────────┐             │
         ▼                   ▼             ▼                   ▼             │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐ │
│security-auditor │ │  code-reviewer  │ │  test-engineer  │ │ui-ux-reviewer│ │
│  opus / Argon 4 │ │ sonnet / Flash  │ │ sonnet / Flash  │ │sonnet / Flash│ │
│                 │ │      3.8        │ │      3.8        │ │(if UI_IMPACT)│ │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘ └──────┬───────┘ │
         └───────────────────┴──────┬──────┴───────────────────┘             │
                                    ▼                                        │
                       ┌──────────────────────────┐   any VERDICT: CHANGES   │
                       │      WAIT FOR ALL        ├──────────────────────────┘
                       │   active reviews in      │   resume builder-<job-id>
                       └────────────┬─────────────┘   (max 2 rounds)
                                    │
                  ┌─────────────────┴─────────────────┐
                  │ all PASS + TEST_COMMAND exits 0   │ round 2 still CHANGES
                  ▼                                   ▼
     ┌─────────────────────────┐         ┌─────────────────────────┐
     │  decision.md: APPROVE   │         │  decision.md: ESCALATE  │
     │  stage: ready-to-merge  │         │  stage: needs-human     │
     └────────────┬────────────┘         └────────────┬────────────┘
                  │                                   │
                  └──────────────┬────────────────────┘
                                 ▼
                    /factory approve <job-id>
                  (merges branch & removes worktree)
```

## Core Process

### Step 0: Initialize Factory (`/factory init` or First Run)

If `factory/board.json` does not exist in the repository root, or if `project.language` in `factory/board.json` is still `"auto"`:
1. Inspect the repository (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to detect:
   - `language` (e.g., `javascript`, `typescript`, `python`, `rust`, `go`)
   - `testCommand` (e.g., `npm test`, `pytest`, `cargo test`)
2. If `factory/` does not exist yet, create `factory/` and copy [`assets/dashboard.html`](assets/dashboard.html), [`assets/board.template.json`](assets/board.template.json) (to `factory/board.json`), and [`assets/backlog.template.md`](assets/backlog.template.md) (to `factory/backlog.md`).
3. Ensure `.worktrees/` is listed in `.gitignore` (even if `factory/board.json` was pre-scaffolded by the CLI installer).
4. Populate `project.name`, `project.language`, and `project.testCommand` in `factory/board.json`.

### Step 1: Specification (`stage: "spec"`)

1. Assign the next sequential job ID (e.g., `001-short-slug`) and create `factory/jobs/<job-id>/`.
2. Add the job entry to `factory/board.json` with `stage: "spec"`, `round: 0`, and empty `reviews`.
3. Spawn [`spec-writer`](../../agents/spec-writer.md) (`opus` / `Gemini 4 Argon`) with instructions to inspect the codebase and write `factory/jobs/<job-id>/spec.md`.
4. Read the first lines of `spec.md` to extract `UI_IMPACT: true | false` and `TEST_COMMAND`. Update `requiresUiReview` and `files` (using paths relative to `factory/`, e.g., `"jobs/<job-id>/spec.md"`) in `factory/board.json`.
5. **If invoked via `/factory spec <feature>`**: set `stage: "spec-review"` in `factory/board.json` and stop so the human can review or edit `spec.md` before running `/factory build <job-id>`.

### Step 2: Worktree Isolation & Build (`stage: "build"`)

1. Create an isolated git worktree on branch `factory/<job-id>` (following [`git-keeper`](../git-keeper/SKILL.md)):
   ```bash
   git worktree add .worktrees/<job-id> -b factory/<job-id>
   ```
2. Update `factory/board.json` to `stage: "build"`.
3. Spawn [`builder`](../../agents/builder.md) (`opus` / `Gemini 4 Argon`) named `builder-<job-id>`, pointing it at:
   - Worktree path: `.worktrees/<job-id>`
   - Spec path: `factory/jobs/<job-id>/spec.md`
   - Output file: `factory/jobs/<job-id>/build.md`
4. Confirm `factory/jobs/<job-id>/build.md` exists and commits are recorded on `factory/<job-id>`.

### Step 3: Parallel Review Round (`stage: "review"`, Round 1..2)

1. Increment `round` (starting at `1`), create `factory/jobs/<job-id>/round-<N>/`, and update `factory/board.json` with:
   - `stage: "review"`, `round: N`
   - `reviews`: `{ "security": "pending", "code": "pending", "tests": "pending", "ui-ux": requiresUiReview ? "pending" : "skipped" }`
2. Spawn all active reviewers **in parallel**, instructing each to inspect `factory/jobs/<job-id>/spec.md`, `factory/jobs/<job-id>/build.md`, and the git diff in `.worktrees/<job-id>` (`git diff main...factory/<job-id>`), and write only its own file starting with `VERDICT: PASS` or `VERDICT: CHANGES`:
   - [`security-auditor`](../../agents/security-auditor.md) (`opus` / `Gemini 4 Argon`) → `factory/jobs/<job-id>/round-<N>/review-security.md`
   - [`code-reviewer`](../../agents/code-reviewer.md) (`sonnet` / `Gemini 3.8 Flash`) → `factory/jobs/<job-id>/round-<N>/review-code.md`
   - [`test-engineer`](../../agents/test-engineer.md) (`sonnet` / `Gemini 3.8 Flash`) → `factory/jobs/<job-id>/round-<N>/review-tests.md`
   - *(Only if `requiresUiReview: true`)* [`ui-ux-reviewer`](../../agents/ui-ux-reviewer.md) (`sonnet` / `Gemini 3.8 Flash`) → `factory/jobs/<job-id>/round-<N>/review-ui-ux.md` (uses Chrome DevTools MCP against a live preview or ephemeral dev server started from `.worktrees/<job-id>` when available, falling back to static diff review)
3. **WAIT FOR ALL**: Wait until every active reviewer's markdown file exists in `round-<N>/`. Never resume the builder mid-round. As verdicts arrive, parse line 1 (`VERDICT: PASS` or `VERDICT: CHANGES`) and update `factory/board.json`.

### Step 4: Deterministic Gate & Rework / Decision

Once all active reviews in `round-<N>` are recorded:

- **Case A — Any reviewer returned `CHANGES` and `round < 2`**:
  1. Update `factory/board.json` to `stage: "build"`.
  2. Resume the existing `builder-<job-id>` subagent (via `send_message` / `SendMessage` or passing `round-<N>/`), instructing it to address all `[Critical]`, `[Required]`, `High`, and actionable `Medium` findings (plus any unverified acceptance criteria or failing tests) in `factory/jobs/<job-id>/round-<N>/`, re-run tests in `.worktrees/<job-id>`, commit fixes, update `build.md`, and then proceed to Round 2 (repeat Step 3).
- **Case B — Any reviewer returned `CHANGES` and `round == 2`**:
  1. Write `factory/jobs/<job-id>/decision.md` starting with `ESCALATE` on line 1, summarizing the remaining unresolved findings from Round 2.
  2. Update `factory/board.json` to `stage: "needs-human"`.
- **Case C — All active reviewers returned `PASS`**:
  1. Run the project's `testCommand` inside `.worktrees/<job-id>` to deterministically confirm tests pass.
  2. If tests fail despite reviewer `PASS`, treat as `CHANGES` (if `round < 2`, resume `builder-<job-id>` with the test failure output; if `round == 2`, write `decision.md` with `ESCALATE` and set `stage: "needs-human"`).
  3. If tests pass (`exit 0`), write `factory/jobs/<job-id>/decision.md` starting with `APPROVE` on line 1, recording the commit hash, test command result, and reviewer sign-offs against [`definition-of-done.md`](../../references/definition-of-done.md).
  4. Update `factory/board.json` to `stage: "ready-to-merge"`, `testStatus: "pass"`.

## Commands

| Command | Action |
|---|---|
| `/factory init` | Inspect repo, scaffold `factory/` (`board.json`, `dashboard.html`, `backlog.md`), and ignore `.worktrees/`. |
| `/factory <feature>` | Run a new job end-to-end through `spec` → `build` → `review` (max 2 rounds) → `ready-to-merge` / `needs-human`. |
| `/factory spec <feature>` | Write `spec.md` only and pause at `stage: "spec-review"` for human inspection. |
| `/factory build <job-id>` | Resume a job from `spec-review` through worktree creation, `build`, and `review`. |
| `/factory next` | Pick the first unchecked item (`- [ ]`) in `factory/backlog.md` and run it through the loop. |
| `/factory approve <job-id>` | Merge `factory/<job-id>` into `main`, remove `.worktrees/<job-id>`, mark `backlog.md` `[x]`, and set `stage: "merged"`. |
| `/factory rework <job-id> <note>` | Write human feedback to `round-<N+1>/review-human.md` (`VERDICT: CHANGES`) and resume `builder-<job-id>`. |

## Target File System & `board.json` Contract

```text
factory/
  board.json                       # durable state, written ONLY by the orchestrator
  dashboard.html                   # visual board, served with `python3 -m http.server` from factory/
  backlog.md                       # markdown checklist queue for `/factory next`
  jobs/003-rate-limiting/          # one folder per job
    spec.md                        # written by spec-writer
    build.md                       # written by builder-<job-id>
    round-1/                       # one folder per review round
      review-security.md           # starts with VERDICT: PASS | CHANGES
      review-code.md               # starts with VERDICT: PASS | CHANGES
      review-tests.md              # starts with VERDICT: PASS | CHANGES
      review-ui-ux.md              # starts with VERDICT: PASS | CHANGES (if UI_IMPACT: true)
    decision.md                    # starts with APPROVE | ESCALATE
```

Each job entry in `factory/board.json` follows this schema (`files` paths are relative to `factory/`):

```json
{
  "id": "003-rate-limiting",
  "title": "Add token-bucket rate limiting to auth endpoints",
  "branch": "factory/003-rate-limiting",
  "stage": "ready-to-merge",
  "round": 1,
  "requiresUiReview": false,
  "testStatus": "pass",
  "reviews": {
    "security": "PASS",
    "code": "PASS",
    "tests": "PASS",
    "ui-ux": "skipped"
  },
  "files": [
    "jobs/003-rate-limiting/spec.md",
    "jobs/003-rate-limiting/build.md",
    "jobs/003-rate-limiting/round-1/review-security.md",
    "jobs/003-rate-limiting/round-1/review-code.md",
    "jobs/003-rate-limiting/round-1/review-tests.md",
    "jobs/003-rate-limiting/decision.md"
  ]
}
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Security already returned `CHANGES`, so I'll resume the builder immediately without waiting for the other reviewers." | Resuming mid-round causes race conditions and forces extra rework rounds when the remaining reviewers finish seconds later. Always **WAIT FOR ALL** active reviews in the round. |
| "I can just switch branches in the main repository root instead of creating a git worktree." | Switching branches in the main root dirties `factory/board.json`, breaks running dashboard servers, and causes merge conflicts with untracked job files. Always isolate builds in `.worktrees/<job-id>`. |
| "This backend CLI feature still needs `ui-ux-reviewer` to run so all 4 boxes are checked." | Running a UI/UX reviewer on backend-only code wastes tokens or produces hallucinated UI critiques. Mark `ui-ux` as `"skipped"` when `UI_IMPACT: false`. |
| "All reviewers returned `PASS`, so I don't need to execute `TEST_COMMAND` before marking `ready-to-merge`." | LLMs reading diffs can miss runtime syntax or import errors. The orchestrator must deterministically verify `TEST_COMMAND` exits `0`. |
| "I'll let subagents update `factory/board.json` directly when they finish." | Concurrent subagents writing `board.json` clobber each other's JSON updates. Only the orchestrator writes `factory/board.json`. |

## Red Flags

- Subagents writing to `factory/board.json` or modifying another agent's markdown file.
- Resuming `builder-<job-id>` before all active reviewers in `round-<N>` have written their files.
- Running more than 2 automated review rounds without escalating to `needs-human`.
- Review files missing `VERDICT: PASS` or `VERDICT: CHANGES` on line 1, or `decision.md` missing `APPROVE` or `ESCALATE` on line 1.
- Leaving orphaned `.worktrees/<job-id>` directories after `/factory approve <job-id>` merges a branch.

## Verification Checklist

Before concluding any `/factory` command, verify:

- [ ] `factory/board.json` is valid JSON and accurately reflects the current `stage`, `round`, `reviews`, `testStatus`, and `files` array.
- [ ] Builder changes are committed on isolated branch `factory/<job-id>` inside `.worktrees/<job-id>`.
- [ ] Every completed review file in `round-<N>/` starts with `VERDICT: PASS` or `VERDICT: CHANGES`.
- [ ] `WAIT FOR ALL` was respected before any builder resumption or stage transition.
- [ ] For `ready-to-merge` jobs: all active reviewers returned `PASS`, `TEST_COMMAND` exited `0`, and `decision.md` starts with `APPROVE`.
- [ ] For `merged` jobs (`/factory approve`): `factory/<job-id>` is merged into `main`, `.worktrees/<job-id>` is removed, and `board.json` shows `stage: "merged"`.

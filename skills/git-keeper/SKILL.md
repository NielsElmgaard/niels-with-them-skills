---
name: git-keeper
description: Structures disciplined git workflows including atomic commits, branch isolation, save points, conventional commit messages, pre-commit checks, and release versioning. Use when making changes, committing, branching, resolving conflicts, isolating parallel agent work with worktrees, or tagging releases.
---

# Git Workflow and Versioning

A practical workflow for disciplined version control, ensuring changes remain incremental, reversible, and easy to review.

## Overview

Treat commits as save points, branches as sandboxes, and git history as living documentation. Small, verified increments prevent regressions and give AI agents and human collaborators a reliable safety net.

## When to Use

Use this skill when:
- Making any code modification or refactoring.
- Creating feature branches or isolating parallel agent work using git worktrees.
- Splitting messy working trees into clean, atomic commits.
- Writing commit messages, opening pull requests, or preparing release tags.

When NOT to use:
- Multi-axis code review criteria (use code review skills).
- Cleaning up outdated repository documentation or phantom file paths (use `audit-align`).

## Core Workflow

```
[1. Branch / Worktree] ──> [2. Small Slice & Verify] ──> [3. Pre-Commit Check] ──> [4. Atomic Commit] ──> [5. Release / Tag]
```

### Step 1: Branch Isolation & Worktrees

- **Branch Naming**: Branch from `main` using descriptive prefixes:
  - `feature/<name>` — New capabilities
  - `fix/<name>` — Bug fixes
  - `refactor/<name>` — Code cleanup without behavior change
  - `chore/<name>` — Tooling, dependencies, or configuration
- **Keep Branches Short-Lived**: Merge back into `main` frequently to minimize merge conflicts.
- **Parallel Agent Worktrees**: When running multiple tasks concurrently, use git worktrees to keep working trees completely isolated:
  ```bash
  # Create a parallel workspace on a dedicated branch
  git worktree add ../task-feature feature/task-name
  # When work is merged, remove the worktree
  git worktree remove ../task-feature
  ```
  For multi-agent coordination patterns, see [orchestration-patterns.md](../../references/orchestration-patterns.md).

### Step 2: Incremental Slices & Save Points

Work in small, testable slices rather than giant all-at-once edits:

```
Implement slice ──> Test & Verify ──> Commit save point ──> Next slice
```

- **Commits as Save Points**: Each time a slice passes tests, commit it immediately.
- **Safe Rollback**: If an experimental direction fails, revert cleanly to the last save point:
  ```bash
  git restore <file>       # Discard uncommitted file changes
  git reset --hard HEAD    # Discard uncommitted edits back to last commit
  ```
- **Size Target**: Aim for focused commits (~50–200 lines). Avoid mixing unrelated changes.

### Step 3: Pre-Commit Hygiene

Before staging and committing, run quick checks:

```bash
# 1. Review exact staged changes
git diff --staged

# 2. Check for leaked secrets or temporary tokens
git diff --staged | grep -iE "(password|secret|api_key|token|private_key)"

# 3. Ensure test suite and linters pass
npm test # or pytest, cargo test, etc.
```

- **File Hygiene**: Verify `.gitignore` excludes `.env`, secrets, build outputs (`dist/`), and dependencies (`node_modules/`).

### Step 4: Atomic Conventional Commits

Each commit must represent one logical change. Never mix formatting refactors with behavioral feature additions.

- **Message Format**:
  ```
  <type>: <concise description of intent>

  [optional body: explain the "why" and context, not the obvious "what"]
  ```
- **Allowed Types**:
  - `feat`: User-facing functionality
  - `fix`: Bug fix
  - `refactor`: Restructuring code with no functional or API change
  - `test`: Adding or correcting tests
  - `docs`: Documentation updates
  - `chore`: Tooling, build config, dependency bumps

### Step 5: Versioning & Human-Readable Changelogs

When releasing changes consumed by others:

- **Semantic Versioning (`MAJOR.MINOR.PATCH`)**:
  - `MAJOR`: Breaking changes or incompatible API changes.
  - `MINOR`: New backward-compatible functionality.
  - `PATCH`: Backward-compatible bug fixes.
- **Annotated Tags**: Mark releases as immutable history:
  ```bash
  git tag -a v1.2.0 -m "Release v1.2.0"
  git push origin v1.2.0
  ```
- **Curated Changelog**: Record user-facing impact under headings: `Added`, `Changed`, `Fixed`, or `Deprecated`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll make one giant commit when everything is done." | Large commits are difficult to review, impossible to cleanly revert, and obscure the root cause when bugs appear. |
| "Commit messages don't matter as long as the code works." | Clear messages explain the *intent* behind decisions, which agents and future maintainers need to avoid reverting intentional behavior. |
| "I'll separate formatting and refactoring later." | Staging mixed changes almost always leads to messy PRs and accidental regressions. Keep concerns separated as you go. |
| "We don't need a `.gitignore` right now." | Secrets and build artifacts get committed by accident unless ignored from day one. |
| "It's a small change, so a patch bump is fine even if an API changed." | If consumers depend on behavior that changed, it is a breaking change regardless of line count. |

## Red Flags

- Accumulating large uncommitted diffs across multiple unrelated files.
- Generic commit messages (`"updates"`, `"fix stuff"`, `"wip"`).
- Committing environment files (`.env`), credentials, or generated build artifacts (`dist/`).
- Combining formatting/whitespace refactors with logic changes in the same commit.
- Force-pushing (`git push --force`) to shared branches.
- Hand-editing version numbers without matching git tags or changelog entries.

## Verification Checklist

Before completing your git workflow task, verify:

- [ ] Working tree is clean and each commit represents a single logical increment.
- [ ] Commit messages follow the conventional `<type>: <summary>` format and explain intent.
- [ ] Changes satisfy the project-wide [definition-of-done.md](../../references/definition-of-done.md).
- [ ] No secrets, credentials, or `.env` files are in the git status or diff.
- [ ] Tests and linters pass before pushing or finalizing commits.
- [ ] If releasing: version bump correctly follows SemVer and release tag matches changelog.
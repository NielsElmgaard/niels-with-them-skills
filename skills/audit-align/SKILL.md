---
name: audit-align
description: Audits and aligns repository documentation, comments, docstrings, project configuration, and commands with actual codebase reality to eliminate misleading context. Use when cleaning up brownfield repositories, fixing stale docs or comments, updating project trees and commands after refactors, or removing misleading context that causes AI agent hallucination.
---

# Audit & Align Codebase Reality

A skill for systematically auditing a codebase to eliminate stale documentation, outdated docstrings, misleading comments, broken commands, and phantom file paths that mislead AI coding agents and human contributors.

## Overview

As software projects evolve, documentation and source comments frequently drift away from the underlying code reality. Humans can often guess through minor discrepancies, but AI coding agents rely on files like `README.md`, `AGENTS.md`, docstrings, and inline comments as authoritative ground truth. When these references are stale or outright incorrect, agents run broken commands, pass invalid arguments, hallucinate legacy architectures, or introduce convoluted workarounds.

`audit-align` executes a structured, zero-assumption audit to restore 1:1 parity between codebase reality and all descriptive context.

---

## When to Use

Use this skill when:
- Cleaning up an aging or "brownfield" repository that has accumulated out-of-sync documentation, obsolete docstrings, or dead code comments.
- Concluding a major refactor, directory reorganization, or toolchain migration (e.g. moving build tools, test runners, or folder layouts).
- An AI coding agent exhibits confusion, hallucinates non-existent flags/paths, or fails commands due to conflicting guidance in `README.md`, `AGENTS.md`, or docstrings.
- Preparing a repository for AI agent pair-programming or team onboarding.
- Scrubbing leaked host-specific paths (`file:///...`, `/workspaces/...`, `/Users/...`, `/home/...`) or broken markdown references.
- Pruning "zombie code" (commented-out implementation blocks) and expired TODOs.

When NOT to use:
- Implementing new business features or functional modifications (keep maintenance audits separate from feature development).
- Reformatting code style or running mechanical linters (use standard formatters like Prettier, Black, Ruff, or ESLint directly).
- Rewriting working code logic or changing public APIs without explicit instructions.
- Authoring a brand-new skill from scratch (use `skill-creator`).

---

## Core Process

```
[Phase 1: Reality Mapping] ──> [Phase 2: Project Root & Agent Config] ──> [Phase 3: Reference & Link Sanitization]
                                                                                     │
                                                                                     ▼
[Phase 6: Verification & Diff] <── [Phase 5: Comment & Zombie Code Triage] <── [Phase 4: Docstring & Interface Parity]
```

### Phase 1: Ground-Truth Reality Mapping

Before touching any documentation or comments, establish what the codebase *actually* is and does today:

1. **Map Real Directory Structure**:
   - Inspect tracking files (e.g. `git ls-files`) to map the true tree without pollution from `node_modules/`, `.git/`, build outputs, or local scratch directories.
   - Note major top-level directories and their current responsibilities.
2. **Inspect Manifests and Toolchains**:
   - Check package and build manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`).
   - Identify active scripts, entrypoints, binary targets, and exported modules.
3. **Probe Current Baseline Commands**:
   - Execute the actual test, build, lint, and validation commands to verify what succeeds right now.
   - Document the working invocations and note any discrepancies between manifests and existing documentation.

### Phase 2: Project Root & Agent Configuration Alignment

Agent guidance files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.) and `README.md` are the front door for AI agents. Keep them strictly synchronized:

1. **Synchronize Project Directory Trees**:
   - Compare the ASCII directory tree in `README.md` and `AGENTS.md` against the actual filesystem.
   - Remove phantom files or directories that were deleted or renamed.
   - Add newly introduced top-level directories (e.g. `bin/`, `agents/`, `references/`) with concise descriptions.
2. **Reconcile Documented Commands**:
   - Cross-check every documented command in `README.md`, `CONTRIBUTING.md`, and `AGENTS.md` against manifests and actual execution.
   - Replace outdated commands (e.g., `python script.py` where `python3` is required, or obsolete runner scripts) with the verified commands discovered in Phase 1.
3. **Maintain Agent Rule Symmetry**:
   - Ensure repository instructions (`AGENTS.md` and agent symlinks or mirrors like `CLAUDE.md`) are unified and reflect current repository boundaries and conventions.
   - Remove obsolete negative boundaries that contradict current architectural patterns.

### Phase 3: Reference & Link Sanitization

Scan documentation and code files for broken references and leaked environment paths:

1. **Run the Reference Auditor**:
   Execute the bundled auditor helper to scan for leaked environment paths and broken relative links:
   ```bash
   python3 skills/audit-align/scripts/audit_refs.py .
   ```
2. **Scrub Leaked Absolute Paths**:
   - Remove or convert any host-specific paths (`file:///workspaces/...`, `/Users/...`, `/home/...`) to clean, relative paths (`docs/guide.md` or `[guide](docs/guide.md)`).
   - Ensure documentation links are portable across all platforms, containers, and CI environments.
3. **Repair Broken Internal Links**:
   - Fix broken relative Markdown links (`[label](path/to/file.md)`) pointing to moved or deleted files.
   - Update script command references in documentation when scripts have been reorganized.

### Phase 4: Interface & Docstring Parity

Stale docstrings poison an agent's understanding of function calls and types:

1. **Audit Exported Signatures**:
   - For key modules, libraries, or shared helpers, compare function/method signatures against their docstrings (JSDoc, Python docstrings, Go comments, Rust doc comments).
2. **Remediate Signature Drift**:
   - **Deleted Parameters**: Remove `@param` / docstring entries for parameters that no longer exist in the function signature.
   - **Renamed or New Parameters**: Update parameter names and document new required or optional arguments.
   - **Return Types**: Verify described return values match actual return types and behavior.
   - **Phantom Exceptions**: Remove claims that functions throw errors or exceptions that were refactored away.
3. **Eliminate Misleading "Docstring Lies"**:
   - If docstrings claim "defaults to X" when the code defaults to Y, update the docstring to match the code reality.

### Phase 5: Inline Comment & Zombie Code Triage

1. **Triage Inline Comments**:
   - Find and review comments asserting outdated constraints (e.g., `// Note: X is not supported` when X was implemented months ago).
   - Remove defensive comments that explain bugs or workarounds that have already been fixed.
2. **Prune "Zombie Code" (Commented-out Implementation Blocks)**:
   - Identify multi-line commented-out code blocks left behind during refactoring or experiments.
   - **Delete them**: Git history retains the historical implementation. Commented-out code causes agents to doubt the active implementation or accidentally revive deprecated logic.
3. **Review TODOs and FIXMEs**:
   - Delete TODOs for features or fixes that have already been completed.
   - For remaining valid TODOs, verify that they accurately reflect current codebase reality rather than an obsolete roadmap.

### Phase 6: Verification & Non-Regression

1. **Run Automated Validation**:
   - Re-run the reference auditor to verify zero broken links or leaked absolute paths:
     ```bash
     python3 skills/audit-align/scripts/audit_refs.py .
     ```
   - Execute project test and validation suites (`npm test`, `pytest`, etc.).
2. **Review the Git Diff**:
   - Inspect the complete diff (`git diff`).
   - Confirm that changes are restricted to:
     - Correcting stale documentation and instructions.
     - Aligning docstrings and comments with code.
     - Scrubbing dead links and leaked environment paths.
     - Pruning zombie code.
   - Ensure no unintended functional behavior regressions were introduced into active code.

---

## Specific Techniques / Patterns

### Pattern 1: Ground-Truth Tree Generation

Avoid guessing directory layouts. Generate a clean snapshot from git tracking:

```bash
# List top-level structure and immediate subdirectories without clutter
git ls-files | awk -F/ '{if (NF>1) print $1"/"$2; else print $1}' | sort -u
```

Use this output to construct an accurate, minimal directory tree for `README.md` and `AGENTS.md`.

### Pattern 2: Verifying Commands Before Documenting

Never document a command from memory or assume it still works. Test every command in the terminal:

```bash
# Test whether documented commands actually succeed
npm run test
npm run validate
node bin/cli.js --help
```

If a command fails or emits deprecation warnings, investigate whether the command, the script, or the configuration needs alignment.

### Pattern 3: Scrubbing Leaked Environment Paths

Replace environment-specific links with portable Markdown links:

```markdown
<!-- Bad: Breaks outside original devcontainer / machine -->
[Runners](file:///workspaces/my-repo/scripts/runners.py)
[Config](/home/user/project/config.json)

<!-- Good: Portable across any clone, CI, or agent runtime -->
[Runners](scripts/runners.py)
[Config](config.json)
```

### Pattern 4: Docstring Parity Check

When auditing source files, check signatures against docstrings:

```python
# Bad: Stale docstring describes old signature
def process_data(data: dict, validate: bool = True) -> dict:
    """
    Process raw payload.

    Args:
        data: The input dictionary.
        schema_path: Path to validation schema.  <-- STALE (param removed)
        output_format: Output serialization.     <-- STALE (param removed)
    """

# Good: Aligned with current signature
def process_data(data: dict, validate: bool = True) -> dict:
    """
    Process raw payload.

    Args:
        data: The input dictionary.
        validate: Whether to validate input before processing.
    """
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Comments don't affect runtime execution, so leaving them alone is harmless." | For AI coding agents, comments are high-priority context. Stale comments directly cause hallucinations, invalid workarounds, and bugs. |
| "I can update the directory tree in README from memory without checking disk." | Memory and assumptions are how trees drifted in the first place. Every path in documentation must be checked against the filesystem. |
| "The command in the docs worked before, so it's fine to keep as-is." | Toolchain upgrades, renamed scripts, and flag changes break commands silently. Every documented command must be tested. |
| "We should keep commented-out code in case someone needs to reference it." | Version control (git) is the permanent archive. Commented-out code pollutes agent context and tempts agents into reviving deprecated patterns. |
| "Absolute links like `file:///workspaces/...` are convenient in my editor." | Hardcoded absolute paths break for every other collaborator, CI pipeline, and agent running in a different directory or machine. |
| "Updating docstrings takes too much time; code changes are enough." | An agent reading a stale docstring will pass deprecated arguments or misinterpret return types, leading to avoidable runtime failures. |

---

## Red Flags

Watch for these warning signs during audits and reviews:
- **Leaked Local URIs**: Any occurrence of `file:///`, `/workspaces/`, `/home/`, or `/Users/` committed to repository files.
- **Phantom Files in Documentation**: Documenting directories, scripts, or config files in `README.md` or `AGENTS.md` that do not exist on disk.
- **Untested Documented Commands**: Adding or updating commands in docs without executing them to confirm success.
- **Docstring Signature Mismatch**: Docstrings listing parameters that have been removed or renamed in code.
- **Zombie Code Clusters**: Blocks of commented-out logic retained in source files instead of relying on git history.
- **Creeping Functional Refactors**: Modifying core business logic or changing public APIs during what was intended to be an alignment and cleanup task.

---

## Verification

Before concluding an `audit-align` task, confirm every item on this checklist:

- [ ] **Filesystem Ground Truth Verified**: Directory structures in `README.md`, `AGENTS.md`, and docs match actual disk contents (`git ls-files`).
- [ ] **Documented Commands Tested**: Every command mentioned in `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, or package manifests executes successfully.
- [ ] **No Leaked Environment Paths**: Ran `python3 skills/audit-align/scripts/audit_refs.py .` and verified zero leaked absolute paths (`file:///`, `/workspaces/`, etc.).
- [ ] **Zero Broken Internal Links**: All relative Markdown links and script references resolve to existing files.
- [ ] **Docstrings Synchronized**: Exported functions and modified interfaces have docstrings matching their current parameter names, types, and return values.
- [ ] **Zombie Code Pruned**: Multi-line commented-out code blocks and resolved TODOs/FIXMEs removed.
- [ ] **Agent Config Symmetry Maintained**: `AGENTS.md`, `CLAUDE.md`, and any related agent rule files are aligned and consistent.
- [ ] **Tests and Linters Pass**: Project test suite and validation scripts (`npm test`, `npm run validate`, `pytest`, etc.) pass with zero regressions.

# Niels With Them Skills

A collection of production-grade engineering and daily task skills for AI coding agents (Google Antigravity / Gemini, Claude Code, Cursor, Codex, etc.).

## Installation in Downstream Projects

You can install skills, agent personas, and shared references directly into any downstream repository using `npx`.

### 1. Dedicated Installer (Skills + Personas + References)

Run inside your project's root directory:

```bash
# List available skills
npx github:NielsElmgaard/niels-with-them-skills --list

# Install a specific skill (e.g. skill-creator)
npx github:NielsElmgaard/niels-with-them-skills --skill skill-creator

# Install all skills, personas, and references
npx github:NielsElmgaard/niels-with-them-skills --all

# Install into a custom agent directory (default is .agents)
npx github:NielsElmgaard/niels-with-them-skills --skill skill-creator --target .claude
```

### 2. Universal Skills CLI ([skills.sh](https://skills.sh))

You can also use the open-standard `skills` CLI:

```bash
# List available skills
npx skills add NielsElmgaard/niels-with-them-skills --list

# Install a specific skill
npx skills add NielsElmgaard/niels-with-them-skills --skill skill-creator

# Install all skills
npx skills add NielsElmgaard/niels-with-them-skills --all
```

---

## Catalog

### Skills

- **[`audit-align`](skills/audit-align/)**: Audits and aligns repository documentation, comments, docstrings, project configuration, and commands with actual codebase reality to eliminate misleading context.
- **[`design-api-and-interface`](skills/design-api-and-interface/)**: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface.
- **[`git-keeper`](skills/git-keeper/)**: Structures disciplined git workflows including atomic commits, branch isolation, save points, conventional commit messages, pre-commit checks, and release versioning.
- **[`phasing-out-and-migration`](skills/phasing-out-and-migration/)**: Manages phasing out and migration of old systems, APIs, or database schemas (expand/contract).
- **[`prepare-shipping`](skills/prepare-shipping/)**: Prepares production launches, pre-launch checklists, monitoring, staged rollouts, and rollback strategies.
- **[`review-that-code`](skills/review-that-code/)**: Conducts multi-axis code reviews across correctness, readability, architecture, security, and performance.
- **[`skill-creator`](skills/skill-creator/)**: Guides agents and users through creating new skills, refining existing skills, and measuring skill performance with evals and benchmarks across AI coding agents.

### Agent Personas

- **[`code-reviewer`](agents/code-reviewer.md)**: Staff Engineer code reviewer evaluating changes across correctness, readability, architecture, security, and performance.
- **[`security-auditor`](agents/security-auditor.md)**: Security engineer focused on vulnerability detection, threat modeling, and secure coding practices.
- **[`test-engineer`](agents/test-engineer.md)**: QA engineer specialized in test strategy, test writing, and coverage analysis.
- **[`web-performance-auditor`](agents/web-performance-auditor.md)**: Web performance engineer focused on Core Web Vitals, loading, rendering, and network optimization.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for pre-flight checks, template conventions, and eval requirements before adding or modifying skills.

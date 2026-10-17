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

# Install the AI Software Factory (skills, personas, references, and visual factory/ board)
npx github:NielsElmgaard/niels-with-them-skills --factory --target .claude
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
- **[`brainstormer`](skills/brainstormer/)**: Generates and refines project ideas through GitHub portfolio analysis and Socratic product, vibe, audience, and business-model interviewing without premature tech-stack decisions.
- **[`design-api-and-interface`](skills/design-api-and-interface/)**: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface.
- **[`factory`](skills/factory/)**: Orchestrates a visual multi-agent software factory loop across spec writing, worktree-isolated building, parallel multi-axis review rounds, and merge gates.
- **[`git-keeper`](skills/git-keeper/)**: Structures disciplined git workflows including atomic commits, branch isolation, save points, conventional commit messages, pre-commit checks, and release versioning.
- **[`phasing-out-and-migration`](skills/phasing-out-and-migration/)**: Manages phasing out and migration of old systems, APIs, or database schemas (expand/contract).
- **[`prepare-shipping`](skills/prepare-shipping/)**: Prepares production launches, pre-launch checklists, monitoring, staged rollouts, and rollback strategies.
- **[`review-that-code`](skills/review-that-code/)**: Conducts multi-axis code reviews across correctness, readability, architecture, security, and performance.
- **[`skill-creator`](skills/skill-creator/)**: Guides agents and users through creating new skills, refining existing skills, and measuring skill performance with evals and benchmarks across AI coding agents.

### Agent Personas

- **[`brainstormer`](agents/brainstormer.md)**: Product Ideation & Vibe Strategist (`opus` / `Gemini 4 Argon`) that analyzes GitHub portfolios for tailored project ideas and refines raw concepts across vibe, audience, and business model into `IDEA.md`.
- **[`spec-writer`](agents/spec-writer.md)**: Staff Product & Systems Architect (`opus` / `Gemini 4 Argon`) that inspects the codebase and writes grounded, testable specifications (`spec.md`).
- **[`builder`](agents/builder.md)**: Senior Implementation Engineer (`opus` / `Gemini 4 Argon`) that implements specs and resolves review rounds inside isolated git worktrees.
- **[`code-reviewer`](agents/code-reviewer.md)**: Staff Engineer code reviewer (`sonnet` / `Gemini 3.8 Flash`) evaluating changes across correctness, readability, architecture, security, and performance.
- **[`security-auditor`](agents/security-auditor.md)**: Security engineer (`opus` / `Gemini 4 Argon`) focused on vulnerability detection, threat modeling, and secure coding practices.
- **[`test-engineer`](agents/test-engineer.md)**: QA engineer (`sonnet` / `Gemini 3.8 Flash`) specialized in test strategy, test writing, and coverage analysis.
- **[`ui-ux-reviewer`](agents/ui-ux-reviewer.md)**: Product Designer & Accessibility Specialist (`sonnet` / `Gemini 3.8 Flash`) evaluating UX states, UI consistency, and WCAG 2.1 AA compliance.
- **[`web-performance-auditor`](agents/web-performance-auditor.md)**: Web performance engineer (`sonnet` / `Gemini 3.8 Flash`) focused on Core Web Vitals, loading, rendering, and network optimization.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for pre-flight checks, template conventions, and eval requirements before adding or modifying skills.

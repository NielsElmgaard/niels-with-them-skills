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

- **[`skill-creator`](skills/skill-creator/)**: Guides agents and users through creating new skills, refining existing skills, and measuring skill performance with evals and benchmarks across AI coding agents.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for pre-flight checks, template conventions, and eval requirements before adding or modifying skills.

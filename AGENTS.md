# niels-with-them-skills

This is the niels-with-them-skills project. My collection of engineering skills and other daily tasks for AI coding agents that I use on daily basis.

> **Scope:** This file configures agents working on the [`NielsElmgaard/niels-with-them-skills`](https://github.com/NielsElmgaard/niels-with-them-skills) repository itself, not other projects. Don't copy it into another project or a global agent configuration; the reusable assets are the skills in `skills/`.

## Project Structure

```
├── agents/ (Reusable agent personas)
├── evals/ (Skill eval cases)
├── references/ (Shared references for multiple skills)
├── skills/
│   ├── skill-name/
│   │   ├── SKILL.md (required)
│   │   ├── YAML frontmatter (required: name, description)
│   │   ├── references/ (optional: Skill-specific reference documentation)
│   │   ├── assets/ (optional: Files used in output (templates, icons, fonts))
│   │   ├── scripts/ (optional: Runnable helpers used by the skill workflow)
│   │   └── supporting-file.md (optional: Reference material loaded on demand)
│   └──
├── .gitignore
├── AGENTS.md
├── CONTRIBUTING.md
└── README.md

```

## Skills by use


## Conventions

- Every skill lives in `skills/<name>/SKILL.md`
- YAML frontmatter with `name` and `description` fields
- Description starts with what the skill does (third person), followed by trigger conditions ("Use when...")
- Every skill has: Overview, When to Use, Process, Common Rationalizations, Red Flags, Verification
- Shared references are in the root `references/` directory; the emerging convention for self-contained, distributable skills keeps a skill's own references inside `skills/<name>/references/`
- Supporting files only created when content exceeds 100 lines

## Contributing

Before adding a new skill or significantly reworking an existing one, run the pre-flight checks in [CONTRIBUTING.md](CONTRIBUTING.md#before-proposing-a-new-skill): search the catalog, check open PRs, confirm the idea fits [references/skill-template.md](references/skill-template.md), and justify the gap. Prefer extending an existing skill over adding a near-duplicate. CONTRIBUTING.md is the single source of truth for this workflow; do not restate its checklist here or elsewhere, link to it.

## Commands

- `npm test` — Not applicable (this is a documentation project)
- Validate: Check that all SKILL.md files have valid YAML frontmatter with name and description
- Evals: `node scripts/run-evals.js` — trigger/routing evals for every skill (CI); `--behavioral <skill>` for graded runs

## Pull Requests

PRs target the upstream repository's default branch. In a typical fork setup the upstream remote is `upstream` and your fork is `origin`, but the exact remote names are not what matters here.

- Before opening a PR, search the upstream repository's open PRs and issues for work that touches the same files or rules. If any overlaps, coordinate (build on it, align your rules with it, or rebase after it merges) instead of opening a conflicting PR.
- Prefer small, focused PRs over large refactors of widely shared files (for example, files under `scripts/`), which are more likely to collide with in-flight work.

## Boundaries

- Always: Run the CONTRIBUTING.md pre-flight checks before creating a new skill directory
- Always: Follow the skill-template.md format for new skills
- Always: Check the upstream repo's open PRs and issues for overlap before opening a new PR
- Never: Add skills that are vague advice instead of actionable processes
- Never: Duplicate content between skills — reference other skills instead
# Contributing to Niels With Them Skills

Thanks for your interest in contributing! This project is a collection of production-grade engineering and daily task skills for AI coding agents.

## Adding a New Skill

### Before proposing a new skill

1. **Search the catalog.** Skim `skills/` for an existing skill that covers your idea, whole or in part. Clusters of near-duplicate skills already exist; don't add to them.
2. **Read the template.** Confirm your idea fits the format in [references/skill-template.md](references/skill-template.md), an actionable workflow with verification, not vague advice.
3. **Strip model-specific workarounds.** If a step can't be justified without naming a model, a model version, or one agent's private tool name, it doesn't belong in a skill — describe the capability instead (see [Write the Procedure, Not the Workaround](references/skill-template.md#write-the-procedure-not-the-workaround)).

If your idea is a refinement of an existing skill, prefer a focused edit to that skill over a new directory.

### Creating the skill

1. Create a directory under `skills/` with a kebab-case name
2. Add a `SKILL.md` following the format in [references/skill-template.md](references/skill-template.md)
3. Include YAML frontmatter with `name` and `description` fields
4. Ensure the `description` starts with what the skill does (third person), then includes one or more `Use when` trigger conditions

### Skill Quality Bar

Skills should be:

- **Specific** — Actionable steps, not vague advice
- **Verifiable** — Clear exit criteria with evidence requirements
- **Battle-tested** — Based on real engineering workflows, not theoretical ideals
- **Minimal** — Only the content needed to guide the agent correctly

### Structure

Every new skill must have:

- `SKILL.md` in the skill directory
- YAML frontmatter with valid `name` and `description`
- Use the `skill-creator` skill to run evals before introducing a new skill or an update to an existing

New skills should generally follow the standard template:

- **Overview** — What this skill does and why it matters
- **When to Use** — Triggering conditions
- **Process** — Step-by-step workflow
- **Common Rationalizations** — Excuses agents use to skip steps, with rebuttals
- **Red Flags** — Warning signs that the skill is being applied incorrectly
- **Verification** — How to confirm the skill was applied correctly

The frontmatter fields above are required. The section template is a recommended pattern: equivalent headings such as `How It Works`, `Workflow`, or `Core Process` are fine when they preserve the same intent and keep the skill easy to follow.

### What Not to Do

- Don't duplicate content between skills — reference other skills instead
- Don't add skills that are vague advice instead of actionable processes
- Don't create supporting files unless content exceeds 100 lines
- Don't create an empty `scripts/` directory just to match another skill — add `scripts/` only when the skill includes runnable helpers
- Don't put reference material inside skill directories — use `references/` instead

## Modifying Existing Skills

Before proposing a change, search the [skill-change rejection ledger](evals/skill-impact.md) for previous attempts affecting the same skill and review their eval evidence.

- Keep changes focused and minimal
- Preserve the existing structure and tone
- Test that YAML frontmatter remains valid after edits

If a skill or description change is rejected based on eval results, add one row to the ledger with the date, affected skill, concise attempted change, before-to-after rank-1 score, and rejected PR link and outcome. Land that ledger-only update separately on the default branch; do not leave it only on the rejected proposal branch, where closing or force-pushing the proposal could discard the record.

## Repo-scoped files

`AGENTS.md` and `CLAUDE.md` at the repo root configure agents working on the [`NielsElmgaard/niels-with-them-skills`](https://github.com/NielsElmgaard/niels-with-them-skills) repository itself. When writing setup guides or docs, do not instruct users to copy these files into their own projects or into a global agent configuration; the reusable assets are the skills in `skills/`.

---
name: skill-creator
description: Guides agents and users through creating new skills, refining existing skills, and measuring skill performance with evals and benchmarks across AI coding agents (Gemini/agy, Claude, Codex, etc.). Use when authoring a new skill from scratch, modifying or improving existing skill workflows, benchmarking skill performance against baselines, or optimizing skill descriptions for accurate triggering.
---

# Skill Creator

A skill for creating new agent skills, refining existing skills, and iteratively measuring performance across AI coding agents.

## Overview

The `skill-creator` guides an AI agent through a rigorous pair-programming workflow with the user to produce production-grade, model-neutral skills. Skills are capability packages containing clear procedural instructions, trigger descriptions, anti-rationalization tables, red flags, verification checklists, and optional bundled resources (scripts, references, assets).

This skill standardizes the end-to-end authoring lifecycle:
1. Understanding intent and gathering requirements.
2. Authoring clean, model-neutral skills following [references/skill-template.md](../../references/skill-template.md).
3. Defining realistic test prompts and running baseline comparisons.
4. Grading outputs, calculating benchmarks, and reviewing results interactively.
5. Optimizing triggering descriptions with automated train/test evaluation loops.

---

## When to Use

Use this skill when:
- Authoring a new skill from scratch based on a user idea or conversation history.
- Refactoring, improving, or updating an existing skill in `skills/`.
- Creating test cases (`evals/evals.json`) and benchmarking an agent's performance with a skill vs. without it (or vs. an older version).
- Tuning and optimizing a skill's description in YAML frontmatter for higher triggering precision and recall.
- Packaging a skill for distribution.

When NOT to use:
- Generating one-off project code or scripts that are not intended to be reused as an agent skill.
- Modifying general repository rules (`AGENTS.md`) that apply globally across all tasks rather than a focused domain workflow.
- Testing non-skill codebases where standard project test suites (`npm test`, `pytest`) apply.

---

## Core Process

The skill authoring workflow follows structured phases:

```
[Phase 1: Intent & Scope] ──> [Phase 2: Author SKILL.md] ──> [Phase 3: Test Cases & User Choice]
                                                                        │
                                        ┌───────────────────────────────┴───────────────────────────────┐
                                        ▼                                                               ▼
                              [Automated Evals]                                              [Manual User Testing]
                        Phase 4: Run, Grade & Benchmark                                        User tests skill directly
                                        │                                                               │
                                        ▼                                                               ▼
                        Phase 5: Iteration Loop                                                User shares feedback
                                        │                                                               │
                                        ▼                                                               ▼
                        Phase 6: Trigger Tuning                                                Refine & Exit
```

### Phase 1: Intent & Scope Interview

Extract what the user actually wants the skill to accomplish:
1. **Analyze conversation context**: Often the user says "turn this into a skill" after completing a task. Extract tools used, sequences of steps, edge cases discovered, and corrections made.
2. **Clarify core intent**:
   - What capability should this skill grant to the AI agent?
   - When should the skill trigger (user phrasing, file types, project contexts)?
   - When should it NOT trigger (adjacent domains, simple queries the agent handles natively)?
   - What tools, runtimes, or libraries are required?
3. **Interview for edge cases**: Proactively ask about input/output formats, example files, error recovery, and success criteria before writing test cases.
4. **Research existing patterns**: Search `skills/` for existing skills covering similar domains. Check available tools and documentation in parallel using subagents if supported.

### Phase 2: Author the SKILL.md and Supporting Resources

Every skill created must follow the format defined in [references/skill-template.md](../../references/skill-template.md).

#### Frontmatter
```yaml
---
name: kebab-case-name
description: Guides agents through [task]. Use when [positive triggers].
---
```
- **name**: Lowercase, hyphen-separated, max 64 characters. Matches the directory name.
- **description**: Third-person summary ("Guides...", "Automates..."), followed by clear "Use when..." conditions. Max 1024 characters. Do not put step-by-step instructions in the description.

#### Standard Sections
Structure the markdown content with these sections:
1. `# Skill Title`: Concise title.
2. `## Overview`: 1-2 sentences explaining what the skill does and why it matters.
3. `## When to Use`:
   - Positive triggers (symptoms, user intents, task types).
   - Negative exclusions (when NOT to use; what other skills or default agent capabilities apply).
4. `## Core Process` / `## Workflow`: Step-by-step procedural instructions. Imperative form. Specific commands and verifiable actions.
5. `## Specific Techniques / Patterns`: Detailed guidance, code snippets, templates, or architectural rules.
6. `## Common Rationalizations`: Table pairing excuses agents make to skip steps with reality rebuttals.
7. `## Red Flags`: Observable behavioral signs that the skill is being violated during execution.
8. `## Verification`: Exit criteria checklist with evidence requirements.

#### Bundled Resources
- `scripts/`: Deterministic or repetitive tasks (bash or python helpers).
- `references/`: Detailed reference documentation loaded on demand (when >100 lines). Shared references across skills live in repository-root `references/`.
- `assets/`: Templates, fixtures, icons, or sample files.

### Phase 3: Test Cases & Evaluation Choice

Every skill with verifiable outcomes needs realistic test prompts.
Save test cases to `evals/evals.json` (see [references/schemas.md](references/schemas.md)):

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user prompt with specific details, context, and file names",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Design realistic test queries:
- **Realistic detail**: Include file names, column headers, personal context, or casual speech rather than abstract commands.
- **Discriminative prompts**: Test tasks where consulting the skill makes a measurable difference in accuracy or quality.

#### Confirm Evaluation Preference with the User
Before executing automated test runs or writing assertions, **always ask the user**:
- **Automated evaluation**: The agent executes test cases against baselines, measures telemetry, grades assertions, and optimizes trigger descriptions (proceed to Phase 4).
- **Manual user testing**: The user tests the newly authored skill themselves. The agent presents example test queries from `evals.json`, provides instructions on how to test and what to observe, and waits for user feedback.

If the user chooses manual testing:
1. Skip Phase 4 (automated execution/grading) and Phase 6 (automated runner loops).
2. Present the user with clear instructions and sample prompts to run in their session.
3. Review the user's manual testing observations, incorporate their requested adjustments into `SKILL.md`, and verify against the checklist before finalizing.

### Phase 4: Execution, Grading, & Benchmarking (Automated Path)

Execute test cases in `<skill-name>-workspace/iteration-<N>/`:

1. **Run With-Skill and Baseline**:
   - For each test case, run two executions:
     - **With-skill run**: Agent has access to the candidate skill. Save outputs to `with_skill/outputs/`.
     - **Baseline run**: For a new skill, run without the skill (save to `without_skill/outputs/`). For an existing skill, snapshot the old skill and run against the snapshot (save to `old_skill/outputs/`).
   - If using subagents (e.g., `invoke_subagent`), launch with-skill and baseline runs concurrently.
2. **Draft Assertions**:
   - While runs execute, draft objective assertions in `eval_metadata.json` for each test case.
   - Assertions must check genuine substance and outcomes (e.g. file content, schema compliance, correct calculation), not mere existence of a file.
3. **Capture Telemetry**:
   - Save execution time, tokens, and tool calls to `timing.json`.
4. **Grade Results**:
   - Grade each assertion (PASS/FAIL with evidence) into `grading.json`.
   - Programmatic grading scripts should be used whenever assertions are deterministic.
5. **Aggregate Benchmark**:
   - Run the aggregation script from the skill-creator directory:
     ```bash
     python3 -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
     ```
   - Produces `benchmark.json` and `benchmark.md` with pass rates, duration, and token usage.
6. **Launch Human Review Viewer**:
   ```bash
   python3 skills/skill-creator/eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "<name>" --benchmark <workspace>/iteration-N/benchmark.json
   ```
   In headless or remote environments, pass `--static <output.html>` to generate a standalone HTML file and collect `feedback.json`.

### Phase 5: Feedback & Iteration Loop

1. **Read Feedback**: Review user notes and ratings in `feedback.json`.
2. **Generalize**:
   - Do not overfit to specific test prompt quirks.
   - Look for systemic root causes in why an agent took a wrong approach.
   - Clarify the *why* behind instructions instead of adding aggressive capitalized commands.
   - Check if subagents repeatedly wrote similar custom scripts — if so, bundle that script into `scripts/`.
3. **Repeat**:
   - Update the skill.
   - Run a new iteration (`iteration-<N+1>`), comparing with baseline or prior iteration.
   - Continue until all assertions pass and user feedback is positive.

### Phase 6: Description Optimization

The frontmatter `description` determines whether agents activate the skill. After the skill workflow is finalized, optimize the description for triggering precision and recall.

1. **Generate Eval Queries**:
   - Create 20 queries (8-10 should-trigger, 8-10 should-not-trigger / near-misses).
   - Review queries with the user via `assets/eval_review.html`.
2. **Run Optimization Loop**:
   Run the optimization loop using the pluggable agent runner:
   ```bash
   python3 -m scripts.run_loop \
     --eval-set <path-to-eval-queries.json> \
     --skill-path <path-to-skill> \
     --agent-runner auto \
     --max-iterations 5 \
     --verbose
   ```
   The runner automatically uses `agy` (Gemini), `claude`, or a configured generic CLI. It splits queries into train (60%) and held-out test (40%), evaluates trigger rates across multiple runs, and iteratively optimizes the description without overfitting.
3. **Apply the Best Description**:
   Update `SKILL.md` frontmatter with the description that achieved the highest test score.

---

## Specific Techniques / Patterns

### Model-Neutral Authoring ("Write the Procedure, Not the Workaround")

Skills must run reliably across different agent runtimes and model generations (Gemini, Claude, GPT, etc.):
- **Describe capabilities, not private tool names**: State "view the file" or "inspect the contents" rather than hardcoding agent-specific API methods.
- **Explain the rationale ("the why")**: Models with strong reasoning follow instructions better when they understand the purpose behind a constraint.
- **Avoid single-model workarounds**: If an instruction exists solely because a specific model version failed a step, fix the prompt generally or report it as an engine issue.

### Pluggable Agent Runners

The evaluation harness in `scripts/` uses a modular runner architecture ([scripts/runners.py](scripts/runners.py)):
- **`agy`**: Google Antigravity / Gemini CLI. Discovers temporary skills in `.agents/skills/<clean_name>/SKILL.md` and detects execution via stream events or transcript logs.
- **`claude`**: Anthropic Claude Code CLI. Discovers temporary skills in `.claude/commands/<clean_name>.md`.
- **`generic`**: Configurable agent CLI or API runner configured via `AGENT_QUERY_CMD` and `AGENT_LLM_CMD`.
- **`auto`**: Auto-detects available CLI in the current environment (defaults to `agy` or `claude`).

Runners can be specified on the command line:
```bash
# Explicitly use agy
python3 -m scripts.run_eval --eval-set evals/trigger.json --skill-path skills/my-skill --agent-runner agy

# Explicitly use claude
python3 -m scripts.run_eval --eval-set evals/trigger.json --skill-path skills/my-skill --agent-runner claude
```

### Progressive Disclosure and Context Efficiency

Keep skills lightweight in context:
- Keep `SKILL.md` under 500 lines.
- Move detailed reference tables or specs (>100 lines) into `references/` within the skill or shared repository references.
- Prefer runnable scripts in `scripts/` over inline code blocks when the procedure is deterministic. Inline code consumes tokens on every skill load; executing a script consumes no context until output is printed.

### Blind A/B Comparison (Advanced)

When comparing two candidate skill designs objectively:
- Use [agents/comparator.md](agents/comparator.md) to evaluate outputs A and B without knowing which version generated which.
- Use [agents/analyzer.md](agents/analyzer.md) to inspect the transcripts of both runs and diagnose why the winning approach succeeded.

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The user's request is simple, so we can skip the interview phase." | Jumping into drafting without confirming edge cases and expected output formats leads to misaligned skills and multiple rework cycles. |
| "We don't need a Common Rationalizations table for this skill." | Rationalization tables are the single most effective defense against agents cutting corners. Every workflow has steps agents tempted to skip. |
| "I'll put step-by-step instructions in the description to make sure it triggers." | Putting workflow steps in the description causes models to follow the brief description summary instead of reading the full `SKILL.md`. |
| "Writing assertions takes too much time; eyeballing the outputs is enough." | Unchecked outputs hide regressions. Objective assertions and quantitative pass rates are required to know if an edit actually improved the skill. |
| "I should make the description 'pushy' with all-caps MUSTs to force triggering." | Heavy-handed descriptions cause false triggers on adjacent tasks. Accurate third-person summaries with precise "Use when" conditions achieve balanced precision and recall. |
| "We only test on one agent, so model-specific tool references are fine." | Skills in this repository are shared assets used across multiple agent runtimes. Hardcoding model-specific mechanics breaks portability. |
| "I should automatically launch benchmark runs without asking the user." | Automated test runs consume significant time, turns, and token budgets. Always confirm whether the user wants automated evals or prefers testing the skill manually. |

---

## Red Flags

Watch for these anti-patterns during authoring and review:
- **Model-Specific Tool References**: Mentioning runtime-specific tools (e.g. `run_command`, `bash`, `write_to_file`) in skill bodies instead of describing procedural actions.
- **Missing Frontmatter or Malformed YAML**: Lacking `name` or `description`, or using unquoted strings that break YAML parsing.
- **Bloated SKILL.md**: A single `SKILL.md` exceeding 500 lines instead of offloading reference material to `references/` or helper code to `scripts/`.
- **Trivial Assertions**: Writing assertions that only verify a file was created rather than validating the accuracy, schema, and correctness of its contents.
- **Unconfirmed Automated Test Execution**: Launching multi-run automated evaluation loops or benchmark suites without first asking the user if they prefer automated evals or manual testing.
- **Overfitted Fixes**: Editing a skill to hardcode a fix for a specific query string from an eval rather than solving the underlying principle.
- **Untested Descriptions**: Changing frontmatter description without verifying trigger accuracy on both positive and negative queries.

---

## Verification

Before finalizing a new or modified skill, confirm all items:

- [ ] **Frontmatter Validated**: Run `python3 skills/skill-creator/scripts/quick_validate.py skills/<skill-name>` and ensure it exits with code 0.
- [ ] **Required Sections Present**: `SKILL.md` contains `# Title`, `## Overview`, `## When to Use` (including positive triggers and negative exclusions), `## Core Process`, `## Common Rationalizations` table, `## Red Flags`, and `## Verification` checklist.
- [ ] **Model-Neutral**: Verified that instructions describe capabilities and actions rather than private agent tool names or workarounds for a specific model generation.
- [ ] **Context Budget Respected**: `SKILL.md` is under 500 lines. Supporting reference material (>100 lines) is placed in `references/`.
- [ ] **Test Cases Defined**: `evals/evals.json` exists with at least 2-3 realistic, discriminative user test prompts.
- [ ] **Evaluation Preference Confirmed**: Asked the user whether to run automated evaluations/benchmarks or let them test the skill manually before starting test executions.
- [ ] **Evaluated (Automated or Manual)**: Either executed automated benchmarks against baseline (with recorded timing/token metrics) or guided the user through manual testing and incorporated feedback.
- [ ] **Exit Criteria Verifiable**: Every checkbox in the skill's own `## Verification` section requires concrete proof/evidence.
- [ ] **Trigger Evaluated**: Description tested with `scripts/run_eval.py` or optimized with `scripts/run_loop.py` to ensure high precision on positive cases and zero false triggers on negative cases (when automated evals are chosen).

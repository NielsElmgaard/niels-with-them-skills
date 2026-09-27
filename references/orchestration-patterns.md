# Orchestration Patterns

A practical guide to agent orchestration patterns, delegation workflows, and anti-patterns for AI coding agents.

## Governing Rule

**The user (or top-level command) is the orchestrator.** Work is delegated to focused agents or subagents with clear, single responsibilities.

- **Flat hierarchy:** Keep orchestration depth at depth ≤ 1 (orchestrator → leaf agent). Personas and subagents do not invoke other personas.
- **No autonomous meta-orchestrators:** Avoid router agents whose sole job is deciding which agent to call or paraphrasing results. They introduce semantic drift and double token consumption.
- **Preserve human checkpoints:** High-judgment phase transitions (e.g., spec → plan → build → review) should remain driven by the user or explicit top-level workflow commands.

---

## Endorsed Patterns

### Pattern 1: Direct Invocation (Single Agent, Single Artifact)

The default and lowest-overhead pattern. One agent or persona handles one bounded task against a specific target.

```
User / Command → Agent → Result → User
```

- **Use when:** The task requires a single perspective or modification on one artifact, describable in a single prompt.
- **Examples:**
  - "Review `auth.ts` for security vulnerabilities."
  - "Add unit test coverage for the payment webhook handler."
- **Trade-offs:** Minimal token consumption and latency; zero coordination overhead; avoids summarization context drift.

### Pattern 2: Parallel Division of Labor (Decoupled Subagents)

Independent subagents execute concurrently across decoupled tasks or files, returning results to the caller for synthesis.

```
                 ┌─→ Subagent A (Domain / Task 1) ─┐
User / Command ──┼─→ Subagent B (Domain / Task 2) ─┼─→ Caller Synthesis
                 └─→ Subagent C (Domain / Task 3) ─┘
```

- **Use when:** Subtasks are genuinely independent with no ordering dependencies or shared mutable state.
- **Isolation strategies:**
  - **Git worktrees or branches:** Isolate working trees when multiple agents make filesystem modifications.
  - **Distinct directories/files:** Assign non-overlapping path scopes to each subagent.
  - **Context preservation:** Isolate heavy research/investigation to prevent bloating the parent context window.
- **Trade-offs:** Higher total token usage, but significantly lower wall-clock time and sharper focus per subagent.

### Pattern 3: Sequential Pipeline / Review Handoff

Staged execution where output from one agent feeds into the next, with human or deterministic checkpoints between stages.

```
User / Command → Implementer Agent → Code / Artifact → Reviewer Agent → Verification
```

- **Use when:** Downstream work strictly depends on upstream deliverables, or when authoring requires independent validation.
- **Examples:**
  - Implementation agent produces a feature branch → Reviewer agent conducts a multi-axis review.
  - Research subagent produces a digest → Implementation agent executes using the digest.
- **Best Practice:** Pass concrete artifacts (commit hashes, diffs, or structured files) between stages rather than raw conversational summaries.

---

## Anti-Patterns

### 1. Agent-Calling-Agent Recursion Storms
- **Problem:** Subagents recursively spawning other subagents, creating deep call hierarchies, runaway token costs, and loss of context.
- **Fix:** Enforce a hard delegation depth limit of 1. Only the user or root command orchestrates.

### 2. Unbounded Agent Loops Without Exit Criteria
- **Problem:** Autonomous retry/fix loops that cycle indefinitely when encountering persistent test failures or reviewer rejections.
- **Fix:** Set hard iteration caps (e.g., maximum 2–3 attempts), require concrete error diffs, and fail fast back to the user.

### 3. Vague Delegation Prompts
- **Problem:** Handing off underspecified instructions ("fix the codebase", "make tests pass") that force subagents to hallucinate requirements.
- **Fix:** Provide explicit boundaries: target file paths, acceptance criteria, constraints, and required output formats.

### 4. Shared Conflicting Working Tree Edits
- **Problem:** Multiple concurrent agents modifying the same repository working tree, causing race conditions and clobbered diffs.
- **Fix:** Partition tasks strictly by disjoint file boundaries or isolate agents into separate git worktrees.

---

## Delegation Checklist

Before launching a subagent or parallel workflow, verify:
- [ ] **Single Responsibility:** Is the subagent's scope restricted to a single well-defined task?
- [ ] **Boundary Isolation:** Are file paths disjoint or isolated via git worktrees to prevent edit conflicts?
- [ ] **Context Budget:** Does the prompt pass only essential context rather than dumping entire session history?
- [ ] **Exit Criteria:** Does the subagent have clear stopping conditions and structured return expectations?

---

## Pattern Selection Matrix

| Scenario | Pattern | Isolation Mechanism |
|---|---|---|
| Single-file fix or targeted review | **Pattern 1: Direct Invocation** | Current workspace |
| Multi-file refactor or independent modules | **Pattern 2: Parallel Division** | Disjoint paths or git worktrees |
| Large context scan / code search | **Pattern 2: Parallel Division** | Read-only subagent context |
| Implement then audit / multi-stage handoff | **Pattern 3: Sequential Pipeline** | Staged artifacts & human review |

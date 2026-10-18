# Reusable Agent Personas

This directory contains reusable agent persona configurations (`<persona-name>.md`) for AI coding agents (Claude Code, Google Antigravity / Gemini, Cursor, Codex, etc.).

Each persona specifies an agent role, its system prompt, tool requirements, model tier mapping, and output contracts so it works both for interactive human sessions and automated [`/factory`](../skills/factory/SKILL.md) loops.

## Persona Catalog & Model Tiers

| Persona | Primary Responsibility | Claude Code (`model`) | Gemini / Antigravity (`gemini_model` / `tier`) |
|---|---|---|---|
| [`brainstormer`](brainstormer.md) | Analyzes GitHub projects to pitch ideas and refines raw concepts on vibe, audience, and business model (`IDEA.md`) | `opus` | `gemini-4-argon` (`pro`) |
| [`spec-writer`](spec-writer.md) | Inspects repo and writes a grounded, testable `spec.md` | `opus` | `gemini-4-argon` (`pro`) |
| [`builder`](builder.md) | Implements `spec.md` and resolves review rounds in an isolated git worktree | `opus` | `gemini-4-argon` (`pro`) |
| [`security-auditor`](security-auditor.md) | Audits code changes for exploitable security vulnerabilities and STRIDE threats | `opus` | `gemini-4-argon` (`pro`) |
| [`code-reviewer`](code-reviewer.md) | Multi-axis review across correctness, readability, architecture, security, and performance | `sonnet` | `gemini-3.8-flash` (`flash`) |
| [`test-engineer`](test-engineer.md) | Designs test suites, verifies acceptance criteria coverage, and catches edge-case gaps | `sonnet` | `gemini-3.8-flash` (`flash`) |
| [`ui-ux-reviewer`](ui-ux-reviewer.md) | Evaluates UX interaction states, UI visual consistency, and WCAG 2.1 AA accessibility via Chrome DevTools MCP & static analysis | `sonnet` | `gemini-3.8-flash` (`flash`) |
| [`web-performance-auditor`](web-performance-auditor.md) | Audits Core Web Vitals (LCP, INP, CLS), loading, rendering, and network performance | `sonnet` | `gemini-3.8-flash` (`flash`) |

## Chrome DevTools MCP (Live Browser Inspection)

Both [`ui-ux-reviewer`](ui-ux-reviewer.md) and [`web-performance-auditor`](web-performance-auditor.md) support **Live DevTools Mode** when [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) is configured in your agent environment (and automatically fall back to **Static Mode** when it is not).

### Claude Code
```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

### `.mcp.json` / `mcp_config.json` (Claude Code, Gemini / Antigravity, Cursor)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Installation

To install agent personas into a project:

```bash
# Install agent personas into .agents/agents/
npx github:NielsElmgaard/niels-with-them-skills --agents

# Install the full software factory (skills + personas + references + factory/ board) into .claude/
npx github:NielsElmgaard/niels-with-them-skills --factory --target .claude
```

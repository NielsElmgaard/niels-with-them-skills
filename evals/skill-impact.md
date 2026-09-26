# Skill-Change Rejection Ledger

This ledger records attempted modifications to skills (instructions in `SKILL.md`, trigger descriptions, or bundled resources) that were evaluated and rejected based on benchmark or routing eval evidence.

Consult this ledger before proposing modifications to existing skills to avoid re-attempting changes that were previously demonstrated to degrade agent performance.

## Rejection Records

| Date | Affected Skill | Concise Attempted Change | Before Score | After Score | Rejected PR / Issue | Outcome & Notes |
|---|---|---|---|---|---|---|
| — | — | No rejected proposals recorded yet | — | — | — | Initial ledger |

## Ledger Entry Guidelines

When an eval run demonstrates that a proposed skill modification causes regressions (e.g. lower test accuracy, routing degradation, or false triggering):
1. Add one row to the table above with the date, affected skill, concise attempted change, before-to-after score, and PR/issue link.
2. Note the specific root cause discovered during the eval review.
3. Land the ledger update directly on the default branch so the rejection record is preserved even if the proposal branch is closed.

#!/usr/bin/env python3
"""Improve a skill description based on eval results.

Takes eval results (from run_eval.py) and generates an improved description
by calling an AI agent LLM runner (supports agy, claude, generic).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.runners import get_runner
from scripts.utils import parse_skill_md


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    model: Optional[str] = None,
    test_results: dict | None = None,
    log_dir: Path | None = None,
    iteration: int | None = None,
    runner_name: Optional[str] = None,
) -> str:
    """Call an AI agent runner to improve the description based on eval results."""
    runner = get_runner(runner_name)

    failed_triggers = [
        r for r in eval_results["results"]
        if r["should_trigger"] and not r["pass"]
    ]
    false_triggers = [
        r for r in eval_results["results"]
        if not r["should_trigger"] and not r["pass"]
    ]

    # Build scores summary
    train_score = f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}"
    if test_results:
        test_score = f"{test_results['summary']['passed']}/{test_results['summary']['total']}"
        scores_summary = f"Train: {train_score}, Test: {test_score}"
    else:
        scores_summary = f"Train: {train_score}"

    prompt = f"""You are optimizing a skill description for an AI coding agent skill called "{skill_name}". A "skill" is a capability package with progressive disclosure -- there's a title and description that the agent sees in its available skills list when deciding whether to invoke the skill. When activated, the agent reads SKILL.md and can leverage bundled resources (scripts, references, assets).

The description appears in the agent's "available_skills" list. When a user sends a query, the agent decides whether to invoke the skill based on this description. Your goal is to write a description that triggers for relevant queries, and does not trigger for irrelevant or adjacent queries.

Here's the current description:
<current_description>
"{current_description}"
</current_description>

Current scores ({scores_summary}):
<scores_summary>
"""
    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for r in false_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (do NOT repeat these — try something structurally different):\n\n"
        for h in history:
            train_s = f"{h.get('train_passed', h.get('passed', 0))}/{h.get('train_total', h.get('total', 0))}"
            test_s = f"{h.get('test_passed', '?')}/{h.get('test_total', '?')}" if h.get('test_passed') is not None else None
            score_str = f"train={train_s}" + (f", test={test_s}" if test_s else "")
            prompt += f'<attempt {score_str}>\n'
            prompt += f'Description: "{h["description"]}"\n'
            if "results" in h:
                prompt += "Train results:\n"
                for r in h["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    prompt += f'  [{status}] "{r["query"][:80]}" (triggered {r["triggers"]}/{r["runs"]})\n'
            if h.get("note"):
                prompt += f'Note: {h["note"]}\n'
            prompt += "</attempt>\n\n"

    prompt += f"""</scores_summary>

Skill content (for context on what the skill does):
<skill_content>
{skill_content}
</skill_content>

Based on the failures, write a new and improved description that is more likely to trigger correctly. Avoid overfitting to the specific test queries — do not produce an ever-expanding list of specific keywords. Generalize from failures to broader categories of user intent and contexts where the skill is helpful or not helpful.

Key formatting rules:
- Format: Start with what the skill does in third person (e.g. "Guides agents through...", "Automates...", "Generates..."), followed by clear trigger conditions ("Use when...").
- Do NOT summarize the step-by-step workflow inside the description — focus strictly on *what* it accomplishes and *when* to activate.
- Make the description distinctive and immediately recognizable to the agent.
- There is a hard limit of 1024 characters — descriptions over that will be truncated, so keep it comfortably under 1024 characters (aim for 100-200 words).

Please respond with only the new description text in <new_description> tags, nothing else."""

    text = runner.call_llm(prompt, model=model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip().strip('"') if match else text.strip().strip('"')

    transcript: dict = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "over_limit": len(description) > 1024,
    }

    # Safety net: rewrite if over 1024 chars
    if len(description) > 1024:
        shorten_prompt = (
            f"{prompt}\n\n"
            f"---\n\n"
            f"A previous attempt produced this description, which at "
            f"{len(description)} characters is over the 1024-character hard limit:\n\n"
            f'"{description}"\n\n'
            f"Rewrite it to be strictly under 1024 characters while keeping the most "
            f"important trigger conditions and intent coverage. Format with third-person summary then 'Use when...'. Respond with only "
            f"the new description in <new_description> tags."
        )
        shorten_text = runner.call_llm(shorten_prompt, model=model)
        match = re.search(r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL)
        shortened = match.group(1).strip().strip('"') if match else shorten_text.strip().strip('"')

        transcript["rewrite_prompt"] = shorten_prompt
        transcript["rewrite_response"] = shorten_text
        transcript["rewrite_description"] = shortened
        description = shortened

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        iter_num = iteration if iteration is not None else 0
        (log_dir / f"improve_iter_{iter_num}.json").write_text(
            json.dumps(transcript, indent=2)
        )

    return description


def main():
    parser = argparse.ArgumentParser(description="Improve a skill description based on eval results")
    parser.add_argument("--eval-results", required=True, help="Path to eval results JSON file (from run_eval.py)")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON file (list of prior attempts)")
    parser.add_argument("--model", default=None, help="Model to use for improvement (default: runner default)")
    parser.add_argument("--agent-runner", default="auto", choices=["auto", "agy", "claude", "generic"], help="Agent runner to use")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_results = json.loads(Path(args.eval_results).read_text())
    skill_path = Path(args.skill_path)

    name, current_description, content = parse_skill_md(skill_path)

    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text())

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        model=args.model,
        runner_name=args.agent_runner,
    )

    if args.verbose:
        print(f"Current: {current_description}", file=sys.stderr)
        print(f"New:     {new_description}", file=sys.stderr)

    print(new_description)


if __name__ == "__main__":
    main()

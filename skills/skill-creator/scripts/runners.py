"""Pluggable Agent Runners for skill evaluation and description optimization.

Supports:
- AgyRunner: Google Antigravity / Gemini CLI (`agy`)
- ClaudeRunner: Anthropic Claude Code CLI (`claude`)
- GenericRunner: Custom/generic agent runner via environment variable or CLI template
"""

import abc
import contextlib
import json
import os
import re
import select
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Generator, Optional


class AgentRunner(abc.ABC):
    """Abstract base class for AI agent runners."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the runner backend."""
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        """Check if this runner's CLI / prerequisites are available."""
        pass

    @abc.abstractmethod
    def find_project_root(self, start_dir: Optional[Path] = None) -> Path:
        """Locate the project root directory for this agent."""
        pass

    @abc.abstractmethod
    @contextlib.contextmanager
    def temporary_skill(
        self,
        project_root: Path,
        skill_name: str,
        skill_description: str,
        content: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """Context manager creating a temporary skill discovery file and cleaning it up.
        
        Yields the unique identifier/clean_name for the skill.
        """
        pass

    @abc.abstractmethod
    def run_query(
        self,
        query: str,
        skill_name: str,
        skill_description: str,
        timeout: int,
        project_root: Path,
        model: Optional[str] = None,
    ) -> bool:
        """Run a single query and return True if the skill was triggered/consulted."""
        pass

    @abc.abstractmethod
    def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        timeout: int = 300,
        project_root: Optional[Path] = None,
    ) -> str:
        """Run an LLM call via the agent backend and return the text response."""
        pass


class AgyRunner(AgentRunner):
    """Runner for Google Antigravity / Gemini CLI (`agy`)."""

    @property
    def name(self) -> str:
        return "agy"

    def is_available(self) -> bool:
        return shutil.which("agy") is not None

    def find_project_root(self, start_dir: Optional[Path] = None) -> Path:
        current = start_dir or Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / ".git").is_dir() or (parent / ".agents").is_dir() or (parent / "AGENTS.md").is_file():
                return parent
        return current

    @contextlib.contextmanager
    def temporary_skill(
        self,
        project_root: Path,
        skill_name: str,
        skill_description: str,
        content: Optional[str] = None,
    ) -> Generator[str, None, None]:
        unique_id = uuid.uuid4().hex[:8]
        clean_name = f"{skill_name}-skill-{unique_id}"
        skill_dir = project_root / ".agents" / "skills" / clean_name
        skill_file = skill_dir / "SKILL.md"

        try:
            skill_dir.mkdir(parents=True, exist_ok=True)
            indented_desc = "\n  ".join(skill_description.split("\n"))
            body = content if content else f"# {skill_name}\n\nThis skill handles: {skill_description}\n"
            skill_content = (
                f"---\n"
                f"name: {clean_name}\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"{body}\n"
            )
            skill_file.write_text(skill_content)
            yield clean_name
        finally:
            shutil.rmtree(skill_dir, ignore_errors=True)

    def run_query(
        self,
        query: str,
        skill_name: str,
        skill_description: str,
        timeout: int,
        project_root: Path,
        model: Optional[str] = None,
    ) -> bool:
        with self.temporary_skill(project_root, skill_name, skill_description) as clean_name:
            cmd = [
                "agy",
                "-p", query,
                "--output-format", "stream-json",
                "--dangerously-skip-permissions",
            ]
            if model:
                cmd.extend(["--model", model])

            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=str(project_root),
                )
            except Exception:
                return False

            start_time = time.time()
            triggered = False
            conv_id = None

            try:
                while time.time() - start_time < timeout:
                    if process.poll() is not None:
                        # Process exited, drain remaining lines
                        for remaining_line in process.stdout:
                            if clean_name in remaining_line or f"skills/{skill_name}" in remaining_line or f"/{skill_name}/" in remaining_line:
                                triggered = True
                                break
                        break

                    rlist, _, _ = select.select([process.stdout], [], [], 0.5)
                    if not rlist:
                        continue

                    line = process.stdout.readline()
                    if not line:
                        if process.poll() is not None:
                            break
                        continue

                    if not conv_id and '"conversation_id"' in line:
                        try:
                            d = json.loads(line)
                            conv_id = d.get("conversation_id") or d.get("step_update", {}).get("conversation_id")
                        except Exception:
                            pass

                    # Real-time trigger check: must be a view_file tool call on the skill
                    is_view_file = ('"tool_name":"view_file"' in line or '"name":"view_file"' in line or 'view_file' in line)
                    has_skill = (clean_name in line or f"{skill_name}/SKILL.md" in line or f".agents/skills/{skill_name}" in line or f"skills/{skill_name}" in line)
                    if is_view_file and has_skill:
                        triggered = True
                        break

            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()

            if triggered:
                return True

            # Fallback: check transcript if conv_id was extracted
            if conv_id:
                try:
                    transcript_path = Path.home() / ".gemini" / "antigravity-cli" / "brain" / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
                    if transcript_path.is_file():
                        with open(transcript_path, 'r', encoding='utf-8') as f:
                            for t_line in f:
                                if '"name":"view_file"' in t_line or '"tool_name":"view_file"' in t_line:
                                    if clean_name in t_line or f"{skill_name}/SKILL.md" in t_line or f".agents/skills/{skill_name}" in t_line:
                                        return True
                except Exception:
                    pass

            return False

    def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        timeout: int = 300,
        project_root: Optional[Path] = None,
    ) -> str:
        cmd = [
            "agy",
            "-p", prompt,
            "--output-format", "text",
            "--dangerously-skip-permissions",
        ]
        if model:
            cmd.extend(["--model", model])

        cwd = str(project_root) if project_root else str(Path.cwd())
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(f"agy -p exited with code {result.returncode}\nstderr: {result.stderr}")
        return result.stdout.strip()


class ClaudeRunner(AgentRunner):
    """Runner for Anthropic Claude Code CLI (`claude`)."""

    @property
    def name(self) -> str:
        return "claude"

    def is_available(self) -> bool:
        return shutil.which("claude") is not None

    def find_project_root(self, start_dir: Optional[Path] = None) -> Path:
        current = start_dir or Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / ".claude").is_dir():
                return parent
        return current

    @contextlib.contextmanager
    def temporary_skill(
        self,
        project_root: Path,
        skill_name: str,
        skill_description: str,
        content: Optional[str] = None,
    ) -> Generator[str, None, None]:
        unique_id = uuid.uuid4().hex[:8]
        clean_name = f"{skill_name}-skill-{unique_id}"
        project_commands_dir = project_root / ".claude" / "commands"
        command_file = project_commands_dir / f"{clean_name}.md"

        try:
            project_commands_dir.mkdir(parents=True, exist_ok=True)
            indented_desc = "\n  ".join(skill_description.split("\n"))
            body = content if content else f"# {skill_name}\n\nThis skill handles: {skill_description}\n"
            command_content = (
                f"---\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"{body}\n"
            )
            command_file.write_text(command_content)
            yield clean_name
        finally:
            if command_file.exists():
                command_file.unlink()

    def run_query(
        self,
        query: str,
        skill_name: str,
        skill_description: str,
        timeout: int,
        project_root: Path,
        model: Optional[str] = None,
    ) -> bool:
        with self.temporary_skill(project_root, skill_name, skill_description) as clean_name:
            cmd = [
                "claude",
                "-p", query,
                "--output-format", "stream-json",
                "--verbose",
                "--include-partial-messages",
            ]
            if model:
                cmd.extend(["--model", model])

            env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=str(project_root),
                env=env,
            )

            triggered = False
            start_time = time.time()
            buffer = ""
            pending_tool_name = None
            accumulated_json = ""

            try:
                while time.time() - start_time < timeout:
                    if process.poll() is not None:
                        break

                    rlist, _, _ = select.select([process.stdout], [], [], 0.5)
                    if not rlist:
                        continue

                    chunk = process.stdout.read1(4096).decode("utf-8", errors="replace")
                    if not chunk:
                        if process.poll() is not None:
                            break
                        continue

                    buffer += chunk
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue

                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        event_type = event.get("type")

                        if event_type == "content_block_start":
                            cb = event.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in (clean_name, f"Skill:{clean_name}"):
                                    triggered = True
                                    return True
                                pending_tool_name = tool_name
                                accumulated_json = ""

                        elif event_type == "content_block_delta":
                            delta = event.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")

                        elif event_type == "content_block_stop":
                            if pending_tool_name:
                                if clean_name in pending_tool_name:
                                    triggered = True
                                    return True
                                try:
                                    tool_input = json.loads(accumulated_json)
                                    skill_val = tool_input.get("skill", "")
                                    if clean_name in str(skill_val):
                                        triggered = True
                                        return True
                                except json.JSONDecodeError:
                                    pass
                                pending_tool_name = None
                                accumulated_json = ""

                        elif event_type == "assistant":
                            message = event.get("message", {})
                            content = message.get("content", [])
                            for block in content:
                                if block.get("type") == "tool_use":
                                    tool_name = block.get("name", "")
                                    if tool_name in (clean_name, f"Skill:{clean_name}"):
                                        triggered = True
                                        return True
                                    skill_arg = block.get("input", {}).get("skill", "")
                                    if clean_name in str(skill_arg):
                                        triggered = True
                                        return True

                return triggered
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()

    def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        timeout: int = 300,
        project_root: Optional[Path] = None,
    ) -> str:
        cmd = ["claude", "-p", "--output-format", "text"]
        if model:
            cmd.extend(["--model", model])

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        cwd = str(project_root) if project_root else str(Path.cwd())

        try:
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                env=env,
                cwd=cwd,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude -p timed out after {timeout} seconds")

        if result.returncode != 0:
            raise RuntimeError(f"claude -p exited {result.returncode}\nstderr: {result.stderr}")

        return result.stdout.strip()


class GenericRunner(AgentRunner):
    """Generic/custom runner that executes configurable commands or scripts."""

    @property
    def name(self) -> str:
        return "generic"

    def is_available(self) -> bool:
        return True

    def find_project_root(self, start_dir: Optional[Path] = None) -> Path:
        current = start_dir or Path.cwd()
        for parent in [current, *current.parents]:
            if (parent / ".git").is_dir():
                return parent
        return current

    @contextlib.contextmanager
    def temporary_skill(
        self,
        project_root: Path,
        skill_name: str,
        skill_description: str,
        content: Optional[str] = None,
    ) -> Generator[str, None, None]:
        unique_id = uuid.uuid4().hex[:8]
        clean_name = f"{skill_name}-skill-{unique_id}"
        skills_dir_name = os.environ.get("AGENT_SKILLS_DIR", ".agents/skills")
        skill_dir = project_root / skills_dir_name / clean_name
        skill_file = skill_dir / "SKILL.md"

        try:
            skill_dir.mkdir(parents=True, exist_ok=True)
            indented_desc = "\n  ".join(skill_description.split("\n"))
            body = content if content else f"# {skill_name}\n\nThis skill handles: {skill_description}\n"
            skill_content = (
                f"---\n"
                f"name: {clean_name}\n"
                f"description: |\n"
                f"  {indented_desc}\n"
                f"---\n\n"
                f"{body}\n"
            )
            skill_file.write_text(skill_content)
            yield clean_name
        finally:
            shutil.rmtree(skill_dir, ignore_errors=True)

    def run_query(
        self,
        query: str,
        skill_name: str,
        skill_description: str,
        timeout: int,
        project_root: Path,
        model: Optional[str] = None,
    ) -> bool:
        cmd_template = os.environ.get("AGENT_QUERY_CMD")
        if not cmd_template:
            # Fallback: check if agy or claude is available
            if shutil.which("agy"):
                return AgyRunner().run_query(query, skill_name, skill_description, timeout, project_root, model)
            elif shutil.which("claude"):
                return ClaudeRunner().run_query(query, skill_name, skill_description, timeout, project_root, model)
            raise RuntimeError(
                "No agent runner command configured. Set AGENT_QUERY_CMD environment variable or install 'agy' or 'claude'."
            )

        with self.temporary_skill(project_root, skill_name, skill_description) as clean_name:
            cmd = cmd_template.format(query=query, skill_name=clean_name, model=model or "")
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(project_root),
                timeout=timeout,
            )
            return clean_name in result.stdout

    def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        timeout: int = 300,
        project_root: Optional[Path] = None,
    ) -> str:
        cmd_template = os.environ.get("AGENT_LLM_CMD")
        if not cmd_template:
            if shutil.which("agy"):
                return AgyRunner().call_llm(prompt, model, timeout, project_root)
            elif shutil.which("claude"):
                return ClaudeRunner().call_llm(prompt, model, timeout, project_root)
            raise RuntimeError(
                "No LLM command configured. Set AGENT_LLM_CMD environment variable or install 'agy' or 'claude'."
            )

        cmd = cmd_template.format(prompt=prompt, model=model or "")
        cwd = str(project_root) if project_root else str(Path.cwd())
        result = subprocess.run(
            cmd,
            shell=True,
            input=prompt,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Generic LLM command failed ({result.returncode}): {result.stderr}")
        return result.stdout.strip()


def get_runner(runner_name: Optional[str] = None) -> AgentRunner:
    """Resolve and return the appropriate agent runner."""
    if runner_name and runner_name != "auto":
        name = runner_name.lower().strip()
        if name in ("agy", "gemini"):
            return AgyRunner()
        elif name in ("claude", "anthropic"):
            return ClaudeRunner()
        elif name in ("generic", "custom"):
            return GenericRunner()
        else:
            raise ValueError(f"Unknown runner '{runner_name}'. Choose from 'agy', 'claude', 'generic', or 'auto'.")

    env_runner = os.environ.get("AGENT_RUNNER")
    if env_runner:
        return get_runner(env_runner)

    if shutil.which("agy"):
        return AgyRunner()
    elif shutil.which("claude"):
        return ClaudeRunner()
    else:
        return GenericRunner()

"""
Ties Task + Environment + Agent + Grader together for a single run,
and writes a structured JSON transcript. Logging is built in from the
first real run, not deferred -- reconstructing "what happened" from
memory doesn't scale past a few failures.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from harness.agent import Agent, ToolCall
from harness.environment import PathEscapeError, Sandbox
from harness.grader import GradeResult, grade
from harness.task import Task


@dataclass
class ToolCallLog:
    turn: int
    tool_name: str
    args: dict[str, Any]
    result_summary: str
    duration_s: float


@dataclass
class RunResult:
    run_id: str
    task_id: str
    outcome: str  # "graded" | "budget_exhausted" | "harness_error"
    tool_calls: list[ToolCallLog]
    grade: dict | None
    total_duration_s: float


def run_task(task: Task, agent: Agent, max_turns: int = 20, sandbox_timeout_s: float = 10.0,
             log_dir: Path = Path("logs")) -> RunResult:
    run_id = str(uuid.uuid4())[:8]
    start = time.monotonic()
    tool_log: list[ToolCallLog] = []
    outcome = "budget_exhausted"
    grade_result: GradeResult | None = None
    last_observation: str | None = None

    with Sandbox(task, timeout_s=sandbox_timeout_s) as sb:
        for turn in range(1, max_turns + 1):
            call_start = time.monotonic()
            call: ToolCall = agent.step(last_observation)

            try:
                if call.name == "read_file":
                    obs = sb.read_file(call.args["path"])
                    summary = f"read {len(obs)} chars from {call.args['path']}"
                elif call.name == "write_file":
                    sb.write_file(call.args["path"], call.args["content"])
                    obs = "ok"
                    summary = f"wrote {len(call.args['content'])} chars to {call.args['path']}"
                elif call.name == "run_command":
                    res = sb.run_command(call.args["command"])
                    obs = res.stdout + res.stderr
                    summary = f"exit={res.exit_code} timed_out={res.timed_out}"
                elif call.name == "submit":
                    obs = "submitted"
                    summary = "agent submitted"
                else:
                    raise ValueError(f"unknown tool: {call.name}")
            except (PathEscapeError, FileNotFoundError, KeyError, ValueError) as e:
                obs = f"ERROR: {e}"
                summary = f"ERROR: {e}"

            duration = time.monotonic() - call_start
            tool_log.append(ToolCallLog(turn, call.name, call.args, summary, duration))
            last_observation = obs

            if call.name == "submit":
                grade_result = grade(task, sb)
                outcome = "graded"
                break

    total_duration = time.monotonic() - start

    result = RunResult(
        run_id=run_id,
        task_id=task.task_id,
        outcome=outcome,
        tool_calls=tool_log,
        grade=asdict(grade_result) if grade_result else None,
        total_duration_s=total_duration,
    )

    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{task.task_id}_{run_id}.json"
    log_path.write_text(json.dumps(asdict(result), indent=2, default=str))

    return result
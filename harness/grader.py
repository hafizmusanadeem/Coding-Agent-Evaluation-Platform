"""
The grader's only input is the environment's final state. It never
looks at what the agent claimed to have done, and it is the same
function whether a ScriptedAgent, a real model, or anything else
produced that state -- if it special-cased "who ran this," it
wouldn't be validating anything.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from harness.environment import Sandbox
from harness.task import Task


@dataclass
class TestVerdict:
    test_id: str
    passed: bool


@dataclass
class GradeResult:
    passed: bool
    fail_to_pass_results: list[TestVerdict]
    pass_to_pass_results: list[TestVerdict]
    raw_stdout: str
    raw_stderr: str


def _run_unittest(sandbox: Sandbox, test_ids: list[str]) -> tuple[dict[str, bool], str, str]:
    """
    Runs each test id individually via `python -m unittest <id>` so a
    crash in one test can't hide the verdict of another, and returns
    a per-test pass/fail map plus the combined raw output.
    """
    verdicts: dict[str, bool] = {}
    stdout_parts, stderr_parts = [], []
    for test_id in test_ids:
        result = sandbox.run_command(f"python3 -m unittest {test_id} -v")
        stdout_parts.append(f"--- {test_id} ---\n{result.stdout}")
        stderr_parts.append(f"--- {test_id} ---\n{result.stderr}")
        verdicts[test_id] = (result.exit_code == 0) and not result.timed_out
    return verdicts, "\n".join(stdout_parts), "\n".join(stderr_parts)


def grade(task: Task, sandbox: Sandbox) -> GradeResult:
    ftp_verdicts, ftp_out, ftp_err = _run_unittest(sandbox, task.fail_to_pass)
    ptp_verdicts, ptp_out, ptp_err = _run_unittest(sandbox, task.pass_to_pass)

    ftp_results = [TestVerdict(t, p) for t, p in ftp_verdicts.items()]
    ptp_results = [TestVerdict(t, p) for t, p in ptp_verdicts.items()]

    overall = all(v.passed for v in ftp_results) and all(v.passed for v in ptp_results)

    return GradeResult(
        passed=overall,
        fail_to_pass_results=ftp_results,
        pass_to_pass_results=ptp_results,
        raw_stdout=ftp_out + "\n" + ptp_out,
        raw_stderr=ftp_err + "\n" + ptp_err,
    )
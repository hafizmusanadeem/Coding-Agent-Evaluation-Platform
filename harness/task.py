"""
The Task is data, not code. It knows nothing about agents, models, or
how the problem gets solved -- only what the starting state is and what
must be true for a solution to count as correct.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    task_id: str
    repo_path: Path            # path to the fixture repo (source of truth, never mutated)
    problem_statement: str     # what the agent is told
    setup_commands: list[str]  # commands to run after materializing the repo (e.g. pip install)
    fail_to_pass: list[str]    # test node ids that currently fail and must pass after a fix
    pass_to_pass: list[str]    # test node ids that currently pass and must KEEP passing

    def __post_init__(self):
        if not self.repo_path.exists():
            raise ValueError(f"Task {self.task_id}: repo_path does not exist: {self.repo_path}")
        if not self.fail_to_pass:
            raise ValueError(f"Task {self.task_id}: fail_to_pass must be non-empty "
                              f"(a task with no red test isn't a task)")


def load_fixture_task(fixture_dir: Path, task_id: str, problem_statement: str,
                       fail_to_pass: list[str], pass_to_pass: list[str],
                       setup_commands: list[str] | None = None) -> Task:
    return Task(
        task_id=task_id,
        repo_path=fixture_dir,
        problem_statement=problem_statement,
        setup_commands=setup_commands or [],
        fail_to_pass=fail_to_pass,
        pass_to_pass=pass_to_pass,
    )
"""
The Environment mediates between the agent and the task. Two rules,
non-negotiable:

1. The fixture on disk is the source of truth and is NEVER mutated.
   Every run gets a fresh tempdir copy.
2. Every path the agent touches is resolved and checked to still be
   inside the sandbox root. No '../../' escapes, no reading files
   outside what this run's copy contains.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from harness.task import Task


class PathEscapeError(Exception):
    pass


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool
    duration_s: float


class Sandbox:
    def __init__(self, task: Task, timeout_s: float = 10.0):
        self.task = task
        self.timeout_s = timeout_s
        self._tmpdir: tempfile.TemporaryDirectory | None = None
        self.root: Path | None = None

    def __enter__(self) -> "Sandbox":
        self._tmpdir = tempfile.TemporaryDirectory(prefix=f"evalharness_{self.task.task_id}_")
        self.root = Path(self._tmpdir.name)
        # Copy fixture contents into the sandbox root (never touch the original)
        shutil.copytree(self.task.repo_path, self.root, dirs_exist_ok=True)
        for cmd in self.task.setup_commands:
            self.run_command(cmd)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._tmpdir is not None:
            self._tmpdir.cleanup()

    def _resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root.resolve())
        except ValueError:
            raise PathEscapeError(
                f"Path '{relative_path}' resolves outside sandbox root: {candidate}"
            )
        return candidate

    def read_file(self, relative_path: str) -> str:
        path = self._resolve(relative_path)
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        return path.read_text()

    def write_file(self, relative_path: str, content: str) -> None:
        path = self._resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def run_command(self, command: str) -> CommandResult:
        start = time.monotonic()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
            duration = time.monotonic() - start
            return CommandResult(proc.returncode, proc.stdout, proc.stderr, False, duration)
        except subprocess.TimeoutExpired as e:
            duration = time.monotonic() - start
            return CommandResult(
                exit_code=-1,
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or ""),
                timed_out=True,
                duration_s=duration,
            )
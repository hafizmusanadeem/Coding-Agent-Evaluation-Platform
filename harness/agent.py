"""
Step 1 of the checklist: a scripted agent that emits a fixed sequence
of tool calls. No model is involved. Its only job is to exercise the
sandbox + grader path so that if something breaks, the bug is
provably in the harness, not in nondeterministic model behavior.

A real (model-driven) agent will implement this same interface later:
`step(observation) -> ToolCall`, looped by the runner until `submit`
or a budget is hit. Swapping the scripted agent for a real one should
require touching nothing else in the harness -- that's the point of
having the interface at all.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolCall:
    name: str                  # "read_file" | "write_file" | "run_command" | "submit"
    args: dict[str, Any]


class Agent:
    """Interface every agent (scripted or model-driven) must implement."""

    def step(self, last_observation: Optional[str]) -> ToolCall:
        raise NotImplementedError


class ScriptedAgent(Agent):
    """
    Plays back a fixed list of ToolCalls regardless of what comes back
    from the environment. This is intentional -- a scripted agent that
    reacted to observations wouldn't be "scripted" anymore, and step 1
    needs a fully deterministic actor to validate the harness against.
    """

    def __init__(self, script: list[ToolCall]):
        self._script = list(script)
        self._i = 0

    def step(self, last_observation: Optional[str]) -> ToolCall:
        if self._i >= len(self._script):
            # Ran off the end of the script without calling submit --
            # this is a harness-authoring bug, not a runtime one, so
            # fail loudly rather than silently returning something.
            raise RuntimeError("ScriptedAgent script exhausted without a submit ToolCall")
        call = self._script[self._i]
        self._i += 1
        return call


def known_correct_fix_script(buggy_source: str) -> list[ToolCall]:
    """
    Builds the fixed sequence for the off_by_one fixture: read the file,
    apply the known-correct patch via precise string replacement (not a
    naive substring match -- that's the exact mistake that produced a
    false failure earlier while proving out the fixture by hand), then
    submit.
    """
    old = "for i in range(a, b):  # BUG: excludes b, should be range(a, b + 1)"
    new = "for i in range(a, b + 1):"
    assert old in buggy_source, "expected marker line not found in fixture source"
    fixed = buggy_source.replace(old, new)

    return [
        ToolCall("read_file", {"path": "mathutils.py"}),
        ToolCall("write_file", {"path": "mathutils.py", "content": fixed}),
        ToolCall("submit", {}),
    ]
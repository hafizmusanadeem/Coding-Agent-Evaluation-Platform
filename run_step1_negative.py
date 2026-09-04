"""
Negative-case check: an agent that reads the file, does nothing, and
submits immediately. If the grader reports pass here, the grader is
broken -- this is the "grader you haven't seen fail is not trustworthy"
test from the design writeup.
"""
from pathlib import Path

from harness.agent import Agent, ToolCall
from harness.runner import run_task
from harness.task import Task

FIXTURE = Path("tasks/fixtures/off_by_one")


class DoNothingAgent(Agent):
    """Reads the file, then submits without changing anything."""
    def __init__(self):
        self._i = 0

    def step(self, last_observation):
        self._i += 1
        if self._i == 1:
            return ToolCall("read_file", {"path": "mathutils.py"})
        return ToolCall("submit", {})


def main():
    task = Task(
        task_id="off_by_one_unfixed",
        repo_path=FIXTURE,
        problem_statement="same task, agent does not actually fix anything",
        setup_commands=[],
        fail_to_pass=["test_mathutils.TestMathUtils.test_sum_range_inclusive"],
        pass_to_pass=[
            "test_mathutils.TestMathUtils.test_double",
            "test_mathutils.TestMathUtils.test_is_even",
        ],
    )

    result = run_task(task, DoNothingAgent(), log_dir=Path("logs"))

    print(f"outcome: {result.outcome}")
    print(f"grade.passed: {result.grade['passed']}")
    for v in result.grade["fail_to_pass_results"]:
        print(f"  FAIL_TO_PASS {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")
    for v in result.grade["pass_to_pass_results"]:
        print(f"  PASS_TO_PASS {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")

    assert result.grade["passed"] is False, "GRADER BUG: rubber-stamped a pass on an unfixed bug"
    assert result.grade["fail_to_pass_results"][0]["passed"] is False
    print("\n[ok] grader correctly reported failure on an unfixed bug")


if __name__ == "__main__":
    main()
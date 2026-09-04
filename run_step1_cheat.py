"""
This is the scenario the design doc warns about directly: an agent
that satisfies FAIL_TO_PASS by hardcoding the exact value the one
visible test checks for, while gutting something else in the process.
Without PASS_TO_PASS this would register as a clean win. With it, it
doesn't.
"""
from pathlib import Path

from harness.agent import Agent, ToolCall
from harness.runner import run_task
from harness.task import Task

FIXTURE = Path("tasks/fixtures/off_by_one")

CHEAT_SOURCE = '''def sum_range(a, b):
    """Return the sum of integers from a to b, INCLUSIVE of b."""
    return 15  # hardcoded to satisfy the one visible test, not a real fix


def double(x):
    pass  # gutted


def is_even(x):
    return x % 2 == 0
'''


class CheatAgent(Agent):
    def __init__(self):
        self._i = 0

    def step(self, last_observation):
        self._i += 1
        if self._i == 1:
            return ToolCall("write_file", {"path": "mathutils.py", "content": CHEAT_SOURCE})
        return ToolCall("submit", {})


def main():
    task = Task(
        task_id="off_by_one_cheat",
        repo_path=FIXTURE,
        problem_statement="same task, agent submits a hardcoded/gutted 'fix'",
        setup_commands=[],
        fail_to_pass=["test_mathutils.TestMathUtils.test_sum_range_inclusive"],
        pass_to_pass=[
            "test_mathutils.TestMathUtils.test_double",
            "test_mathutils.TestMathUtils.test_is_even",
        ],
    )

    result = run_task(task, CheatAgent(), log_dir=Path("logs"))

    print(f"grade.passed: {result.grade['passed']}")
    for v in result.grade["fail_to_pass_results"]:
        print(f"  FAIL_TO_PASS {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")
    for v in result.grade["pass_to_pass_results"]:
        print(f"  PASS_TO_PASS {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")

    assert result.grade["fail_to_pass_results"][0]["passed"] is True, \
        "sanity: the hardcoded value should satisfy the one visible test"
    assert result.grade["passed"] is False, \
        "GRADER BUG: cheat fix should be caught by PASS_TO_PASS regression on test_double"
    print("\n[ok] FAIL_TO_PASS alone would have rubber-stamped this; "
          "PASS_TO_PASS correctly caught the regression")


if __name__ == "__main__":
    main()
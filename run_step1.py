"""
Step 1 of the checklist: scripted stand-in agent, real sandbox, real
grader, full logging. No model call anywhere in this file.
"""
from pathlib import Path

from harness.agent import ScriptedAgent, known_correct_fix_script
from harness.runner import run_task
from harness.task import Task

FIXTURE = Path("tasks/fixtures/off_by_one")


def main():
    task = Task(
        task_id="off_by_one",
        repo_path=FIXTURE,
        problem_statement=(
            "sum_range(a, b) is documented as inclusive of b, but the test "
            "test_sum_range_inclusive is failing. Fix mathutils.py so it passes "
            "without breaking test_double or test_is_even."
        ),
        setup_commands=[],
        fail_to_pass=["test_mathutils.TestMathUtils.test_sum_range_inclusive"],
        pass_to_pass=[
            "test_mathutils.TestMathUtils.test_double",
            "test_mathutils.TestMathUtils.test_is_even",
        ],
    )

    buggy_source = FIXTURE.joinpath("mathutils.py").read_text()
    script = known_correct_fix_script(buggy_source)
    agent = ScriptedAgent(script)

    result = run_task(task, agent, log_dir=Path("logs"))

    print(f"run_id:   {result.run_id}")
    print(f"task_id:  {result.task_id}")
    print(f"outcome:  {result.outcome}")
    print(f"duration: {result.total_duration_s:.3f}s")
    print(f"tool calls: {len(result.tool_calls)}")
    for tc in result.tool_calls:
        print(f"  [{tc.turn}] {tc.tool_name}: {tc.result_summary}")
    if result.grade:
        print(f"grade.passed: {result.grade['passed']}")
        print("  FAIL_TO_PASS:")
        for v in result.grade["fail_to_pass_results"]:
            print(f"    {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")
        print("  PASS_TO_PASS:")
        for v in result.grade["pass_to_pass_results"]:
            print(f"    {v['test_id']}: {'PASS' if v['passed'] else 'FAIL'}")

    # Confirm the original fixture is still buggy on disk -- the whole
    # point of copy-not-mutate.
    original = FIXTURE.joinpath("mathutils.py").read_text()
    assert "BUG" in original, "CRITICAL: original fixture was mutated by this run"
    print("\noriginal fixture on disk: still buggy (untouched) -- confirmed")


if __name__ == "__main__":
    main()
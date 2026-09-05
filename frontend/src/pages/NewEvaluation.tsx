import { useState, type FormEvent } from "react";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { Select } from "../components/ui/Select";
import { AGENTS, TASKS } from "../lib/mockData";

export function NewEvaluation() {
  const [task, setTask] = useState<string>(TASKS[0]);
  const [agent, setAgent] = useState<string>(AGENTS[0]);
  const [maxToolCalls, setMaxToolCalls] = useState("20");
  const [notice, setNotice] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice(
      `Mock only: ${agent} would run ${task} with max ${maxToolCalls} tool calls. No evaluation was executed.`,
    );
  }

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">New Evaluation</h1>
        <p className="mt-1 text-sm text-muted">
          Configure a coding-agent run. Execution is not wired up in this step.
        </p>
      </header>

      <Card className="p-5">
        <form className="space-y-5" onSubmit={handleSubmit}>
          <Select label="Task" value={task} onChange={(event) => setTask(event.target.value)}>
            {TASKS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </Select>

          <Select
            label="Agent"
            value={agent}
            onChange={(event) => setAgent(event.target.value)}
          >
            {AGENTS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </Select>

          <label className="flex flex-col gap-1.5 text-sm" htmlFor="max-tool-calls">
            <span className="text-muted">Max Tool Calls</span>
            <input
              id="max-tool-calls"
              type="number"
              min={1}
              max={200}
              value={maxToolCalls}
              onChange={(event) => setMaxToolCalls(event.target.value)}
              className="h-9 rounded-md border border-line bg-canvas px-3 font-mono text-fg hover:border-muted focus:border-accent"
            />
          </label>

          <Button type="submit">Run Evaluation</Button>
        </form>
      </Card>

      {notice ? (
        <div
          role="status"
          className="rounded-md border border-line bg-panel px-4 py-3 text-sm text-muted"
        >
          {notice}
        </div>
      ) : null}
    </div>
  );
}

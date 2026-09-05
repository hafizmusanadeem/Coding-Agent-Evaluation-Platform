import { useNavigate } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { ResultBadge } from "../components/ui/Badge";
import { EmptyState } from "../components/ui/EmptyState";
import { getDashboardMetrics, runs } from "../lib/mockData";

const metrics = getDashboardMetrics();
const recentRuns = [
  runs.find((run) => run.id === "41"),
  runs.find((run) => run.id === "40"),
  runs.find((run) => run.id === "42"),
].filter((run) => run !== undefined);

export function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Evaluation Lab</h1>
        <p className="mt-1 text-sm text-muted">
          Monitor and analyze your coding-agent evaluations.
        </p>
      </header>

      <section className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <MetricCard label="Total Runs" value={String(metrics.total)} />
        <MetricCard label="Passed" value={String(metrics.passed)} tone="pass" />
        <MetricCard label="Failed" value={String(metrics.failed)} tone="fail" />
        <MetricCard label="Success Rate" value={`${metrics.successRate}%`} />
      </section>

      <section>
        <h2 className="mb-3 text-sm font-medium text-fg">Recent Runs</h2>
        {recentRuns.length === 0 ? (
          <EmptyState
            title="No runs yet"
            detail="Start an evaluation to see recent activity here."
          />
        ) : (
          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-line bg-raised/60 text-xs uppercase tracking-wide text-muted">
                  <tr>
                    <th className="px-4 py-2.5 font-medium">Task</th>
                    <th className="px-4 py-2.5 font-medium">Agent</th>
                    <th className="px-4 py-2.5 font-medium">Result</th>
                    <th className="px-4 py-2.5 font-medium">Tool Calls</th>
                    <th className="px-4 py-2.5 font-medium">Duration</th>
                  </tr>
                </thead>
                <tbody>
                  {recentRuns.map((run) => (
                    <tr
                      key={run.id}
                      tabIndex={0}
                      className="cursor-pointer border-b border-line last:border-0 hover:bg-raised/70"
                      onClick={() => navigate(`/runs/${run.id}`)}
                      onKeyDown={(event) => {
                        if (event.key === "Enter" || event.key === " ") {
                          event.preventDefault();
                          navigate(`/runs/${run.id}`);
                        }
                      }}
                    >
                      <td className="px-4 py-2.5 font-mono text-[13px]">{run.task}</td>
                      <td className="px-4 py-2.5">{run.agent}</td>
                      <td className="px-4 py-2.5">
                        <ResultBadge result={run.result} />
                      </td>
                      <td className="px-4 py-2.5 font-mono text-[13px] text-muted">
                        {run.toolCallCount}
                      </td>
                      <td className="px-4 py-2.5 font-mono text-[13px] text-muted">
                        {run.duration}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </section>
    </div>
  );
}

function MetricCard({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone?: "pass" | "fail";
}) {
  return (
    <Card className="px-4 py-4">
      <p className="text-xs uppercase tracking-wide text-muted">{label}</p>
      <p
        className={
          tone === "pass"
            ? "mt-2 text-2xl font-semibold text-pass"
            : tone === "fail"
              ? "mt-2 text-2xl font-semibold text-fail"
              : "mt-2 text-2xl font-semibold"
        }
      >
        {value}
      </p>
    </Card>
  );
}

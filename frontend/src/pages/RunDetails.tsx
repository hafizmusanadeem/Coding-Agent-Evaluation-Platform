import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Check, X } from "lucide-react";
import { Card } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { ResultBadge, StatusBadge } from "../components/ui/Badge";
import { cn } from "../lib/utils";
import { getRunById, type ToolCall } from "../lib/mockData";

export function RunDetails() {
  const { runId } = useParams();
  const run = runId ? getRunById(runId) : undefined;
  const [selectedId, setSelectedId] = useState<string | undefined>(
    run?.transcript[0]?.id,
  );

  const selected = useMemo(
    () => run?.transcript.find((item) => item.id === selectedId) ?? run?.transcript[0],
    [run, selectedId],
  );

  if (!run) {
    return (
      <div className="space-y-4">
        <BackLink />
        <EmptyState
          title="Run not found"
          detail={`No evaluation run matches id ${runId ?? ""}.`}
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <BackLink />
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-semibold tracking-tight">Run #{run.id}</h1>
          <ResultBadge result={run.result} />
        </div>
      </div>

      <dl className="grid grid-cols-2 gap-3 rounded-lg border border-line bg-panel px-4 py-3 text-sm md:grid-cols-4">
        <Meta label="Task" value={run.task} mono />
        <Meta label="Agent" value={run.agent} />
        <Meta label="Duration" value={run.duration} mono />
        <Meta label="Tool Calls" value={String(run.toolCallCount)} mono />
      </dl>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
        <Card className="overflow-hidden">
          <h2 className="border-b border-line px-4 py-3 text-sm font-medium">
            Transcript
          </h2>
          <ol className="divide-y divide-line">
            {run.transcript.map((item) => {
              const isActive = item.id === selected?.id;
              return (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => setSelectedId(item.id)}
                    className={cn(
                      "flex w-full items-center gap-3 px-4 py-2.5 text-left text-sm hover:bg-raised/70",
                      isActive && "bg-raised",
                    )}
                  >
                    <span className="w-6 font-mono text-xs text-muted">
                      {String(item.step).padStart(2, "0")}
                    </span>
                    <span className="flex-1 font-mono text-[13px]">{item.tool}</span>
                    {item.status === "Success" ? (
                      <Check className="h-4 w-4 text-pass" aria-label="Success" />
                    ) : (
                      <X className="h-4 w-4 text-fail" aria-label="Failed" />
                    )}
                  </button>
                </li>
              );
            })}
          </ol>
        </Card>

        <Card className="overflow-hidden">
          <h2 className="border-b border-line px-4 py-3 text-sm font-medium">
            Tool Call Details
          </h2>
          {selected ? <ToolCallDetails call={selected} /> : (
            <div className="p-4">
              <EmptyState
                title="No tool call selected"
                detail="Choose an item from the transcript."
              />
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

function BackLink() {
  return (
    <Link
      to="/runs"
      className="inline-flex items-center gap-1.5 text-sm text-muted hover:text-fg"
    >
      <ArrowLeft className="h-4 w-4" aria-hidden="true" />
      Runs
    </Link>
  );
}

function Meta({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div>
      <dt className="text-xs text-muted">{label}</dt>
      <dd className={cn("mt-0.5", mono && "font-mono text-[13px]")}>{value}</dd>
    </div>
  );
}

function ToolCallDetails({ call }: { call: ToolCall }) {
  return (
    <div className="space-y-5 p-4">
      <Detail label="Tool" value={call.tool} mono />

      <div>
        <p className="mb-1.5 text-xs uppercase tracking-wide text-muted">Arguments</p>
        <ArgumentsView call={call} />
      </div>

      <div>
        <p className="mb-1.5 text-xs uppercase tracking-wide text-muted">Output</p>
        {call.tool === "run_command" ? (
          <pre className="overflow-x-auto rounded-md border border-line bg-canvas p-3 font-mono text-[12px] leading-5 text-fg">
            {call.stdout ? `$ ${call.arguments.command}\n${call.stdout}` : call.output}
            {call.stderr ? `\n${call.stderr}` : ""}
          </pre>
        ) : (
          <pre className="overflow-x-auto rounded-md border border-line bg-canvas p-3 font-mono text-[12px] leading-5 text-fg">
            {call.output ?? "—"}
          </pre>
        )}
      </div>

      <Detail label="Duration" value={call.duration} mono />
      <div>
        <p className="mb-1.5 text-xs uppercase tracking-wide text-muted">Status</p>
        <StatusBadge status={call.status} />
      </div>
    </div>
  );
}

function ArgumentsView({ call }: { call: ToolCall }) {
  if (call.tool === "edit_file") {
    return (
      <div className="space-y-2 rounded-md border border-line bg-canvas p-3">
        <p className="font-mono text-[12px] text-muted">{call.arguments.path}</p>
        <pre className="overflow-x-auto font-mono text-[12px] leading-5">
          <span className="block text-fail">- {call.arguments.before}</span>
          <span className="mt-1 block text-pass">+ {call.arguments.after}</span>
        </pre>
      </div>
    );
  }

  if (call.tool === "run_command") {
    return (
      <pre className="overflow-x-auto rounded-md border border-line bg-canvas p-3 font-mono text-[12px]">
        {call.arguments.command}
      </pre>
    );
  }

  if (call.tool === "read_file") {
    return (
      <pre className="overflow-x-auto rounded-md border border-line bg-canvas p-3 font-mono text-[12px]">
        {call.arguments.path}
      </pre>
    );
  }

  return (
    <pre className="overflow-x-auto rounded-md border border-line bg-canvas p-3 font-mono text-[12px]">
      {call.arguments.message ?? "—"}
    </pre>
  );
}

function Detail({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div>
      <p className="mb-1 text-xs uppercase tracking-wide text-muted">{label}</p>
      <p className={cn("text-sm", mono && "font-mono text-[13px]")}>{value}</p>
    </div>
  );
}

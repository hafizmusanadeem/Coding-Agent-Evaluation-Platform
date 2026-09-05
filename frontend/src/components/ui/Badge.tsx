import type { ReactNode } from "react";
import { cn } from "../../lib/utils";
import type { RunResult, ToolStatus } from "../../lib/mockData";

type BadgeProps = {
  children: ReactNode;
  tone?: "neutral" | "pass" | "fail";
  className?: string;
};

export function Badge({ children, tone = "neutral", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border px-2 py-0.5 font-mono text-xs font-medium tracking-wide",
        tone === "neutral" && "border-line bg-raised text-muted",
        tone === "pass" && "border-pass/30 bg-pass/10 text-pass",
        tone === "fail" && "border-fail/30 bg-fail/10 text-fail",
        className,
      )}
    >
      {children}
    </span>
  );
}

export function ResultBadge({ result }: { result: RunResult }) {
  return <Badge tone={result === "PASS" ? "pass" : "fail"}>{result}</Badge>;
}

export function StatusBadge({ status }: { status: ToolStatus }) {
  return <Badge tone={status === "Success" ? "pass" : "fail"}>{status}</Badge>;
}

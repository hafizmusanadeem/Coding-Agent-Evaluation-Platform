import type { SelectHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  label: string;
};

export function Select({ label, id, className, children, ...props }: SelectProps) {
  const selectId = id ?? label.toLowerCase().replace(/\s+/g, "-");

  return (
    <label className="flex min-w-40 flex-col gap-1.5 text-sm" htmlFor={selectId}>
      <span className="text-muted">{label}</span>
      <select
        id={selectId}
        className={cn(
          "h-9 rounded-md border border-line bg-canvas px-3 text-fg",
          "hover:border-muted focus:border-accent",
          className,
        )}
        {...props}
      >
        {children}
      </select>
    </label>
  );
}

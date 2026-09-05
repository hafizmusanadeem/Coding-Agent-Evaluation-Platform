import type { ButtonHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost";
};

export function Button({
  className,
  variant = "primary",
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-md px-3.5 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50",
        variant === "primary" &&
          "bg-accent text-white hover:bg-accent/90",
        variant === "ghost" &&
          "border border-line bg-transparent text-fg hover:bg-raised",
        className,
      )}
      {...props}
    />
  );
}

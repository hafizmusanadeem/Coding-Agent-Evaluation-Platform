export function EmptyState({ title, detail }: { title: string; detail: string }) {
  return (
    <div className="rounded-lg border border-dashed border-line px-6 py-10 text-center">
      <p className="text-sm font-medium text-fg">{title}</p>
      <p className="mt-1 text-sm text-muted">{detail}</p>
    </div>
  );
}

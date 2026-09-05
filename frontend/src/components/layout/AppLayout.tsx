import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { Sidebar } from "./Sidebar";

export function AppLayout() {
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-canvas text-fg">
      <div className="hidden md:fixed md:inset-y-0 md:flex md:w-60">
        <Sidebar />
      </div>

      {open ? (
        <div className="fixed inset-0 z-40 md:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-black/50"
            aria-label="Close navigation"
            onClick={() => setOpen(false)}
          />
          <div className="relative z-50 h-full w-60">
            <Sidebar onNavigate={() => setOpen(false)} />
          </div>
        </div>
      ) : null}

      <div className="md:pl-60">
        <header className="sticky top-0 z-30 flex items-center gap-2 border-b border-line bg-canvas/90 px-4 py-3 backdrop-blur md:hidden">
          <button
            type="button"
            className="rounded-md border border-line p-1.5 text-fg"
            onClick={() => setOpen((value) => !value)}
            aria-label={open ? "Close menu" : "Open menu"}
          >
            {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
          <span className="text-sm font-medium">Evaluation Lab</span>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-6 md:px-8 md:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

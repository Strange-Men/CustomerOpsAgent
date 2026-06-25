import type { ReactNode } from "react";
import { Header } from "./Header";
import { StatusBar } from "./StatusBar";

interface AppShellProps {
  children: ReactNode;
}

/**
 * Root layout wrapper — dark background, header, main content area, status bar.
 */
export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />
      <main className="flex-1 max-w-[1600px] w-full mx-auto px-6 py-6">
        {children}
      </main>
      <StatusBar />
    </div>
  );
}

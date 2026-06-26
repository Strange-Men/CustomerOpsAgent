import type { ReactNode } from "react";
import { Header } from "./Header";

interface AppShellProps {
  children: ReactNode;
}

/**
 * Root layout wrapper — dark background, header, centered main content, footer.
 * Single-column layout, max-width 1100px.
 */
export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />
      <main className="flex-1 max-w-[1100px] w-full mx-auto px-4 sm:px-6 pt-3 pb-6">
        {children}
      </main>
      <footer className="border-t border-purple-500/10 bg-slate-950/80">
        <div className="max-w-[1100px] mx-auto px-4 sm:px-6 py-1.5 text-center text-[10px] text-slate-700">
          Demo 限制：未接真实物流 API / 未接真实订单系统 / 真实 LLM 为可选配置 / Render 免费实例可能冷启动
        </div>
      </footer>
    </div>
  );
}

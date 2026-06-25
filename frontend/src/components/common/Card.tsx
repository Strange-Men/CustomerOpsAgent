import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
}

/**
 * Dark surface card with thin accent border and optional subtle glow.
 */
export function Card({ children, className = "", glow = false }: CardProps) {
  return (
    <div
      className={`
        rounded-xl border border-purple-500/15 bg-slate-900/80 p-4
        ${glow ? "shadow-[0_0_20px_rgba(168,85,247,0.08)]" : ""}
        ${className}
      `.trim()}
    >
      {children}
    </div>
  );
}

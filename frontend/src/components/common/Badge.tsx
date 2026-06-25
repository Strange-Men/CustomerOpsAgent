interface BadgeProps {
  label: string;
  variant?: "accent" | "success" | "warning" | "info" | "muted";
  className?: string;
}

const VARIANT_CLASSES: Record<string, string> = {
  accent:
    "bg-fuchsia-500/15 text-fuchsia-300 border-fuchsia-500/25",
  success:
    "bg-emerald-500/15 text-emerald-300 border-emerald-500/25",
  warning:
    "bg-amber-500/15 text-amber-300 border-amber-500/25",
  info:
    "bg-sky-500/15 text-sky-300 border-sky-500/25",
  muted:
    "bg-slate-500/15 text-slate-400 border-slate-500/25",
};

/**
 * Pill-style badge for tags and status indicators.
 */
export function Badge({ label, variant = "accent", className = "" }: BadgeProps) {
  return (
    <span
      className={`
        inline-block px-2.5 py-0.5 text-xs font-medium rounded-full border
        ${VARIANT_CLASSES[variant]}
        ${className}
      `.trim()}
    >
      {label}
    </span>
  );
}

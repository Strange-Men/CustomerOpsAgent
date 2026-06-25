import type { ReactNode, ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md";
  className?: string;
}

const VARIANT_CLASSES: Record<string, string> = {
  primary:
    "bg-fuchsia-600/90 hover:bg-fuchsia-500/90 text-white border-fuchsia-500/30 shadow-[0_0_12px_rgba(217,70,239,0.15)]",
  secondary:
    "bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border-slate-600/30",
  ghost:
    "bg-transparent hover:bg-slate-800/50 text-slate-400 hover:text-slate-200 border-transparent",
};

const SIZE_CLASSES: Record<string, string> = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
};

/**
 * Themed button with dark + accent styling.
 */
export function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ButtonProps) {
  return (
    <button
      className={`
        inline-flex items-center justify-center gap-2 rounded-lg border
        font-medium transition-colors duration-150 cursor-pointer
        disabled:opacity-50 disabled:cursor-not-allowed
        ${VARIANT_CLASSES[variant]}
        ${SIZE_CLASSES[size]}
        ${className}
      `.trim()}
      {...props}
    >
      {children}
    </button>
  );
}

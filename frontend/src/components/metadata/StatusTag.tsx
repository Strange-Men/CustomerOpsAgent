interface StatusTagProps {
  label: string;
  value: string;
  className?: string;
}

/**
 * Key-value status display tag.
 */
export function StatusTag({ label, value, className = "" }: StatusTagProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-xs text-slate-500 font-medium">{label}</span>
      <span className="text-xs text-slate-300 px-2 py-0.5 rounded-full bg-slate-800/60 border border-slate-700/30">
        {value}
      </span>
    </div>
  );
}

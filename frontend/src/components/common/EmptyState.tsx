interface EmptyStateProps {
  title: string;
  description?: string;
  className?: string;
}

/**
 * Placeholder display when a section has no content.
 */
export function EmptyState({ title, description, className = "" }: EmptyStateProps) {
  return (
    <div className={`text-center py-8 ${className}`}>
      <p className="text-slate-500 text-sm font-medium">{title}</p>
      {description && (
        <p className="text-slate-600 text-xs mt-1">{description}</p>
      )}
    </div>
  );
}

import type { Citation } from "../../lib/types";

interface CitationCardProps {
  citation: Citation;
  className?: string;
}

/**
 * Single citation card — compact document metadata.
 */
export function CitationCard({ citation, className = "" }: CitationCardProps) {
  return (
    <div
      className={`
        rounded-md border border-purple-500/10 bg-slate-800/40 px-3 py-2
        ${className}
      `.trim()}
    >
      <p className="text-[11px] font-medium text-slate-300 mb-1">
        {citation.title}
      </p>
      <div className="flex flex-wrap gap-x-2.5 gap-y-0.5 text-[10px] text-slate-500">
        <span>{citation.doc_id}</span>
        <span>{citation.category}</span>
        <span>{citation.market}</span>
      </div>
    </div>
  );
}

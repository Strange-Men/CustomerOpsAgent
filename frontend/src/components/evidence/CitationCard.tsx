import type { Citation } from "../../lib/types";

interface CitationCardProps {
  citation: Citation;
  className?: string;
}

/**
 * Single citation card showing document metadata.
 */
export function CitationCard({ citation, className = "" }: CitationCardProps) {
  return (
    <div
      className={`
        rounded-lg border border-purple-500/10 bg-slate-800/50 p-3
        ${className}
      `.trim()}
    >
      <p className="text-xs font-medium text-slate-200 mb-1.5">
        {citation.title}
      </p>
      <div className="flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-slate-500">
        <span>doc: {citation.doc_id}</span>
        <span>chunk: {citation.chunk_id}</span>
        <span>cat: {citation.category}</span>
        <span>market: {citation.market}</span>
        <span>lang: {citation.language}</span>
      </div>
      <p className="text-[11px] text-slate-600 mt-1.5 truncate">
        {citation.source}
      </p>
    </div>
  );
}

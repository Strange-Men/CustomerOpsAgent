import { Card } from "../common/Card";
import { Badge } from "../common/Badge";
import { CitationCard } from "./CitationCard";
import type { AgentResponse } from "../../lib/types";

interface CitationPanelProps {
  response: AgentResponse;
}

/**
 * Right panel showing citations and retrieved document IDs.
 */
export function CitationPanel({ response }: CitationPanelProps) {
  return (
    <aside className="space-y-4">
      {/* Retrieved doc IDs */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Retrieved Documents
        </h3>
        {response.retrieved_doc_ids.length > 0 ? (
          <div className="flex flex-wrap gap-1.5">
            {response.retrieved_doc_ids.map((id) => (
              <Badge key={id} label={id} variant="muted" />
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-600">No documents retrieved</p>
        )}
      </Card>

      {/* Citations */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Citations
        </h3>
        {response.citations.length > 0 ? (
          <div className="space-y-2">
            {response.citations.map((citation) => (
              <CitationCard key={citation.doc_id + citation.chunk_id} citation={citation} />
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-600">No citations available</p>
        )}
      </Card>
    </aside>
  );
}

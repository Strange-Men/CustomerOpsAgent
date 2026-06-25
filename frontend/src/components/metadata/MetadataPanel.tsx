import { Card } from "../common/Card";
import { StatusTag } from "./StatusTag";
import { RouteBadge } from "./RouteBadge";
import type { AgentResponse } from "../../lib/types";

interface MetadataPanelProps {
  response: AgentResponse;
}

/**
 * Right panel showing agent response metadata.
 */
export function MetadataPanel({ response }: MetadataPanelProps) {
  return (
    <aside className="space-y-4">
      {/* Route */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Route
        </h3>
        <RouteBadge route={response.route} />
      </Card>

      {/* Intent */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Intent
        </h3>
        <div className="space-y-2">
          <StatusTag label="intent" value={response.intent} />
          <StatusTag label="detail_intent" value={response.detail_intent} />
          <StatusTag label="confidence" value={response.confidence} />
        </div>
      </Card>

      {/* Answer Source */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Answer Source
        </h3>
        <div className="space-y-2">
          <StatusTag label="source" value={response.answer_source} />
          {response.tool_used && (
            <StatusTag label="tool" value={response.tool_used} />
          )}
          {response.llm_provider && (
            <StatusTag label="provider" value={response.llm_provider} />
          )}
          {response.llm_model && (
            <StatusTag label="model" value={response.llm_model} />
          )}
        </div>
      </Card>

      {/* Fallback */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Fallback
        </h3>
        <div className="space-y-2">
          <StatusTag
            label="triggered"
            value={response.fallback_triggered ? "yes" : "no"}
          />
          {response.fallback_reason && (
            <StatusTag label="reason" value={response.fallback_reason} />
          )}
        </div>
      </Card>
    </aside>
  );
}

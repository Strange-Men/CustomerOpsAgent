import { Card } from "../common/Card";
import { StatusTag } from "./StatusTag";
import { RouteBadge } from "./RouteBadge";
import type { AgentResponse } from "../../lib/types";

interface MetadataPanelProps {
  response: AgentResponse;
}

/**
 * Right panel showing agent response metadata.
 * Displays llm_profile, answer_source, provider, model, route, intent, fallback.
 */
export function MetadataPanel({ response }: MetadataPanelProps) {
  // Determine profile fallback hint
  const profileFallbackHint =
    response.llm_profile &&
    response.llm_profile !== "mock" &&
    response.answer_source === "mock"
      ? "当前模型档案未启用或未配置，使用 Mock 回答"
      : null;

  const realLlmFallbackHint =
    response.answer_source === "real_llm_fallback_mock"
      ? "真实模型不可用，已降级 Mock"
      : null;

  return (
    <aside className="space-y-4">
      {/* LLM Profile */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          LLM Profile
        </h3>
        <div className="space-y-2">
          <StatusTag label="profile" value={response.llm_profile ?? "mock"} />
          <StatusTag label="source" value={response.answer_source} />
          {response.llm_provider && (
            <StatusTag label="provider" value={response.llm_provider} />
          )}
          {response.llm_model && (
            <StatusTag label="model" value={response.llm_model} />
          )}
        </div>
        {profileFallbackHint && (
          <p className="text-[10px] text-amber-400/80 mt-2">
            {profileFallbackHint}
          </p>
        )}
        {realLlmFallbackHint && (
          <p className="text-[10px] text-amber-400/80 mt-2">
            {realLlmFallbackHint}
          </p>
        )}
      </Card>

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

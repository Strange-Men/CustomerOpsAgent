import { useState } from "react";
import { Card } from "../common/Card";
import { Badge } from "../common/Badge";
import { CitationCard } from "../evidence/CitationCard";
import type { AgentResponse } from "../../lib/types";

interface AnswerDetailsProps {
  response: AgentResponse;
}

/**
 * Compact answer details section shown below the chat.
 * Displays metadata badges and collapsible citations.
 */
export function AnswerDetails({ response }: AnswerDetailsProps) {
  const [citationsOpen, setCitationsOpen] = useState(false);

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
    <Card>
      <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
        本次回答详情
      </h3>

      {/* Metadata badges — compact row */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        <Badge label={`Profile: ${response.llm_profile ?? "mock"}`} variant="accent" />
        <Badge label={`来源: ${response.answer_source}`} variant="muted" />
        <Badge label={`路由: ${response.route}`} variant="info" />
        <Badge label={`意图: ${response.intent}`} variant="success" />
        <Badge label={`置信度: ${response.confidence}`} variant="success" />
        {response.fallback_triggered && (
          <Badge label="Fallback: yes" variant="warning" />
        )}
      </div>

      {/* Fallback hints */}
      {(profileFallbackHint || realLlmFallbackHint) && (
        <p className="text-[11px] text-amber-400/80 mb-3">
          {profileFallbackHint || realLlmFallbackHint}
        </p>
      )}

      {/* Citations — collapsible */}
      <div className="border-t border-slate-700/30 pt-3">
        <button
          onClick={() => setCitationsOpen(!citationsOpen)}
          className="flex items-center gap-2 text-xs text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
        >
          <span className="text-[10px]">{citationsOpen ? "▼" : "▶"}</span>
          引用证据
          {response.citations.length > 0 && (
            <span className="text-[10px] text-slate-600">
              ({response.citations.length})
            </span>
          )}
        </button>

        {citationsOpen && (
          <div className="mt-3 space-y-2">
            {response.citations.length > 0 ? (
              response.citations.map((citation) => (
                <CitationCard
                  key={citation.doc_id + citation.chunk_id}
                  citation={citation}
                />
              ))
            ) : (
              <p className="text-xs text-slate-600">
                本次回答没有返回 citations。
              </p>
            )}
          </div>
        )}
      </div>

      {/* Retrieved doc IDs — compact row */}
      {response.retrieved_doc_ids.length > 0 && (
        <div className="border-t border-slate-700/30 pt-3 mt-3">
          <p className="text-[10px] text-slate-500 mb-1.5">检索文档 ID：</p>
          <div className="flex flex-wrap gap-1.5">
            {response.retrieved_doc_ids.map((id) => (
              <Badge key={id} label={id} variant="muted" />
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

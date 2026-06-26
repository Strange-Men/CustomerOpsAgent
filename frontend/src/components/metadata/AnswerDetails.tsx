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
 * Lightweight metadata row + collapsible citations.
 */
export function AnswerDetails({ response }: AnswerDetailsProps) {
  const [citationsOpen, setCitationsOpen] = useState(false);

  const profileFallbackHint =
    response.llm_profile &&
    response.llm_profile !== "mock" &&
    response.answer_source === "mock"
      ? "该模型档案未启用或未配置，已降级 Mock"
      : null;

  const realLlmFallbackHint =
    response.answer_source === "real_llm_fallback_mock"
      ? "真实模型不可用，已降级 Mock"
      : null;

  // Limit citations to first 3
  const visibleCitations = response.citations.slice(0, 3);

  return (
    <Card className="!py-3 !px-4">
      {/* Fallback hint — visible but restrained */}
      {response.fallback_triggered && (
        <p className="text-[11px] text-amber-400/70 mb-2">
          已触发兜底回答
          {response.fallback_reason ? `：${response.fallback_reason}` : ""}
        </p>
      )}
      {(profileFallbackHint || realLlmFallbackHint) && (
        <p className="text-[11px] text-amber-400/70 mb-2">
          {profileFallbackHint || realLlmFallbackHint}
        </p>
      )}

      {/* Metadata badges — single compact row */}
      <div className="flex flex-wrap items-center gap-1.5 mb-2">
        <Badge label={response.llm_profile ?? "mock"} variant="accent" />
        <Badge label={response.answer_source} variant="muted" />
        <Badge label={response.route} variant="info" />
        <Badge label={response.intent} variant="success" />
        <Badge label={response.confidence} variant="success" />
        {response.fallback_triggered && (
          <Badge label="fallback" variant="warning" />
        )}
      </div>

      {/* Citations — collapsible, max 3 visible */}
      <div className="border-t border-slate-700/20 pt-2">
        <button
          onClick={() => setCitationsOpen(!citationsOpen)}
          className="flex items-center gap-1.5 text-[11px] text-slate-500 hover:text-slate-300 transition-colors cursor-pointer"
        >
          <span className="text-[9px]">{citationsOpen ? "▼" : "▶"}</span>
          知识库依据
          {response.citations.length > 0 && (
            <span className="text-[10px] text-slate-600">
              ({response.citations.length})
            </span>
          )}
        </button>

        {citationsOpen && (
          <div className="mt-2 space-y-1.5">
            {visibleCitations.length > 0 ? (
              <>
                {visibleCitations.map((citation) => (
                  <CitationCard
                    key={citation.doc_id + citation.chunk_id}
                    citation={citation}
                  />
                ))}
                {response.citations.length > 3 && (
                  <p className="text-[10px] text-slate-600">
                    还有 {response.citations.length - 3} 条依据未显示
                  </p>
                )}
              </>
            ) : (
              <p className="text-[11px] text-slate-600">
                本次回答没有返回 citations。
              </p>
            )}
          </div>
        )}
      </div>

      {/* Retrieved doc IDs — inline, compact */}
      {response.retrieved_doc_ids.length > 0 && (
        <div className="border-t border-slate-700/20 pt-2 mt-2">
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-[10px] text-slate-600">文档 ID：</span>
            {response.retrieved_doc_ids.map((id) => (
              <Badge key={id} label={id} variant="muted" className="!text-[10px] !px-1.5" />
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

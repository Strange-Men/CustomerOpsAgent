import { useState } from "react";
import type { AgentResponse } from "../../lib/types";

/** Answers longer than this threshold show a collapse/expand button. */
const COLLAPSE_THRESHOLD = 280;

/** Collapsed answer max-height in px. */
const COLLAPSED_MAX_H = 220;

/** Route display names (raw → friendly Chinese). */
const ROUTE_LABELS: Record<string, string> = {
  rag_knowledge_base: "RAG 知识库",
  logistics_tool: "Mock 物流工具",
  fallback: "兜底回复",
};

/** Answer source display names. */
const SOURCE_LABELS: Record<string, string> = {
  mock: "Mock",
  real_llm: "真实 LLM",
  real_llm_fallback_mock: "已降级 Mock",
};

interface AnswerCardProps {
  response: AgentResponse;
}

/**
 * Displays the agent's answer as the primary assistant message card.
 * Long answers are collapsed by default with an expand/collapse toggle.
 * Shows RAG citation evidence prominently when available.
 */
export function AnswerCard({ response }: AnswerCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [citationsOpen, setCitationsOpen] = useState(false);
  const isLong = response.answer.length > COLLAPSE_THRESHOLD;
  const hasCitations = response.citations.length > 0;

  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] w-full">
        <div className="rounded-2xl rounded-bl-md px-3.5 py-2.5 text-sm leading-relaxed bg-slate-800/80 text-slate-200 border border-slate-700/40">
          {/* RAG evidence banner */}
          {hasCitations ? (
            <div className="flex items-center gap-1.5 mb-2 px-2 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <span className="text-emerald-400 text-xs">📚</span>
              <span className="text-[11px] text-emerald-300">
                已命中知识库证据 · {response.citations.length} 条引用
              </span>
            </div>
          ) : response.route === "rag_knowledge_base" ? (
            <div className="flex items-center gap-1.5 mb-2 px-2 py-1 rounded-lg bg-slate-700/30 border border-slate-600/20">
              <span className="text-slate-400 text-xs">📄</span>
              <span className="text-[11px] text-slate-400">
                本次未返回引用证据
              </span>
            </div>
          ) : null}

          {/* Answer text — collapsed or expanded */}
          <div
            className="relative overflow-hidden transition-[max-height] duration-300 ease-in-out"
            style={
              isLong && !expanded
                ? { maxHeight: COLLAPSED_MAX_H }
                : undefined
            }
          >
            <p>{response.answer}</p>

            {/* Bottom fade when collapsed */}
            {isLong && !expanded && (
              <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-slate-800/80 to-transparent pointer-events-none" />
            )}
          </div>

          {/* Expand / collapse toggle */}
          {isLong && (
            <button
              type="button"
              onClick={() => setExpanded((v) => !v)}
              className="mt-1.5 text-[11px] text-fuchsia-400 hover:text-fuchsia-300 transition-colors cursor-pointer"
            >
              {expanded ? "收起" : "展开全文"}
            </button>
          )}

          {/* Citations collapsible section */}
          {hasCitations && (
            <div className="mt-2 pt-2 border-t border-slate-700/25">
              <button
                type="button"
                onClick={() => setCitationsOpen((v) => !v)}
                className="text-[11px] text-emerald-400 hover:text-emerald-300 transition-colors cursor-pointer"
              >
                {citationsOpen ? "收起引用详情" : `查看引用详情（${response.citations.length} 条）`}
              </button>
              {citationsOpen && (
                <div className="mt-1.5 space-y-1">
                  {response.citations.map((c, i) => (
                    <div
                      key={c.chunk_id}
                      className="text-[10px] px-2 py-1 rounded bg-slate-700/40 text-slate-300"
                    >
                      <span className="text-emerald-400">[{i + 1}]</span>{" "}
                      {c.title}{" "}
                      <span className="text-slate-500">({c.doc_id})</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Retrieved doc IDs */}
          {response.retrieved_doc_ids.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-1.5">
              {response.retrieved_doc_ids.map((id) => (
                <span
                  key={id}
                  className="text-[9px] px-1.5 py-0.5 rounded bg-slate-700/50 text-slate-400 border border-slate-600/20"
                >
                  {id}
                </span>
              ))}
            </div>
          )}

          {/* Inline metadata — compact badges */}
          <div className="flex flex-wrap items-center gap-1 mt-2 pt-2 border-t border-slate-700/25">
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-fuchsia-500/15 text-fuchsia-300 border border-fuchsia-500/20">
              {response.llm_profile ?? "mock"}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/20">
              {ROUTE_LABELS[response.route] ?? response.route}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/20">
              {response.confidence}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-500/15 text-slate-400 border border-slate-500/20">
              {SOURCE_LABELS[response.answer_source] ?? response.answer_source}
            </span>
            {response.fallback_triggered && (
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/20">
                fallback
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

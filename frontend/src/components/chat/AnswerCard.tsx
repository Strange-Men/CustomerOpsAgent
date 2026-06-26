import { useState } from "react";
import type { AgentResponse } from "../../lib/types";

/** Answers longer than this threshold show a collapse/expand button. */
const COLLAPSE_THRESHOLD = 280;

/** Collapsed answer max-height in px. */
const COLLAPSED_MAX_H = 220;

interface AnswerCardProps {
  response: AgentResponse;
}

/**
 * Displays the agent's answer as the primary assistant message card.
 * Long answers are collapsed by default with an expand/collapse toggle.
 * Compact inline metadata badges sit below the answer text.
 */
export function AnswerCard({ response }: AnswerCardProps) {
  const [expanded, setExpanded] = useState(false);
  const isLong = response.answer.length > COLLAPSE_THRESHOLD;

  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] w-full">
        <div className="rounded-2xl rounded-bl-md px-3.5 py-2.5 text-sm leading-relaxed bg-slate-800/80 text-slate-200 border border-slate-700/40">
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

          {/* Inline metadata — compact badges */}
          <div className="flex flex-wrap items-center gap-1 mt-2 pt-2 border-t border-slate-700/25">
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-fuchsia-500/15 text-fuchsia-300 border border-fuchsia-500/20">
              {response.llm_profile ?? "mock"}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/20">
              {response.route}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/20">
              {response.confidence}
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

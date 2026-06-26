import type { AgentResponse } from "../../lib/types";

interface AnswerCardProps {
  response: AgentResponse;
}

/**
 * Displays the agent's answer as the primary assistant message card.
 * Shows answer text with inline metadata badges below.
 */
export function AnswerCard({ response }: AnswerCardProps) {
  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] w-full">
        <div className="rounded-2xl rounded-bl-md px-4 py-3 text-sm leading-relaxed bg-slate-800/80 text-slate-200 border border-slate-700/40">
          {/* Answer text */}
          <p>{response.answer}</p>

          {/* Inline metadata */}
          <div className="flex flex-wrap items-center gap-1.5 mt-3 pt-2.5 border-t border-slate-700/30">
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-fuchsia-500/15 text-fuchsia-300 border border-fuchsia-500/25">
              {response.llm_profile ?? "mock"}
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/25">
              {response.route}
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/25">
              {response.confidence}
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-500/15 text-slate-400 border border-slate-500/25">
              {response.answer_source}
            </span>
            {response.fallback_triggered && (
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/25">
                fallback
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

import { Card } from "../common/Card";
import { Badge } from "../common/Badge";
import type { AgentResponse } from "../../lib/types";

interface AnswerCardProps {
  response: AgentResponse;
}

/**
 * Displays the agent's answer with route, confidence, answer source,
 * llm_profile, and other metadata.
 */
export function AnswerCard({ response }: AnswerCardProps) {
  return (
    <Card glow>
      <div className="space-y-3">
        {/* Answer text */}
        <p className="text-sm text-slate-200 leading-relaxed">
          {response.answer}
        </p>

        {/* Meta row */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-700/30">
          <Badge label={`Profile: ${response.llm_profile ?? "mock"}`} variant="accent" />
          <Badge label={`路由: ${response.route}`} variant="info" />
          <Badge label={`置信度: ${response.confidence}`} variant="success" />
          <Badge label={`来源: ${response.answer_source}`} variant="muted" />
          {response.order_id && (
            <Badge label={`订单: ${response.order_id}`} variant="accent" />
          )}
        </div>

        {/* Fallback warning */}
        {response.fallback_triggered && (
          <div className="flex items-center gap-2 pt-2 border-t border-slate-700/30">
            <Badge label="已触发 Fallback" variant="warning" />
            {response.fallback_reason && (
              <span className="text-xs text-amber-400/80">
                原因: {response.fallback_reason}
              </span>
            )}
          </div>
        )}

        {/* Citation hint */}
        <div className="pt-2 border-t border-slate-700/30">
          <p className="text-[10px] text-slate-600">
            引用见右侧 Evidence Panel
          </p>
        </div>
      </div>
    </Card>
  );
}

import { Card } from "../common/Card";
import { Badge } from "../common/Badge";
import type { AgentResponse } from "../../lib/types";

interface AnswerCardProps {
  response: AgentResponse;
}

/**
 * Displays the agent's answer with route, confidence, and answer source.
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
          <Badge label={`route: ${response.route}`} variant="info" />
          <Badge label={`confidence: ${response.confidence}`} variant="success" />
          <Badge label={`source: ${response.answer_source}`} variant="muted" />
          {response.order_id && (
            <Badge label={`order: ${response.order_id}`} variant="accent" />
          )}
        </div>
      </div>
    </Card>
  );
}

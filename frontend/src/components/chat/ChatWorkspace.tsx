import { MessageBubble } from "./MessageBubble";
import { AnswerCard } from "./AnswerCard";
import { ExamplePrompts } from "./ExamplePrompts";
import { MOCK_RESPONSE, MOCK_USER_QUERY } from "../../data/mockResponse";

/**
 * Central chat workspace — displays a static conversation with mock data.
 * No API calls, no real chat state management.
 */
export function ChatWorkspace() {
  return (
    <div className="space-y-4">
      {/* Chat messages area */}
      <div className="space-y-4">
        <MessageBubble role="user" text={MOCK_USER_QUERY} />
        <AnswerCard response={MOCK_RESPONSE} />
      </div>

      {/* Example prompts */}
      <div className="pt-4 border-t border-slate-700/30">
        <p className="text-xs text-slate-500 mb-2">Example questions:</p>
        <ExamplePrompts />
      </div>
    </div>
  );
}

import type { ChatMessage } from "../../lib/types";
import { MessageBubble } from "./MessageBubble";
import { AnswerCard } from "./AnswerCard";

interface MessageListProps {
  messages: ChatMessage[];
}

/**
 * Renders a list of chat messages.
 * Assistant messages with response data show only the AnswerCard (no duplicate bubble).
 * Pending/error assistant messages show a plain bubble.
 */
export function MessageList({ messages }: MessageListProps) {
  return (
    <div className="space-y-4">
      {messages.map((msg) => {
        if (msg.role === "system") {
          return (
            <div key={msg.id} className="flex justify-center">
              <div className="px-3 py-1.5 text-xs text-slate-500 bg-slate-800/40 rounded-full border border-slate-700/30">
                {msg.content}
              </div>
            </div>
          );
        }

        if (msg.role === "user") {
          return (
            <MessageBubble
              key={msg.id}
              role="user"
              text={msg.content}
              timestamp={msg.createdAt}
            />
          );
        }

        // assistant with full response — show AnswerCard only (no duplicate bubble)
        if (msg.response) {
          return <AnswerCard key={msg.id} response={msg.response} />;
        }

        // assistant pending or error — show plain bubble
        return (
          <MessageBubble
            key={msg.id}
            role="assistant"
            text={msg.content}
            timestamp={msg.createdAt}
          />
        );
      })}
    </div>
  );
}

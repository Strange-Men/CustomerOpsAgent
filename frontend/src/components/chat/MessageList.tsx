import type { ChatMessage } from "../../lib/types";
import { MessageBubble } from "./MessageBubble";
import { AnswerCard } from "./AnswerCard";

interface MessageListProps {
  messages: ChatMessage[];
}

/**
 * Renders a list of chat messages.
 * Supports user, assistant, and system roles.
 * No API calls — static display only.
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

        // assistant role
        if (msg.response) {
          return (
            <div key={msg.id} className="space-y-2">
              <MessageBubble
                role="assistant"
                text={msg.content}
                timestamp={msg.createdAt}
              />
              <AnswerCard response={msg.response} />
            </div>
          );
        }

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

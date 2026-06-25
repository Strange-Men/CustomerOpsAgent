import type { ChatRole } from "../../lib/types";

interface MessageBubbleProps {
  role: ChatRole;
  text: string;
  timestamp?: string;
  className?: string;
}

/**
 * Chat message bubble — user messages right-aligned, assistant messages left-aligned.
 * Supports timestamp display. No API calls.
 */
export function MessageBubble({
  role,
  text,
  timestamp,
  className = "",
}: MessageBubbleProps) {
  const isUser = role === "user";
  const isSystem = role === "system";

  // System messages are handled by MessageList, but just in case
  if (isSystem) {
    return (
      <div className={`flex justify-center ${className}`}>
        <div className="px-3 py-1.5 text-xs text-slate-500 bg-slate-800/40 rounded-full border border-slate-700/30">
          {text}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} ${className}`}>
      <div className="max-w-[80%]">
        <div
          className={`
            rounded-2xl px-4 py-3 text-sm leading-relaxed
            ${
              isUser
                ? "bg-gradient-to-br from-fuchsia-600/20 to-purple-600/20 text-fuchsia-100 border border-fuchsia-500/25 rounded-br-md"
                : "bg-slate-800/80 text-slate-200 border border-slate-700/40 rounded-bl-md"
            }
          `.trim()}
        >
          {text}
        </div>
        {timestamp && (
          <div className={`mt-1 text-[10px] text-slate-600 ${isUser ? "text-right" : "text-left"}`}>
            {new Date(timestamp).toLocaleTimeString("zh-CN", {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </div>
        )}
      </div>
    </div>
  );
}

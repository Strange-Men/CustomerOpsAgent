interface MessageBubbleProps {
  role: "user" | "agent";
  text: string;
  className?: string;
}

/**
 * Chat message bubble — user messages right-aligned, agent messages left-aligned.
 */
export function MessageBubble({ role, text, className = "" }: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} ${className}`}>
      <div
        className={`
          max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed
          ${
            isUser
              ? "bg-fuchsia-600/20 text-fuchsia-100 border border-fuchsia-500/20 rounded-br-md"
              : "bg-slate-800/80 text-slate-200 border border-slate-700/40 rounded-bl-md"
          }
        `.trim()}
      >
        {text}
      </div>
    </div>
  );
}

import { useState } from "react";

interface ChatInputProps {
  onSend?: (message: string) => void;
  disabled?: boolean;
}

/**
 * Chat input area — textarea with send and clear buttons.
 * When onSend is provided, sends the message to the parent.
 */
export function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [inputValue, setInputValue] = useState("");

  const handleClear = () => {
    setInputValue("");
  };

  const handleSend = () => {
    const trimmed = inputValue.trim();
    if (trimmed && onSend) {
      onSend(trimmed);
      setInputValue("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="space-y-1.5">
      <div className="relative">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入跨境电商客服问题…"
          rows={2}
          disabled={disabled}
          className="
            w-full px-3 py-2 text-sm text-slate-200
            bg-slate-800/60 border border-slate-700/40 rounded-lg
            placeholder:text-slate-600
            focus:outline-none focus:border-fuchsia-500/30 focus:ring-1 focus:ring-fuchsia-500/20
            resize-none
            disabled:opacity-50 disabled:cursor-not-allowed
          "
        />
      </div>

      <div className="flex items-center justify-between">
        <p className="text-[10px] text-slate-600">
          Enter 发送 · Shift+Enter 换行
        </p>
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleClear}
            disabled={!inputValue || disabled}
            className="
              px-2.5 py-1 text-[11px] text-slate-500
              bg-transparent border border-slate-700/20 rounded-md
              hover:bg-slate-800/60 hover:text-slate-300
              disabled:opacity-40 disabled:cursor-not-allowed
              transition-colors duration-150
            "
          >
            清除
          </button>
          <button
            onClick={handleSend}
            disabled={!inputValue.trim() || disabled}
            className="
              px-3 py-1 text-[11px] text-fuchsia-200
              bg-fuchsia-600/25 border border-fuchsia-500/30 rounded-md
              hover:bg-fuchsia-600/40
              disabled:opacity-40 disabled:cursor-not-allowed
              transition-colors duration-150
            "
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
}

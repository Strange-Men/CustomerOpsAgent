import { useState, useCallback } from "react";
import { MessageList } from "./MessageList";
import { ExamplePrompts } from "./ExamplePrompts";
import { ChatInput } from "./ChatInput";
import { ModelSelector } from "./ModelSelector";
import { sendAgentMessage } from "../../lib/api";
import { DEFAULT_LLM_PROFILE } from "../../lib/constants";
import type { AgentResponse, ChatMessage, LLMProfile } from "../../lib/types";

interface ChatWorkspaceProps {
  onResponseChange?: (response: AgentResponse | null) => void;
}

/**
 * Central chat workspace — manages real chat state and API calls.
 * Wrapped in a card container; the visual core of the page.
 */
export function ChatWorkspace({ onResponseChange }: ChatWorkspaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [selectedProfile, setSelectedProfile] =
    useState<LLMProfile>(DEFAULT_LLM_PROFILE);

  /** Build conversation history from existing messages (last 5 text entries). */
  const buildHistory = useCallback((msgs: ChatMessage[]): string[] => {
    return msgs
      .filter((m) => m.role === "user" || m.role === "assistant")
      .slice(-5)
      .map((m) => m.content);
  }, []);

  /** Clear all messages and reset response. */
  const handleClear = useCallback(() => {
    setMessages([]);
    setErrorMessage(null);
    onResponseChange?.(null);
  }, [onResponseChange]);

  /** Send a message to the backend. */
  const handleSend = useCallback(
    async (query: string) => {
      if (!query.trim() || isLoading) return;

      setErrorMessage(null);

      // Add user message
      const userMsg: ChatMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: query,
        createdAt: new Date().toISOString(),
        status: "success",
      };

      // Add pending assistant message
      const pendingId = `assistant-${Date.now()}`;
      const pendingMsg: ChatMessage = {
        id: pendingId,
        role: "assistant",
        content: "",
        createdAt: new Date().toISOString(),
        status: "pending",
      };

      setMessages((prev) => [...prev, userMsg, pendingMsg]);
      setIsLoading(true);

      try {
        const history = buildHistory([...messages, userMsg]);
        const response: AgentResponse = await sendAgentMessage({
          user_query: query,
          conversation_history: history,
          llm_profile: selectedProfile,
        });

        // Update pending message with real response
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId
              ? {
                  ...m,
                  content: response.answer,
                  status: "success" as const,
                  response,
                }
              : m
          )
        );

        // Notify parent of new response for details section
        onResponseChange?.(response);
      } catch (err) {
        const msg =
          err instanceof Error ? err.message : "请求失败，请稍后重试";
        setErrorMessage(msg);

        // Mark pending message as error
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingId
              ? { ...m, content: msg, status: "error" as const }
              : m
          )
        );
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, messages, selectedProfile, buildHistory, onResponseChange]
  );

  /** Handle example prompt click — sends directly. */
  const handleExampleSelect = useCallback(
    (query: string) => {
      handleSend(query);
    },
    [handleSend]
  );

  return (
    <div className="rounded-xl border border-purple-500/15 bg-slate-900/80 flex flex-col" style={{ minHeight: "520px" }}>
      {/* Top bar: model selector + clear */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-700/30">
        <ModelSelector
          selected={selectedProfile}
          onSelect={setSelectedProfile}
          disabled={isLoading}
        />
        {messages.length > 0 && (
          <button
            onClick={handleClear}
            disabled={isLoading}
            className="px-3 py-1.5 text-xs text-slate-400 bg-slate-800/40 border border-slate-700/30 rounded-lg hover:bg-slate-700/60 hover:text-slate-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150"
          >
            清空
          </button>
        )}
      </div>

      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm text-slate-600">
              输入问题或点击示例开始对话
            </p>
          </div>
        ) : (
          <MessageList messages={messages} />
        )}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-sky-400">
            <div className="w-2 h-2 bg-sky-400 rounded-full animate-pulse" />
            Agent 正在分析...
          </div>
        )}
      </div>

      {/* Error banner */}
      {errorMessage && (
        <div className="mx-4 mb-2 px-3 py-2 bg-red-900/20 border border-red-500/20 rounded-lg">
          <p className="text-xs text-red-400">{errorMessage}</p>
        </div>
      )}

      {/* Example prompts */}
      {messages.length === 0 && (
        <div className="px-4 py-3 border-t border-slate-700/30">
          <p className="text-xs text-slate-500 mb-2">示例问题：</p>
          <ExamplePrompts onSelect={handleExampleSelect} />
        </div>
      )}

      {/* Chat input */}
      <div className="px-4 py-3 border-t border-slate-700/30">
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
}

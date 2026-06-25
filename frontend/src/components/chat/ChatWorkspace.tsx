import { useState, useCallback } from "react";
import { MessageList } from "./MessageList";
import { ExamplePrompts } from "./ExamplePrompts";
import { ChatInput } from "./ChatInput";
import { ModelSelector } from "./ModelSelector";
import { sendAgentMessage } from "../../lib/api";
import { DEFAULT_LLM_PROFILE } from "../../lib/constants";
import type { AgentResponse, ChatMessage, LLMProfile } from "../../lib/types";

interface ChatWorkspaceProps {
  onResponseChange?: (response: AgentResponse) => void;
}

/**
 * Central chat workspace — manages real chat state and API calls.
 * Sends user queries to the backend with the selected llm_profile.
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

        // Notify parent of new response for metadata/citation panels
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
    [isLoading, messages, selectedProfile, buildHistory]
  );

  /** Handle example prompt click — sends directly. */
  const handleExampleSelect = useCallback(
    (query: string) => {
      handleSend(query);
    },
    [handleSend]
  );

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex-none pb-4 border-b border-slate-700/30">
        <h2 className="text-lg font-semibold text-slate-100">
          客服 Agent 对话
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          已接入后端 API · 模型选择只传 profile，不传 key
        </p>
      </div>

      {/* Model selector */}
      <div className="flex-none py-3 border-b border-slate-700/30">
        <ModelSelector
          selected={selectedProfile}
          onSelect={setSelectedProfile}
          disabled={isLoading}
        />
      </div>

      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm text-slate-600">
              输入问题或点击示例开始对话
            </p>
          </div>
        ) : (
          <MessageList messages={messages} />
        )}
      </div>

      {/* Error banner */}
      {errorMessage && (
        <div className="flex-none px-3 py-2 bg-red-900/20 border border-red-500/20 rounded-lg">
          <p className="text-xs text-red-400">{errorMessage}</p>
        </div>
      )}

      {/* Example prompts */}
      <div className="flex-none pt-3 border-t border-slate-700/30">
        <p className="text-xs text-slate-500 mb-2">示例问题：</p>
        <ExamplePrompts onSelect={handleExampleSelect} />
      </div>

      {/* Chat input */}
      <div className="flex-none pt-4">
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
}

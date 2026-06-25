import { MessageList } from "./MessageList";
import { ExamplePrompts } from "./ExamplePrompts";
import { ChatInput } from "./ChatInput";
import { ChatStatePreview } from "./ChatStatePreview";
import { STATIC_MESSAGES } from "../../data/chat";

/**
 * Central chat workspace — displays a static conversation with mock data.
 * No API calls, no real chat state management.
 */
export function ChatWorkspace() {
  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex-none pb-4 border-b border-slate-700/30">
        <h2 className="text-lg font-semibold text-slate-100">
          客服 Agent 对话
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          当前为静态 UI，M4 接入 API
        </p>
      </div>

      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        <MessageList messages={STATIC_MESSAGES} />
      </div>

      {/* Example prompts */}
      <div className="flex-none pt-4 border-t border-slate-700/30">
        <p className="text-xs text-slate-500 mb-2">示例问题：</p>
        <ExamplePrompts />
      </div>

      {/* Chat input */}
      <div className="flex-none pt-4">
        <ChatInput />
      </div>

      {/* Static state preview */}
      <div className="flex-none pt-4">
        <ChatStatePreview />
      </div>
    </div>
  );
}

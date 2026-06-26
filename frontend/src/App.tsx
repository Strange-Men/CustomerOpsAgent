import { useState } from "react";
import { AppShell } from "./components/layout/AppShell";
import { ChatWorkspace } from "./components/chat/ChatWorkspace";
import { AnswerDetails } from "./components/metadata/AnswerDetails";
import type { AgentResponse } from "./lib/types";

/**
 * Root application — single-column chat-first demo layout.
 * Chat is the primary focus; answer details appear below the latest response.
 */
function App() {
  const [activeResponse, setActiveResponse] = useState<AgentResponse | null>(
    null
  );

  return (
    <AppShell>
      <div className="space-y-4">
        {/* Hero intro — compact */}
        <section className="text-center space-y-1 pt-1 pb-0">
          <p className="text-sm text-slate-300 leading-relaxed max-w-[680px] mx-auto">
            跨境电商客服 Agent Demo：RAG 检索、意图路由、Mock 工具调用与安全模型 profile 选择。
          </p>
          <p className="text-[11px] text-slate-600">
            默认 Mock 可运行；DeepSeek / Doubao 仅作为后端 profile，前端不保存 key。
          </p>
        </section>

        {/* Chat console — main card */}
        <ChatWorkspace onResponseChange={setActiveResponse} />

        {/* Answer details — below chat */}
        {activeResponse && <AnswerDetails response={activeResponse} />}
      </div>
    </AppShell>
  );
}

export default App;

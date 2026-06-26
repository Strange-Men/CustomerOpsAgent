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
      <div className="space-y-6">
        {/* Hero intro */}
        <section className="text-center space-y-2 py-2">
          <p className="text-sm text-slate-300 leading-relaxed max-w-[700px] mx-auto">
            跨境电商客服 Agent Demo：支持 RAG 知识库检索、意图路由、Mock 工具调用与安全模型 profile 选择。
          </p>
          <p className="text-xs text-slate-500">
            默认使用 Mock 数据，可选择 DeepSeek / Doubao profile；真实 API key 只配置在后端。
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

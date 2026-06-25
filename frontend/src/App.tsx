import { useState } from "react";
import { AppShell } from "./components/layout/AppShell";
import { InfoPanel } from "./components/layout/InfoPanel";
import { ChatWorkspace } from "./components/chat/ChatWorkspace";
import { MetadataPanel } from "./components/metadata/MetadataPanel";
import { CitationPanel } from "./components/evidence/CitationPanel";
import { MOCK_RESPONSE } from "./data/mockResponse";
import type { AgentResponse } from "./lib/types";

/**
 * Root application — composes layout and panels.
 * Right panel shows real API response when available, falls back to mock.
 */
function App() {
  const [activeResponse, setActiveResponse] =
    useState<AgentResponse>(MOCK_RESPONSE);

  return (
    <AppShell>
      {/* Three-column desktop layout */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr_280px] gap-6">
        {/* Left: Project info */}
        <InfoPanel />

        {/* Center: Chat workspace */}
        <ChatWorkspace onResponseChange={setActiveResponse} />

        {/* Right: Metadata + Citations */}
        <div className="space-y-4">
          <MetadataPanel response={activeResponse} />
          <CitationPanel response={activeResponse} />
        </div>
      </div>
    </AppShell>
  );
}

export default App;

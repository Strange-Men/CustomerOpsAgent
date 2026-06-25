import { AppShell } from "./components/layout/AppShell";
import { InfoPanel } from "./components/layout/InfoPanel";
import { ChatWorkspace } from "./components/chat/ChatWorkspace";
import { MetadataPanel } from "./components/metadata/MetadataPanel";
import { CitationPanel } from "./components/evidence/CitationPanel";
import { MOCK_RESPONSE } from "./data/mockResponse";

/**
 * Root application — composes layout and panels with static mock data.
 * No API calls, no real state management.
 */
function App() {
  return (
    <AppShell>
      {/* Three-column desktop layout */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr_280px] gap-6">
        {/* Left: Project info */}
        <InfoPanel />

        {/* Center: Chat workspace */}
        <ChatWorkspace />

        {/* Right: Metadata + Citations */}
        <div className="space-y-4">
          <MetadataPanel response={MOCK_RESPONSE} />
          <CitationPanel response={MOCK_RESPONSE} />
        </div>
      </div>
    </AppShell>
  );
}

export default App;

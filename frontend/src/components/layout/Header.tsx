import { Badge } from "../common/Badge";
import { APP_NAME, RELEASE_TAG, API_INTEGRATION_STAGE } from "../../lib/constants";

/**
 * Top header bar showing project name, release tag, and system status badges.
 */
export function Header() {
  return (
    <header className="border-b border-purple-500/15 bg-slate-950/90 backdrop-blur-sm">
      <div className="max-w-[1600px] mx-auto px-6 py-3 flex items-center justify-between">
        {/* Left: project name */}
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold tracking-tight text-slate-100">
            {APP_NAME}
          </h1>
          <Badge label={RELEASE_TAG} variant="accent" />
        </div>

        {/* Right: status badges */}
        <div className="flex items-center gap-2">
          <Badge label="Mock Default" variant="warning" />
          <Badge label="RAG Enabled" variant="success" />
          <Badge label="Optional LLM" variant="info" />
          <span className="text-xs text-slate-600 ml-2">
            API integration in {API_INTEGRATION_STAGE}
          </span>
        </div>
      </div>
    </header>
  );
}

import { Badge } from "../common/Badge";
import { APP_NAME, RELEASE_TAG } from "../../lib/constants";

/**
 * Compact top header — project name, release tag, status badges.
 */
export function Header() {
  return (
    <header className="border-b border-purple-500/15 bg-slate-950/90 backdrop-blur-sm">
      <div className="max-w-[1100px] mx-auto px-4 sm:px-6 py-2 flex flex-wrap items-center justify-between gap-1.5">
        {/* Left: project name + release */}
        <div className="flex items-center gap-2">
          <h1 className="text-sm sm:text-base font-bold tracking-tight text-slate-100">
            {APP_NAME}
          </h1>
          <Badge label={RELEASE_TAG} variant="accent" />
        </div>

        {/* Right: status badges */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <Badge label="Mock Default" variant="warning" />
          <Badge label="RAG Enabled" variant="success" />
          <Badge label="Optional LLM" variant="info" />
        </div>
      </div>
    </header>
  );
}

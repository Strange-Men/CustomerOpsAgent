import { Card } from "../common/Card";
import { Badge } from "../common/Badge";
import {
  PROJECT_NAME,
  PROJECT_TAGLINE,
  PROJECT_DESCRIPTION,
  CAPABILITIES,
  LIMITATIONS,
  STATUS_BADGES,
} from "../../data/project";

/**
 * Left panel showing project info, capabilities, and limitations.
 */
export function InfoPanel() {
  return (
    <aside className="space-y-4">
      {/* Project overview */}
      <Card glow>
        <h2 className="text-base font-semibold text-slate-100 mb-1">
          {PROJECT_NAME}
        </h2>
        <p className="text-xs text-purple-300/80 mb-3">{PROJECT_TAGLINE}</p>
        <p className="text-xs text-slate-400 leading-relaxed">
          {PROJECT_DESCRIPTION}
        </p>
      </Card>

      {/* Status badges */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Status
        </h3>
        <div className="flex flex-wrap gap-1.5">
          {STATUS_BADGES.map((badge) => (
            <Badge key={badge.label} label={badge.label} variant={badge.variant} />
          ))}
        </div>
      </Card>

      {/* Capabilities */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Capabilities
        </h3>
        <ul className="space-y-1.5">
          {CAPABILITIES.map((cap) => (
            <li key={cap} className="flex items-start gap-2 text-xs text-slate-300">
              <span className="text-fuchsia-400 mt-0.5">&#9670;</span>
              <span>{cap}</span>
            </li>
          ))}
        </ul>
      </Card>

      {/* Limitations */}
      <Card>
        <h3 className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-3">
          Limitations
        </h3>
        <ul className="space-y-1.5">
          {LIMITATIONS.map((lim) => (
            <li key={lim} className="flex items-start gap-2 text-xs text-slate-400">
              <span className="text-slate-600 mt-0.5">&#9670;</span>
              <span>{lim}</span>
            </li>
          ))}
        </ul>
      </Card>
    </aside>
  );
}

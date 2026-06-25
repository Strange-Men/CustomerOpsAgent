import { Badge } from "../common/Badge";
import type { RouteType } from "../../lib/types";

interface RouteBadgeProps {
  route: RouteType;
  className?: string;
}

const ROUTE_VARIANT: Record<RouteType, "accent" | "success" | "warning"> = {
  logistics_tool: "success",
  rag_knowledge_base: "accent",
  fallback: "warning",
};

const ROUTE_LABEL: Record<RouteType, string> = {
  logistics_tool: "Logistics Tool",
  rag_knowledge_base: "RAG Knowledge Base",
  fallback: "Fallback",
};

/**
 * Route type displayed as a styled badge.
 */
export function RouteBadge({ route, className = "" }: RouteBadgeProps) {
  return (
    <Badge
      label={ROUTE_LABEL[route]}
      variant={ROUTE_VARIANT[route]}
      className={className}
    />
  );
}

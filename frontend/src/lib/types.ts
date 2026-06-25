/**
 * Core type definitions for CustomerOpsAgent frontend.
 * Based on the backend API contract defined in backend/app/agent/schemas.py
 * and backend/app/api/agent.py.
 */

/** Route types for customer service agent workflow. */
export type RouteType = "logistics_tool" | "rag_knowledge_base" | "fallback";

/** High-level route intent. */
export type IntentType =
  | "logistics"
  | "aftersale"
  | "trace"
  | "other";

/** Detailed intent for prompt and citation context. */
export type DetailIntentType =
  | "logistics_status"
  | "logistics_policy"
  | "customs"
  | "return"
  | "refund"
  | "exchange"
  | "address"
  | "order"
  | "payment"
  | "package"
  | "coupon"
  | "trace"
  | "unknown";

/** Answer source: where the answer was generated from. */
export type AnswerSource = "mock" | "real_llm" | "real_llm_fallback_mock";

/** Confidence level. */
export type ConfidenceLevel = "high" | "medium" | "low";

/** Supported locales — planned for i18n, not yet implemented. */
export type Locale = "zh-CN" | "en-US";

/** Citation from retrieved chunks. */
export interface Citation {
  doc_id: string;
  chunk_id: string;
  title: string;
  source: string;
  category: string;
  market: string;
  language: string;
}

/** Chat message sent from the user to the agent. */
export interface AgentRequest {
  user_query: string;
  order_id?: string | null;
  conversation_history?: string[];
}

/** Chat message returned by the agent. */
export interface AgentResponse {
  answer: string;
  route: RouteType;
  intent: IntentType;
  detail_intent: DetailIntentType;
  citations: Citation[];
  fallback_triggered: boolean;
  fallback_reason: string | null;
  confidence: ConfidenceLevel;
  retrieved_doc_ids: string[];
  order_id: string | null;
  tool_used: string | null;
  answer_source: AnswerSource;
  llm_provider: string | null;
  llm_model: string | null;
}

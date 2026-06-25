/**
 * Static mock AgentResponse for M2 display.
 * This is frontend-only fake data — not from a real API call.
 * Field names match the backend API contract exactly.
 */

import type { AgentResponse } from "../lib/types";

export const MOCK_RESPONSE: AgentResponse = {
  answer:
    "根据物流查询，您的订单 ORD-2024-0088 目前正在海关清关中。由于近期节假日影响，清关流程可能需要额外 2-3 个工作日。建议您耐心等待，如超过 5 个工作日仍未更新，请联系客服获取进一步协助。",
  route: "rag_knowledge_base",
  intent: "logistics",
  detail_intent: "customs",
  citations: [
    {
      doc_id: "DOC-CUSTOMS-001",
      chunk_id: "CHK-001-03",
      title: "跨境电商清关流程指南",
      source: "knowledge_base/policies/customs_guide.md",
      category: "customs",
      market: "CN-Global",
      language: "zh",
    },
    {
      doc_id: "DOC-LOGISTICS-015",
      chunk_id: "CHK-015-07",
      title: "物流延迟处理标准流程",
      source: "knowledge_base/policies/logistics_delay.md",
      category: "logistics",
      market: "CN-Global",
      language: "zh",
    },
  ],
  fallback_triggered: false,
  fallback_reason: null,
  confidence: "high",
  retrieved_doc_ids: ["DOC-CUSTOMS-001", "DOC-LOGISTICS-015"],
  order_id: "ORD-2024-0088",
  tool_used: null,
  answer_source: "mock",
  llm_provider: null,
  llm_model: null,
};

export const MOCK_USER_QUERY = "我的订单 ORD-2024-0088 清关延迟了，怎么办？";

/**
 * Example questions for the chat UI.
 * Used as static placeholder suggestions — not connected to any API.
 * Selected to demonstrate RAG, logistics tool, and fallback capabilities.
 */

import type { ExamplePrompt } from "../lib/types";

export const EXAMPLE_QUESTIONS: ExamplePrompt[] = [
  {
    id: "customs-delay",
    label: "清关延迟一般是什么原因？",
    query: "清关延迟一般是什么原因？",
    scenario: "customs",
    expectedRoute: "rag_knowledge_base",
  },
  {
    id: "refund-timeline",
    label: "退款多久到账？",
    query: "退款多久到账？",
    scenario: "refund",
    expectedRoute: "rag_knowledge_base",
  },
  {
    id: "order-tracking",
    label: "我的订单123456到哪了？",
    query: "我的订单123456到哪了？",
    scenario: "logistics",
    expectedRoute: "logistics_tool",
  },
  {
    id: "payment-failed",
    label: "支付失败怎么办？",
    query: "支付失败怎么办？",
    scenario: "payment",
    expectedRoute: "rag_knowledge_base",
  },
  {
    id: "off-topic",
    label: "你能帮我写论文吗？",
    query: "你能帮我写论文吗？",
    scenario: "fallback",
    expectedRoute: "fallback",
  },
];

/**
 * Example questions for the chat UI.
 * Used as static placeholder suggestions — not connected to any API.
 */

export interface ExamplePrompt {
  id: string;
  text: string;
  category: string;
}

export const EXAMPLE_QUESTIONS: ExamplePrompt[] = [
  {
    id: "customs-delay",
    text: "清关延迟怎么办？",
    category: "customs",
  },
  {
    id: "refund-timeline",
    text: "退款多久到账？",
    category: "refund",
  },
  {
    id: "order-tracking",
    text: "我的订单123456到哪了？",
    category: "logistics",
  },
  {
    id: "package-status",
    text: "我的快递到哪了？",
    category: "logistics",
  },
  {
    id: "off-topic",
    text: "你能帮我写论文吗？",
    category: "fallback",
  },
];

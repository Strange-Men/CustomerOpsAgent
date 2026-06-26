/**
 * Project metadata — static display data for the info panel.
 */

export const PROJECT_NAME = "CustomerOpsAgent";

export const PROJECT_TAGLINE =
  "跨境电商智能客服 Agent 演示，支持 RAG 知识库检索、工作流路由与兜底回复。";

export const PROJECT_DESCRIPTION =
  "基于 RAG + 工作流的智能客服 Agent 演示系统，覆盖物流查询、售后处理等场景。默认使用 Mock 数据，可选接入真实 LLM。";

export const RELEASE_TAG_DISPLAY = "v1.2.0-demo";

export const CAPABILITIES = [
  "RAG 知识库检索",
  "Mock 物流工具集成",
  "意图识别与两层路由",
  "确定性兜底工作流",
  "可选真实 LLM 适配器",
  "引用与证据追踪",
  "回答来源透明标注",
];

export const LIMITATIONS = [
  "演示环境 — 使用 Mock 数据，未接入真实物流 API。",
  "未连接真实订单管理系统。",
  "回复由确定性工作流生成，非生产级 LLM 流水线。",
  "无身份认证或多租户支持。",
  "无流式输出或 WebSocket 支持。",
];

export const STATUS_BADGES = [
  { label: "默认 Mock", variant: "warning" as const },
  { label: "RAG 已启用", variant: "success" as const },
  { label: "可选 LLM", variant: "info" as const },
  { label: "v1.2.0-demo", variant: "accent" as const },
];

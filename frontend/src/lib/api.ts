/**
 * API client for CustomerOpsAgent backend.
 *
 * Safety rules:
 * - Only calls the Render backend via VITE_API_BASE_URL.
 * - Never sends API keys, base URLs, or real model names.
 * - Only sends the public llm_profile field (mock / deepseek / doubao).
 */

import type { AgentRequest, AgentResponse } from "./types";
import { DEFAULT_API_BASE_URL, DEFAULT_LLM_PROFILE } from "./constants";

/**
 * Resolve the backend API base URL.
 * Priority: VITE_API_BASE_URL env var → DEFAULT_API_BASE_URL constant.
 * Strips trailing slash.
 */
export function getApiBaseUrl(): string {
  const envUrl = import.meta.env.VITE_API_BASE_URL as string | undefined;
  const raw = envUrl?.trim() || DEFAULT_API_BASE_URL;
  return raw.replace(/\/+$/, "");
}

/**
 * Send a chat message to the agent backend.
 *
 * @param request - Agent request with user_query, optional order_id,
 *                  conversation_history, and llm_profile.
 * @returns Parsed AgentResponse from the backend.
 * @throws Error with user-readable message on failure.
 */
export async function sendAgentMessage(
  request: AgentRequest
): Promise<AgentResponse> {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}/api/agent/chat`;

  const body = {
    user_query: request.user_query,
    order_id: request.order_id ?? null,
    conversation_history: request.conversation_history ?? [],
    llm_profile: request.llm_profile ?? DEFAULT_LLM_PROFILE,
  };

  let response: Response;
  try {
    response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error(
      "无法连接后端服务，请确认 Render API 是否可用。"
    );
  }

  if (!response.ok) {
    let detail = "";
    try {
      const errData = await response.json();
      detail = errData.detail || JSON.stringify(errData);
    } catch {
      detail = response.statusText;
    }
    throw new Error(`请求失败 (${response.status}): ${detail}`);
  }

  return response.json() as Promise<AgentResponse>;
}

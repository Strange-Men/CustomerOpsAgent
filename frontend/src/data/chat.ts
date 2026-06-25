/**
 * Static chat messages for demo display.
 * This is frontend-only fake data — not from a real API call.
 * Used to demonstrate the chat UI layout without backend integration.
 */

import type { ChatMessage } from "../lib/types";
import { MOCK_RESPONSE, MOCK_USER_QUERY } from "./mockResponse";

/** System message shown at the top of chat. */
export const SYSTEM_MESSAGE: ChatMessage = {
  id: "system-001",
  role: "system",
  content: "当前为静态 Demo 模式，M4 将接入后端 API。",
  createdAt: new Date().toISOString(),
};

/** Example user message. */
export const USER_MESSAGE: ChatMessage = {
  id: "user-001",
  role: "user",
  content: MOCK_USER_QUERY,
  createdAt: new Date().toISOString(),
};

/** Example assistant message with mock response. */
export const ASSISTANT_MESSAGE: ChatMessage = {
  id: "assistant-001",
  role: "assistant",
  content: MOCK_RESPONSE.answer,
  createdAt: new Date().toISOString(),
  response: MOCK_RESPONSE,
};

/** Static message list for demo. */
export const STATIC_MESSAGES: ChatMessage[] = [
  SYSTEM_MESSAGE,
  USER_MESSAGE,
  ASSISTANT_MESSAGE,
];

/**
 * Core type definitions for CustomerOpsAgent frontend.
 * Based on the backend API contract defined in backend/app/agent.py.
 */

/** Chat message sent from the user to the agent. */
export interface AgentRequest {
  question: string;
}

/** Chat message returned by the agent. */
export interface AgentResponse {
  answer: string;
  reasoning_steps?: string[];
  metadata?: Record<string, unknown>;
}

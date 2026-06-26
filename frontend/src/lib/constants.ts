/**
 * Application-wide constants.
 */

export const RELEASE_TAG = "v1.6.1-final-polish";

export const APP_NAME = "CustomerOpsAgent";

export const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

/** Stage at which real API integration will be added. */
export const API_INTEGRATION_STAGE = "Frontend M4";

export const THEME_NAME = "Dark Pink-Purple Agent Console";

/** Deployed URLs */
export const FRONTEND_DEMO_URL = "https://customer-ops-agent.vercel.app/";
export const BACKEND_API_BASE_URL = "https://customeropsagent.onrender.com";
export const API_DOCS_URL = "https://customeropsagent.onrender.com/docs";

/** Default LLM profile — always safe, no key needed. */
export const DEFAULT_LLM_PROFILE = "mock" as const;

/** i18n planning constants (not implemented yet) */
export const DEFAULT_LOCALE = "zh-CN";
export const SUPPORTED_LOCALES = ["zh-CN", "en-US"] as const;
export const LANGUAGE_SWITCH_STAGE = "Frontend M7.5";

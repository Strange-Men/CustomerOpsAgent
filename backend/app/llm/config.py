"""
CustomerOps Agent - LLM Adapter Configuration

Reads LLM configuration from environment variables.
Supports profile-based selection: mock, deepseek, doubao.
No API keys are printed or stored in code.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Environment variable names (legacy global config)
ENV_LLM_MODE = "CUSTOMEROPS_LLM_MODE"
ENV_LLM_PROVIDER = "CUSTOMEROPS_LLM_PROVIDER"
ENV_LLM_BASE_URL = "CUSTOMEROPS_LLM_BASE_URL"
ENV_LLM_API_KEY = "CUSTOMEROPS_LLM_API_KEY"
ENV_LLM_MODEL = "CUSTOMEROPS_LLM_MODEL"
ENV_LLM_TIMEOUT_SECONDS = "CUSTOMEROPS_LLM_TIMEOUT_SECONDS"

# Allowed profile names (public, sent by frontend)
ALLOWED_PROFILES: tuple[str, ...] = ("mock", "deepseek", "doubao")

# Profile → environment variable mapping
# Each profile maps to (base_url_env, api_key_env, model_env)
_PROFILE_ENV_MAP: dict[str, tuple[str, str, str]] = {
    "deepseek": (
        "CUSTOMEROPS_LLM_DEEPSEEK_BASE_URL",
        "CUSTOMEROPS_LLM_DEEPSEEK_API_KEY",
        "CUSTOMEROPS_LLM_DEEPSEEK_MODEL",
    ),
    "doubao": (
        "CUSTOMEROPS_LLM_DOUBAO_BASE_URL",
        "CUSTOMEROPS_LLM_DOUBAO_API_KEY",
        "CUSTOMEROPS_LLM_DOUBAO_MODEL",
    ),
}


@dataclass(frozen=True)
class LLMConfig:
    """LLM adapter configuration."""

    mode: str  # "mock" or "real"
    provider: str  # "openai_compatible"
    base_url: str | None
    api_key: str | None
    model: str | None
    timeout_seconds: int

    @property
    def is_real_mode(self) -> bool:
        """Check if real LLM mode is enabled."""
        return self.mode == "real"

    @property
    def is_config_complete(self) -> bool:
        """Check if all required config for real LLM is present."""
        return bool(self.base_url and self.api_key)


def _parse_timeout() -> int:
    """Parse timeout from env with safe default."""
    timeout_str = os.environ.get(ENV_LLM_TIMEOUT_SECONDS, "20").strip()
    try:
        timeout_seconds = int(timeout_str)
        if timeout_seconds <= 0:
            return 20
        return timeout_seconds
    except ValueError:
        return 20


def load_llm_config() -> LLMConfig:
    """
    Load LLM configuration from environment variables (legacy global config).

    Returns:
        LLMConfig with values from environment or defaults.
        No API key is logged.
    """
    mode = os.environ.get(ENV_LLM_MODE, "mock").strip().lower()
    provider = os.environ.get(ENV_LLM_PROVIDER, "openai_compatible").strip().lower()
    base_url = os.environ.get(ENV_LLM_BASE_URL, "").strip() or None
    api_key = os.environ.get(ENV_LLM_API_KEY, "").strip() or None
    model = os.environ.get(ENV_LLM_MODEL, "").strip() or None
    timeout_seconds = _parse_timeout()

    # Log config without API key
    if mode == "real":
        if not base_url or not api_key:
            logger.warning(
                "LLM mode is 'real' but configuration is incomplete "
                "(base_url=%s, api_key=%s). Will fallback to mock.",
                "set" if base_url else "missing",
                "set" if api_key else "missing",
            )
        else:
            logger.info(
                "LLM config loaded: mode=%s, provider=%s, base_url=%s, model=%s, timeout=%ds",
                mode,
                provider,
                base_url,
                model or "default",
                timeout_seconds,
            )
    else:
        logger.info("LLM config: mode=mock (default)")

    return LLMConfig(
        mode=mode,
        provider=provider,
        base_url=base_url,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )


def load_llm_config_for_profile(profile: str) -> LLMConfig:
    """
    Load LLM configuration for a specific profile.

    Profiles:
        - "mock": Always returns mock config (mode=mock).
        - "deepseek": Reads CUSTOMEROPS_LLM_DEEPSEEK_* env vars.
        - "doubao": Reads CUSTOMEROPS_LLM_DOUBAO_* env vars.

    If the profile is not in the allowed list, falls back to mock.
    If the profile's env vars are incomplete, falls back to mock config
    (mode=mock, so factory will return MockLLMAdapter).

    Args:
        profile: One of "mock", "deepseek", "doubao".

    Returns:
        LLMConfig for the requested profile. Never raises.
    """
    profile = profile.strip().lower()

    if profile not in ALLOWED_PROFILES:
        logger.warning("Unknown llm_profile '%s', falling back to mock", profile)
        return LLMConfig(
            mode="mock", provider="openai_compatible",
            base_url=None, api_key=None, model=None,
            timeout_seconds=_parse_timeout(),
        )

    if profile == "mock":
        return LLMConfig(
            mode="mock", provider="openai_compatible",
            base_url=None, api_key=None, model=None,
            timeout_seconds=_parse_timeout(),
        )

    # Profile is deepseek or doubao — read profile-specific env vars
    base_url_env, api_key_env, model_env = _PROFILE_ENV_MAP[profile]
    base_url = os.environ.get(base_url_env, "").strip() or None
    api_key = os.environ.get(api_key_env, "").strip() or None
    model = os.environ.get(model_env, "").strip() or None
    timeout_seconds = _parse_timeout()

    if not base_url or not api_key:
        logger.warning(
            "Profile '%s' config incomplete (base_url=%s, api_key=%s). "
            "Will fallback to mock.",
            profile,
            "set" if base_url else "missing",
            "set" if api_key else "missing",
        )
        # Return mode="mock" so factory returns MockLLMAdapter
        return LLMConfig(
            mode="mock", provider="openai_compatible",
            base_url=None, api_key=None, model=None,
            timeout_seconds=timeout_seconds,
        )

    logger.info(
        "Profile '%s' config loaded: base_url=%s, model=%s, timeout=%ds",
        profile,
        base_url,
        model or "default",
        timeout_seconds,
    )
    return LLMConfig(
        mode="real",
        provider="openai_compatible",
        base_url=base_url,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
    )

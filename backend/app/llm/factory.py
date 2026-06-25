"""
CustomerOps Agent - LLM Adapter Factory

Creates the appropriate LLM adapter based on configuration.
Default is always MockLLMAdapter.
"""

from __future__ import annotations

import logging

from .base import BaseLLMAdapter
from .config import LLMConfig, load_llm_config
from .mock_adapter import MockLLMAdapter

logger = logging.getLogger(__name__)


def create_llm_adapter(config: LLMConfig | None = None) -> BaseLLMAdapter:
    """
    Create an LLM adapter based on configuration.

    Decision logic:
    1. If mode != "real" → MockLLMAdapter
    2. If mode == "real" but config incomplete → MockLLMAdapter (fallback)
    3. If mode == "real" and config complete → provider-specific adapter

    Args:
        config: LLM configuration. If None, loads from environment variables.

    Returns:
        An LLM adapter instance. Always returns a valid adapter, never raises.
    """
    if config is None:
        config = load_llm_config()

    # Default: mock
    if not config.is_real_mode:
        logger.info("LLM adapter: mock (default)")
        return MockLLMAdapter()

    # Real mode requested but config incomplete → fallback to mock
    if not config.is_config_complete:
        logger.warning(
            "LLM mode is 'real' but config incomplete. Falling back to mock adapter."
        )
        return MockLLMAdapter()

    # Real mode with complete config → create provider adapter
    if config.provider == "openai_compatible":
        from .openai_compatible_adapter import OpenAICompatibleAdapter

        logger.info("LLM adapter: openai_compatible (real)")
        return OpenAICompatibleAdapter(config)

    # Unknown provider → fallback to mock
    logger.warning("Unknown LLM provider '%s'. Falling back to mock adapter.", config.provider)
    return MockLLMAdapter()

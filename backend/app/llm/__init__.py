"""
CustomerOps Agent - LLM Adapter Package

Optional real LLM adapter for answer generation.
Default mode is mock (no real LLM calls).
"""

from .base import BaseLLMAdapter
from .config import LLMConfig, load_llm_config
from .factory import create_llm_adapter
from .mock_adapter import MockLLMAdapter
from .schemas import LLMGenerationRequest, LLMGenerationResult, LLMMessage

__all__ = [
    "BaseLLMAdapter",
    "LLMConfig",
    "LLMGenerationRequest",
    "LLMGenerationResult",
    "LLMMessage",
    "MockLLMAdapter",
    "create_llm_adapter",
    "load_llm_config",
]

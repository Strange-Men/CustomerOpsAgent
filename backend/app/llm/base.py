"""
CustomerOps Agent - LLM Adapter Base Class

Abstract base class for LLM adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import LLMGenerationRequest, LLMGenerationResult


class BaseLLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    @abstractmethod
    def generate(self, request: LLMGenerationRequest) -> LLMGenerationResult:
        """
        Generate text from a conversation.

        Args:
            request: Generation request with messages and parameters

        Returns:
            LLMGenerationResult with generated text and metadata
        """
        ...

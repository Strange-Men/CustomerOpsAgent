"""
CustomerOps Agent - Mock LLM Adapter

Default adapter that returns deterministic text without calling any real LLM API.
Used for testing and as fallback when real LLM is unavailable.
"""

from __future__ import annotations

from .base import BaseLLMAdapter
from .schemas import LLMGenerationRequest, LLMGenerationResult


class MockLLMAdapter(BaseLLMAdapter):
    """Mock LLM adapter that returns deterministic responses."""

    def generate(self, request: LLMGenerationRequest) -> LLMGenerationResult:
        """
        Generate a deterministic mock response.

        Extracts the last user message and returns a template-based answer.
        Does not call any external API.

        Args:
            request: Generation request with messages

        Returns:
            LLMGenerationResult with mock text
        """
        # Return a deterministic mock response

        # Return a deterministic mock response
        mock_text = (
            "您好，感谢您的咨询。根据当前知识库信息，"
            "建议您联系人工客服获取更详细的帮助。"
            "如有其他问题，请随时联系我们。"
        )

        return LLMGenerationResult(
            text=mock_text,
            provider="mock",
            model=None,
            is_real_llm=False,
            fallback_used=False,
            error_reason=None,
        )

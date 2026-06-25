"""
CustomerOps Agent - OpenAI-Compatible LLM Adapter

Calls a generic OpenAI-compatible /chat/completions endpoint.
Only used when CUSTOMEROPS_LLM_MODE=real and config is complete.

Safety:
- API key is never logged or included in error messages.
- Timeout is enforced.
- Errors are caught and returned as fallback results.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from .base import BaseLLMAdapter
from .config import LLMConfig
from .schemas import LLMGenerationRequest, LLMGenerationResult

logger = logging.getLogger(__name__)


class OpenAICompatibleAdapter(BaseLLMAdapter):
    """Adapter for OpenAI-compatible chat completion APIs."""

    def __init__(self, config: LLMConfig) -> None:
        """
        Initialize the adapter.

        Args:
            config: LLM configuration with base_url, api_key, model, timeout.
                    api_key is stored in memory only, never logged.
        """
        self._config = config

    def generate(self, request: LLMGenerationRequest) -> LLMGenerationResult:
        """
        Call the /chat/completions endpoint.

        Args:
            request: Generation request with messages and parameters

        Returns:
            LLMGenerationResult with generated text or fallback result on error.
            Error messages never contain the API key.
        """
        url = f"{self._config.base_url.rstrip('/')}/chat/completions"

        # Build request payload
        messages_payload = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        payload: dict[str, Any] = {
            "messages": messages_payload,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if self._config.model:
            payload["model"] = self._config.model

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._config.api_key}",
        }

        try:
            response = httpx.post(
                url,
                json=payload,
                headers=headers,
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()

            data = response.json()
            # Extract text from OpenAI-compatible response format
            text = _extract_text_from_response(data)

            return LLMGenerationResult(
                text=text,
                provider="openai_compatible",
                model=self._config.model,
                is_real_llm=True,
                fallback_used=False,
                error_reason=None,
            )

        except httpx.TimeoutException:
            error_msg = f"LLM request timed out after {self._config.timeout_seconds}s"
            logger.warning(error_msg)
            return _build_fallback_result(error_msg)

        except httpx.HTTPStatusError as exc:
            # Sanitize error: remove any potential key leakage from response body
            error_msg = f"LLM API returned HTTP {exc.response.status_code}"
            logger.warning("%s for %s", error_msg, url)
            return _build_fallback_result(error_msg)

        except (httpx.RequestError, json.JSONDecodeError, KeyError, ValueError) as exc:
            # Catch network errors, JSON parse errors, missing keys
            error_msg = f"LLM request failed: {type(exc).__name__}"
            logger.warning(error_msg)
            return _build_fallback_result(error_msg)


def _extract_text_from_response(data: dict[str, Any]) -> str:
    """
    Extract generated text from OpenAI-compatible response.

    Args:
        data: Parsed JSON response from /chat/completions

    Returns:
        Generated text string
    """
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("No choices in LLM response")

    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise ValueError("Empty content in LLM response")

    return content


def _build_fallback_result(error_reason: str) -> LLMGenerationResult:
    """
    Build a fallback result when real LLM fails.

    Args:
        error_reason: Description of what went wrong (must not contain API key)

    Returns:
        LLMGenerationResult indicating fallback to mock
    """
    return LLMGenerationResult(
        text="",
        provider="openai_compatible",
        model=None,
        is_real_llm=False,
        fallback_used=True,
        error_reason=error_reason,
    )

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - runtime dependency guard
    requests = None


class OpenRouterLLM:
    """Minimal OpenRouter chat client used by AgentV4 chat mode."""

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MAX_TOKENS = 512

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: int = 30,
    ) -> None:
        file_config = self._load_file_config()
        self.api_key = (
            api_key
            or os.getenv("OPENROUTER_API_KEY", "")
            or file_config.get("OPENROUTER_API_KEY", "")
        ).strip()
        self.model = (
            model
            or os.getenv("OPENROUTER_MODEL", "")
            or file_config.get("OPENROUTER_MODEL", "~openai/gpt-latest")
        ).strip()
        self.http_referer = (
            os.getenv("OPENROUTER_HTTP_REFERER", "")
            or file_config.get("OPENROUTER_HTTP_REFERER", "")
        ).strip()
        self.app_title = (
            os.getenv("OPENROUTER_APP_TITLE", "")
            or file_config.get("OPENROUTER_APP_TITLE", "")
        ).strip()
        configured_max_tokens = (
            os.getenv("OPENROUTER_MAX_TOKENS", "")
            or file_config.get("OPENROUTER_MAX_TOKENS", "")
        ).strip()
        self.max_tokens = self._parse_positive_int(configured_max_tokens, self.DEFAULT_MAX_TOKENS)
        self.timeout_seconds = timeout_seconds

    def generate(self, user_query: str) -> str:
        if not user_query.strip():
            return "Please ask a question."

        if requests is None:
            return "LLM dependency missing. Install `requests` to use chat mode."

        if not self.api_key:
            return (
                "LLM is not configured. Set `OPENROUTER_API_KEY` to enable chat generation."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful study assistant. Give accurate, concise answers."
                ),
            },
            {"role": "user", "content": user_query},
        ]
        return self._request_completion(messages)

    def generate_with_context(self, user_query: str, context: str, mode_name: str) -> str:
        if not context.strip():
            return "No relevant context found."
        if not user_query.strip():
            return "Please ask a question."
        if not self.is_configured():
            return (
                "LLM is not configured. Set `OPENROUTER_API_KEY` to enable chat generation."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a study assistant using retrieval context. "
                    "Answer the user query based only on the provided context. "
                    "If context is insufficient, clearly say so."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Mode: {mode_name}\n"
                    f"Question: {user_query}\n\n"
                    "Context:\n"
                    f"{context}\n\n"
                    "Give a concise, accurate answer."
                ),
            },
        ]
        return self._request_completion(messages)

    def is_configured(self) -> bool:
        return bool(self.api_key and requests is not None)

    def is_failure_message(self, message: str) -> bool:
        if not message:
            return True
        return message.startswith(
            (
                "LLM request failed",
                "LLM returned invalid JSON.",
                "LLM returned no answer choices.",
                "LLM returned an empty answer.",
                "LLM dependency missing.",
                "LLM is not configured.",
            )
        )

    def _error_message(self, response: Any) -> str:
        try:
            payload = response.json()
        except ValueError:
            text = (response.text or "").strip()
            return text or "Unknown error."

        error = payload.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            if isinstance(message, str) and message.strip():
                return message.strip()
        if isinstance(error, str) and error.strip():
            return error.strip()

        message = payload.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()

        return "Unknown error."

    def _request_completion(self, messages: list[dict[str, str]]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self.http_referer:
            headers["HTTP-Referer"] = self.http_referer

        if self.app_title:
            headers["X-Title"] = self.app_title

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
        except Exception as exc:  # pragma: no cover - network runtime guard
            return f"LLM request failed: {exc}"

        if response.status_code >= 400:
            return f"LLM request failed ({response.status_code}): {self._error_message(response)}"

        try:
            data = response.json()
        except ValueError:
            return "LLM returned invalid JSON."

        choices = data.get("choices") or []
        if not choices:
            return "LLM returned no answer choices."

        message = choices[0].get("message", {})
        content = self._content_to_text(message.get("content"))
        if not content:
            return "LLM returned an empty answer."
        return content

    def _content_to_text(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            chunks: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str) and text.strip():
                        chunks.append(text.strip())
            return "\n".join(chunks).strip()

        return ""

    def _candidate_env_paths(self) -> list[Path]:
        src_dir = Path(__file__).resolve().parents[1]
        project_dir = src_dir.parent
        return [
            project_dir / ".env",
            src_dir / ".env",
        ]

    def _load_file_config(self) -> dict[str, str]:
        config: dict[str, str] = {}
        for env_path in self._candidate_env_paths():
            if not env_path.exists():
                continue
            config.update(self._parse_env_file(env_path))
        return config

    def _parse_env_file(self, env_path: Path) -> dict[str, str]:
        values: dict[str, str] = {}
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", maxsplit=1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                values[key] = value
        return values

    def _parse_positive_int(self, value: str, default: int) -> int:
        if not value:
            return default
        try:
            parsed = int(value)
        except ValueError:
            return default
        if parsed <= 0:
            return default
        return parsed

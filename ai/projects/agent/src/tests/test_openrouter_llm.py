from pathlib import Path

from core.openrouter_llm import OpenRouterLLM


def test_openrouter_llm_reads_api_key_from_env_file(tmp_path: Path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENROUTER_API_KEY=file-key\nOPENROUTER_MODEL=~openai/gpt-latest\n",
        encoding="utf-8",
    )

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    monkeypatch.setattr(OpenRouterLLM, "_candidate_env_paths", lambda self: [env_file])

    llm = OpenRouterLLM()

    assert llm.api_key == "file-key"
    assert llm.model == "~openai/gpt-latest"


def test_openrouter_llm_prefers_os_env_over_env_file(tmp_path: Path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENROUTER_API_KEY=file-key\nOPENROUTER_MODEL=file-model\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("OPENROUTER_API_KEY", "env-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "env-model")
    monkeypatch.setattr(OpenRouterLLM, "_candidate_env_paths", lambda self: [env_file])

    llm = OpenRouterLLM()

    assert llm.api_key == "env-key"
    assert llm.model == "env-model"


def test_openrouter_llm_uses_safe_default_max_tokens(monkeypatch):
    monkeypatch.delenv("OPENROUTER_MAX_TOKENS", raising=False)
    monkeypatch.setattr(OpenRouterLLM, "_candidate_env_paths", lambda self: [])

    llm = OpenRouterLLM()

    assert llm.max_tokens == 512


def test_openrouter_llm_reads_max_tokens_from_env_file(tmp_path: Path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_MAX_TOKENS=256\n", encoding="utf-8")

    monkeypatch.delenv("OPENROUTER_MAX_TOKENS", raising=False)
    monkeypatch.setattr(OpenRouterLLM, "_candidate_env_paths", lambda self: [env_file])

    llm = OpenRouterLLM()

    assert llm.max_tokens == 256


def test_openrouter_llm_detects_failure_messages(monkeypatch):
    monkeypatch.setattr(OpenRouterLLM, "_candidate_env_paths", lambda self: [])
    llm = OpenRouterLLM()

    assert llm.is_failure_message("LLM request failed (402): credits")
    assert not llm.is_failure_message("Here is your answer.")

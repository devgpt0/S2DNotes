from core.agent_v4 import AgentV4


def test_mode_menu_shows_numbered_options():
    agent = AgentV4()
    response = agent.run("/mode")

    assert "1. chat" in response
    assert "2. keyword" in response
    assert "3. semantic" in response
    assert "4. hybrid" in response


def test_direct_numeric_mode_selection():
    agent = AgentV4()
    response = agent.run("/mode 2")

    assert "Mode changed to KEYWORD." == response
    assert agent.router.get_mode().value == "keyword"


def test_follow_up_numeric_selection_after_mode_menu():
    agent = AgentV4()
    agent.run("/mode")
    response = agent.run("1")

    assert "Mode changed to CHAT." == response
    assert agent.router.get_mode().value == "chat"


def test_keyword_mode_returns_focused_run_section_for_start_query():
    agent = AgentV4()
    agent.run("/mode 2")
    agent.llm.is_configured = lambda: False

    response = agent.run("How to start this application ?")

    assert "## Run" in response
    assert "uv run core-agent" in response
    assert "## CLI commands" not in response


def test_chat_mode_uses_llm_client_answer():
    agent = AgentV4()
    agent.llm.generate = lambda query: f"LLM::{query}"

    response = agent.run("Explain Python lists")

    assert response == "LLM::Explain Python lists"


def test_keyword_mode_uses_llm_with_retrieved_context_when_configured():
    agent = AgentV4()
    agent.run("/mode 2")
    agent.llm.is_configured = lambda: True
    agent.llm.generate_with_context = (
        lambda query, context, mode: f"RAG::{mode}::{query}::{'## Run' in context}"
    )
    agent.llm.is_failure_message = lambda message: False

    response = agent.run("How to start this application ?")

    assert response == "RAG::keyword::How to start this application ?::True"

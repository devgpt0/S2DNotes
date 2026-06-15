from core.agent_v4 import AgentV4


def test_load_command_indexes_text_file_for_keyword_retrieval(tmp_path):
    doc_path = tmp_path / "zephyria_guide.txt"
    doc_path.write_text(
        "Zephyria is a fictional language used for retrieval tests.",
        encoding="utf-8",
    )

    agent = AgentV4()
    agent.llm.is_configured = lambda: False

    load_response = agent.run(f"load {doc_path}")
    assert "Loaded 1 document(s)" in load_response

    agent.run("/mode 2")
    answer = agent.run("What is Zephyria?")

    assert "Zephyria is a fictional language" in answer


def test_load_command_returns_error_for_missing_path(tmp_path):
    missing_file = tmp_path / "missing.txt"

    agent = AgentV4()
    response = agent.run(f"load {missing_file}")

    assert "Path does not exist" in response


def test_load_command_skips_duplicate_file(tmp_path):
    doc_path = tmp_path / "duplicate.md"
    doc_path.write_text("# Duplicate\n\nThis is a test document.", encoding="utf-8")

    agent = AgentV4()
    first = agent.run(f"load {doc_path}")
    second = agent.run(f"load {doc_path}")

    assert "Loaded 1 document(s)" in first
    assert "Skipped already-loaded document(s): 1." in second

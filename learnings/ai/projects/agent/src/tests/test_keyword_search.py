from nlp.keyword_search import KeywordEngine


def test_keyword_search_returns_ranked_results():
    engine = KeywordEngine()
    engine.add_document("python programming language")
    engine.add_document("artificial intelligence systems")

    results = engine.search("python")

    assert results
    assert results[0][0] == "python programming language"

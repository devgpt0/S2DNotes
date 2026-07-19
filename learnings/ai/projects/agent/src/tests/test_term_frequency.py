from nlp.tfidf import TFIDF

def test_term_frequency():
    
    tfidf = TFIDF()
    
    tokens = ["the", "cat", "sat", "on", "the", "mat"]
    
    assert tfidf.term_frequency(tokens, "the") == 2 / 6
    assert tfidf.term_frequency(tokens, "cat") == 1 / 6
    assert tfidf.term_frequency(tokens, "dog") == 0.0
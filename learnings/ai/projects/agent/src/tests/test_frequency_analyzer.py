from nlp.frequency_analyzer import FrequencyAnalyzer

def test_count_tokens():
    
    analyzer = FrequencyAnalyzer()
    
    tokens = ["hello", "world", "hello"]
    
    result = analyzer.count_tokens(tokens)
    
    assert result == {"hello": 2, "world": 1}
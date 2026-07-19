from nlp.tokenizer_engine import TokenizerEngine

def test_tokenizer_engine():
    
    engine = TokenizerEngine()
    
    text = "Hello world! This is a test."
    
    token_ids = engine.encode(text)
    
    assert token_ids == [0, 1, 2, 3, 4, 5]
    
    decoded_text = engine.decode(token_ids)
    
    assert decoded_text == "hello world this is a test"
from nlp.vocabulary import Vocabulary

def test_encode():
    
    vocab = Vocabulary()
    
    tokens = ["hello", "world", "hello"]
    
    token_ids = vocab.encode(tokens)
    
    assert token_ids == [0, 1, 0]
    
def test_decode():
    
    vocab = Vocabulary()
    
    token_ids = [0, 1, 0]
    
    tokens = vocab.decode(token_ids)
    
    assert tokens == ["hello", "world", "hello"]
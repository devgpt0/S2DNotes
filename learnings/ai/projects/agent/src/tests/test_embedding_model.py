from nlp.embedding_model import EmbeddingModel

def test_embedding():
    model = EmbeddingModel()
    
    vector = model.embed("python")
    
    assert len(vector)>0
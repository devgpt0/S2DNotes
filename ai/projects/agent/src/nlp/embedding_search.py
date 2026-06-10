import numpy as np

from nlp.embedding_model import EmbeddingModel


class EmbeddingSearch:
    def __init__(self):
        self.model = EmbeddingModel()
        self.documents = []
        self.embeddings = []

    def add_document(self, document: str):
        self.documents.append(document)
        embedding = self.model.embed(document)
        self.embeddings.append(embedding)

    def cosine_similarity(self, a, b):
        denominator = np.linalg.norm(a) * np.linalg.norm(b)
        if denominator == 0:
            return 0.0
        return float(np.dot(a, b) / denominator)

    def search(self, query: str):
        query_embedding = self.model.embed(query)
        results = []

        for doc, emb in zip(self.documents, self.embeddings):
            score = self.cosine_similarity(query_embedding, emb)
            results.append((doc, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def semantic_search(self, query: str):
        return self.search(query)

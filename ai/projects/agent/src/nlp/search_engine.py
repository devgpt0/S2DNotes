from nlp.document_corpus import DocumentCorpus

from nlp.tfidf import TFIDF

class SearchEngine:
    def __init__(self):
        self.corpus = DocumentCorpus()
        self.tfidf = TFIDF()
        
    def add_document(self, document):
        self.corpus.add_document(document)
    
    def search(self,query,):
        
        results = []
        
        for doc in self.corpus.get_documents():
            score = self.tfidf.score_query_against_document(query, doc ,self.corpus)
            results.append((doc, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    

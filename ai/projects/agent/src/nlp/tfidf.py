import math

from collections import Counter

from nlp.pipeline import Pipeline

from nlp.document_corpus import DocumentCorpus

class TFIDF:
    
    def __init_(self,corpus:DocumentCorpus):
        self.pipeline = Pipeline()
    
    def term_frequency(self,tokens:list[str],term:str)->float:
        
        if not tokens:
            return 0.0
        
        counter = Counter(tokens)
        
        return counter[term] / len(tokens)
    
    def inverse_document_frequency(self,corpus:DocumentCorpus,term:str)->float:
       
       total_docs = corpus.total_documents()
       
       docs_with_term = 0
       
       for doc in (
           corpus.get_documents()
       ):
           tokens = (
               self.pipeline.tokenize(doc)
           )
           if term in tokens:
               docs_with_term += 1
               
    
       if docs_with_term == 0:
            return 0.0
        
       return math.log(total_docs / docs_with_term)
        

    def tf_idf(self,document:str,term:str)->float:
        tf = self.term_frequency(document, term)
        idf = self.inverse_document_frequency(term)
        return tf * idf

    def tfdif_score(
        self,
        tokens:list[str],
        corpus:DocumentCorpus,
        term:str
    )->float:
        
        tf = self.term_frequency(tokens, term)
        idf = self.inverse_document_frequency(corpus, term)
        
        return tf * idf
    
    def score_query_against_document(
        self,
        query:str,
        document:str,
        corpus:DocumentCorpus
    )->float:
       query_tokens = self.pipeline.process(query)
       
       doc_tokens = self.document_vector(document, corpus)
       
       score = 0.0
       
       for token in query_tokens:
           score += doc_tokens.get(token, 0.0)
           
       return score
           
    
    
def document_vector(self,document:str, corpus:DocumentCorpus)->dict[str,float]:
        tokens = self.pipeline.tokenize(document)
        unique_terms = set(tokens)
        
        vector = {}
        
        for token in unique_terms:
            score = self.tfdif_score(tokens, corpus, token)
            vector[token] = score
        
        return vector 
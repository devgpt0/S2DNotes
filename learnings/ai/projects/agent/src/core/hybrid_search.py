class HybridSearch:
    def search(self,query,keyword_engine,sematic_engine):
        keyword_results = keyword_engine.keyword_search(query)
        
        sematic_results = sematic_engine.semantic_search(query)
        
        combined ={}
        
        for doc,score in keyword_results:
            combined[doc]=(combined.get(doc,0)+score)
            
        ranked = sorted(combined.items(),key = lambda x:x[1],reverse = True)
        
        return ranked
from collections import Counter

class FrequencyAnalyzer:
    
    def count_tokens(self,tokens:list[str])->dict[str,int]:
        
        return dict(Counter(tokens))
    
    def most_common(self, tokens:list[str]):
        counter = Counter(tokens)
        
        return counter.most_common(1)[0] if counter else (None, 0) 
    
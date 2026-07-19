import re
from nlp.stopword import STOP_WORDS

class TextProcessor:
    
    def normalize(
        self,
        text:str
    )->str:
        
        text = text.lower()
        
        text = re.sub(r'[^\w\s]', '', text)
        
        text = text.strip()
        
        return text
    
    def remove_stopwords(
        self,
        tokens
    ):
        return [
            token 
            for token in tokens
            if token not in STOP_WORDS
        ]
        
        
    
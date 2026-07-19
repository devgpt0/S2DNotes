from nlp.pipeline import NLPPipeline

from nlp.frequency_analyzer import FrequencyAnalyzer


class BagOfWords:
    
    def __init__(self):
        self.pipeline = NLPPipeline()
        self.analyzer = FrequencyAnalyzer()
        
    def transform(self,text:str)->dict[str,int]:
        tokens = self.pipeline.process(text)
        
        return self.analyzer.count_tokens(tokens)
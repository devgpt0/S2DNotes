from study_agent.models import Task
from nlp.pipeline import NLPPipeline
from nlp.tokenizer_engine import TokenizerEngine
from nlp.bag_of_words import BagOfWords
from nlp.search_engine import SearchEngine

class StudyAgent:

    def __init__(self):
        self.name = "StudyAgent"
        self.tokenizer_engine = TokenizerEngine()
        self.nlp_pipeline = NLPPipeline()
        self.bag_of_words = BagOfWords()
        self.search_engine = SearchEngine()
        
        self.search_engine.add_document("Python is programming language")
        self.search_engine.add_document("AI enables intelligent system")
        self.search_engine.add_document("Machine learning learns from data")

    def think(self, task: Task):
        if task.query.startswith("search"):
            
            query = task.query.replace("search","")
            
            results = self.search_engine.search(query) 
            
            best_doc = results[0][0]
            
            return (f"Best Match: \n{best_doc}")
        
        token_ids = self.tokenizer_engine.encode(task.query)
        print(f"Encoded Task: {token_ids}")
    
        
        tokens = self.tokenizer_engine.decode(token_ids).split()
        print(f"Decoded  Tokens: {tokens}")
        
        
        bow_features = self.bag_of_words.transform(task.query)
        print(f"Bag of Words Features: {bow_features}")
        
        if "python" in tokens:
            return "Python is a popular programming language used for web development, data science, and automation."
        
        if "ai" in tokens:
            return "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines."
        
        return "I'm not sure how to help with that. Can you ask something else?"


    def run(self, user_input: str) -> str:
        task = Task(query=user_input)
        response = self.think(task)
        return response

from study_agent.models import Task
from nlp.pipeline import NLPPipeline
from nlp.tokenizer_engine import TokenizerEngine

class StudyAgent:

    def __init__(self):
        self.name = "StudyAgent"
        self.tokenizer_engine = TokenizerEngine()
        self.nlp_pipeline = NLPPipeline()

    def think(self, task: Task):
        token_ids = self.tokenizer_engine.encode(task.query)
        print(f"Encoded Task: {token_ids}")
        
        tokens = self.tokenizer_engine.decode(token_ids).split()
        print(f"Decoded  Tokens: {tokens}")
        
        if "python" in tokens:
            return "Python is a popular programming language used for web development, data science, and automation."
        
        if "ai" in tokens:
            return "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines."
        
        return "I'm not sure how to help with that. Can you ask something else?"


    def run(self, user_input: str) -> str:
        task = Task(query=user_input)
        response = self.think(task)
        return response

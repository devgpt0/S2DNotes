from study_agent.models import Task
from nlp.pipeline import NLPPipeline

class StudyAgent:

    def __init__(self):
        self.name = "StudyAgent"
        self.nlp_pipeline = NLPPipeline()

    def think(self, task: Task):
        query = task.query.lower()
        print(f"Thinking about the query: {query}")

        tokens = self.nlp_pipeline.process(query)

        if "python" in tokens:
            print("[Decision] I know something about Python!")

            return "Python is a popular programming language known for its simplicity and versatility."

        if "ai" in tokens:
            print("[Decision] I know something about AI!")
            return "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."

        print("[Decision] I don't know much about that.")
        return "I'm not sure how to answer that. Can you please provide more details or ask a different question?"

    def run(self, user_input: str) -> str:
        task = Task(query=user_input)
        response = self.think(task)
        return response

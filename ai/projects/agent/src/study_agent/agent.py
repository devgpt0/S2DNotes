from study_agent.models import Task 

class StudyAgent:
    
    def __init__(self):
        self.name = "StudyAgent"
        
    def think(self,task:Task):
        
        query = task.query.lower()
        print(f"Thinking about the query: {query}")
        
        if "python" in query:
            print("[Decision] I know something about Python!")
            
            return "Python is a popular programming language known for its simplicity and versatility."
        
        if "ai" in query:
            print("[Decision] I know something about AI!")
            return "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."
        
        print("[Decision] I don't know much about that.")
        return "I'm not sure how to answer that. Can you please provide more details or ask a different question?"
    
    def run(self, user_input:str)-> str:
        task = Task(query=user_input)
        response = self.think(task)
        return response
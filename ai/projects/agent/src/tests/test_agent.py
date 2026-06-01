from study_agent.agent import StudyAgent

def test_agent_response():
    
    agent = StudyAgent()
    
    #Test Python query
    response = agent.run("What is Python?")
    assert "Python is a popular programming language" in response
    
    #Test AI query
    response = agent.run("What is AI?")
    assert "Artificial Intelligence (AI) is the simulation of human intelligence processes" in response
    #Test unknown query
    
    
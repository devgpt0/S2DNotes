from study_agent.agent import StudyAgent


def main():
    print("Hello from study_agent!")
    agent = StudyAgent()
    
    while True:
        
        query = input("You >")
        
        if query.lower() == "exit":
            break
        
        response = agent.run(query)
        
        print(f"Agent> {response}")

if __name__ == "__main__":
    main()

Study Agent : 
A terminal Based Agent that : 
1.Accept user query/goal
2.Classify your intent
3.Execute actions
4.Return a response5.Logs reasoning steps

Architecture: 
User -> Agent -> Think -> Decide ->Act->Response

What is an Agent?
Normal Program : Input -> Output
Agent : Goal -> Reason -> Action -> Result

version : 1 
UserInput -> Agent -> Think and Match with Key words -> Answer

version : 2
UserInput->Text Processor -> Normalize Text->Tokenizer -> Token -> Agent -> Think ->Answer 

version : 3
UserInput->Tokenizer Engine (Encode)->Think -> Tokenizer(Decode)->Output



Agent = LLM + Memory + Tools + Planning + Loop

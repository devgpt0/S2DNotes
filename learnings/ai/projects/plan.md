Study Agent : 
A terminal Based Agent that : 
1.Accept user query/goal
2.Classify your intent
3.Execute actions
4.Return a responses.Logs reasoning steps

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
Encode : Words -> Tokens -> TokenIDs
Decode : TokenIds->Tokens -> Words

version : 4
UserInput-> Check (Wethear the user want to ask or want to search)
Ask -> Tokenizer(Encode)-> Think ->Tokenizer(Decode)->Output
Search-> IF/TDF ( Keyword Search)-> Output

Search -> Keywords(Excat) and Sematic(Similar) 

version : 5
UserInput->Check ( Wether it is sematic / keyword / ask)-> Response
Ask -> Tokenizer(Encode)-> Think ->Tokenizer(Decode)->Output
Keyword Search-> IF/TDF ( Keyword Search)-> Output
Sematic Search -> Embeddings -> Cosine Similarity -> Output


Python , python ,PYTHON -> Response

AI ,Aritifical Intelligence -> Same ? -> Keyword -> Excat , Similiar -> Sematic search 

Agent = LLM + Memory + Tools + Planning + Loop

class Vocabulary:
    DEFAULT_ID_TO_TOKEN = {
        0: "hello",
        1: "world",
    }
    
    def __init__(self):
        self.token_to_id = {}
        self.id_to_token = {}
        self.next_id = 0
        
    def add_token(self,token:str):
        
        if token not in self.token_to_id:
            token_id = self.next_id
            
            self.token_to_id[token] = token_id
            
            self.id_to_token[token_id] = token
            
            self.next_id +=1
            
    def encode(self, tokens:list[str])->list[int]:
        
        token_ids = []
        
        for token in tokens:
            
            self.add_token(token)
            
            token_ids.append(self.token_to_id[token])
        
        return token_ids
    
    def decode(self, token_ids:list[int])->list[str]:
        
        return [
            self.id_to_token.get(
                token_id,
                self.DEFAULT_ID_TO_TOKEN.get(token_id, "<UNK>")
            )
            for token_id in token_ids
        ]
        
    def size(self)->int:
        return len(self.token_to_id)

from core.search_mode import SearchMode

class QueryRouter:
    
    def __init__(self):
        self.mode = SearchMode.CHAT
        
    def set_mode(self,mode:str):
        self.mode = SearchMode(mode.lower())
    
    def get_mode(self):
        return self.mode

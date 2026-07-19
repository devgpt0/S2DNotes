class DocumentStats:
    def word_count(self, tokens: list[str]) -> int:
        return len(tokens)
    
    def unique_words(self,tokens:list[str]) -> int:
        return len(set(tokens))
import re

from nlp.vocabulary import Vocabulary


class TokenizerEngine:

    def __init__(self):
        self.vocab = Vocabulary()

    def encode(self, text: str) -> list[int]:
        cleaned_text = re.sub(r"[^\w\s]", "", text).strip().lower()
        tokens = cleaned_text.split()
        token_ids = self.vocab.encode(tokens)
        return token_ids

    def decode(self, token_ids: list[int]) -> str:
        tokens = self.vocab.decode(token_ids)
        return " ".join(tokens)


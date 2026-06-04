from nlp.text_processor import TextProcessor
from nlp.tokenzier import Tokenizer

class    NLPPipeline:

    def __init__(self):
        self.text_processor = TextProcessor()
        self.tokenizer = Tokenizer()

    def process(self, text: str) -> list[str]:
        normalized = self.text_processor.normalize(text)
        tokens = self.tokenizer.tokenize(normalized)
        tokens = self.text_processor.remove_stopwords(tokens)
        return tokens

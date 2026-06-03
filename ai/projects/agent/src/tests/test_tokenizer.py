from nlp.tokenzier import Tokenizer

def test_tokenizer():
    tokenizer = Tokenizer()

    result = tokenizer.tokenize(
        "Python is great"
    )

    assert result == ["Python", "is", "great"]

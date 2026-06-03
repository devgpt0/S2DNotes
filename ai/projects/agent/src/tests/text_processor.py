from nlp.text_processor import TextProcessor

def test_text_processor():
    
    processor = TextProcessor()
    
    result = processor.normalize(
        "Python  !!!!  "
    )
    
    assert result == "python"

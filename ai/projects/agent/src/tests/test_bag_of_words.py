from nlp.bag_of_words import BagOfWords

def test_bag_of_words():
    
    bow = BagOfWords()
    
    text = "Hello world! Hello everyone."
    
    features = bow.transform(text)
    
    assert features == {"hello": 2, "world": 1, "everyone": 1}
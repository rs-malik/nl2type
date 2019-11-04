import nl2type.nl_utils as nlu


def test_camel_case_tokenize():
    tokens = nlu.camel_case_tokenize("getRectangleArea")
    assert len(tokens) == 3
    assert tokens[0] == 'get'
    assert tokens[1] == 'Rectangle'
    assert tokens[2] == 'Area'


def test_camel_case_tokenize_empty_string():
    tokens = nlu.camel_case_tokenize("")
    assert len(tokens) == 0


def test_camel_case_tokenize_one_token():
    tokens = nlu.camel_case_tokenize("getrectanglearea")
    assert len(tokens) == 1
    assert tokens[0] == 'getrectanglearea'


def test_lemmatize_empty_string():
    lemmatized = nlu.lemmatize_sentence("")
    assert len(lemmatized) == 0


def test_lemmatize():
    lemmatized = nlu.lemmatize_sentence("dogs are running")
    assert lemmatized == "dog be run"


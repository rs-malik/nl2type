import nl2type.nl_utils as nlu


def test_camel_case_tokenize():
    tokenized = nlu.tokenize("getRectangleArea")
    assert tokenized == "get rectangle area"


def test_camel_case_tokenize_empty_string():
    tokens = nlu.tokenize("")
    assert len(tokens) == 0


def test_camel_case_tokenize_one_token():
    assert nlu.tokenize("getrectanglearea") == "getrectanglearea"


def test_lemmatize_empty_string():
    lemmatized = nlu.lemmatize_sentence("")
    assert len(lemmatized) == 0


def test_lemmatize():
    lemmatized = nlu.lemmatize_sentence("dogs are running")
    assert lemmatized == "dog be run"


def test_remove_periods_no_space():
    assert nlu.remove_punctuation_and_linebreaks("object.property") == "object property"


def test_periods_with_space_not_removed():
    assert nlu.remove_punctuation_and_linebreaks("object. property") == "object. property"

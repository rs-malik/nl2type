import re
from typing import List

from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import wordnet, stopwords


def lemmatize_sentence(sentence: str) -> str:
    """
    Lemmatizes words in a sentence.
    Lemmatizes on the sentence level because position of words is important.
    :param sentence: the sentence to lemmatize
    :return: the lemmatized sentence
    """
    words = [word for word in sentence.split(" ") if word != '']
    lemmatizer = WordNetLemmatizer()
    if len(words) == 0:
        return ""

    word_positions = pos_tag(words)
    lemmatized = []
    for p in word_positions:
        word_pos = _get_wordnet_pos(p[1])
        if word_pos != '' and len(word_pos) > 0:
            lemmatized.append(lemmatizer.lemmatize(p[0], pos=word_pos))
        else:
            lemmatized.append(lemmatizer.lemmatize(p[0]))
    return " ".join(lemmatized)


def _get_wordnet_pos(treebank_tag: str) -> str:
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def replace_digits_with_space(sentence: str) -> str:
    return re.sub('[0-9]+', ' ', sentence)


def camel_case_tokenize(word: str) -> List[str]:
    """
    Example: "getRectangleArea" -> ["get", "Rectangle", "Area"]
    :param word: the word to tokenize
    :return: list of tokens
    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', word)
    return [m.group(0) for m in matches]


def remove_punctuation_and_linebreaks(sentence: str) -> str:
    # we only care about sentences, not about questions.
    sentence = re.sub('[^A-Za-z0-9. ?]+', ' ', sentence).replace("?", ".")

    sentence = sentence.replace('\n', '')
    sentence = sentence.replace('\r', '')

    # we want to get replace full stops not followed by a space with a space.
    # For example object.property --> object property
    return re.sub("[.](?! )", ' ', sentence)


def remove_stop_words(sentence : str) -> str:
    return ' '.join([word for word in sentence.split(' ') if word not in stopwords.words('english')])

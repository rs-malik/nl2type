from gensim.models import Word2Vec

from nl2type import convert
from nl2type import extract
from nl2type import vectorize
import pandas as pd


def run(js_files_dir):
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', 500)
    extracted_jsdoc = extract.extract_from_dir(js_files_dir)
    df = convert.convert_func_to_df(extracted_jsdoc)
    word2vec_code = Word2Vec.load('/home/rabee/projects/nl2type/nl2type/models/word_vecs/word2vec_model_code.bin')
    word2vec_lang = Word2Vec.load('/home/rabee/projects/nl2type/nl2type/models/word_vecs/word2vec_model_language.bin')
    vectors = vectorize.df_to_vec(df, word2vec_lang, word2vec_code)

    print(df)


if __name__ == '__main__':
    run("/home/rabee/projects/nl2type/nl2type/data/input")

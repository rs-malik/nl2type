import argparse
import json

from gensim.models import Word2Vec
from tensorflow_core.python.keras.models import load_model

import convert
import extract
import predict
import vectorize
from annotation import annotate


def main(input_file: str, output_file: str):
    extracted_jsdoc = extract.extract_from_file(input_file)
    df = convert.convert_func_to_df(extracted_jsdoc)
    word2vec_code = Word2Vec.load('data/word_vecs/word2vec_model_code.bin')
    word2vec_lang = Word2Vec.load('data/word_vecs/word2vec_model_language.bin')
    vectors = vectorize.df_to_vec(df, word2vec_lang, word2vec_code)
    model = load_model('data/model.h5')
    with open("data/types.json") as f:
        types_map = json.load(f)
    predictions = predict.predict(model, vectors, types_map)
    annotate.annotate(df, predictions, input_file, output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", type=str, help="Path of the input file")
    parser.add_argument("output_file_path", type=str, help="Path of the output file")
    args = parser.parse_args()
    main(args.input_file_path, args.output_file_path)

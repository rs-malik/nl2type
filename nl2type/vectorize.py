import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from pandas import Series

WORD_VEC_LENGTH = 100
to_predict_feature = 'type'

features = {
    "datapoint_type": 1,
    "cleaned_name": 6,
    "comment": 12,
    "return_param_comment": 10,
    "params": 10
}
features_list = ['comment', 'params', 'cleaned_name', 'return_param_comment']


def df_to_vec(df: pd.DataFrame, word2vec_language: Word2Vec, word2vec_code: Word2Vec) -> np.ndarray:
    """
    vectorizes a dataframe to a 3 dimensional matrix
    :param df: the dataframe to vectorize
    :param word2vec_language: the word2vec model for comments
    :param word2vec_code: the word2vec model for identifiers
    :return: a three dimensional matrix
    """
    data = np.zeros((df.shape[0], sum(features.values()) + len(features.values()) - 1, WORD_VEC_LENGTH))
    count = 0
    for index, row in df.iterrows():
        data[count] = _vectorize_row(row, word2vec_code, word2vec_language, np.ones(WORD_VEC_LENGTH))
        count += 1
    return data


def _vectorize_row(row: Series, w2v_model_code: Word2Vec, w2v_model_language: Word2Vec,
                   separator: np.ndarray) -> np.ndarray:
    data_point = np.zeros((sum(features.values()) + len(features.values()) - 1, WORD_VEC_LENGTH))
    data_point[0] = _vectorize_data_point_type(row)
    data_point[1] = separator

    data_point_index = 2
    for feature_name in features_list:
        feature_length = features[feature_name]
        if type(row[feature_name]) is str:
            if feature_name == "cleaned_name" or feature_name == "params":
                vectorized_feature = _vectorize_string(row[feature_name], feature_length, w2v_model_code)
            elif feature_name == "comment" or feature_name == "return_param_comment":
                vectorized_feature = _vectorize_string(row[feature_name], feature_length, w2v_model_language)

            for word in vectorized_feature:
                data_point[data_point_index] = word
                data_point_index += 1
        elif feature_name != "datapoint_type":
            for i in range(0, feature_length):
                data_point[data_point_index] = np.zeros((1, WORD_VEC_LENGTH))
                data_point_index += 1
        elif feature_name == 'datapoint_type':
            continue

        if data_point_index >= len(data_point):
            break

        data_point[data_point_index] = separator
        data_point_index += 1
    return data_point


def _vectorize_data_point_type(row: pd.Series) -> np.ndarray:
    datapoint_type = np.zeros((1, WORD_VEC_LENGTH))
    if row['datapoint_type'] == 0:
        datapoint_type[0][0] = 1
    else:
        datapoint_type[0][1] = 1
    return datapoint_type


def _vectorize_string(text: str, feature_length: int, w2v_model: Word2Vec) -> np.ndarray:
    text_vec = np.zeros((feature_length, WORD_VEC_LENGTH))
    if text == 'unknown' or len(text) == 0:
        return text_vec
    count = 0
    for word in text.split():
        if count >= feature_length:
            return text_vec
        try:
            text_vec[count] = w2v_model.wv[word]
        except KeyError:
            pass
        count += 1

    return text_vec

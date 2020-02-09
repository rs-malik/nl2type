import os
from typing import Dict, List

import pandas as pd

from nl2type import nl_utils as nlu


COLUMNS = ['params',
           'return_param_comment',
           'datapoint_type',
           'line_number',
           'filename',
           'name',
           'cleaned_name',
           'comment',
           'cleaned_comment']


def convert_func_to_df(func_sigs: Dict) -> pd.DataFrame:
    """
    Converts function signatures from a json format to a pandas Dataframe.
    Also cleans natural language information for the following columns:
    name, comment, return_param_comment, params.
    :param func_sigs: the json for function signatures, as output by the jsdoc tool
    :return: a data frame with the columns as given by the COLUMNS list
    """
    data = _init_dict()
    for func in func_sigs:
        line_num = _get_line_number(func)
        filename = _get_filename(func)
        params_data = _convert_params_data_to_dict(func, line_num, filename)
        data = _merge_dicts(data, params_data)

        data['params'].append(' '.join([param['name'] for param in func.get('params', [])]))
        data['return_param_comment'].append(_get_return_param_comment(func))
        data['datapoint_type'].append(0)
        data['line_number'].append(line_num)
        data['filename'].append(filename)
        data['name'].append(func['name'])

        cleaned_name = nlu.lemmatize_sentence \
            (nlu.remove_punctuation_and_linebreaks
             (nlu.lemmatize_sentence
              (nlu.tokenize
               (nlu.replace_digits_with_space(func['name'])))))

        data['cleaned_name'].append(cleaned_name)
        data['comment'] = func.get('description', '')

        cleaned_comment = nlu.lemmatize_sentence \
            (nlu.remove_punctuation_and_linebreaks
             (nlu.lemmatize_sentence
              (nlu.tokenize
               (nlu.replace_digits_with_space(func.get('description', ''))))))
        data['cleaned_comment'].append(cleaned_comment)

    return pd.DataFrame.from_dict(data)


def _get_line_number(function: Dict) -> int:
    if "meta" in function and "lineno" in function["meta"]:
        return int(function["meta"]["lineno"])
    else:
        return -1


def _get_filename(function: Dict) -> str:
    if "meta" in function and "filename" in function["meta"] and "path" in function["meta"]:
        return os.path.join(function['meta']['path'], function["meta"]["filename"])
    else:
        return ""


def _get_return_param_comment(function: Dict) -> str:
    return_param_comment = ""
    for return_type in function.get('returns', []):
        if "description" in return_type:
            return_param_comment +=  nlu.lemmatize_sentence \
            (nlu.remove_punctuation_and_linebreaks
             (nlu.lemmatize_sentence
              (nlu.tokenize
               (nlu.replace_digits_with_space(return_type['description'])))))
    return return_param_comment


def _convert_params_data_to_dict(function: Dict, line_num: int, filename: str) -> Dict[str, List]:
    params_data = _init_dict()

    params = function.get('params', [])
    for param in params:
        params_data.get('params').append('')
        params_data.get('return_param_comment').append('')
        params_data.get('datapoint_type').append('1')
        params_data.get('line_number').append(line_num)
        params_data.get('filename').append(filename)

        name = param.get('name', '')
        cleaned_name = nlu.lemmatize_sentence \
            (nlu.remove_punctuation_and_linebreaks
             (nlu.lemmatize_sentence
              (nlu.tokenize
               (nlu.replace_digits_with_space(name)))))

        params_data.get('name').append(name)
        params_data.get('cleaned_name').append(cleaned_name)

        comment = param.get('description', '')
        cleaned_comment = nlu.remove_stop_words \
            (nlu.lemmatize_sentence
            (nlu.remove_punctuation_and_linebreaks
             (nlu.lemmatize_sentence
              (nlu.tokenize
               (nlu.replace_digits_with_space(comment))))))

        params_data.get('comment').append(comment)
        params_data.get('cleaned_comment').append(cleaned_comment)

    return params_data


def _init_dict() -> Dict[str, List[str]]:
    return {k: [] for k in COLUMNS}


def _merge_dicts(dict1: Dict[str, List], dict2: Dict[str, List]) -> Dict[str, List]:
    merged = _init_dict()
    for key in dict1:
        merged.get(key).extend(dict1[key])
        merged.get(key).extend(dict2[key])

    return merged

from collections import defaultdict
from typing import List, Dict

import pandas as pd

from annotation import jsdoc
from annotation.param import Param
from loguru import logger


def annotate(df: pd.DataFrame, results: List[str], input_file: str, output_file: str):
    """
    :param df: the dataframe which contains all of the information for each datapoint.
    :param results: the prediction for each datapoint
    :param input_file: the unannotated file
    :param output_file: the name of the file to annotate
    """

    logger.info("annotating from df of size {}".format(df.shape[0]))

    df["prediction"] = results
    annotations = _build_annotations_list(df)

    with open(input_file, 'r') as f:
        lines = f.readlines()

    logger.info("annotating file at {}".format(output_file))
    with open(output_file, 'w') as f:
        for idx, line in enumerate(lines):
            if idx in annotations:
                logger.debug("adding annotation at line {}".format(idx))
                f.write(str(annotations[idx]))
            f.write(line)


def _build_annotations_list(df: pd.DataFrame) -> Dict:
    annotations = defaultdict(jsdoc.Jsdoc)
    for index, row in df.iterrows():
        line_number = row['line_number']
        annotation = annotations[line_number - 1]
        if row['datapoint_type'] == 0:
            annotation.set_name(row['name'])
            annotation.set_line_number(line_number - 1)
            annotation.set_type(row['prediction'])
        else:
            annotations[line_number - 1].add_param(Param(row['name'], row['prediction']))

    logger.info("generated {} annotations".format(len(annotations)))
    return annotations

import tensorflow as tf
import numpy as np

from typing import Dict, List
from loguru import logger


def init_tf():
    logger.info("initializing tf")
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)


def predict(model, data: np.ndarray, types_map: Dict) -> List[str]:
    """
    :param model: the model to use to make a type predictoin
    :param data: the feature vectors on which to make the prediction
    :param types_map: a map which maps the softmax position to the actual type
    :return: a list of types for each of the data points
    """
    logger.info("making {} predictions".format(len(data)))
    predictions = model.predict(data)
    reversed_types = reverse_dict(types_map)
    return [reversed_types[np.argmax(prediction)] for prediction in predictions]


def reverse_dict(types_map: Dict) -> Dict:
    reversed_dict = {}
    for key, val in types_map.items():
        reversed_dict[val] = key
    return reversed_dict

from typing import Dict
import tensorflow as tf
import numpy as np


def init_tf():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)


def predict(model, data, types_map: Dict):
    predictions = model.predict(data)
    reversed_types = reverse_dict(types_map)
    for prediction in predictions:
        print(reversed_types[np.argmax(prediction)])


def reverse_dict(types_map: Dict) -> Dict:
    reversed_dict = {}
    for key, val in types_map.items():
        reversed_dict[val] = key
    return reversed_dict

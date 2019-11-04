import json
import os
import subprocess
from typing import Dict, List

from loguru import logger

JSDOC_COMMAND = "jsdoc -X {}"


def extract_from_dir(dir_path: str = "../files") -> List[Dict]:
    """
    Extracts function type signatures from JavaScript files by parsing JSDocs
    :param dir_path: path to the directory of JavaScript files
    :return: list of function type signatures
    """
    logger.info("Extracting json from path {}".format(dir_path))
    js_files = [os.path.join(dp, f) for dp, dn, file_names in os.walk(dir_path) for f in file_names]
    jsdoc_output = [extract_from_file(f) for f in js_files]
    jsdoc_output_flat = [out for sublist in jsdoc_output for out in sublist]
    return [sig for sig in jsdoc_output_flat if is_function_signature(sig)]


def extract_from_file(file_path: str) -> Dict:
    """
        Extracts function type signatures from individual JavaScript files by parsing
        JSDocs using the npm package JSDoc
        :param file_path: path to the JavaScript file
        :return: dict of function type signatures. Does not validate the output of the command
        """
    logger.debug("Extracting json from file {}".format(file_path))
    json_str = subprocess.check_output(JSDOC_COMMAND.format(file_path), shell=True)
    return json.loads(json_str)


def is_function_signature(jsdoc_output: Dict) -> bool:
    """
    Checks to see if the passed jsdoc output is a function signature
    :param jsdoc_output: the output of the jsdoc tool
    :return: True, if output is a function signature, False otherwise
    """
    return jsdoc_output is not None and "kind" in jsdoc_output and jsdoc_output["kind"] == "function"

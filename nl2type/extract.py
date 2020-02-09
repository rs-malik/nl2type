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
    return jsdoc_output_flat


def extract_from_file(file_path: str) -> List[Dict]:
    """
        Extracts function type signatures from individual JavaScript files by parsing
        JSDocs using the npm package JSDoc
        :param file_path: path to the JavaScript file
        :return: dict of function type signatures. Does not validate the output of the command
        """
    logger.debug("Extracting json from file {}".format(file_path))
    func_signatures = []
    json_str = subprocess.check_output(JSDOC_COMMAND.format(file_path), shell=True)
    jsdoc_output_dict = json.loads(json_str)
    for output_dict in jsdoc_output_dict:
        if is_function_signature(output_dict):
            func_signatures.append(standardize_jdsoc_output(output_dict))

    return func_signatures


def is_function_signature(jsdoc_output: Dict) -> bool:
    """
    Checks to see if the passed jsdoc output is a function signature
    :param jsdoc_output: the output of the jsdoc tool
    :return: True, if output is a function signature, False otherwise
    """
    return jsdoc_output is not None and "kind" in jsdoc_output and jsdoc_output["kind"] == "function"


def standardize_jdsoc_output(jsdoc_output: Dict) -> Dict:
    """
    Converts the dict output by the jsdoc tool to a standard format.
    This is required because functions which have a jsdoc are output differently than functions without
    :param jsdoc_output: the dict output by the jsdoc tool
    :return: a standard representation of a function
    """

    # if "undocumented" in jsdoc_output and jsdoc_output["undocumented"]:
    filename = jsdoc_output["meta"]["path"] + "/" + jsdoc_output["meta"]["filename"]
    line_no = jsdoc_output["meta"]["lineno"]
    standard_rep = {"description": jsdoc_output["description"],
                    "name": jsdoc_output["name"], "filename" : filename, "line_number": line_no}
    param_names = jsdoc_output["meta"]["code"]["paramnames"]
    standard_params = []
    for param_name in param_names:
        standard_params.append({"name": param_name, "line_number": line_no, "filename": filename})

    for param in jsdoc_output['params']:
        for standard_param in standard_params:
            if standard_param["name"] == param["name"]:
                standard_param["description"] = param["description"]
    standard_rep["params"] = standard_params
    return standard_rep

    # return jsdoc_output

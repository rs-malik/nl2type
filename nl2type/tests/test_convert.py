import json

import pytest

from nl2type import convert


@pytest.fixture
def json_data():
    with open("tests/resources/function_data.json") as f:
        return json.load(f)


def test_params_converted(json_data):
    df = convert.convert_func_to_df(json_data)
    assert list(df.columns) == convert.COLUMNS
    assert len(df.index) == 3
    # names
    assert 'first point' == df['cleaned_name'][0]
    assert 'second point' == df['cleaned_name'][1]
    # filename
    assert 'input/test.js' == df['filename'][0]
    assert 'input/test.js' == df['filename'][1]


def test_func_converted(json_data):
    df = convert.convert_func_to_df(json_data)
    assert 'multiply' == df['cleaned_name'][2]
    assert 'multiplies two decimal' == df['cleaned_comment'][2]
    assert 'firstPoint secondPoint' == df['params'][2]
    assert 'input/test.js' == df['filename'][2]
    assert '' == df['return_param_comment'][2]

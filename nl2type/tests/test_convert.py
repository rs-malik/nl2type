import json

import pytest

from nl2type import convert


@pytest.fixture
def json_data():
    with open("resources/function_data.json") as f:
        return json.load(f)


def test_params_converted(json_data):
    df = convert.convert_jsdoc_to_df(json_data)
    assert list(df.columns) == convert.COLUMNS
    assert len(df.index) == 3
    # names
    assert 'first' == df['name'][0]
    assert 'second' == df['name'][1]
    # comments
    assert 'first number' == df['cleaned_comment'][0]
    assert 'second number' == df['cleaned_comment'][1]
    # types
    assert 'number' == df['type'][0]
    assert 'number' == df['type'][1]
    # filename
    assert 'resources/with_jsdoc.js' == df['filename'][0]
    assert 'resources/with_jsdoc.js' == df['filename'][1]


def test_func_converted(json_data):
    df = convert.convert_jsdoc_to_df(json_data)
    assert 'add' == df['cleaned_name'][2]
    assert 'add two number together' == df['cleaned_comment'][2]
    assert 'first second' == df['params'][2]
    assert 'number' == df['type'][0]
    assert 'resources/with_jsdoc.js' == df['filename'][2]
    assert '' == df['return_param_comment'][2]

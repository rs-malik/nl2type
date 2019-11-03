from nl2type import extract


def test_jsdoc_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    assert jsdoc_output is not None
    functions = [out for out in jsdoc_output if extract.is_function_signature(out)]
    assert len(functions) == 1


def test_name_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)][0]
    assert func['name'] == 'add'


def test_params_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)][0]
    assert len(func['params']) == 2


def test_param_names_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)][0]
    params = func['params']
    param_first = [param for param in params if param['name'] == 'first']
    assert len(param_first) == 1
    param_second = [param for param in params if param['name'] == 'second']
    assert len(param_second) == 1


def test_param_types_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    params = [out for out in jsdoc_output if extract.is_function_signature(out)][0]['params']
    param_first = [param for param in params if param['name'] == 'first'][0]
    assert len(param_first['type']['names']) == 1
    assert param_first['type']['names'][0] == 'number'


def test_param_comments_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    params = [out for out in jsdoc_output if extract.is_function_signature(out)][0]['params']
    param_first = [param for param in params if param['name'] == 'first'][0]
    assert param_first['description'] == 'The First Number'


def test_return_comment_extracted():
    jsdoc_output = extract.extract_from_file("resources/with_jsdoc.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)][0]
    assert len(func['returns']) == 1
    assert len(func['returns'][0]['type']['names']) == 1
    assert func['returns'][0]['type']['names'][0] == 'number'


def test_nothing_extracted_from_empty_file():
    jsdoc_output = extract.extract_from_file("resources/empty.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)]
    assert len(func) == 0


def test_no_return_type_extracted_from_no_jsdoc():
    jsdoc_output = extract.extract_from_file("resources/without_jsdoc.js")
    func = [out for out in jsdoc_output if extract.is_function_signature(out)][0]
    assert 'returns' not in func

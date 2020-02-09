from nl2type import extract


def test_jsdoc_extracted():
    funcs = extract.extract_from_file("resources/with_jsdoc.js")
    assert len(funcs) == 1


def test_name_extracted_with_jsdoc():
    func = extract.extract_from_file("resources/with_jsdoc.js")[0]
    assert func['name'] == 'add'


def test_params_extracted_with_jsdoc():
    func = extract.extract_from_file("resources/with_jsdoc.js")[0]
    assert len(func['params']) == 2


def test_param_names_extracted_with_jsdoc():
    func = extract.extract_from_file("resources/with_jsdoc.js")[0]
    params = func['params']
    assert len([param for param in params if param['name'] == 'first']) == 1
    assert len([param for param in params if param['name'] == 'second']) == 1


def test_param_comments_extracted():
    func = extract.extract_from_file("resources/with_jsdoc.js")[0]
    params = func['params']
    param_first = [param for param in params if param['name'] == 'first'][0]
    assert param_first['description'] == 'The First Number'


def test_nothing_extracted_from_empty_file():
    assert len(extract.extract_from_file("resources/empty.js")) == 0


def test_no_return_type_extracted_from_no_jsdoc():
    func = extract.extract_from_file("resources/without_jsdoc.js")[0]
    assert 'returns' not in func


def test_names_extracted_from_no_jsdoc():
    func = extract.extract_from_file("resources/without_jsdoc.js")[0]
    assert func['name'] == 'add'


def test_param_names_extracted_from_no_jsdoc():
    func = extract.extract_from_file("resources/without_jsdoc.js")[0]
    params = func['params']
    assert len([param for param in params if param['name'] == 'first']) == 1
    assert len([param for param in params if param['name'] == 'second']) == 1


def test_comment_extracted_from_no_jsdoc():
    func = extract.extract_from_file("resources/without_jsdoc.js")[0]
    assert func['description'] == "this is only a test function";
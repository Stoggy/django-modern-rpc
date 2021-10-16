# coding: utf-8
import future.utils
import pytest
import six

from modernrpc.compat import standardize_strings


@pytest.mark.skipif(future.utils.PY2, reason='Python 3 specific test')
def test_standardize_str_error_with_py3():
    with pytest.raises(AssertionError) as excpinfo:
        standardize_strings('123')
    assert 'python 2 only' in str(excpinfo.value).lower()


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_1():
    # six.text_type is 'unicode' in Python 2
    assert standardize_strings('abc', six.text_type) == u'abc'


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_2():
    # six.binary_type is 'str' in Python 2
    assert standardize_strings(u'abc', six.binary_type) == 'abc'


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_3():
    input_val_ = [145, 964, 84, ['ghjfgh', 64], [[84, 9.254, b'trdf', 645], '456', u'784', 'sdfg']]
    output_val = [145, 964, 84, [u'ghjfgh', 64], [[84, 9.254, b'trdf', 645], u'456', u'784', u'sdfg']]
    # six.text_type is 'unicode' in Python 2
    assert standardize_strings(input_val_, six.text_type) == output_val


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_4():
    input_val_ = [145, 964, 84, [u'ghjfgh', 64], [[84, 9.254, b'trdf', 645], u'456', u'784', 'sdfg']]
    output_val = [145, 964, 84, ['ghjfgh', 64], [[84, 9.254, b'trdf', 645], '456', '784', 'sdfg']]
    # six.binary_type is 'str' in Python 2
    assert standardize_strings(input_val_, six.binary_type) == output_val


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_5():
    input_val_ = (145, 964, 84, ['ghjfgh', 64], [(84, 9.254, b'trdf', 645), '456', u'784', 'sdfg'])
    output_val = (145, 964, 84, [u'ghjfgh', 64], [(84, 9.254, b'trdf', 645), u'456', u'784', u'sdfg'])
    # six.text_type is 'unicode' in Python 2
    assert standardize_strings(input_val_, six.text_type) == output_val


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_6():
    input_val_ = (145, 964, 84, (u'ghjfgh', 64), ([84, 9.254, b'trdf', 645], u'456', u'784', 'sdfg'))
    output_val = (145, 964, 84, ('ghjfgh', 64), ([84, 9.254, b'trdf', 645], '456', '784', 'sdfg'))
    # six.binary_type is 'str' in Python 2
    assert standardize_strings(input_val_, six.binary_type) == output_val


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_7():
    input_dict = {
        'a': 456,
        'b': [84, 5.1, 'strdfg', u'trdt'],
        'pp': {
            'x': 32,
            'y': ['rtg', 'poi', 'aze']
        },
    }
    expected_out = {
        'a': 456,
        'b': [84, 5.1, u'strdfg', u'trdt'],
        'pp': {
            'x': 32,
            'y': [u'rtg', u'poi', u'aze']
        },
    }
    # six.text_type is 'unicode' in Python 2
    assert standardize_strings(input_dict, six.text_type) == expected_out


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_8():
    input_dict = {
        'a': 456,
        'b': [84, 5.1, u'strdfg', u'trdt'],
        'pp': {
            'x': 32,
            'y': [u'rtg', 'poi', u'aze']
        },
    }
    expected_out = {
        'a': 456,
        'b': [84, 5.1, 'strdfg', 'trdt'],
        'pp': {
            'x': 32,
            'y': ['rtg', 'poi', 'aze']
        },
    }
    # six.binary_type is 'str' in Python 2
    assert standardize_strings(input_dict, six.binary_type) == expected_out


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_9():
    assert standardize_strings(54, None) == 54


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_standardize_str_10():
    with pytest.raises(TypeError):
        assert standardize_strings("64", int)


@pytest.mark.skipif(future.utils.PY3, reason='Python 2 specific test')
def test_method_level_str_std(xmlrpc_client, jsonrpc_client):
    """TODO: what was the idea here ?"""
    assert jsonrpc_client.force_unicode_input("abcde") == "<type 'unicode'>"
    assert xmlrpc_client.force_unicode_input("abcde") == "<type 'unicode'>"

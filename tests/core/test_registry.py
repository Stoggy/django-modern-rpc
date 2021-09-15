# coding: utf-8
import jsonrpcclient.exceptions
import pytest
from django.core.exceptions import ImproperlyConfigured

import modernrpc
from modernrpc.core import ALL
from tests import xmlrpclib
from tests.mocks import dummy_remote_procedure_1, dummy_remote_procedure_2, dummy_remote_procedure_3, \
    dummy_remote_procedure_4, not_decorated_procedure


def test_registry_empty_after_reset(rpc_registry):
    # Ensure a normal init registered some rpc methods
    assert len(rpc_registry.get_all_method_names()) > 0
    # Reset
    rpc_registry.reset()
    # After reset, no mre remote procedure in registry
    assert len(rpc_registry.get_all_method_names()) == 0


def test_manual_registration(rpc_registry):
    assert 'dummy_remote_procedure_1' not in rpc_registry.get_all_method_names()
    rpc_registry.register_method(dummy_remote_procedure_1)
    assert 'dummy_remote_procedure_1' in rpc_registry.get_all_method_names()


def test_double_registration(rpc_registry):
    # Registering twice is not a problem
    assert rpc_registry.register_method(dummy_remote_procedure_1) == 'dummy_remote_procedure_1'
    assert rpc_registry.register_method(dummy_remote_procedure_1) == 'dummy_remote_procedure_1'


def test_manual_registration_with_different_name(rpc_registry):
    assert 'another_name' not in rpc_registry.get_all_method_names()
    rpc_registry.register_method(dummy_remote_procedure_2)
    assert 'another_name' in rpc_registry.get_all_method_names()
    assert 'dummy_remote_procedure_2' not in rpc_registry.get_all_method_names()


def test_invalid_custom_name(rpc_registry):
    with pytest.raises(ImproperlyConfigured) as exc_info:
        rpc_registry.register_method(dummy_remote_procedure_3)

    assert 'method names starting with "rpc." are reserved' in str(exc_info.value)
    assert 'rpc.invalid.name' not in rpc_registry.get_all_method_names()
    assert 'dummy_remote_procedure_3' not in rpc_registry.get_all_method_names()


def test_duplicated_name(rpc_registry):
    with pytest.raises(ImproperlyConfigured) as exc_info:
        rpc_registry.register_method(dummy_remote_procedure_4)

    assert 'has already been registered' in str(exc_info.value)


def test_wrong_manual_registration(rpc_registry):
    # Trying to register a not decorated method with the latest version raises an ImproperlyConfigured exception
    with pytest.raises(ImproperlyConfigured):
        rpc_registry.register_method(not_decorated_procedure)


def test_method_names_list(rpc_registry):
    raw_list = rpc_registry.get_all_method_names()
    sorted_list = rpc_registry.get_all_method_names(sort_methods=True)

    assert len(raw_list) == len(sorted_list)
    assert raw_list != sorted_list

    for n in raw_list:
        assert n in sorted_list


def test_methods_list(rpc_registry):
    raw_list = rpc_registry.get_all_methods()
    sorted_list = rpc_registry.get_all_methods(sort_methods=True)

    assert len(raw_list) == len(sorted_list)
    assert raw_list != sorted_list

    for m in raw_list:
        assert m in sorted_list

    for m in sorted_list:
        assert m in raw_list


# Tests for backward compatiility
def test_backward_compat_register_method(rpc_registry):
    assert 'dummy_remote_procedure_1' not in modernrpc.core.get_all_method_names()
    modernrpc.core.register_rpc_method(dummy_remote_procedure_1)
    assert 'dummy_remote_procedure_1' in modernrpc.core.get_all_method_names()


def test_backward_compat_registry(rpc_registry):
    assert rpc_registry.get_method("divide", ALL, ALL) == modernrpc.core.get_method("divide", ALL, ALL)
    assert rpc_registry.get_all_method_names() == modernrpc.core.get_all_method_names()

    # registry.get_all_methods() return a dict_values instance
    # It needs to be casted to list to allow comparison
    assert list(rpc_registry.get_all_methods()) == list(modernrpc.core.get_all_methods())


def test_backward_compat_registry_reset(rpc_registry):
    # Ensure a normal init registered some rpc methods
    assert len(modernrpc.core.get_all_method_names()) > 0
    # Reset
    modernrpc.core.reset_registry()
    # After reset, no mre remote procedure in registry
    assert len(modernrpc.core.get_all_method_names()) == 0


# In testsite.rpc_methods_stub.generic, a function has not been decorated
# Ensure it is not available in registry
def test_xmlrpc_not_registered(xmlrpc_client):
    result = xmlrpc_client.system.listMethods()
    assert 'existing_but_not_decorated' not in result


def test_xmlrpc_not_decorated(xmlrpc_client):
    with pytest.raises(xmlrpclib.Fault) as exc_info:
        xmlrpc_client.existing_but_not_decorated()
    assert 'Method not found: "existing_but_not_decorated"' in str(exc_info.value)


def test_jsonrpc_not_registered(jsonrpc_client):
    result = jsonrpc_client.request('system.listMethods')
    assert 'existing_but_not_decorated' not in result


def test_jsonrpc_not_decorated(jsonrpc_client):
    with pytest.raises(jsonrpcclient.exceptions.ReceivedErrorResponse) as exc_info:
        jsonrpc_client.existing_but_not_decorated()
    assert 'Method not found: "existing_but_not_decorated"' in str(exc_info.value)

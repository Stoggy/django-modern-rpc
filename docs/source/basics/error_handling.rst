Error handling
==============

Internally, django-modern-rpc must deal with a number of errors. Anything can break, from request parsing to procedure
execution. Even result serialization may fail. In any situation, both XML-RPC and JSON-RPC standards state an correct
error result must be returned to client.

Such result must contain an error code, and a text message providing more context. Here is the list of common errors:

.. list-table:: Common errors
   :widths: 20 50
   :header-rows: 1

   * - Code
     - Message
   * - -32700
     - parse error. not well formed
   * - -32701
     - parse error. unsupported encoding


RPC Error codes and pre-defined exceptions
------------------------------------------

django-modern-rpc provide exceptions to cover common errors when requests are processed.

Customize error handling
------------------------

If you want to define customized exceptions for your application, you can create ``RPCException`` sub-classes and set,
for each custom exception, a *faultCode* to ``RPC_CUSTOM_ERROR_BASE + N`` with ``N`` a unique number.

Here is an example:

.. code:: python

   class MyException1(RPCException):
       def __init__(self, message):
           super().__init__(RPC_CUSTOM_ERROR_BASE + 1, message)

   class MyException2(RPCException):
       def __init__(self, message):
           super().__init__(RPC_CUSTOM_ERROR_BASE + 2, message)

Anyway, any exception raised during the RPC method execution will generate a ``RPCInternalError`` with an error message
constructed from the underlying error. As a result, the RPC client will have a correct message describing what went
wrong.

Logging
-------

Internally, django-modern-rpc use exceptions and Python logging system to handle errors.
This design choice has 2 goals:

 1. **Return useful error message to clients** Both XML-RPC and JSON-RPC describe how a server must provide
    error response if something in the remote procedure failed. In django-modern-rpc, we try to be as accurate as
    possible when returning an error response.
 2. **Allow for error logging** The server administrators should be informed when a RPC call has failed, and get all
    information needed to decide if a bug should be fixed in procedure's code or if an error can be ignored.

If you need to troubleshoot issues, you can enable logging capabilities.

You only have to configure ``settings.LOGGING`` to handle log messages from ``modernrpc.core`` and ``modernrpc.views``.
Here is a basic example of such a configuration:

.. code:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # Your formatters configuration...
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            # your other loggers configuration
            'modernrpc': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

All information about logging configuration can be found in `official Django docs`_.

.. versionadded:: 0.7
   By default, logs from ``modernrpc.*`` modules are discarded silently. This behavior prevent
   the common Python 2 error message "No handlers could be found for logger XXX".

.. _official Django docs: https://docs.djangoproject.com/en/dev/topics/logging/#configuring-logging

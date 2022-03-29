Implementation details
======================

XML-RPC
-------

The most recent XML-RPC specification page used as reference for django-modern-rpc development
is http://xmlrpc.com/spec.md. It is part of `xmlrpc.com`_, a website created by `Dave Winer`_ in 2019 to
propose updated tools around XML-RPC standard.

The original website (xmlrpc.scripting.com) has also been archived with a new URL: `1998.xmlrpc.com`_

.. _Dave Winer: https://github.com/scripting
.. _xmlrpc.com: http://xmlrpc.com
.. _1998.xmlrpc.com: http://1998.xmlrpc.com

System introspection methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

System introspection methods (listMethods, methodHelp, methodSignature) were not part of the original standard but were
proposed in an unofficial addendum. Here is a list of references pages:

- http://xmlrpc-c.sourceforge.net/introspection.html
- http://scripts.incutio.com/xmlrpc/introspection.html (dead)
- http://xmlrpc.usefulinc.com/doc/reserved.html) (dead)

Multicall
^^^^^^^^^

Multicall was first proposed by Eric Kidd on 2001-01. Since the original article is now gone from the internet, it has
been archived at https://mirrors.talideon.com/articles/multicall.html

Other useful links
^^^^^^^^^^^^^^^^^^

- Eric Kidd's XML-RPC How To: https://tldp.org/HOWTO/XML-RPC-HOWTO/index.html

JSON-RPC
--------

Since JSON-RPC specification is more recent, available documentation is easier to find. The main specification is
available at https://www.jsonrpc.org/specification

The current official standard for JSON format is `RFC 8259`_.

.. _RFC 8259: https://datatracker.ietf.org/doc/html/rfc8259

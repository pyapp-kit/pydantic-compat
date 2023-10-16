"""This module is a try/except pass-through for the pydantic.v1 namespace.

The pydantic.v1 namespace was added in pydantic v2.  It contains the entire
pydantic v1 package.  For packages that would like to unpin their 'pydantic<2'
dependency *without* needing to update all of their code to use the pydantic v2 api,
this provides a simple way to delay that update.

This is different from the goal of pydantic_compat on the whole, which is to provide
an API translation layer that allows you to actually use pydantic v2 features
(e.g. rust-backed speed, etc...) while also being compatible with packages that pin
pydantic<2.
"""
try:
    from pydantic.v1 import *  # noqa
except ImportError:
    from pydantic import *  # type: ignore # noqa

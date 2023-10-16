"""This module is a try/except wrapper the pydantic.v1 namespace."""
try:
    from pydantic.v1 import *  # noqa
except ImportError:
    from pydantic import *  # type: ignore # noqa

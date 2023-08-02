import pydantic.version

if int(pydantic.version.VERSION[0]) <= 1:  # pragma: no cover
    raise ImportError("pydantic_compat._v2 only supports pydantic v2.x")

from .decorators import root_validator as root_validator
from .decorators import validator as validator
from .mixin import PydanticCompatMixin as PydanticCompatMixin

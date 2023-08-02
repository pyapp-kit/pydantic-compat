import pydantic.version

if not pydantic.version.VERSION.startswith("1"):  # pragma: no cover
    raise ImportError("pydantic_compat._v1 only supports pydantic v1.x")


from .decorators import field_validator as field_validator
from .decorators import model_validator as model_validator
from .decorators import root_validator as root_validator
from .mixin import PydanticCompatMixin as PydanticCompatMixin

"""CompatibilityMixin for pydantic v1/1/v2."""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

from typing import TYPE_CHECKING

try:
    __version__ = version("pydantic-compat")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "uninstalled"

__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
__all__ = [
    "__version__",
    "field_validator",
    "model_validator",
    "PYDANTIC2",
    "PydanticCompatMixin",
    "root_validator",
    "validator",
    "Field",
    "BaseModel",
]

from ._shared import PYDANTIC2

if TYPE_CHECKING:
    from pydantic import (
        Field,
        field_validator,
        model_validator,
        root_validator,
        validator,
    )

    # using this to avoid breaking pydantic mypy plugin
    # not that we could use a protocol. but it will be hard to provide proper names
    # AND proper signatures for both versions of pydantic without a ton of potentially
    # outdated signatures
    PydanticCompatMixin = type
else:
    from ._shared import Field

    if PYDANTIC2:
        from pydantic import field_validator, model_validator

        from ._v2 import PydanticCompatMixin, root_validator, validator

    else:
        from pydantic import validator

        from ._v1 import (
            PydanticCompatMixin,
            field_validator,
            model_validator,
            root_validator,
        )


import pydantic


class BaseModel(PydanticCompatMixin, pydantic.BaseModel):
    """BaseModel with pydantic_compat mixins."""


del pydantic
